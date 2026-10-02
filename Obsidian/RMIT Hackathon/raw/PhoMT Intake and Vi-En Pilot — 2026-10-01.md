# PhoMT intake and Vi–En preliminary pilot — 2026-10-01

Source: direct user instructions and local tool/command results from this project conversation on 2026-10-01. This record contains aggregate metadata only, no PhoMT rows or generated dataset examples. It preserves the completed handoff after the earlier empty-folder check.

## User decisions

- Continue to an English–Vietnamese completion milestone; defer Phan Rang Cham until dataset-use permission is obtained. Linguistic/community review remains required before Cham training/evaluation.
- User explicitly authorized AI authoring, review and adjudication for a preliminary pilot, with personal/human review later: “Đúng, dùng AI để hoàn thiện pilot sơ bộ”. This is not evidence of human validation.
- Newly created agents/subagents must use `gpt-6-luna` with `high` or `xhigh`; another model requires prior user agreement. The two interrupted earlier review tasks were stopped and transferred to separate Luna/high agents, `luna_review_vi_en_a` and `luna_review_vi_en_b`. No earlier reviewer was reactivated.

## Archive and source selection evidence

The two authorized locations were checked first. `data/raw/phomt/PhoMT.zip` exists at 355,890,192 bytes; `C:\Users\ANHKHOI\Downloads\PhoMT.zip` is absent. No matching partial download was found in those directories. No new download or login was attempted.

SHA-256 matches the user-supplied value exactly: `fd58972b5058b17d0823b78e6ce7dbb775243e156efa2ca222079dbdd76e6a2e`. Supplied file revision: `aee99d07f0f5e6faf64b64f52adf314563350ce5`. The revision is a provenance reference supplied with the hash; it is not independently inferred from ZIP contents.

The project auditor ran with `verify_crc=False`. It accepted paths, member counts and declared sizes: 22 members, 13 files, 1,064,737,892 declared uncompressed bytes. Suffixes: six `.en`, six `.vi`, one `.md`; no `.pkl`/`.pickle` suffix. No member was decompressed during this metadata audit, extracted, unpickled or executed. Report: `data/raw/phomt/PhoMT.metadata-audit.json` (Git-ignored).

After the user authorized continuation, the original source sampler streamed only `PhoMT/detokenization/train/train.en` and `.vi`. It checked 2,977,999 paired lines, found 2,944,299 eligible pairs under a predeclared 384-byte-per-language bound, and selected 160 pending packets with seed 20261001. No official dev/test members were read, no full extraction was performed, and no translation links were inferred to be semantic-action labels. Selection metadata: `data/derived/phomt/pilot-source-v1/selection.json`; source text remains private in `authoring.jsonl`. Packet SHA-256: `2669c7c29c56d45720c02b39247cd6aa8fc76eb829bfcac52501d84c9ad146fd`. No PhoMT rows were used in any training run.

## Original synthetic pilot and reviews

The preliminary training corpus was authored independently in `tide_jepa/pilot_seed.py`; it contains no PhoMT content. It has 400 records, 20 predicate/event families and 4 explicit time/polarity states per event. Split: 240 train, 80 validation, 80 test records; 12/4/4 families. English/Vietnamese equivalents and path states share groups. Sentence templates are shared across partitions: this is not template/domain generalization evidence.

Two separately dispatched Luna/high reviewers checked all 400 actual draft rows, explicit alignments and paths. One v1 review approved; the other requested a singular-book specificity correction. The root accepted the finding. Only 10 Vietnamese read-family rows changed, representing 20 sentence endpoints; both reviewers approved v2 independently. V1 is preserved. The v3 final run uses the exact same corrected data/review files; the version change concerns engineering guard fixes, not test-informed label or hyperparameter changes.

Draft SHA-256: `1963ed3a7e6feb9071d8a8f68b81de383e969db8067a08e35a5f2262ab673ed0`. Approved corpus fingerprint: `5cfc86a691b262e055100cb395a251cffd1e01afa5b0ab50c91fc2cfdebf3929`. Frozen split SHA-256: `a03526e9b6a95778755d8f9a2ec9fcedf8b0c3da41a5bc61cfc3188944380534`. Review files, adjudication, approval, frozen protocol and corpus are private under `data/pilot/vi-en-ai-v3/`.

Training/validation paths use negative polarity then past time; test paths use the held-out reverse order. Constituent single actions remain in training. The user-approved review status is `AI-preliminary`, with `human_validated=false`. Local metadata is an assertion rather than cryptographic proof of reviewer identity; independent dispatches are evidenced in this conversation.

## Completed runs, results and engineering evidence

Final suite: four modes (`token_only`, `generic_jepa`, `static_alignment`, `tide`) × three seeds (17, 23, 41), 40 epochs, 120 updates per run. Identical corpus/split, byte tokenizer, width 32, four heads, one layer, maximum length 192, batch size 80 and learning rate 0.001. All 12 training runs finished before test evaluation. Checkpoint selection uses validation token loss plus path token loss for all modes. Generation bound: 160 new byte tokens.

The final suite recorded **0/864 exact matches** and **564/864 valid UTF-8 outputs**. It reproduces the initial suite's generation totals after runtime/checkpoint guard repairs with unchanged data and budgets. These negative results do not show useful language generation or a TIDE advantage. Public aggregate tables and per-language/task breakdown are in [VI_EN_RESULTS.md](../../../VI_EN_RESULTS.md); private run report is `data/pilot/vi-en-ai-v3/suite_report.json`. Checkpoints, loss logs, private generations, verified screenshot and implementation snapshot are under `runs/vi-en-ai-v3/`, which is Git-ignored.

The final CPU suite passed **48 tests, 0 skipped**; compilation and `pip check` passed. The base Python 3.11.9 interpreter used `.venv/Lib/site-packages` because the venv launcher failed. No new runtime, GPU build or external code was installed. Tests exercised approval/split/provenance checks, actual mixed-length teacher-forcing padding, checkpoint/inventory identity, protection from fresh-run overwrite, invalid-alignment rollback, local demo API, and epoch-resume tensor equivalence.

Independent Luna/high engineering review found and rechecked provenance/approval, freeze publication order, inference identity, resume RNG state and demo provenance/model-label issues. The final closure approves those fixes. Review evidence is copied under `data/pilot/vi-en-ai-v3/engineering-*.json`; no independent reviewer modified source or trained a model.

The browser demo at `http://127.0.0.1:8765` was exercised using TIDE/seed 17. The UI displayed a generated result and the invalid-UTF-8 indicator. It renders checkpoint mode/seed from validated metadata, binds only to loopback, uses no cloud calls and does not save/log user input/output. Launch script: `scripts/run_vi_en_demo.ps1`. Screenshot: `runs/vi-en-ai-v3/demo-verified.jpg`.

## Unfinished scientific/data gates

The engineering pilot is complete; a useful or human-validated English–Vietnamese generator is not complete. PhoMT-derived action annotations, independent human bilingual evaluation, accepted variants, stronger preregistered generation experiments and matched-compute evidence remain unfinished. Phan Rang Cham stays deferred. PhoMT terms and EMNLP citation remain binding as recorded in [[PhoMT Permission Confirmation — 2026-10-01]]. No dataset or weights were published.
