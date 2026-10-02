/goal Hoàn thiện TIDE-JEPA thành một pilot Anh–Việt sơ bộ có đầu ra sử dụng được trong phạm vi được kiểm chứng: sửa toàn bộ lỗi xác nhận trong báo cáo audit và lỗi mới phát hiện, kiểm chứng dữ liệu/split/training/evaluation/checkpoint/demo/tái lập, bảo toàn bằng chứng cũ, hoàn tất các hạng mục kỹ thuật trước giai đoạn Chăm Phan Rang; chỉ đánh dấu mục tiêu hoàn thành khi có bằng chứng nghiệm thu, không triển khai dữ liệu Chăm.

Bạn là GPT-6-Luna, reasoning effort high hoặc xhigh, tiếp quản trực tiếp dự án tại:

`C:\Users\ANHKHOI\Documents\ChatGPT\RMIT_HACKATHON`

Tôi muốn bạn thực hiện sửa lỗi đến khi đạt mục tiêu, không chỉ lập kế hoạch hay trả lời “có thể làm”. Dùng `/goal` ở đầu prompt này để tạo **một mục tiêu duy nhất**. Nếu môi trường cung cấp công cụ `create_goal`, tạo mục tiêu tương ứng một lần; nếu mục tiêu này đã tồn tại thì tiếp tục nó, không tạo mục tiêu trùng. Không đặt token budget vì tôi chưa yêu cầu. Các chặng dưới đây là công việc của cùng mục tiêu, không phải các goal mới.

## Quyền đã cấp và giới hạn bắt buộc

- Chỉ tạo agents/subagents bằng **gpt-6-luna**, reasoning **high hoặc xhigh**. Quy tắc áp dụng cả agents con và agents thay thế. Muốn dùng model khác phải hỏi tôi trước. Không kích hoạt lại `review_vi_en_a` / `review_vi_en_b` đã bị ngắt. Khi dùng tool spawn có override model, chọn `fork_turns="none"` hoặc số lượt thích hợp, không dùng full-history fork không hỗ trợ override.
- Tôi đã cho phép AI tự soạn, hai AI duyệt độc lập và AI phân xử để hoàn thiện **pilot Anh–Việt sơ bộ**. Tôi sẽ rà soát/nâng cấp sau. Không hỏi lại quyền này. Tuyệt đối không gọi kết quả đó là người duyệt, người bản ngữ xác nhận, ground truth ngôn ngữ đã được con người kiểm chứng, hoặc kết quả khoa học hoàn chỉnh.
- Tiếng Chăm Phan Rang chờ dataset-use permission và language/community review. Không tải, tự tạo nhãn/ngữ pháp Chăm, huấn luyện hoặc đánh giá Chăm. Có thể giữ registry và thiết kế adapter/gate chờ dữ liệu; workflow đang hoạt động chỉ dùng `en`, `vi`.
- Model, tokenizer/trainer và baseline do nhóm tự viết từ đầu; PyTorch được dùng làm runtime/primitives. Không sao chép implementation của repo/dự án khác, không dùng pretrained weights/tokenizers, không dùng LLM bên ngoài thay cho model để làm đẹp kết quả.
- Đọc `AGENTS.md` thực tế và tuân thủ. Sửa mã, bổ sung test có ý nghĩa, chạy thử trên dữ liệu được phép, tạo phiên bản pilot mới và cập nhật tài liệu nằm trong phạm vi đã được giao. Không cần xin lại xác nhận cho các bước này. Không tự xuất bản, gửi dữ liệu ra ngoài, phát hành weights, deploy công khai, commit/push hay viết lại lịch sử Git.
- Giữ toàn bộ PhoMT raw **và derived rows** trong `data/` được Git-ignore. Không in chúng vào chat, terminal log, traceback, tài liệu public, test snapshot hoặc Git. Dữ liệu chứa reference/generated text có nguồn gốc PhoMT cũng chịu ràng buộc này. Dùng báo cáo chỉ gồm số lượng/hash/aggregate ngoài `data/`; không để đường output cấu hình làm lọt rows.
- Không unpickle, không thực thi nội dung ZIP, không giải nén toàn archive. Translation link Anh–Việt không phải nhãn semantic action. Không gán action bằng cách coi một cặp dịch là một biến đổi trong cùng ngôn ngữ.

## Đọc bằng chứng trước khi sửa

Đọc theo thứ tự:

1. `AGENTS.md`, `audits/2026-10-02/AUDIT_SUMMARY.md` và ba báo cáo chi tiết trong cùng thư mục. Đọc probe và kết quả kèm theo; tái hiện các lỗi quan trọng trước khi sửa.
2. `README.md`, `ROADMAP.md`, `tide_jepa_spec.md`, `VI_EN_PILOT.md`, `VI_EN_RESULTS.md`, `vi_en_annotation_protocol.md`.
3. `Obsidian/RMIT Hackathon/wiki/Project Ground Truth.md`, `Obsidian/RMIT Hackathon/wiki/Dataset Research — 2026-09-30.md` và bằng chứng quyền trong `Obsidian/RMIT Hackathon/raw/PhoMT Permission Confirmation — 2026-10-01.md`.
4. Toàn bộ `tide_jepa/`, `tests/`, `scripts/`, requirements, Git-ignore và workflow/vault liên quan. Dùng `rg --files` vì phần lớn workspace còn untracked; `git diff` đơn thuần không đại diện toàn bộ code.

Raw notes trong Obsidian là lịch sử bằng chứng, không sửa chúng để làm quá khứ trông đúng. Thêm note mới, cập nhật wiki/index/log và liên kết bằng chứng. Tài liệu lịch sử không được ghi như trạng thái hiện tại.

## Trạng thái bàn giao có thật

- Audit ngày 2026-10-02: CPU suite **48/48 passed, 0 skipped**; `pip check` passed. Test passing chưa chứng minh chất lượng ngôn ngữ.
- Python 3.11.9 và project-local `.venv` chứa `torch==2.14.0+cpu`. Launcher `.venv/Scripts/python.exe` từng lỗi spawn base. Cách chạy đã hoạt động:

```powershell
Set-Location -LiteralPath 'C:\Users\ANHKHOI\Documents\ChatGPT\RMIT_HACKATHON'
$env:PYTHONPATH = Join-Path (Get-Location) '.venv\Lib\site-packages'
py -3.11 -B -m unittest discover -s tests -v
```

Không cài CUDA/GPU runtime mới theo quyền CPU hiện có. Kiểm tra runtime thực tế; ghi phiên bản, không giả định các launcher/PATH hoạt động ở shell khác.

- Pilot `data/pilot/vi-en-ai-v3/`: **400 original AI-authored records**, 20 event families, 240/80/80 train/validation/test. Chỉ biến đổi **trong cùng ngôn ngữ**, chưa có translation edge. Shared sentence templates giữa splits; không phải template/domain-generalization benchmark.
- Bốn objective controls `token_only`, `generic_jepa`, `static_alignment`, `tide`; seeds 17, 23, 41; width32, heads4, layers1, max_length192, batch80, lr0.001, 40 epochs, 120 updates/run. Kết quả **0/864 exact**, **564/864 valid UTF-8 (65.3%)**. Đây là kết quả âm tính, phải giữ nguyên. Chưa có chứng cứ TIDE vượt baseline, chưa có natural-corpus efficacy hoặc human evaluation.
- Bằng chứng cũ: `data/pilot/vi-en-ai-v3/suite_report.json`, `protocol.json`, `approval.json`, review/adjudication files; checkpoints/log/provenance dưới `runs/vi-en-ai-v3/`. Không ghi đè hoặc tiếp tục tối ưu trên test đã mở của v3 để gọi đó là test mới.
- `data/raw/phomt/PhoMT.zip` kiểm tra lại ngày 2026-10-02: **355,890,192 bytes**, SHA-256 đúng:
  `fd58972b5058b17d0823b78e6ce7dbb775243e156efa2ca222079dbdd76e6a2e`.
  Revision đã biết `aee99d07f0f5e6faf64b64f52adf314563350ce5`.
  `C:\Users\ANHKHOI\Downloads\PhoMT.zip` không thấy tại lần kiểm tra này. Không tải lại trước khi kiểm tra local. Chỉ kiểm tra archive và tệp tải dở ở hai vị trí đã định trong yêu cầu bàn giao; không quét máy.
- Metadata audit trước đó: 22 ZIP members, 13 files, không `.pkl`/`.pickle`, không unpickle/execution/full extraction; CRC không được kiểm riêng. 160 source packets **pending**, lấy từ detokenization/train, nằm ở `data/derived/phomt/pilot-source-v1/`. Không có PhoMT action corpus đã duyệt và **chưa huấn luyện bằng PhoMT**. Không coi các packets pending là dữ liệu đã approved.
- Các review gates hiện tại chuyên cho original synthetic corpus và cố ý từ chối PhoMT. Để dùng PhoMT, thiết kế workflow riêng có provenance/quyền/annotation/review/split đầy đủ; không gỡ gate hay đổi nhãn “no-PhoMT-content” để lách kiểm tra. Nếu ràng buộc không đưa rows ra chat khiến việc AI review nội dung chưa thực hiện được trong môi trường hiện tại, báo rõ dependency đó và hoàn thiện pipeline chờ review; không bịa review đã đọc rows.
- Phiên browser/server không được bảo đảm chia sẻ sang chat mới. Kiểm tra trước khi mở thêm server; không chạy hai tiến trình trên cùng port. Demo hiện tại là checkpoint kém chất lượng, chưa được coi là sản phẩm đã nghiệm thu.

## PhoMT permission và citation

Tác giả Dat Quoc Nguyen đã xác nhận phạm vi nghiên cứu/giáo dục, internal selection/annotation/training/evaluation và trình bày học thuật/hackathon đã mô tả, với điều kiện:

1. Chỉ nghiên cứu/giáo dục.
2. Không phân phối PhoMT hay bất kỳ phần nào, nguyên bản hoặc đã chỉnh sửa.
3. Mọi kết quả công bố sử dụng PhoMT phải trích dẫn bài EMNLP 2021.
4. Nếu phát hành weights học bằng PhoMT phải dùng giấy phép phi thương mại; email chưa xác định tên/phiên bản, cần xác nhận trước khi phát hành. Goal này không bao gồm release weights.

Citation: Doan, Long; Nguyen, Linh The; Tran, Nguyen Luong; Hoang, Thai; Nguyen, Dat Quoc. 2021. “PhoMT: A High-Quality and Large-Scale Benchmark Dataset for Vietnamese-English Machine Translation.” EMNLP 2021, pp. 4495–4503. https://aclanthology.org/2021.emnlp-main.369/ DOI: 10.18653/v1/2021.emnlp-main.369.

## Cách sửa và nghiệm thu

### A. Sửa tính đúng của code trước khi tăng training

Lập bảng issue ID → repro → nguyên nhân → fix → regression test → trạng thái; sử dụng E01–E14, Q01 và G01–G05 trong audit summary. Đây là backlog đã rà soát, không phải chứng minh không còn lỗi khác. Kiểm tra lại để không sửa dựa trên suy đoán hoặc đánh dấu một lỗi đã sửa là lỗi còn tồn tại. Đặc biệt PAD/BOS đã được mask trong generation hiện tại; không báo “chưa mask” nếu code vẫn như bàn giao. Các acceptance về human validation ở report thành phần dành cho scientific track; engineering AI pilot dùng quyền và giới hạn được nêu trong prompt tổng hợp này.

Ưu tiên:

- Unicode generation/termination: bảo đảm output được chấp nhận là Unicode hợp lệ, phát hiện unfinished UTF-8/truncation/empty/nonfinite output, trả metadata rõ ràng. Nếu dùng UTF-8 constrained decoding, ghi rõ ràng và vẫn báo chất lượng hành động/ngữ nghĩa; valid UTF-8 không đồng nghĩa câu đúng.
- Khôi phục checkpoint và metrics sau crash ở từng điểm ghi file; `latest`, `best`, log và epoch/selection score phải nhất quán hoặc phát hiện mismatch có cách phục hồi. Tái hiện `audits/2026-10-02/root_probes.py` trước sửa. Resume thành công mà thiếu best không được coi là hoàn tất.
- Corpus/split invariants phải đồng nhất giữa grouped split mới và frozen manifest: frame/text reuse, explicit group/path/alignment continuity, duplicate IDs, language/action gates. Không chỉ kiểm leakage khi đọc frozen split.
- Metric reduction theo đúng mẫu số: token CE theo số token hợp lệ, path CE/JEPA theo unit đã định nghĩa, alignment theo số cặp; báo mẫu số. Số liệu evaluation phải ổn định khi đổi cách chia batch trong cùng điều kiện, trừ metric đã ghi rõ phụ thuộc batch (ví dụ variance). Không gộp mọi scalar theo số rows rồi gọi là corpus CE.
- Protocol/provenance phải ràng buộc implementation và evaluator/decoder policy liên quan trước chạy; suite không trộn code versions. Inference/evaluation phải kiểm tra artifact thực tế phù hợp checkpoint và có chính sách explicit cho archival code snapshot. Không chỉ tin hash tự ghi trong JSON. Cache/report phải gắn checkpoint/protocol/evaluator/decoding hashes và tránh ghi đè test evidence.
- Hàm `evaluate_generation` phải từ chối corpus/split/approval đã đổi dù checkpoint/config/inventory còn khớp. Root probe hiện xác nhận evaluator nhận corpus synthetic đã đổi trong khi strict runner từ chối cùng corpus. Direct evaluator phải có validation/binding tương đương, không chỉ suite wrapper. Enforce test policy bằng immutable/cached idempotent evaluation có identity, tránh rescore/overwrite vô tình.
- Kiểm tra type/shape/range của EOS, token budget, action/language IDs và padding ở public APIs; báo lỗi có chủ đích thay vì TypeError/IndexError ở tensor internals.
- HTTP/CLI: giới hạn action count/path depth và chi phí request, timeout/body handling, lỗi request không làm treo hoặc giết server, source/target language contract không nhận translation không hỗ trợ. Source/action/error không được rò vào log.
- UI: kết quả phải gắn với snapshot request đã gửi, không hiển thị stale output như response của request mới, lỗi/timeout có trạng thái rõ; không chỉ thay ký tự Unicode rồi gọi đã tạo xong.
- Runtime/start script/report generator: chạy từ directory bất kỳ, check exit code/artifacts, cấu hình đường dẫn/port/checkpoint; report lấy số liệu từ bằng chứng thực tế, không hard-code số seeds/updates/tests/review đã xảy ra.

### B. Truy nguyên và cải thiện chất lượng Anh–Việt thật sự

Đừng chỉ vá UTF-8 rồi tuyên bố hết lỗi đầu ra. Chẩn đoán riêng teacher forcing vs free generation, EOS/length behavior, training-data fit, action sensitivity, source/entity preservation, latent collapse, architecture/conditioning, lượng dữ liệu và tối ưu hóa. Tăng epochs tùy tiện không thay thế chẩn đoán.

1. Dùng dữ liệu original synthetic để làm overfit sanity test nhỏ: model phải học được source-dependent transformations, không chỉ trả cùng một câu. Báo train generation, action counterfactual và mức khớp tham chiếu. Một sanity test không chứng minh generalization.
2. Tạo phiên bản mới và protocol mới; coi test v3 đã mở là evidence cũ. Dùng train/validation/development cho sửa lỗi/tuning. Freeze release holdout mới trước model selection, giữ frame/group/near-duplicate/family leakage audit và phạm vi generalization đã khai báo. Không đổi test hoặc nới tiêu chí vì đã thấy model thất bại; nếu có vòng mới thì gắn version và gọi bộ trước là development.
3. Corpus mới phải có semantic frame/action/context rõ, nhiều source realizations phù hợp phạm vi, reviewer độc lập, adjudication và accepted variants. Không dựng hai tên reviewer nhưng thực chất tự ký cả hai; review phải thực sự đọc phiên bản đã hash. Chỉ agents Luna được tạo. AI review provenance luôn sơ bộ.
4. Đánh giá per-language/per-single-action/per-path: action fidelity, preservation của entity/predicate/roles và phần nghĩa không được đổi, accepted-reference match/CER, Unicode, EOS/truncation, failure/refusal/OOD. Nếu dùng deterministic semantic checker cho task hẹp, khai báo grammar/coverage; ngoài coverage là unknown, không tự pass. Không gọi exact-match/CER hoặc AI judgments là human naturalness.
5. Đặt trước tiêu chí chất lượng kỹ thuật cho **phạm vi hẹp được công bố**, tối thiểu: output được chấp nhận 100% valid Unicode; trên holdout mới mỗi ngôn ngữ đạt action fidelity và preservation ≥90% cho single action, ≥80% cho held-out paths, có số mẫu/mẫu số và lỗi cụ thể; OOD/unsupported requests có phản hồi giới hạn rõ. Đây là mục tiêu nghiệm thu engineering do prompt đặt, không phải chuẩn khoa học hay chứng cứ human validation. Không đạt thì tiếp tục sửa có phương pháp, không hạ ngưỡng sau khi xem test để đóng goal.
6. Chạy lại bốn controls từ đầu theo protocol và data access giống nhau, nhiều seeds (ít nhất ba cho engineering pilot; nghiên cứu rộng hơn tùy hardware), đo tokens/updates/wall time/memory; CPU-only theo quyền hiện có. Không tuyên bố matched FLOPs nếu chưa đo. Không cần TIDE thắng baseline để code được coi đúng; kết quả âm tính phải được giữ và giải thích.
7. Nếu một template/rule baseline hữu ích, triển khai riêng, gắn nhãn output engine và báo điểm riêng. Không dùng hard-coded references, nearest-test lookup, rule fallback hoặc oracle để làm điểm neural model đẹp hơn. Không hiển thị fallback dưới tên “mô hình TIDE tạo” hoặc trộn fallback metrics vào neural metrics.

### C. Demo và các hạng mục trước Chăm

Chỉ checkpoint đạt quality contract mới được gọi là ready cho phạm vi đó. Checkpoint chưa đạt chỉ ở diagnostic mode; UI/API nói rõ và không trình bày gibberish như câu dùng được. Fallback/refusal chỉ là bảo vệ trải nghiệm, không thay thế mục tiêu cải thiện model.

Hoàn thiện offline inference/demo, request/response schema, threat model phù hợp loopback, regression/integration tests, latency/resource benchmark và reproduction workflow. Tài liệu hướng dẫn phải cho người khác chạy được bằng command cụ thể, mô tả phạm vi within-language vs translation và các giới hạn. Nếu muốn thêm cross-language generation thì cần hợp đồng dữ liệu/source_language/target_language và benchmark riêng; không suy diễn rằng target-language dropdown đã thực hiện dịch.

Map toàn bộ ROADMAP M1–M5 tới bảng trạng thái: completed engineering / preliminary evidence / external gate / future research. Viết báo cáo, model/data card và research package trung thực cho Vi–En; các mục human evaluation, scientific novelty/efficacy, task hackathon chưa công bố và giấy phép release không được bịa là đã hoàn tất. Các mục có thể xây kỹ thuật mà không cần dữ liệu Chăm thì hoàn thiện; giữ Cham gate đóng. Không biến task này thành mục tiêu “đạt Q1/được chấp nhận bài báo”.

## Điều kiện đóng một goal này

Chỉ đánh dấu complete khi:

- Tất cả lỗi xác nhận trong audit và lỗi mới liên quan phạm vi được sửa, hoặc bị bác bỏ bằng repro/evidence rõ; không còn issue nghiêm trọng bị bỏ qua. Có bảng closure kèm file/test/result.
- Test cũ và regression mới chạy thật, không skip phần cần thiết; check compile/runtime/dependency và UI/API integration phù hợp. Không sửa test để bỏ đòi hỏi đang lỗi.
- Leakage, metric denominators, protocol/code identity, provenance/evaluator binding và crash-safe recovery có bằng chứng nghiệm thu. Giữ đủ code/artifact versions để tái lập bảng kết quả.
- Neural generation đạt contract chất lượng engineering nêu trên trong phạm vi đã freeze và được ghi rõ là AI-reviewed preliminary. Báo per-language/action/path, baseline, failure/refusal, latency/memory. Test passing hoặc UI refusal riêng lẻ chưa đủ để đóng mục tiêu này.
- Demo offline đã kiểm thử bằng checkpoint đúng provenance và phản hồi đúng cả supported/OOD/malformed input; không che lỗi model bằng fallback không nhãn.
- README/ROADMAP/spec/pilot/results/Ground Truth và evidence note mới nhất nhất quán; source data không lọt khỏi `data/`, không bị commit/publish; kết quả v3 không bị sửa.
- Cham training/evaluation vẫn disabled và các dependency bên ngoài được liệt kê đúng. Human validation/PhoMT annotation còn thiếu không được gọi complete; phân biệt rõ phần này với engineering goal đã kiểm chứng. Nếu dependency đó chặn thực sự tiêu chí đã chọn thì chưa complete, báo điều kiện cần thiết cụ thể.

Không dừng sau một vòng test hoặc một lần tăng training chỉ vì muốn trả lời sớm. Nếu không thể tiến thêm vì giới hạn thực tế, giữ trạng thái goal đúng theo quy tắc công cụ và nêu failure/dependency; không giả vờ hoàn thành. Không xin mật khẩu/token, không tự đăng nhập hoặc chấp nhận điều khoản mới để vượt cổng dữ liệu.

Khi làm, cập nhật ngắn gọn bằng tiếng Việt về phát hiện và bằng chứng; tránh xuất nội dung dataset. Cuối cùng báo: sửa gì, kiểm chứng gì, chất lượng neural thật, phạm vi dùng được, hạn chế/gate còn lại, đường dẫn các báo cáo/pilot mới và command chạy demo/tái lập. Dùng đường dẫn tuyệt đối có thể bấm được.
