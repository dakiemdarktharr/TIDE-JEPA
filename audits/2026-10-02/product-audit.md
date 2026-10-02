# TIDE-JEPA product and pre-Cham audit — 2026-10-02

## Scope and evidence boundaries

Read-only review of `tide_jepa/demo.py`, `demo.html`, `infer.py`, relevant model/tokenizer contracts and tests, the launch/results/setup scripts, dependency declaration, current specification/roadmap/README, Vi–En annotation protocol and research notes, and current Ground Truth/first-milestone Obsidian notes. Raw Obsidian sources and PhoMT intake/permission notes were not opened. No PhoMT rows or private pilot artifacts were read, copied, or printed. No archive was unpickled or executed. Only this audit file was written.

The already-running demo at `127.0.0.1:8765` was left running. Read-only `GET /health` reported `mode=tide`, `seed=17`, `human_validated=false`, and `phomt_trained=false`. Synthetic HTTP probes returned 404 for an unknown GET, 415 for a non-JSON POST, and 400 for malformed JSON. A valid synthetic English request with one action and `max_new_tokens=1` returned HTTP 200 and valid UTF-8, but only one generated character. This last probe demonstrates the endpoint accepts requests and returns a result; it is not a language-quality measurement. No test suite or browser automation was run for this audit.

## Prioritized findings

### P1 — The demo admits a checkpoint with known failed generation quality

**Evidence:** `tide_jepa/demo.py:82-87` requires preliminary provenance and checks language set, then starts the service. Its admission checks bind approval/review file hashes (`:67-81`) but do not inspect generation-quality evidence. `/health` reports operational `status=ready` and checkpoint metadata (`:28-33`). The page warns that output may be wrong (`tide_jepa/demo.html:15,29`), but it does not disclose the measured failure beside the generate action. `VI_EN_RESULTS.md:18-20` reports 0/864 exact matches and 564/864 valid UTF-8 (65.3%), and explicitly says the pilot did not produce a useful controlled language generator. The results note says the browser demo was exercised (`:48`).

**Impact:** Users can launch the default TIDE seed-17 model through an interface that looks like a generator even though the only measured pilot has no exact matches and about one third of generated strings fail UTF-8 decoding. Provenance checks answer where the checkpoint came from; they do not establish that it is useful or safe to present as a working generator.

**Repair direction:** Make quality state a first-class serving/UI decision. For this checkpoint, prominently state “research prototype; measured generation failed; outputs are not usable language results,” or refuse generation behind an explicit research-only mode. Future admission thresholds must be declared on a new protocol and must include human bilingual action-fidelity, meaning-preservation, and naturalness review; do not tune against the existing test set or erase these negative results.

**Acceptance:** The current checkpoint cannot appear as a validated/useful generator; API/UI status explicitly separates provenance/operational readiness from quality status; a later checkpoint can be called a language-quality pass only after a frozen evaluation and qualified human review meet predeclared criteria. Keep `human_validated=false` for this AI-only pilot.

### P1 — Source language and target language can disagree silently

**Evidence:** `tide_jepa/demo.html:19-24` has a source textarea and an output-language dropdown, but no source-language selector or mismatch check. The helper text at `:21` says to enter Vietnamese for Vietnamese output and English for English output. The live interface instead allows a Vietnamese default sample with English output. `tide_jepa/infer.py:67-84` validates only `target_language`, action inventory, and source length; it cannot enforce the documented same-language contract. `VI_EN_PILOT.md:42` says translation edges are unsupported. The current annotation draft describes source/target language fields and both translation directions (`vi_en_annotation_protocol.md:10,19-22,60`), which is a future protocol mismatch with the implemented within-language edge model.

**Impact:** The UI can request an unsupported translation-like operation and return arbitrary model text without warning. This misrepresents the pilot interface and confounds a user’s interpretation of an already low-quality output.

**Repair direction:** Expose source language and require it to match target language for this pilot, or design and validate a separate translation path under an approved protocol. Do not infer language from script or model output. Reconcile the annotation protocol's cross-language source/target record with the model’s within-language transitions before using it to create data.

**Acceptance:** A mismatched source/target pair is rejected before inference with a clear message; same-language requests continue to use only the approved actions; protocol documentation states exactly which operation the implementation supports. Add focused tests for both routes.

### P2 — Results can be shown beside form values that were not submitted

**Evidence:** The submit handler at `tide_jepa/demo.html:36` snapshots form values into the JSON body, then awaits the response. Only the submit button is disabled; the textarea and selects remain editable. The output panel (`:29`) never shows which submitted source/actions produced the text.

**Reproduction:** Submit a request that takes long enough to run, edit the source or an action while it is pending, and wait for the response. The output was generated from the earlier snapshot but appears beside the changed form state.

**Impact:** It is easy to attribute an output to the wrong source/action, especially when requests take time or results are poor.

**Repair direction:** Lock inputs during a request or render an immutable submitted-request summary with each result; clear or label stale results after edits.

**Acceptance:** Every displayed result is visibly associated with the exact submitted source, language, and ordered actions; editing controls cannot make a completed result appear to belong to a different request.

### P2 — HTTP request size is capped, but inference work and request time are not

**Evidence:** `tide_jepa/demo.py:36-50` limits JSON body length to 65,536 bytes and performs generation synchronously. It uses single-threaded `HTTPServer` at `:87`; it has no socket/body read timeout, request timeout, or origin/host check. `tide_jepa/infer.py:74-82,91-109` accepts any nonempty action list and iterates every action through path inference. The web form offers at most two actions, but the HTTP endpoint imposes no matching path limit.

**Impact:** A malformed or unintended local client request can monopolize the sole server thread with a long action path, preventing the UI and `/health` from responding. A slow request body can also hold the connection open. Loopback binding and lack of request logging are useful protections, but the resource budget is not enforced at the inference boundary.

**Repair direction:** Apply a demo-specific maximum path length and generation-token cap, set a request read timeout, validate Host/Origin for the local UI threat model, and return bounded client errors for expected inference failures. Preserve loopback binding and no-content logging.

**Acceptance:** Requests above each documented limit fail quickly without invoking generation; a stalled/oversized request does not block health checks indefinitely; unsupported origins are rejected; synthetic concurrency/malformed-input checks do not expose or log request text.

### P2 — The annotation protocol and implementation do not yet describe one data contract

**Evidence:** `vi_en_annotation_protocol.md:10,19-25,60` models a source utterance, target language, and both translation directions. `tide_jepa/data.py` / `infer.py` model a within-language transition (the inference API accepts a source plus target language and action, without source-language metadata); `VI_EN_PILOT.md:42` explicitly excludes translation edges. The protocol is correctly labeled a draft and says no examples are approved (`vi_en_annotation_protocol.md:1,6`), but its “CURRENT COMPONENT DRAFT” label can lead future annotators to expect a directly ingestible implementation schema.

**Impact:** Future source packets could be annotated against fields and operations the runner cannot represent, or translation links could be mistaken for action supervision despite the current warnings.

**Repair direction:** Mark the protocol as a design-only future schema and add a mapping note: either create separately reviewed within-language transitions from source meanings, or extend the model/data contract for genuine cross-language edges after a design decision. Never infer semantic actions from translation links.

**Acceptance:** An annotator can tell which schema is currently ingestible and which is aspirational; a documented fixture maps each approved annotation record to model edges without assuming translations preserve action semantics.

### P2 — The demo launcher does not select the documented virtual-environment interpreter

**Evidence:** `scripts/run_vi_en_demo.ps1:4-5` adds `.venv\Lib\site-packages` to `PYTHONPATH` but invokes the global Python launcher `py -3.11`, rather than `.venv\Scripts\python.exe`. `requirements-test-cpu.txt:1-4` pins PyTorch only and explicitly leaves transitive dependencies to resolution. `README.md:41-48` discloses that this is not a full lock; `VI_EN_PILOT.md:27-42` documents the same PYTHONPATH workaround.

**Impact:** A fresh machine depends on its registered Python 3.11 and a populated compatible `.venv` package directory. The launcher can combine one interpreter with another environment’s packages, so the documented venv creation alone does not guarantee the demo startup path and dependency graph.

**Repair direction:** Launch through the project venv executable and provide a reproducible install/verification command for the demo. If full dependency locking is intentionally out of scope, document that limitation with the tested interpreter and package versions and fail with an actionable missing-environment message.

**Acceptance:** On a clean Windows checkout, the documented setup creates the runtime and the launch script uses that exact interpreter; `python -m pip check` and a health/generate smoke test pass without global package-path assumptions. Keep model/data artifacts local and ignored.

## Documentation conflicts and stale claims

- `Obsidian/RMIT Hackathon/wiki/First Implementation Milestone.md:6,12` calls the first-milestone snapshot “Current” and says paths and corpus ingestion do not yet exist. The active Ground Truth says M1–M3 and action-path support are implemented (`Project Ground Truth.md:6,36-38`), and the README documents path composition (`README.md:11-17`). The note has a 2026-09-28 fingerprint, so its facts can remain as historical evidence; change the status label and wording to make that explicit.
- `tide_jepa_spec.md:23-31,35-37,52` contains M1-era future-work and evidence text that predates the later M2/M3/pilot updates, while subsequent sections document paths, data contracts and 48-test/current pilot evidence. For example, `:52` still lists corpus-to-batch integration and serialization/resumption as future work even though current README/ROADMAP and Ground Truth describe M3 and experiment checkpointing as implemented. Label those paragraphs as dated milestone snapshots or refresh their current status so users do not mistake them for open work.
- `Obsidian/RMIT Hackathon/wiki/Project Ground Truth.md:29-30` says the pilot runs are complete and then says the Vi–En pilot “still needs” human-authored edits, bilingual review and held-out split design. The latter is true of the human-validated scientific benchmark but ambiguous because the AI-authored synthetic pilot already has a held-out split. Clarify that it refers to PhoMT-derived/human-validated follow-on data, not the completed preliminary pilot.
- `vi_en_annotation_protocol.md:55,67` requires disjoint template families across splits. `VI_EN_PILOT.md:11` says the completed AI pilot intentionally shares sentence patterns across splits. The pilot doc correctly limits its claim to held-out event/predicate families, and the annotation protocol correctly describes a stricter future human benchmark. Make the distinction explicit at the protocol's pilot composition section to prevent readers from assuming the current pilot met this future gate.

## Areas that pass or are appropriately bounded

- Loopback-only binding (`demo.py:87`), request-text log suppression (`:13-15`), JSON content-type/size checks (`:40-50`), `Cache-Control: no-store`, `nosniff` (`:20-25`), `textContent` output rendering (`demo.html:36`), and the provenance/review hash checks (`demo.py:67-84`) are good current controls.
- The result page and source notes identify AI provenance, no PhoMT training, absent human linguistic review, and deferred Cham. The report does not claim a useful generator or human validation.
- `VI_EN_RESULTS.md:18-20,51-55` honestly records poor generation and the limits of exact match/UTF-8 metrics. The open gap is that this negative result is not an enforced product state in the running demo.
- Research notes describe Cham data and linguistic permission as unresolved. No Cham training/evaluation should enter the demo or pilot before its separate permission and language-review gate passes.

## Honest completion criteria for a follow-on demo repair

Treat the engineering demo repair as complete when all of the following are evidenced: the current model is unmistakably marked research-only or prevented from generating under a validated-quality label; source/target language mismatch is rejected; request/result association is stable; resource bounds and local request checks are enforced; the documented Windows setup and launcher work from a clean checkout; and focused HTTP/UI tests cover those behaviors with synthetic text only. Keep the app and all data offline, keep PhoMT raw/derived rows under ignored `data/`, and never print rows into logs or chat.

Treat M4 language-quality completion as a separate gate: approved data-use and language-specific action decisions; independently authored examples with qualified bilingual review, adjudication and reported agreement; disjoint/frozen benchmark splits; a new preregistered evaluation with untouched test material; and human scores for action fidelity, meaning preservation, grammaticality/naturalness and acceptable variants. These are not satisfied by the current AI-only pilot, its 0/864 exact match score, or a repaired UI. Keep Phan Rang Cham deferred until source-use permission and language review are independently resolved.


