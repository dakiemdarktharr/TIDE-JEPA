# Dataset research — 2026-09-30

> Raw: [[../raw/PhoMT Permission Confirmation — 2026-10-01]], [[../raw/PhoMT Intake and Vi-En Pilot — 2026-10-01]]
> Fingerprint: no Git commit exists yet; workspace changes are uncommitted.
> Monitored: `data/raw/phomt/**`, `tide_jepa/phomt_audit.py`, `ROADMAP.md`, `README.md`
> Status: Current — conditional permission documented; later check found a hash-verified local archive and safe metadata audit. Private train-only source selection produced 160 pending packets; no PhoMT model training. The completed preliminary Vi–En pilot uses original synthetic text. Source: [[../raw/PhoMT Intake and Vi-En Pilot — 2026-10-01]].

## Latest intake correction

The later local check supersedes the original acquisition statements below. Archive size is 355,890,192 bytes; supplied SHA-256 matches; metadata audit reports 22 members and 13 files. No new download, login, full extraction or unpickling occurred. PhoMT-derived action annotations remain pending, and official dev/test files were not opened. Source: [[../raw/PhoMT Intake and Vi-En Pilot — 2026-10-01]]. The original research/acquisition narrative below is retained as dated history.

## Decision summary

No complete, already action-annotated TIDE-JEPA corpus was found for Vietnamese, English, and Phan Rang Cham. The available English–Vietnamese datasets provide translation pairs, not the same-language, action-conditioned transitions and expert-approved action/path correspondences the project schema requires. We must curate those labels and validate them. No dataset data was downloaded or ingested during the initial search or after the later permission reply.

The best identified English–Vietnamese starting source is **PhoMT**. The publisher reports 3.02 million sentence pairs. On 2026-10-01, author Dat Quoc Nguyen confirmed in writing that the requested internal selection/annotation, model training/evaluation, and limited hackathon/academic presentation are allowed under the stated terms. Conditions: research/education only; do not distribute PhoMT or any portion in original or modified form; cite the EMNLP 2021 paper; and release PhoMT-trained weights only under a non-commercial license. Preserve the email privately. This is conditional permission, not a general commercial or redistribution license. [PhoMT repository](https://github.com/VinAIResearch/PhoMT); [EMNLP paper](https://aclanthology.org/2021.emnlp-main.369/); [Hugging Face dataset card and access terms](https://huggingface.co/datasets/vinai/PhoMT).

The Hugging Face page currently gates archive access behind sign-in and acceptance of conditions that include sharing account contact information. The archive has not been downloaded. Its file listing reports `PhoMT.zip` at 356 MB, revision `aee99d07f0f5e6faf64b64f52adf314563350ce5`, and flags pickle content. The project must not execute/unpickle archive content blindly; place an authorized copy only in Git-ignored `data/raw/phomt/PhoMT.zip`, inspect the archive, and keep both raw and derived rows private. [PhoMT file listing](https://huggingface.co/datasets/vinai/PhoMT/tree/aee99d07f0f5e6faf64b64f52adf314563350ce5).

**Tatoeba** is a smaller potential source with clearer text-sentence terms: the project says textual sentences use CC BY 2.0 France, requiring attribution to sentence authors; its current download page includes both English and Vietnamese. It is a community corpus, so preserve sentence IDs/authors and audit the actual translation links and sentence-level provenance before adopting it. It is not action-labeled and does not solve the annotation problem. [Tatoeba usage terms](https://en.wiki.tatoeba.org/articles/show/using-the-tatoeba-corpus); [Tatoeba download page](https://tatoeba.org/en/downloads).

For **Phan Rang Cham**, the California Language Archive lists an Eastern Cham Field Materials collection. A dissertation reports fieldwork in Cham villages near Phan Rang and says its research data are archived at Berkeley's CLA. This is a definite archival lead, not confirmed bulk-access, AI-training, redistribution, or community permission. The materials may be recordings, field notes, transcripts, or judgments; first request the collection inventory and item restrictions. Do not treat Eastern Cham archival records as a ready-to-use generation corpus. [CLA collection listing](https://cla.berkeley.edu/browse/collection-list.html); [Baclawski dissertation](https://escholarship.org/uc/item/0349w4fh); [CLA access and contact FAQ](https://cla.berkeley.edu/faq.html).

The prior search of British Library EAP698 likewise found Eastern Cham manuscript images, access described for research purposes, no explicit model-training license, and culturally sensitive item descriptions. It is not a suitable ready-to-train controlled-generation corpus. [EAP698 sample item](https://searcharchives.bl.uk/catalog/032-003319252).

## What data the model actually needs

For each approved language, the training JSONL needs same-language source/target pairs that realize an explicitly annotated semantic action, stable meaning-frame and split-group IDs, traceable provenance/license references, and approved action inventory. To activate cross-language alignment losses, an additional explicit alignment file must identify expert-approved equivalent edges or complete paths. A translation corpus alone provides neither those transformations nor their semantic licenses. The final held-out test set must be separately authored/reviewed and kept out of training/model selection.

Minimum sensible pilot:

- English and Vietnamese controlled examples authored/curated and double-reviewed for the selected action task, plus explicit translation/path correspondences where aligned loss is evaluated.
- Phan Rang Cham only after a speaker/community partner and a linguist approve source access, variety, orthography, translations, task actions, and accepted outputs. If that gate is not reached, report a two-language pilot and do not claim Cham coverage.
- A source-specific rights note covering research, the RMIT hackathon/demo, publication, derived weights, and any redistribution. Dataset access alone is not permission for all these uses.

## PhoMT permission correspondence

### PhoMT: request sent and conditional approval received (2026-10-01)

**Gửi đến:** `business@vinai.io`  
**Cc:** `datnq@qti.qualcomm.com`

**Tiêu đề:** Xin xác nhận quyền sử dụng PhoMT cho nghiên cứu TIDE-JEPA

Dat Quoc Nguyen replied in the thread and confirmed the scopes described in the request, conditional on all repository terms. He added that any released model trained using PhoMT must be under a non-commercial license. The current reply does not specify a license name/version; clarify that before releasing weights. The correspondence is permission evidence; keep the original email and headers in the user's mailbox rather than committing a screenshot or dataset excerpt to this repository.

## Mandatory publication and release checklist

Treat these as a release gate for every paper, preprint, academic report, or published result that PhoMT helped produce:

- Cite the paper below in the manuscript bibliography and identify PhoMT in the data/methods section. The email explicitly requires citation whenever PhoMT is used to help produce published results.
- State the exact PhoMT revision, subset, and number of pairs actually used once intake occurs. Do not claim a revision or subset before verifying the downloaded archive.
- Keep PhoMT use within research/education. Do not distribute PhoMT or any portion of it, whether original or modified; do not commit rows, derived copies, or archive contents to the repository or supplements.
- If releasing model weights trained using PhoMT, use a non-commercial license. The correspondence does not select a specific license name/version, so confirm this before release.
- Any hackathon/academic examples must remain within the scope explicitly described and approved in the email; do not publish raw PhoMT pairs as examples.

Ready-to-paste ACL Anthology BibTeX:

```bibtex
@inproceedings{doan-etal-2021-phomt,
    title = "{P}ho{MT}: A High-Quality and Large-Scale Benchmark Dataset for {V}ietnamese-{E}nglish Machine Translation",
    author = "Doan, Long and
      Nguyen, Linh The and
      Tran, Nguyen Luong and
      Hoang, Thai and
      Nguyen, Dat Quoc",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.369/",
    doi = "10.18653/v1/2021.emnlp-main.369",
    pages = "4495--4503"
}
```

Verified against the [ACL Anthology record](https://aclanthology.org/2021.emnlp-main.369/), which lists the authors, venue, year, pages, DOI, and citation export. Permission conditions are summarized from [[../raw/PhoMT Permission Confirmation — 2026-10-01]] and the [PhoMT dataset card](https://huggingface.co/datasets/vinai/PhoMT).

Kính gửi nhóm tác giả PhoMT,

Em là Lưu Anh Khôi, sinh viên UEH, hiện thực hiện dự án TIDE-JEPA về sinh câu có kiểm soát bằng tiếng Anh và tiếng Việt; phần mở rộng sang tiếng Chăm Phan Rang sẽ chỉ được thực hiện khi có đủ sự chấp thuận và thẩm định phù hợp.

TIDE-JEPA là một nguyên mẫu nghiên cứu do nhóm tự xây dựng, không dùng mô hình hay trọng số có sẵn. Mô hình nhận câu đầu vào cùng một yêu cầu ngữ nghĩa, chẳng hạn đổi thời điểm hoặc sắc thái khẳng định/phủ định, rồi tạo câu đích bằng ngôn ngữ được chọn. Nhóm muốn nghiên cứu xem việc học những thay đổi về ý nghĩa này có giúp mô hình tạo câu đúng yêu cầu hơn khi dữ liệu hạn chế hay không. Đây mới là hướng nghiên cứu cần kiểm chứng, chưa phải kết quả đã được xác nhận.

Em đang tìm một nguồn câu Anh–Việt cho nghiên cứu. Em đọc được rằng PhoMT có điều khoản chỉ dành cho nghiên cứu/giáo dục và không cho phép phân phối lại dữ liệu. Dự án của em hoàn toàn phi thương mại: nhóm làm nghiên cứu học thuật và dự kiến trình bày nguyên mẫu tại một hackathon sinh viên, không dùng dữ liệu để bán sản phẩm hay cung cấp dịch vụ.

Trước khi tải dữ liệu, em muốn xin xác nhận liệu nhóm có thể dùng PhoMT nội bộ để chọn và gán nhãn một tập ví dụ nhỏ, rồi huấn luyện mô hình do nhóm tự xây dựng hay không. Nếu được phép, nhóm cũng mong được trình bày một số câu đầu ra và kết quả tổng hợp tại hackathon hoặc trong báo cáo học thuật. Nhóm sẽ không chia sẻ dữ liệu PhoMT hay các bản đã chỉnh sửa; em cũng xin hỏi liệu có điều kiện riêng nào áp dụng cho trọng số mô hình và câu đầu ra.

Nếu phạm vi này chưa được phép, mong anh/chị cho em biết giới hạn sử dụng và cách trích dẫn phù hợp. Nhóm sẽ chờ xác nhận trước khi tải hoặc dùng dữ liệu.

Em cảm ơn anh/chị đã dành thời gian xem xét.

Trân trọng,

Lưu Anh Khôi  
UEH  
`khoiluu.31251021752@st.ueh.edu.vn`

### Eastern Cham Field Materials: inquiry about materials, access, and community review

**To:** `scoil-ling@berkeley.edu` — California Language Archive

**Subject:** Inquiry about the Eastern Cham Field Materials (2014–20)

Dear California Language Archive team,

My name is Lưu Anh Khôi, and I am a student at UEH working on a small research project on controlled generation in English and Vietnamese. Our team is also exploring whether Phan Rang Cham could be included. We will not use Cham materials unless access rights are clear and the work has been reviewed with appropriate speakers, community members, and linguistic experts.

I saw “Eastern Cham Field Materials (2014–20)” in the CLA collection list. Kenneth Baclawski’s dissertation also says that research materials from fieldwork near Phan Rang are archived at CLA. Could you let me know what kinds of materials the collection contains—for example, recordings, transcripts, translations, or speaker judgments—and which items are available? I would also appreciate guidance on any access restrictions or permissions required from depositors or speakers.

We are considering whether a small portion of the materials could be used to train a model developed by our team and to present academic results at a student hackathon. This would be non-commercial research; we do not intend to redistribute any archival materials. Could you clarify whether the permissions for relevant items allow these uses? If appropriate, could you also point us to a community contact, speaker, or linguistic expert who could advise us on a suitable review and permission process?

We will not download, transcribe, train on, or publish any collection material unless item-level permissions and the appropriate community review clearly allow it.

Thank you for your time and guidance.

Best regards,

Lưu Anh Khôi  
UEH  
`khoiluu.31251021752@st.ueh.edu.vn`

## Status

- PhoMT: conditional written permission received for the described research/education and hackathon use. On 2026-10-01, the expected project intake folder `data/raw/phomt/` existed but contained no files, and no `PhoMT*` file was found in the user's Downloads folder. This check does not cover other locations on the computer. The Hugging Face access gate still requires user login and acceptance. No rows have been ingested or used in training.
- Tatoeba: potentially clear attribution-based text license; coverage, item-level provenance, and relevance need audit before use.
- CLA Eastern Cham: definite archival collection/research-data lead; item-level availability, ML use, and community permission remain unknown. Request clarification at `scoil-ling@berkeley.edu`.
- PhoMT translations do not provide action labels or within-language semantic transitions. Action transformations, explicit cross-language path correspondences, expert review, and a held-out benchmark still need to be curated; translation links must not be relabeled as action transitions.
