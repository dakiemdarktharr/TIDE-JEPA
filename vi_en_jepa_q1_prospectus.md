> **SUPERSEDED DESIGN DRAFT — 2026-09-28.** The active model is **TIDE-JEPA** and the approved languages are **Vietnamese, English, and Phan Rang Cham**. The MATE-JEPA name, La Ha scope, and implementation timing below are historical assistant proposals, not current decisions. Read [the active specification](tide_jepa_spec.md). The original draft remains below for provenance; its factual/source claims are not revalidated by retention.
# Research prospectus — multilingual action-transition JEPA under unequal data budgets

Date: 2026-09-28  
Status: falsifiable research design; no experiment run; La Ha inclusion is gated on community validation and usable data; novelty and Q2-venue suitability unverified.

## Scope and constraints

- Proposed language roles: English is the high-resource pivot/control; Vietnamese is the core written-generation language; La Ha is the selected low-resource extension, contingent on confirming the specific variety, writing/transcription practice, speaker access, consent, and independent fluent-speaker evaluation with the community.
- No reused third-party implementation, model checkpoint, or tokenizer. Implement the proposed model and controlled baselines in-house and initialize from scratch. Build input/output handling only for community-approved forms. Related papers may be cited to state prior art; that is not reliance on their code or model.
- Data-source policy is awaiting clarification. Working assumption: create a human-validated English–Vietnamese core corpus and, only with La Ha community authorization, a small La Ha pilot. Do not treat a wordlist as a ready-made generation corpus.
- Do not claim “low-resource language” as an inherent property of all Vietnamese NLP. Operationalize it as a task-level, fixed budget over independent meaning frames per language (pilot: 250/500/1,000/2,000 frames, subject to annotation feasibility); derived realizations do not count as independent frames. Keep approved items and compute matched across model comparisons.
- Keep an autoregressive Transformer decoder. JEPA is the central latent-dynamics learner, not a replacement for token generation.

## Research claim to attempt

**Proposed model name:** **MATE-JEPA** (*Multilingual Action-Transition Equivariance JEPA*).

**Working paper title, conditional on La Ha validation:** *Community-Guided MATE-JEPA: Action-Transition Learning for Data-Constrained English–Vietnamese–La Ha Generation*.

**Safer title if La Ha cannot pass the data-and-community gate:** *Beyond Sentence Alignment: Action-Transition JEPA for Data-Constrained Vietnamese–English Generation*.

The core task is **controlled generation of a specified event in Vietnamese or English**, focusing first on temporal anchoring (`PAST` versus `NOW`) and polarity (`POSITIVE` versus `NEGATIVE`). Example: given the event “Lan buy the book,” target language `vi`, and actions `[PAST, NEGATIVE]`, generate a natural sentence with the requested meaning. English and Vietnamese realize these meanings differently, so reviewers define accepted forms rather than assuming a one-word mapping such as English `past` = Vietnamese `đã`. La Ha is the selected extension, but its task and semantic actions must be chosen with speakers and a field linguist before it enters model training or evaluation.

The proposed contribution is not “use JEPA in NLP,” static multilingual alignment, latent tense composition, or counterfactual augmentation by itself. [LLM-JEPA (ICLR 2026)](https://proceedings.iclr.cc/paper_files/paper/2026/hash/ac818ec2da1c976b267de32f59709c69-Abstract-Conference.html), [BERT-JEPA (2026 preprint)](https://arxiv.org/abs/2601.00366), and [LATENTOPS (EMNLP 2023)](https://aclanthology.org/2023.emnlp-main.1030/) establish close neighboring work. The candidate contribution is to align **action-induced latent transitions across languages with very unequal task data**, then use transition disagreement to prioritize which examples deserve scarce community validation. The empirical claim is lower semantic error at the same data, compute, and speaker-hour budget—not gains from simply collecting more examples. English–Vietnamese is the controlled core; La Ha tests transfer only after community-approved task design and validation. This added active-elicitation component needs its own prior-art audit; no exact match surfaced in the scoped transition-JEPA review, but that does not prove novelty.

This remains only a candidate novelty claim. A prior-art audit must still test it against generic JEPA, latent operators, bilingual contrastive learning, grammar constraints, and selective prediction. If the gain vanishes against those controls, the paper should not claim a new JEPA method.

## Reasoning from the error to a theory

1. With few paired examples, a model can memorize the surface strings for “past” or “negative” but fail when asked for both together.
2. English often realizes time through verb/auxiliary form; Vietnamese often relies on particles and context. Copying a surface edit across languages is therefore the wrong bias.
3. Represent an event as a small state: who did what, when, and whether it happened. Actions update named fields; learn whether the *change* caused by the same action is reusable across languages, while a language-specific decoder turns the resulting state into words.
4. The two state updates are composable in the abstract event representation, but their **linguistic realization is partial and typed**: order/scope matters in some constructions. Compare paths only when bilingual reviewers certify that they reach the same intended event; never force unknown interactions to commute.
5. JEPA is useful if, with exactly the same text examples and compute, its predicted event-state transitions help the decoder generalize to held-out combinations and predict its own errors.

### Falsifiable theory

Let an event state be `s=(e,a,l)`: event/roles `e`, an annotation-approved set of semantic attributes/actions `a`, and realization language/variety `l`. The English–Vietnamese core tests `PAST` and `NEGATIVE`; La Ha must not inherit those categories until fluent speakers and linguists validate that they are appropriate. Abstract semantic changes may be shared, but surface realization is language- and variety-specific.

For parallel examples that express the same event before and after a community-approved shared semantic action `a`, let `z_l` and `z'_l` be its source and predicted target states for language/variety `l`. The theory predicts that the action-induced changes, after language-specific projection into a canonical semantic subspace, agree:

`Δ_l(a)=g_l(z'_l)-g_l(z_l)` and `L_transition = d(Δ_vi(a), Δ_en(a))`.

This is a falsifiable inductive bias, not a theorem that latent geometry must be linear. For two paths `p` and `r` independently annotated as valid and reaching the same abstract target, the JEPA rollouts should also agree. They need not agree for an unlicensed pair whose ordering changes meaning. Let `P_l,p` be a rollout and `d` a distance in predicted state space. The licensed-path residual is:

`ρ(x,a*) = Dispersion({P_l,p(E_l(x)) : p ∈ Paths(x,a*)})`.

**Hypotheses:** (H1) in the English–Vietnamese core, at fixed training-frame and compute budgets, transition alignment improves human-verified event/role/time/polarity accuracy on held-out `PAST × NEGATIVE` combinations versus token-only, generic-JEPA, and static-alignment controls; (H2) `ρ` predicts those errors beyond sequence NLL, entropy, and a separately trained confidence head; (H3) in a community-approved La Ha pilot, action-transition structure transfers better than static alignment at the same target-language budget; (H4) ranking candidate examples by valid-path transition disagreement reaches a pre-registered semantic-accuracy target with fewer speaker/annotator minutes than random sampling or token-entropy sampling. H3/H4 are not testable until the La Ha data and governance gates pass. Failure of H1 rejects the core generation claim; H4-only evidence supports more efficient elicitation, not a better generator.

**Intuition for a young child:** a sentence is a little picture. We show the same picture in English and Vietnamese, then—only if La Ha speakers approve the way to write or record it—in La Ha too. JEPA learns what changes in the picture when we add a meaning-card such as “yesterday” or “not.” Each language can tell the picture differently. The decoder says it in the chosen language. If the system cannot tell whether two routes made the same picture, it should ask a person instead of pretending.

No theorem is claimed yet. A useful theory result would need to characterize when sparse multilingual action-path observations identify an endpoint *modulo accepted realizations*, including language-specific non-commuting actions. A generic Lipschitz error-propagation bound or standard confluence theorem alone is not a contribution.

## Model: MATE-JEPA (Multilingual Action-Transition Equivariance JEPA; provisional name)

- **Input/target encoders:** byte- or Unicode-grapheme-level encoders trained from scratch; preserve Vietnamese diacritics and do not depend on an external segmenter. Online encoder `E_l` and EMA/stop-gradient target encoder `Ē_l` map sentences/forms to latent state.
- **State projections:** `z=(z_content,z_realization)`. For content-preserving edits, the content projection is constrained to remain stable. For actions that change proposition semantics (e.g., negation or tense), the annotation gives an explicit semantic delta; do not label those as invariant.
- **JEPA predictor:** `P_(l,a)` receives the source latent, target language, and typed action; it predicts the target latent. A shared low-rank core can model abstract dynamics, with small language-conditioned adapters for realization. A separate projection compares the **change** in canonical semantic state across matched language/variety action edges. This—not static endpoint alignment—is the main proposed novelty. The shared core is a hypothesis, not an assumption of identical grammars.
- **Decoder:** a small autoregressive Transformer conditions on source, action, language ID, and predicted latent to generate the output string. It is kept in all systems so gains are attributable to the JEPA dynamics rather than a changed decoder.
- **Action graph (v1):** the English–Vietnamese core uses `PAST/NOW` and `POSITIVE/NEGATIVE`, plus validated compositions. La Ha starts with speaker/linguist-selected phenomena; do not copy category labels by assumption. Reviewers label action preconditions and mark path pairs `same-event`, `scope-different`, or `unknown`. Only `same-event` paths contribute consistency loss. Number, voice, classifiers, and agreement remain out of scope unless later selected through linguistic consultation.
- **Multiple valid outputs:** use a set/distribution target or acceptability set; never collapse legitimate Vietnamese variants to one gold string without human adjudication.

### Budgeted community elicitation (candidate workflow component)

At each data-collection round, rank unvalidated meaning/action contexts using (a) disagreement between reviewer-licensed latent paths, (b) transition-predictor uncertainty, and (c) under-covered meaning/action groups. A community collaborator chooses whether each candidate is appropriate to elicit or review; the model never treats uncertainty as permission to record people or publish their language. Compare this policy with random and token-entropy sampling under the same speaker-hour and example budget. The objective is to spend limited validation time better, not to present active learning as a substitute for language transmission or community control.

### Training objective

`L = L_token + λJ L_JEPA + λT L_transition + λP L_licensed-path + λS L_semantic/action + λR L_repr`.

- `L_token`: ordinary autoregressive cross-entropy on the output.
- `L_JEPA`: distance between `P_(l,a)(E_l(x))` and `stopgrad(Ē_l(y))` for a labeled transition `(x,a,y)`.
- `L_transition`: distance between projected action-induced latent changes for bilingual edges that reviewers certify as the same meaning change.
- `L_licensed-path`: latent dispersion only among annotated valid paths with a shared target; no penalty on unknown or non-commuting paths.
- `L_semantic/action`: verifies content preservation or the specified semantic delta, using in-house labels. If a semantic classifier is used, it must be trained from scratch on the same language budget and included as a control.
- `L_repr`: anti-collapse regularization/variance monitoring; ablate it and publish representation-covariance diagnostics.

Use the same textual training examples for all baselines. The main contrast is how bilingual labeled transitions supervise hidden-state dynamics, not extra synthetic strings. If counterfactual sentences are created, expose the **same strings and labels to every baseline** and run a separate no-counterfactual condition.

### Inference workflow

1. The user or task supplies a source sentence, target language, explicit time context, and requested action/intent.
2. The encoder produces an event-state representation; the action predictor rolls that state forward for the requested action sequence.
3. A language-conditioned autoregressive Transformer decoder renders the predicted target state in Vietnamese or English. JEPA predicts meaning-space states; it does not replace this word-generating decoder.
4. If multiple reviewer-licensed action paths exist, decode/compare their predicted states. Use calibrated path residual only if it detects errors beyond NLL/entropy; otherwise do not retain it as a reliability claim. If validated risk is high, abstain or ask for clarification.

This is a reliability-oriented generation workflow, not a claim to repair arbitrary free-form hallucinations.

## Data and evaluation plan

### In-house multilingual corpus (working assumption; Vietnamese–English core)

Build a new set of English–Vietnamese event descriptions and sentence realizations with event frame, time, polarity, action labels, preconditions, and accepted variants. Initial pilot: 100–200 event frames; scale the main study only if native review shows the tense/polarity labels are unambiguous. Hold out event templates and predicate families so test combinations are not paraphrases of training examples. No test prompts or variants may be used for training or threshold selection.

Data budget curve: 250/500/1,000/2,000 independent event frames, if the pilot and review budget support it. These are experimental budgets, not a universal definition of “low-resource.” For every budget, fix the actual frame IDs across methods and report each language/variety's realized examples, action-label count, unique templates, training tokens, updates, FLOPs, wall-clock, peak VRAM, and speaker/annotator minutes. The same labels are exposed to relevant baselines; compare both matched-update and matched-compute. The central experiment is held-out composition and error per human-validation hour at each matched budget—not a comparison that gives the proposed model more text or annotation time.

### Baselines written in-house

1. Byte/grapheme-level bilingual seq2seq Transformer trained only with token loss.
2. Same model plus generic JEPA next-span/paired-target prediction (control for “any JEPA loss”).
3. Same model plus static bilingual endpoint alignment (control for cross-lingual sentence alignment without action dynamics).
4. Same model plus supervised latent contrastive/action-classification objectives (control for generic structured latent supervision).
5. Proposed MATE-JEPA without transition-delta loss; without path loss; without language adapters; and with all actions naively forced to commute (negative control).
6. Elicitation baselines: random selection, token-entropy selection, and path-residual/transition-disagreement selection, all capped at the same number of speaker/annotator minutes.
7. Confidence/risk baselines: sequence NLL, token entropy, independently trained error classifier, and uncalibrated versus calibrated path residual.

No third-party code or checkpoint is needed for these comparisons. Published work is used for novelty auditing and baseline definitions only. At least one strong published baseline can be independently reimplemented if the paper claim depends on outperforming it; report that reimplementation variance.

### Metrics

- **Primary:** human-judged event-role preservation, time accuracy, polarity accuracy, target-language grammaticality, and semantic errors per fixed speaker/annotator hour, each separated rather than collapsed into one score.
- **Secondary:** exact accepted-set match for controlled one-sentence cases; chrF/character edit distance; error-type breakdown for tense/aspect marker choice, negation scope/placement, missing content, and Vietnamese diacritics.
- **Reliability:** error-detection AUROC/AUPRC, risk–coverage/AURC, and coverage at pre-registered human error ceilings. Report full-coverage generation separately from abstention-assisted results.
- Two blinded raters per output, independent adjudication, agreement and confidence intervals; bootstrap paired items and use mixed effects for template/domain. At least five seeds if compute permits; always publish per-action and per-direction results.

## Go/no-go for a Q2-target journal submission

Proceed to a Q2-target submission only if (i) action-JEPA beats token-only and generic-JEPA at the **same data and compute budget** on human-validated outcomes; (ii) licensed-path residual adds calibrated risk signal beyond NLL/entropy/error-classifier if reliability remains a claim; (iii) gains survive held-out semantic templates/domains and both translation directions; (iv) ablations show the transition structure matters; and (v) language/community reviewers confirm the benchmark labels and output forms. A leaderboard or BLEU gain alone is insufficient.

No-go/reframe if gains come only from more counterfactual text, more labels, more compute, or the confidence gate; if results occur only in one direction; or if residual is a proxy for token entropy. Q2 suitability cannot be promised before those experiments, community validation, and a venue-specific literature audit.

## Evidence and next steps proposed by this superseded draft

The items below record what the earlier MATE-JEPA / La Ha draft proposed. They are historical and do not set the active TIDE-JEPA project's next steps; use [the active specification](tide_jepa_spec.md) and [ground-truth ledger](Obsidian/RMIT%20Hackathon/wiki/Project%20Ground%20Truth.md).

- The RMIT site describes GenAI accuracy/reliability for low-resource languages but says the specific 2026 challenge will be announced later: [official site](https://rmit-hackathon.com/).
- JEPA plus token generation already has direct precedent: [LLM-JEPA, ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/ac818ec2da1c976b267de32f59709c69-Abstract-Conference.html). This proposal therefore makes no claim that JEPA-in-language is new.
- Vietnamese word segmentation is a methodological risk; [AAAI 2025 work on Vietnamese word formation](https://ojs.aaai.org/index.php/AAAI/article/view/34581/36736) argues against treating syllable segmentation as a neutral preprocessing step. The scratch byte/grapheme tokenizer avoids depending on a segmenter; this does not establish that it is optimal.
- Existing English–Vietnamese MT literature exists (e.g. [empirical study](https://vjs.ac.vn/jcc/article/view/13233), [low-resource MT study](https://aclanthology.org/2020.loresmt-1.8/)); therefore bilingual direction alone is not novelty.
- Environment audit: local machine has an RTX 5050 with 8 GB VRAM, but both available Python runtimes currently lack PyTorch/Transformers/datasets. No code, corpus, or experiments exist in this workspace yet.
- The current RMIT page lists the hackathon for 22–23 October 2026, labels the challenge language as English, and says task details will be announced on the event day; do not assume extra languages affect scoring until the rubric is public.
- Resource audit for the selected extension: La Ha wordlist evidence is not a generation corpus. La Ha is selected for a community-led pilot, but remains gated on speaker access, approved writing/transcription, task design, and permissions.
- Data-policy question still open: whether public datasets are allowed as an external replication set or the study must use only newly authored data. Until answered, keep the in-house-corpus assumption explicit and do not download external corpora/checkpoints.

The historical draft's proposed immediate step was to consult La Ha speakers and a field linguist, then author a 100–200-frame English–Vietnamese pilot centered on `PAST × NEGATIVE`. It also proposed inspecting a future GitHub repo and delaying model code. These proposals are superseded and are not active instructions for this project.

