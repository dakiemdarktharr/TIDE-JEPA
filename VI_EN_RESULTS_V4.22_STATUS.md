# v4.22 draft status — review concerns unresolved; no protocol frozen

v4.22 is a private, AI-authored preliminary synthetic English–Vietnamese draft. It was not trained, no protocol was frozen, and its release holdout was never opened. The corpus remains under Git-ignored `data/`; PhoMT and Phan Rang Cham were not used.

The draft has 15,360 records and 192 event combinations (112/40/40 groups). Two independent Luna reviewers checked every record and both requested adjudication. Structural/frame/action/alignment checks found no mismatches. The reviews identified three methodological or bilingual issues to address before any experiment:

- Agent-factor counts were strongly uneven in the train split, and validation/holdout omitted one of the three agent factors.
- English present-progressive forms and Vietnamese forms did not consistently mark progressive aspect; one achievement predicate was specifically flagged.
- The split statement did not quantify repeated path-step rows, which make the training row distribution path-enriched.

Draft SHA-256: `e5761740396de00cc2e827ac5c481ceacd05596fefaaad61b774272643b5f8d5`. Review decisions are `needs-adjudication`; no adjudication approved the corpus. Preserve this draft and its reviews as audit evidence. v4.23 adds balanced factor marginals, an explicit progressive translation, and an exposure note, and will receive fresh independent reviews and a separately frozen protocol. No row-level text, examples, or generated outputs are published here.
