# v4.33 English–Vietnamese pilot status — 2026-10-09

This is preliminary, AI-authored/AI-reviewed synthetic evidence. It is not human/native-speaker validation, natural-language translation quality, or evidence of research efficacy. PhoMT was not used. Phan Rang Cham remains disabled pending dataset-use permission and language/community review.

## Frozen experiment and checker repair

v4.33 froze a fresh corpus/split, an isolated train/validation review bundle, and six fixed-final runs (TIDE and token-only control × seeds 17/23/41; 58 epochs). All six completed and passed checkpoint/run identity checks. Validation generation ran before any release-holdout scoring.

The first frozen validation report showed zero semantic-checker coverage for the new `compose433_` event family. Investigation found the narrow checker had omitted the v4.33 event registry. This was a checker registration defect, not a changed generation output. The generated validation text was preserved unchanged and rescored with the corrected checker. The original evaluator report remains intact as incident evidence; the aggregate-only reassessment is [here](audits/2026-10-08/v433_validation_checker_reassessment.json).

The correction changed the current evaluator hash, so release scoring used a separate local v2 amendment bound to the original protocol, unchanged thresholds/runtime/data/split/configs/checkpoints, current evaluator hashes, and corrected validation report. The amendment did not alter model weights or training identity. The first release attempt was rejected by the checkpoint identity guard before it wrote any test output; the inference adapter was then updated to accept only the protocol’s original implementation identity after the amendment validates. Regression tests preserve the default strict identity check. The amendment and all dataset/review/checkpoint files remain under Git-ignored `data/` and `runs/`.

## Results

All three primary TIDE configurations passed every frozen validation bucket and all 30/30 release-test buckets. Per TIDE run, the release set contains 2,880 generated examples (1,280 single-action examples per language and 160 held-out paths per language). Across the three TIDE seeds, the minima by task were:

| Release-test task | Lowest action fidelity | Lowest preservation | Unicode / EOS / checker coverage |
|---|---:|---:|---:|
| English single-action | 99.06% | 94.38% | 100% |
| English held-out path | 99.38% | 96.25% | 100% |
| Vietnamese single-action | 99.69% | 98.75% | 100% |
| Vietnamese held-out path | 100% | 100% | 100% |

The corresponding corrected validation minima were 99.06% action fidelity / 92.81% preservation for English singles, 100% / 96.88% for English paths, 99.69% / 98.75% for Vietnamese singles, and 99.38% / 98.75% for Vietnamese paths. The frozen thresholds were unchanged: single-action ≥90%, paths ≥80%, Unicode and semantic-checker coverage 100%.

Token-only is the control and remains `control_only` for the primary quality gate. It performed similarly; it was slightly better on some Vietnamese and English path metrics and slightly worse on others. These results do not establish a consistent TIDE advantage. Detailed aggregate-only release results, per-bucket checks, protocol/checkpoint/evaluation hashes, and the amendment hash are in [the release report](audits/2026-10-08/v433_release_holdout_aggregate.json).

## Preliminary AI linguistic spot check

Two independent `gpt-6-luna` high reviewers assessed a seeded, stratified sample of 48 validation outputs (four per seed × language × task cell). They judged 47/48 acceptable for grammaticality/naturalness, 48/48 for meaning preservation, and 48/48 for requested-action fidelity. Both identified one minor spelling issue. One reviewer had medium confidence on fine-grained Vietnamese idiom; some synthetic event/object pairings were described as contextually unusual. The sample is small and synthetic, does not include release-test rows, and is not human/native-speaker validation. The frozen output was not edited and must not be tuned against this sample. See the [aggregate report](audits/2026-10-08/v433_validation_ai_linguistic_review.json) and [summary](audits/2026-10-08/v433_validation_ai_linguistic_review.md). Recreate the same private 48-case packet without printing text using:

```sh
.venv/bin/python -B scripts/sample_v433_validation_review.py --output /tmp/v433-validation-review-reproduction.jsonl
```

The packet SHA-256 is `3af4273d31d6878b305446533946419b7617abdcb8819dd7e357cefc3153b018`.

To advance beyond AI-only evidence, two separate blank-rating handoff forms were prepared locally for independent bilingual reviewers: [review packet instructions](data/pilot/vi-en-ai-v4.33/human-review/README.md), [reviewer A](data/pilot/vi-en-ai-v4.33/human-review/reviewer-a.csv), and [reviewer B](data/pilot/vi-en-ai-v4.33/human-review/reviewer-b.csv). They contain validation-only synthetic examples and are Git-ignored. No human ratings have been collected; do not report this as human validation. Once returned, the [aggregate-only summarizer](scripts/summarize_v433_human_review.py) checks alignment/completeness and reports agreement without storing reviewer notes or examples; it does not set a quality pass threshold.

## Demo and use boundary

The updated local runner serves the seed-17 TIDE checkpoint only on loopback and reports `validation_gate_status=pass`, `human_validated=false`, and `quality_status=diagnostic_only`. The stock page's old default had zero exact matches in the v4.33 corpus and produced a semantically corrupted output; this indicates an out-of-corpus demo input, not an in-distribution estimate. The current runner now fills the default from an approved train-only Vietnamese `TIME:PAST` example and allows only exact train source/action combinations. A direct loopback smoke returned HTTP 200 for an approved example and HTTP 400 for an unknown source, an unregistered action on a known source, unsupported action, and cross-language request. A separate 19-case boundary smoke passed the exact train-only default and expected refusals for whitespace/case/punctuation/Unicode variants, a plausible out-of-corpus source, an injection suffix, empty source, cross-language/action/token-limit requests, malformed or oversized bodies, invalid Host/Origin, wrong content type, and unknown route; it does not establish a general semantic OOD detector. The earlier browser smoke also verified valid UTF-8 and the narrow semantic frame check. A real-browser test with a deliberate two-second response delay verified that edits made while waiting remain separate from the submitted request and the returning result is visibly marked stale. A 120-request sequential smoke returned 200/valid UTF-8 for every request (p50 91.0 ms, p95 103.5 ms, maximum 108.2 ms); an eight-request burst produced one 200 and seven 503 busy responses, after which health returned 200. A separate five-minute loopback soak completed 3,132/3,132 successful UTF-8 requests, with 31/31 health checks passing (p95 108.7 ms, p99 116.7 ms, max 149.4 ms). An incomplete-body test returned 400 after timeout while four concurrent health checks remained 200. A historical one-process smoke observed RSS rising from 285,356 to 303,720 KiB over 20 requests; it was not a benchmark and is not directly comparable to the current listener measurement. Two current-listener runs of 240 sequential requests each returned 240/240 HTTP 200 responses, valid UTF-8, nonempty diagnostic-only outputs, and p95 latencies of 106.920 ms and 106.642 ms. RSS was sampled 14 times per run and remained 85,520 KiB throughout both; aggregate-only reports are linked below. These bounded results do not establish long-duration behavior: natural/arbitrary request workloads, production capacity, and semantic OOD remain unverified; synthetic varied train-only workloads and concurrent refusal behavior have separate aggregate checks. Naturalness and human evaluation remain unverified, so the checkpoint is not approved for natural-language or translation use. A current loopback smoke returned 200 for `/`, `/health`, and an approved train-only request, and 400 for unknown-source and cross-language requests; the response passed the narrow action/preservation checker and only aggregate fields were recorded. A repeated 300-second sequential soak passed 3,219/3,219 requests with valid UTF-8, 30/30 health checks, p95 103.5 ms, p99 108.7 ms, and max 143.8 ms; it recorded no source or generated text. The varied synthetic and concurrent-overload checks are now separately reported below; natural/arbitrary payload quality and production capacity remain open. See [current request/checker smoke](audits/2026-10-08/v433_current_loopback_smoke_v3.json), [current health/allowlist smoke](audits/2026-10-08/v433_current_loopback_smoke_v2.json), [19-case boundary smoke](audits/2026-10-08/v433_demo_boundary_smoke.json), [five-minute soak](audits/2026-10-08/v433_live_loopback_soak_repeat.json), [runtime benchmark run 1](audits/2026-10-08/v433_demo_runtime_benchmark_3.json), [runtime benchmark run 2](audits/2026-10-08/v433_demo_runtime_benchmark_4.json), [benchmark script](scripts/benchmark_v433_demo_runtime.py), and [demo smoke history](audits/2026-10-08/v433_demo_smoke.json).

## Linux verification and reproduction

Host: Arch Linux 7.2.8-arch1-2, x86_64; AMD Ryzen 5 4600H, 12 logical CPUs; Python 3.11.17; PyTorch 2.14.0+cpu; CUDA unavailable. At the original v4.33 evaluation checkpoint, the full suite passed 147 tests with zero skips; the DOM behavior test, final-code browser stale-response smoke, `compileall`, `pip check`, and `git diff --check` passed. The pinned Linux CPU lock was satisfied in a temporary CPython 3.11 virtualenv, which also passed 147 tests with zero skips and `compileall`/`pip check` from a 197-path source-only snapshot excluding `.git`, `.venv`, `data/`, and `runs/`. The strengthened cross-process output-lock test was then targeted-tested in both environments. [Current follow-up evidence](audits/2026-10-08/linux-lock-bootstrap.json) now records the 150-test suite after durability changes and the lock/source scope. The snapshot was made from the current uncommitted working tree, not a committed revision or clean OS image. PyTorch emits an optional NumPy initialization warning; it did not affect the checks.

E02 follow-up: training-run split-manifest, resolved JSON, CSV, and checkpoint publication fsyncs file contents before rename and the parent directory after rename on POSIX. The standalone data-authoring manifest helper remains atomic without an fsync durability claim. Fault injection covers `os.replace`, file `fsync`, and directory `fsync` errors through the run publication helpers; pre-rename failure preserves the old destination, while post-rename directory-sync failure leaves a complete new destination visible and propagates the failure. Subprocess hard-exit tests cover restart before initial metrics publication, recovery after durable metrics/latest publication, and cleanup of a synced metrics temp left before rename. The current project and pinned-lock source-only environments each pass 150 tests with zero skips; compileall and pip check pass in both. The source-only snapshot excludes `.git`, `.venv`, `data/`, and `runs/`. This engineering update does not change frozen v4.33 training, validation, or release evidence, and does not simulate physical power loss.

2026-10-09 source-only follow-up: after adding four regression tests for the human-review aggregate tool, a refreshed 219-file source snapshot passed 154 tests with zero skips, plus `compileall` and `pip check`, in a newly created virtualenv installed from the pinned Python 3.11/PyTorch 2.14 CPU lock. The snapshot excluded `.git`, `.venv`, `data/`, and `runs/`. PyTorch emitted a non-fatal warning because NumPy is not part of the pinned lock; all tests passed. See the [final reproduction report](audits/2026-10-09/linux-source-only-final-reproduction.json). This does not simulate a clean OS image or physical power loss.

Re-score cached validation output without regenerating text:

```sh
.venv/bin/python -B scripts/rescore_v433_validation_checker.py data/pilot/vi-en-ai-v4.33
```

The v2 release amendment and holdout are already recorded. To verify/rebuild the aggregate from the immutable cached results (this reopens the already-scored test metrics but does not regenerate text):

```sh
.venv/bin/python -B scripts/evaluate_v433_release_holdout.py
```

Run the diagnostic-only local demo:

```sh
.venv/bin/python -B scripts/run_v433_demo.py --port 8765
```

Open `http://127.0.0.1:8765`; stop the process with Ctrl-C. The test metrics and generated text stay in Git-ignored `runs/`; the audit reports contain only aggregates and hashes. No commit or push was made.


### 2026-10-09 bounded concurrency follow-up

The already-running loopback service was confirmed as `run_v433_demo.py` and `/health` remained operational with `diagnostic_only`, `human_validated=false`, and `phomt_trained=false`. Two aggregate-only 4-client/80-request runs used only the approved page-default request. Each returned one HTTP 200 and 79 schema-valid HTTP 503 busy refusals, as expected from the one-inference limit; RSS increased 112 KiB on the repeated run after an initial 1.6 MiB warm-up. The behavior is bounded overload refusal, not queued multi-user serving. See [concurrency run 1](audits/2026-10-09/v433_demo_concurrent_bound.json), [run 2](audits/2026-10-09/v433_demo_concurrent_bound_repeat.json), and the [refreshed Linux reproduction report](audits/2026-10-09/linux-source-only-final-reproduction.json). Varied payloads and production capacity remain unverified.


### 2026-10-09 varied train-only request follow-up

The aggregate-only runtime tool now supports `--vary-approved`, which constructs requests only from the exact v4.33 train split after confirming the AI-preliminary, PhoMT-free provenance. It balances 64 candidates across English/Vietnamese and single-action/two-action paths, keeps text in process memory only, and emits aggregate counts. Two sequential 40-request runs returned 40/40 HTTP 200 with valid UTF-8 and nonempty diagnostic outputs; the narrow checker passed all 40 cases in four language/task cells (10/10 each). RSS was unchanged during the first pass and rose 4 KiB across the repeated pass. Reports: [run 1](audits/2026-10-09/v433_demo_varied_quality_benchmark_1.json), [run 2](audits/2026-10-09/v433_demo_varied_quality_benchmark_2.json). This does not establish natural-corpus, human, semantic OOD, or production-capacity quality.
