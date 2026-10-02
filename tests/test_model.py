import importlib.util
import unittest
from dataclasses import replace

TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None
if TORCH_AVAILABLE:
    import torch
    from tide_jepa import Action, Edge, EdgePair, EdgePath, Inventory, ModelConfig, PathPair
    from tide_jepa.model import TIDEJEPA
    from tide_jepa.training import Batch, Objective, Trainer, compute_loss


@unittest.skipUnless(TORCH_AVAILABLE, "PyTorch is not installed; tensor execution is unverified")
class ModelTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(7)
        self.cfg = ModelConfig(vocab_size=16, action_count=1, width=8, heads=2, layers=1, max_length=12)
        self.model = TIDEJEPA(self.cfg)
        action = Action("TEST_KIND", "TEST_VALUE")
        self.inventory = Inventory((action,), {"en": frozenset([action]), "vi": frozenset([action])})
        edges = (Edge("en", "s", "t", action), Edge("vi", "s", "t", action))
        self.batch = Batch(
            source=torch.tensor([[4, 5, 0], [6, 7, 8]]),
            target=torch.tensor([[9, 10, 2], [11, 12, 2]]),
            decoder_input=torch.tensor([[1, 9, 10], [1, 11, 12]]),
            labels=torch.tensor([[9, 10, 2], [11, 12, 2]]),
            action_ids=torch.tensor([0, 0]), language_ids=torch.tensor([1, 0]),
            edges=edges, pairs=(EdgePair(0, 1, "same_event"),),
        )

    def test_frozen_target_and_gradient_flow(self):
        loss, _ = compute_loss(self.model, self.batch, self.inventory, Objective())
        loss.backward()
        self.assertTrue(all(p.grad is None and not p.requires_grad for p in self.model.target.parameters()))
        self.assertGreater(self.model.online.tokens.weight.grad.abs().sum().item(), 0)
        self.assertGreater(self.model.transition[0].weight.grad.abs().sum().item(), 0)
        self.assertGreater(self.model.output.weight.grad.abs().sum().item(), 0)
        self.assertGreater(self.model.decoder_cross_attention[0].key_value.weight.grad.abs().sum().item(), 0)

    def test_ema_formula_and_training_mode(self):
        original = [p.clone() for p in self.model.target.parameters()]
        with torch.no_grad():
            for parameter in self.model.online.parameters():
                parameter.add_(0.2)
        self.model.update_target(0.75)
        for before, target, online in zip(original, self.model.target.parameters(), self.model.online.parameters()):
            torch.testing.assert_close(target, 0.75 * before + 0.25 * online)
        self.model.train()
        self.assertFalse(self.model.target.training)

    def test_padding_and_causal_future_independence(self):
        state = self.model.online(torch.tensor([[4, 5]]))
        padded = self.model.online(torch.tensor([[4, 5, 0, 0]]))
        torch.testing.assert_close(state, padded)
        predicted = torch.randn(1, 8)
        first = self.model.decode(torch.tensor([[1, 4, 5]]), predicted, torch.tensor([0]))
        second = self.model.decode(torch.tensor([[1, 4, 9]]), predicted, torch.tensor([0]))
        torch.testing.assert_close(first[:, :2], second[:, :2])

    def test_decoder_uses_source_memory_and_masks_source_padding(self):
        predicted = torch.randn(1, 8)
        decoder = torch.tensor([[1, 4, 5]])
        language = torch.tensor([0])
        _, memory_a, valid_a = self.model.online.encode(torch.tensor([[4, 5, 0, 0]]))
        _, memory_a_short, valid_a_short = self.model.online.encode(torch.tensor([[4, 5]]))
        _, memory_b, valid_b = self.model.online.encode(torch.tensor([[6, 7]]))
        padded_logits = self.model.decode(decoder, predicted, language, memory_a, valid_a)
        short_logits = self.model.decode(decoder, predicted, language, memory_a_short, valid_a_short)
        different_source_logits = self.model.decode(decoder, predicted, language, memory_b, valid_b)
        torch.testing.assert_close(padded_logits, short_logits)
        self.assertFalse(torch.allclose(padded_logits, different_source_logits))

    def test_control_losses_and_training_step(self):
        for mode in ("token_only", "generic_jepa", "static_alignment", "tide"):
            with self.subTest(mode=mode):
                loss, values = compute_loss(self.model, self.batch, self.inventory, Objective(mode=mode))
                self.assertTrue(torch.isfinite(loss))
                if mode == "token_only":
                    torch.testing.assert_close(loss, values["token"])
                if mode == "generic_jepa":
                    self.assertEqual(values["alignment"].item(), 0)
        old_online = self.model.online.tokens.weight.detach().clone()
        trainer = Trainer(self.model, self.inventory, Objective())
        metrics = trainer.step(self.batch)
        self.assertEqual(trainer.steps, 1)
        self.assertGreater(metrics["loss"], 0)
        self.assertFalse(torch.equal(old_online, self.model.online.tokens.weight))

    def test_source_copy_loss_is_optional_and_uses_aligned_target_denominator(self):
        mask = torch.zeros_like(self.batch.labels, dtype=torch.bool)
        mask[:, :2] = True
        batch = replace(self.batch, copy_mask=mask)
        base_loss, base_values = compute_loss(
            self.model, batch, self.inventory, Objective(mode="token_only"))
        weighted_loss, weighted_values = compute_loss(
            self.model, batch, self.inventory,
            Objective(mode="token_only", source_copy_weight=0.5))
        self.assertEqual(weighted_values["copy_token_count"], 4)
        self.assertTrue(torch.isfinite(weighted_values["copy_token"]))
        torch.testing.assert_close(weighted_loss - base_loss,
                                   0.5 * weighted_values["copy_token"])
        self.assertEqual(base_values["copy_token_count"], 0)

    def test_source_copy_loss_requires_alignment_mask(self):
        with self.assertRaisesRegex(ValueError, "alignment mask"):
            compute_loss(self.model, self.batch, self.inventory,
                         Objective(mode="token_only", source_copy_weight=0.5))

    def test_batch_rejects_unlicensed_or_mislabelled_edges(self):
        self.batch.pairs = (EdgePair(0, 1, "unknown"),)
        with self.assertRaises(ValueError):
            self.batch.validate(self.cfg, self.inventory)
        self.batch.pairs = ()
        self.batch.language_ids = torch.tensor([0, 1])
        with self.assertRaises(ValueError):
            self.batch.validate(self.cfg, self.inventory)

    def test_target_and_teacher_forcing_must_agree(self):
        self.batch.target = self.batch.target.clone()
        self.batch.target[0, 0] = 3
        with self.assertRaises(ValueError):
            self.batch.validate(self.cfg, self.inventory)

    def test_batch_rejects_wrong_bos_even_when_remaining_shift_matches(self):
        self.batch.validate(self.cfg, self.inventory)
        self.batch.decoder_input[0, 0] = 3
        with self.assertRaisesRegex(ValueError, "configured BOS"):
            self.batch.validate(self.cfg, self.inventory)

    def test_nondefault_bos_is_shared_by_training_and_generation(self):
        cfg = replace(self.cfg, bos_id=3)
        model = TIDEJEPA(cfg)
        with self.assertRaisesRegex(ValueError, "configured BOS"):
            self.batch.validate(cfg, self.inventory)
        self.batch.decoder_input[:, 0] = cfg.bos_id
        self.batch.validate(cfg, self.inventory)
        with self.assertRaisesRegex(ValueError, "configured BOS"):
            model.generate(self.batch.source, self.batch.action_ids, self.batch.language_ids, 1, 2, 4)
        with torch.no_grad():
            model.output.weight.zero_()
            model.output.bias.zero_()
            model.output.bias[2] = 10
        output = model.generate(self.batch.source, self.batch.action_ids, self.batch.language_ids, cfg.bos_id, 2, 4)
        self.assertEqual(output.tolist(), [[3, 2], [3, 2]])

    def test_autoregressive_generation_ends_at_eos(self):
        with torch.no_grad():
            self.model.output.weight.zero_()
            self.model.output.bias.zero_()
            self.model.output.bias[2] = 10
        output = self.model.generate(self.batch.source, self.batch.action_ids, self.batch.language_ids, 1, 2, 4)
        self.assertEqual(output.tolist(), [[1, 2], [1, 2]])

    def test_byte_decoder_masks_invalid_utf8_and_finishes_codepoints(self):
        cfg = replace(self.cfg, vocab_size=259)
        model = TIDEJEPA(cfg)
        source = torch.tensor([[4, 5]])
        action = torch.tensor([0])
        language = torch.tensor([0])
        with torch.no_grad():
            model.output.weight.zero_()
            model.output.bias.fill_(-20)
            model.output.bias[3 + 0x80] = 100  # Invalid as a first byte.
        output = model.generate(source, action, language, 1, 2, 4)[0].tolist()
        self.assertEqual(output[-1], 2)
        self.assertTrue(bytes(token - 3 for token in output[1:-1]).decode("utf-8") is not None)
        with torch.no_grad():
            model.output.bias.fill_(-20)
            model.output.bias[3 + 0xC3] = 100
            model.output.bias[3 + 0xA9] = 90
            model.output.bias[2] = 80
        output = model.generate(source, action, language, 1, 2, 3)[0].tolist()
        self.assertEqual(output[-1], 2)
        self.assertEqual(bytes(token - 3 for token in output[1:-1]).decode("utf-8"), "é")

    def test_generation_rejects_fractional_or_boolean_eos_and_budget(self):
        for value in (2.5, 2.0, True, None, -1, self.cfg.vocab_size):
            with self.subTest(eos=value), self.assertRaises(ValueError):
                self.model.generate(self.batch.source, self.batch.action_ids, self.batch.language_ids, 1, value, 4)
        with self.assertRaisesRegex(ValueError, "max_new_tokens"):
            self.model.generate(self.batch.source, self.batch.action_ids, self.batch.language_ids, 1, 2, 4.0)

    def test_direct_encoder_rejects_left_padding(self):
        with self.assertRaisesRegex(ValueError, "right padding"):
            self.model.online(torch.tensor([[0, 4, 5]], dtype=torch.long))

    def make_composition_batch(self):
        first = Action("TEST_KIND", "FIRST_VALUE")
        second = Action("TEST_KIND", "SECOND_VALUE")
        inventory = Inventory(
            (first, second),
            {
                "en": frozenset((first, second)),
                "vi": frozenset((first, second)),
            },
        )
        edges = (
            Edge("en", "frame-0", "frame-1", first),
            Edge("en", "frame-1", "frame-2", second),
            Edge("vi", "frame-0", "frame-1", first),
            Edge("vi", "frame-1", "frame-2", second),
        )
        target = torch.tensor([[9, 10, 2], [11, 12, 2], [13, 14, 2], [6, 7, 2]])
        batch = Batch(
            source=torch.tensor([[4, 5, 0], [10, 11, 0], [7, 8, 0], [12, 13, 0]]),
            target=target,
            decoder_input=torch.cat((torch.ones(4, 1, dtype=torch.long), target[:, :-1]), dim=1),
            labels=target.clone(),
            action_ids=torch.tensor([0, 1, 0, 1]),
            language_ids=torch.tensor([1, 1, 0, 0]),
            edges=edges,
            paths=(EdgePath((0, 1)), EdgePath((2, 3))),
            path_pairs=(PathPair(0, 1, "same_event"),),
        )
        cfg = replace(self.cfg, action_count=2)
        return TIDEJEPA(cfg), inventory, batch

    def test_action_path_is_sequential_and_ordered(self):
        model, _, batch = self.make_composition_batch()
        state = model.online(batch.source[:1])
        language = torch.tensor([1])
        actions = torch.tensor([0, 1])
        path_prediction = model.predict_path(state, actions, language)
        sequential = model.predict(model.predict(state, actions[:1], language), actions[1:], language)
        torch.testing.assert_close(path_prediction, sequential)
        reversed_prediction = model.predict_path(state, torch.tensor([1, 0]), language)
        self.assertFalse(torch.allclose(path_prediction, reversed_prediction))

    def test_composed_training_objective_has_endpoint_text_and_cross_language_losses(self):
        model, inventory, batch = self.make_composition_batch()
        loss, values = compute_loss(model, batch, inventory, Objective(mode="tide"))
        self.assertTrue(torch.isfinite(loss))
        for key in ("path_jepa", "path_token", "path_alignment"):
            self.assertTrue(torch.isfinite(values[key]))
            self.assertGreater(values[key].item(), 0)
        loss.backward()
        self.assertGreater(model.transition[0].weight.grad.abs().sum().item(), 0)
        self.assertGreater(model.output.weight.grad.abs().sum().item(), 0)
        trainer = Trainer(model, inventory, Objective(mode="tide"))
        metrics = trainer.step(batch)
        self.assertEqual(trainer.steps, 1)
        self.assertGreater(metrics["path_jepa"], 0)
        self.assertGreater(metrics["path_token"], 0)

    def test_baselines_receive_the_same_composed_path_text_supervision(self):
        model, inventory, batch = self.make_composition_batch()
        _, token_values = compute_loss(model, batch, inventory, Objective(mode="token_only"))
        _, generic_values = compute_loss(model, batch, inventory, Objective(mode="generic_jepa"))
        _, static_values = compute_loss(model, batch, inventory, Objective(mode="static_alignment"))
        _, tide_values = compute_loss(model, batch, inventory, Objective(mode="tide"))
        self.assertGreater(token_values["path_token"].item(), 0)
        self.assertEqual(token_values["path_jepa"].item(), 0)
        self.assertEqual(token_values["path_alignment"].item(), 0)
        self.assertGreater(generic_values["path_jepa"].item(), 0)
        self.assertGreater(generic_values["path_token"].item(), 0)
        self.assertEqual(generic_values["path_alignment"].item(), 0)
        for mode, values in (("generic_jepa", generic_values), ("static_alignment", static_values), ("tide", tide_values)):
            with self.subTest(mode=mode):
                torch.testing.assert_close(values["path_token"], token_values["path_token"])

        # Static alignment compares final states; TIDE compares their changes.
        # The fixture has different source states, so these contracts differ.
        with torch.no_grad():
            starts = model.online(batch.source[[0, 2]])
            endpoints = torch.cat((
                model.predict_path(starts[:1], batch.action_ids[:2], batch.language_ids[:1]),
                model.predict_path(starts[1:], batch.action_ids[2:], batch.language_ids[2:3]),
            ))
            canonical_endpoints = model.canonical(endpoints)
            deltas = canonical_endpoints - model.canonical(starts)
            expected_static = (canonical_endpoints[0] - canonical_endpoints[1]).square().mean()
            expected_tide = (deltas[0] - deltas[1]).square().mean()
        self.assertGreater(static_values["path_alignment"].item(), 0)
        torch.testing.assert_close(static_values["path_alignment"], expected_static)
        torch.testing.assert_close(tide_values["path_alignment"], expected_tide)
        self.assertFalse(torch.isclose(expected_static, expected_tide))

    def test_generation_accepts_an_ordered_action_path(self):
        model, _, batch = self.make_composition_batch()
        with torch.no_grad():
            model.output.weight.zero_()
            model.output.bias.zero_()
            model.output.bias[2] = 10
        output = model.generate_path(
            batch.source[:1], torch.tensor([0, 1]), batch.language_ids[:1], 1, 2, 4
        )
        self.assertEqual(output.tolist(), [[1, 2]])


if __name__ == "__main__":
    unittest.main()
