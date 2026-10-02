> **CURRENT COMPONENT DRAFT — TIDE-JEPA, 2026-09-28.** The project covers Vietnamese, English, and Phan Rang Cham. This document specifies only the proposed Vi–En annotation component; its example schema and action inventory are not a complete multilingual corpus specification. The [active specification](tide_jepa_spec.md) keeps language IDs, actions, and tokenization configurable. Phan Rang Cham actions, forms, and writing conventions require speaker and language-expert validation; none are defined here. No example below is approved data.
# Vi–En tense–polarity corpus: annotation protocol draft

The user separately authorized an **AI-authored/AI-reviewed preliminary pilot** with later human review. That engineering workflow is documented in [VI_EN_PILOT.md](VI_EN_PILOT.md); its results are preliminary and do not satisfy this document's human-validated scientific benchmark gates. PhoMT translation pairs remain source material, not action-labeled transitions.

Status: English–Vietnamese core authoring specification only; no examples in this file are approved training or test data. Human bilingual review is required before any item is treated as ground truth. This action inventory must not be copied to Phan Rang Cham without community and linguist validation.

## Unit of annotation

One item is a source utterance, a target language, and an explicit action program that describes what the generated utterance must realize. Store an abstract event/meaning record only for annotation and evaluation; it is not a third training language. One item may have several accepted target strings.

Required JSONL fields:

```json
{
  "item_id": "stable-id",
  "template_family_id": "held-out-split-key",
  "domain": "one-of-the-registered-domains",
  "source_language": "en|vi",
  "source_text": "",
  "target_language": "en|vi",
  "meaning_frame": {"predicate": "", "roles": {}, "polarity": "positive", "time": "current|past", "time_context": ""},
  "action_program": [{"type": "TIME", "value": "PAST", "preconditions": ["explicit temporal context"]}],
  "licensed_relations": [{"action_a": "", "action_b": "", "relation": "same_event|scope_different|unknown", "context": ""}],
  "accepted_targets": [""],
  "disallowed_targets": [""],
  "phenomena": [""],
  "review": {"reviewer_count": 0, "adjudicated": false}
}
```

Annotator IDs and free-text rationales stay in a private adjudication file; public data uses anonymized IDs and only consented material.

## Version 1 action inventory

| Abstract action | English realization to review | Vietnamese realization to review | Semantic status |
|---|---|---|---|
| `TIME=NOW` / `TIME=PAST` | tense and auxiliary form; temporal adverb when needed | temporal context/adverb and particles; do not equate a single particle with English tense | Changes the event's temporal relation; time anchor must be explicit |
| `POLARITY=POSITIVE` / `POLARITY=NEGATIVE` | `not`/auxiliary choice and scope | `không`, `chưa`, or another reviewed form with correct scope | Changes truth conditions; annotate polarity explicitly |

The abstract action label may be shared only for the same event-state operation. Surface realization and preconditions are language-specific. For `TIME` and `POLARITY`, reviewers compare the final event meaning and scope after each proposed path. Mark a pair `same_event` only when both routes express the same time and polarity; mark `scope_different` when interpretation changes; otherwise mark `unknown`. Only `same_event` path pairs enter JEPA path-consistency loss. For TIDE-JEPA, English–Vietnamese alignment is applied to the meaning-space transition caused by a shared action, not just to static sentence endpoints.

Illustrative item shape (not approved as a gold example): event frame `Lan / buy / book`, temporal anchor `before reference time`, polarity `negative`; target language `vi` or `en`; action program `[TIME=PAST, POLARITY=NEGATIVE]`; one or more native-reviewed target sentences. The Vietnamese wording must be chosen by reviewers in context rather than obtained by mechanically substituting a particle.

## Gate before Phan Rang Cham inclusion

This protocol does not define a Phan Rang Cham corpus. Before collecting or generating Phan Rang Cham, consult the specific language community and a field linguist to identify the variety/autonym, current speakers, accepted writing or recording/transcription practices, task-appropriate semantic actions, consent and data rights. Ethnic-population counts and lexical wordlists are not substitutes for verified language data. If ordinary text generation is not community-appropriate, do not claim written-language generation; treat a separately approved oral pilot as a different modality and study.

## Authoring and adjudication

1. Authors draft source meanings and transformations directly; no model-generated sentence is accepted as gold without human revision.
2. Two independent fluent/native reviewers assess meaning, action satisfaction, grammar, orthography/diacritics, and acceptable variants. A third reviewer adjudicates disagreements.
3. Keep all acceptable forms. Do not penalize word-order, pronoun, particle, or classifier variants that preserve the annotated meaning and are judged natural.
4. Record reviewer agreement per field and per phenomenon. Drop or rewrite items with unresolved scope, ambiguous temporal reference, dialect mismatch, or unresolvable variation.
5. Use a held-out test set split by template family, underlying meaning frame, and domain. No near-duplicate transformation from the same template family may cross train/dev/test.
6. Freeze the test before model tuning. Threshold calibration uses a separate validation partition, never test labels.

## Pilot composition

Proposed first pilot: 100–200 event frames, both translation directions, the two actions above, and a deliberately held-out set of `TIME × POLARITY` combinations. The pilot estimates ambiguity and inter-annotator agreement; it is not a publishable result or evidence of generalization. Expand only after the action schema passes adjudication. Number/classifiers, voice, and agreement are outside version 1.

## Quality gates

- Every target must satisfy its action program and preserve or modify meaning exactly as declared.
- Every claimed valid path must end in the same meaning frame and have independent reviewer approval.
- Report accepted-variant count, unresolved/discarded items, and per-language/direction counts.
- Training examples, validation examples, and final test examples are authored from disjoint template families.
- The same approved text examples and action labels are supplied to every baseline; JEPA is tested as a learning objective, not as a hidden data-augmentation advantage.

