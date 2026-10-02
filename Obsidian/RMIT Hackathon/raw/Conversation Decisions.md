# Conversation decisions — source record

> Source: Codex project chat **“Tìm hiểu hackathon sắp tới”**, thread `01a0bd75-30b8-7a80-bf1d-f38ba389dddc`; and **“Tìm giải pháp AI cho ngôn ngữ dữ li”**, thread `01a0c822-9b76-72b0-a77a-826dde6be86b`. Read on 2026-09-28.
> Record type: concise extraction of decisions and findings, not a verbatim transcript.
> Status: Current source record. Add a new dated record if the user changes a decision.

## Explicit user decisions

- User selected the name **TIDE-JEPA** and asked for a specific title, model name, scope, workflow diagram, and solution approach.
- User later narrowed the training languages to **Vietnamese and English only**: “ngôn ngữ train chỉ cần tiếng việt và tiếng anh”. This later, explicit constraint supersedes earlier Cham/La Ha/Bố Y language exploration. No non-Vietnamese/English training data is in scope unless the user changes this.
- User then corrected the ground truth on 2026-09-28: the project languages are **Vietnamese, English, and Phan Rang Cham**. This latest instruction supersedes the intermediate Vietnamese–English-only restriction. La Ha and Bố Y remain out of scope.
- User prohibited basing the implementation on existing repositories or open-source source code: “cấm dựa code trên repo có sẵn hoặc mã nguồn mở. phải phát triển từ đầu”.
- User approved PyTorch as the runtime; model and trainer are to be implemented from scratch. This does not prohibit consulting papers or using public datasets unless separately decided.
- User asked for a concrete direction and child-friendly explanation, and said code was not yet wanted until a GitHub repository was sent. The current request now says to start the project after workflow setup; a first implementation task can be assigned, but do not assume an external GitHub repository exists.

## Most recent research direction in project files

- Controlled generation of a specified event across Vietnamese, English, and Phan Rang Cham, with language-specific task design and validated realizations.
- Initial semantic actions: temporal anchoring (`PAST`/`NOW`) and polarity (`POSITIVE`/`NEGATIVE`); human reviewers define accepted forms and scope.
- Test whether action-conditioned latent transition learning helps compose held-out action combinations under matched data and compute, with an autoregressive decoder retained for text generation.
- Treat the novelty as a hypothesis only. Compare against token-only, generic-JEPA, and structured-alignment controls; abandon claims unsupported by results.
- Existing draft files currently use the name **MATE-JEPA** and include a gated La Ha extension. These are assistant-authored draft content, not a later user decision. They conflict with the explicit TIDE-JEPA name and the latest Phan Rang Cham scope and must be reconciled before being treated as ground truth. Any Cham action inventory, writing system, and data collection requires suitable speaker/community validation.
- Public-dataset policy, desired first milestone, and any hackathon-specific adaptation remain open. The user assigned `find` to search for relevant datasets, so `find` should report licensing, language/task match, and whether data can be used under the from-scratch code constraint.

## Hackathon facts reported in the earlier conversation

The earlier research final reported, as of its stated research date, that the official 2026 page described four linked Kaggle tasks whose detailed prompts would be released on the event day; exact file deliverables, evaluation metrics, and presentation requirements were not published on the pages reviewed. Previous-year Kaggle examples were explicitly treated as precedent, not 2026 rules. The project should not claim TIDE-JEPA solves the event challenge before the actual task is known.

## Source links

- [RMIT Hackathon official site](https://rmit-hackathon.com/) — current rules must be rechecked before relying on dates or deliverables.
- Original Codex threads: `01a0bd75-30b8-7a80-bf1d-f38ba389dddc` and `01a0c822-9b76-72b0-a77a-826dde6be86b`.
