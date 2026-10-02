> **HISTORICAL PROSPECTUS — current authority: [TIDE-JEPA specification](tide_jepa_spec.md).** Approved languages: Vietnamese, English, and Phan Rang Cham. Earlier pointers and language sets below are retained as history and do not define the current project.
# Archived prospectus — multilingual morphological branch (superseded)

This was an exploratory direction before the scope was narrowed and later reset to TIDE-JEPA. It is **not** the current method or experiment plan. Use the [active TIDE-JEPA specification](tide_jepa_spec.md) and [project ground-truth ledger](Obsidian/RMIT%20Hackathon/wiki/Project%20Ground%20Truth.md). Keep this file only as a literature/idea audit; do not use its SIGMORPHON language set or proposed code/data dependencies for the current study.

Ngày rà soát: 28-09-2026  
Trạng thái: bản thiết kế nghiên cứu có thể bác bỏ; chưa có thực nghiệm, chưa xác nhận novelty, không khẳng định đủ chuẩn Q1.

## Luận điểm nghiên cứu

**Working title:** *When Morphological Paths Disagree: Partial-Action JEPA for Reliable Low-Resource Generation*

JEPA là thành phần bắt buộc và nằm ở trung tâm phương pháp: nó học dự đoán latent target sau từng feature-action, rồi composition các dự đoán latent thành form chưa thấy. Transformer chỉ giữ vai trò decoder autoregressive để hiện thực hóa chuỗi bề mặt. Không cần JEPA thay Transformer. LLM-JEPA cũng giữ objective sinh token và thêm JEPA; nó không chứng minh JEPA có thể thay decoder ngôn ngữ [ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/file/ac818ec2da1c976b267de32f59709c69-Paper-Conference.pdf).

### JEPA đóng vai trò gì trong model

Từ các paradigm hiện có, tạo các transition triples (form nguồn, feature edit, form đích) mà không thêm parallel corpus. Online encoder mã hóa form nguồn; EMA/stop-gradient target encoder mã hóa form đích. Predictor JEPA nhận latent nguồn + action và dự đoán latent đích. Khi cần một bundle có nhiều feature, predictor được rollout bằng chuỗi actions hợp lệ. Decoder nhận latent rollout và sinh dạng chữ.

Training ở mức một bước học transition đã quan sát; path-consistency so hai rollout hợp lệ đến cùng endpoint; token loss giữ decoder grounded vào dạng chữ. Ở inference, model bắt đầu từ lemma/ô paradigm sẵn có, áp các đường action có thể dùng để tạo bundle đích, decode từng dự đoán và đo bất đồng latent giữa các đường. Đây không phải “thêm một JEPA loss vào NMT” đơn thuần: core operator dynamics được học bằng JEPA, nhưng giá trị của nó vẫn phải chứng minh so với action-transducer và paradigm baselines.

Trang chính thức RMIT 2026 hiện mô tả chủ đề là độ chính xác và độ tin cậy của GenAI cho ngôn ngữ ít tài nguyên, nhưng nói challenge cụ thể sẽ được công bố gần sự kiện. Vì vậy, không giả định trước đây là MT hay một cặp dịch cụ thể [RMIT Hackathon 2026](https://rmit-hackathon.com/).

Để có câu hỏi khoa học kiểm soát được, paper nên giới hạn claim vào **morphosyntactic accuracy dưới ngân sách dữ liệu thấp**: core study là inflection với feature bundle cho trước; validation là grammatical agreement trong câu/minimal pairs. Đây là lát cắt có benchmark đo được, không đồng nghĩa giải mọi lỗi ngôn ngữ. Nếu challenge RMIT công bố tác vụ phù hợp, dùng nó như external application test, không đổi benchmark khoa học sau khi xem test.

## Từ quan sát bằng lời đến giả thuyết

Model ít dữ liệu thường vẫn sinh câu nghe có vẻ hợp lý; điều khó là biết nó đã học một quy tắc hình thái hay chỉ nhớ các cặp lemma–form và tương quan của chúng. Một tổ hợp feature chưa được thấy không luôn đồng nghĩa với “thiếu thêm câu”: trong một số ngôn ngữ, tổ hợp có thể được suy ra từ các biến đổi đã thấy; trong ngôn ngữ khác, allomorphy, syncretism, reduplication hoặc tương tác phonology khiến phép ghép đơn giản sai.

Do đó, giả thuyết không phải “mọi feature đều cộng được”. Giả thuyết là: **nếu hai đường biến đổi được ngôn ngữ cấp phép và cùng kết thúc ở một feature bundle, độ bất đồng giữa dự đoán trên hai đường có thể phản ánh rủi ro hiện thực hóa chưa được dữ liệu định danh.** Score này chỉ có giá trị nếu dự báo lỗi tốt hơn token entropy, ensemble/dropout, OOD, round-trip quality estimation và confidence/QE thông thường.

Đây là câu hỏi hẹp hơn các cơ chế đã có. Latent linguistic transformations đã được nghiên cứu bởi [RISE, ICLR 2026 Poster](https://iclr.cc/virtual/2026/poster/10007262); latent operators cùng encoder–decoder đã có trong [INTERSENT, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.900/); [NSL-MT, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.465/) đã dùng grammar-violation negatives trong low-resource MT; selective generation và conformal generation cũng có tiền lệ ([Ren et al., ICLR 2023](https://openreview.net/forum?id=kJUS5nD0vPB), [Deutschmann et al., AAAI 2024](https://ojs.aaai.org/index.php/AAAI/article/view/29062)). Vì vậy riêng JEPA, operator, compositional split, grammar penalty hay abstention đều không phải novelty.

## Lý thuyết thiết kế: confluence có điều kiện

Gọi s=(ℓ,c,F) là trạng thái nguồn gồm lemma ℓ, context/inflection class c, và feature bundle F. Mỗi feature edit a là một **partial map** Tₐ: nó chỉ định nghĩa khi tiền điều kiện ngôn ngữ được thỏa mãn. Không giả định các Tₐ là khả nghịch, toàn phần, hay giao hoán.

Với bundle đích F′, gọi Π(s,F′) là tập các đường biến đổi được xác nhận hợp lệ từ s đến cùng endpoint. Target encoder Ē mã hóa form đích; predictor JEPA Pθ nhận latent form nguồn và feature action; decoder Dφ biến predicted latent thành chuỗi.

Với một đường p=(a₁,…,aₖ), phép rollout là:

zₚ⁽⁰⁾ = E(x);  zₚ⁽ᵢ⁾ = Pθ(zₚ⁽ⁱ⁻¹⁾, aᵢ, ℓ);  ŷₚ = Dφ(x, zₚ⁽ᵏ⁾, ℓ).

JEPA loss cho edge đã quan sát đưa zₚ⁽ᵏ⁾ gần stop-gradient(Ē(y)). Với nhiều path p,q cùng endpoint, path residual là r(x,F′)=Dispersion({zₚ⁽ᵏ⁾ : p ∈ Π(s,F′)}).

Nếu có nhiều realization được người bản ngữ/benchmark chấp nhận, dispersion so với **tập hoặc phân phối latent của các realization hợp lệ**, không ép về một điểm. Không tính residual trên các thứ tự không hợp lệ hoặc các phép biến đổi có tương tác/allomorphy chưa được kiểm soát.

**Confluence hypothesis:** trên nhóm các feature bundles mà các biến đổi thành phần đã được quan sát và các critical pairs được cấp phép/đánh dấu độc lập, regularizing dự đoán JEPA theo đường sẽ (a) cải thiện exact-form accuracy ở ngân sách cố định, và (b) làm path residual tăng có hệ thống trên output sai, kể cả sau khi ghép cặp theo token NLL và các confidence baseline. Ở câu/minimal pair, phép biến đổi hợp lệ phải bảo toàn latent ngữ nghĩa trong khi đổi đúng latent feature; chỉ các cặp action được xác nhận commute mới bị buộc hội tụ. Nếu chỉ (b) đúng, kết quả là selective reliability chứ không phải khả năng sinh tốt hơn; cần báo rõ trade-off coverage. Nếu residual không thêm thông tin sau các baseline, bác bỏ hướng.

**Giới hạn lý thuyết:** định lý local-confluence/global-confluence chuẩn từ term rewriting không phải đóng góp mới. Một error bound Lipschitz/margin chung cũng không đủ. Lý thuyết riêng cần chứng minh điều kiện **identifiability modulo accepted allomorphs/variant forms** từ đồ thị feature một phần và số edge/paradigm quan sát được, hoặc chỉ nên gọi đây là design hypothesis. Chưa có chứng minh như vậy trong prospectus này.

## Thuật toán đề xuất: Partial-Action JEPA (tên tạm)

### Biểu diễn/model

- **Backbone:** cùng một character/byte-level encoder–decoder Transformer cho baseline và model chính; giữ tokenizer, checkpoint, update budget và data cố định. Character model là baseline tự nhiên cho word-form inflection; pretrained multilingual model là một ablation riêng.
- **Target encoder:** mã hóa target form thành latent; thử frozen/EMA target encoder như ablation vì mục tiêu JEPA nhạy với target collapse.
- **Action predictor:** nhận source representation, language ID, context/inflection class nếu có, và chuỗi feature actions hợp lệ; dự đoán latent target theo từng bước và theo cả đường.
- **Tách invariant/equivariant:** một projection latent giữ phần nghĩa ổn định qua grammatical edit; một projection giữ trạng thái hình thái/cú pháp phải biến đổi theo action. Chỉ dùng nhãn feature hoặc phép sửa đã có trong paradigm/treebank và ghi rõ ngân sách supervision; không suy diễn rằng mọi ngôn ngữ chia sẻ cùng algebra.
- **Decoder:** autoregressive decoder sinh form/string từ input, target-feature state và predicted latent. JEPA không trực tiếp “giải mã từ latent” nếu thiếu decoder đã học surface realization.
- **Uncertainty:** nếu có nhiều output hợp lệ, dự đoán phân phối/set; không mặc định MSE một target latent. Đây là lựa chọn chống collapse/đa nghiệm, không phải novelty riêng.

### Huấn luyện và suy luận

Training objective, viết tường minh bằng lời:

- Tổng loss = token/character NTP loss + λJ × JEPA edge-prediction loss + λC × valid-path consistency loss + λI × interaction loss.
- JEPA edge loss: distance(predicted target latent, stop-gradient(EMA target encoder(target form))).
- Invariance/equivariance loss: latent ngữ nghĩa không đổi qua grammatical counterfactual; latent feature đổi đúng theo action, với acceptance set nếu có nhiều realization hợp lệ.
- Path loss: distance(rollout through p, rollout through q), chỉ với path pair được xác nhận cùng endpoint và được ngôn ngữ cấp phép; mask các critical pairs có allomorphy/tương tác chưa được xác định.
- Interaction loss: chỉ áp dụng cho các tương tác được gắn nhãn/quan sát; không ép commute ở cặp feature chưa biết.

Mỗi loss phải được ablate riêng. Cần matched-compute comparison vì JEPA predictor làm tăng FLOPs; báo cả matched-update và matched-wall-clock.

Inference: sinh ứng viên theo các path hợp lệ; tính dispersion/residual và log-probability. Chọn ứng viên consensus nếu đạt ngưỡng đã hiệu chỉnh; nếu không, defer/fallback. Calibrate hậu nghiệm trên validation tách biệt; không gọi đó là đảm bảo OOD nếu calibration và test khác phân phối. Báo risk–coverage và kết quả ở full coverage song song.

**Dữ liệu:** không tăng parallel pairs trong so sánh chính. Tuy vậy, mô hình cần feature tags và tập path hợp lệ; có thể lấy từ annotation/lexicon/analyzer sẵn có hoặc một ngân sách native annotation được giới hạn và báo cáo. So sánh “cùng số cặp” nhưng khác lượng feature supervision là không công bằng. Không giả vờ rằng grammar labels là miễn phí.

## Thí nghiệm paper-ready

### RQ và giả thuyết đăng ký trước

- **RQ1 — Generation:** với cùng số form instances, JEPA + path consistency có tăng exact-form accuracy trên held-out compositions so với NTP, JEPA không path loss, và morphology/operator baselines không?
- **RQ2 — Risk score:** sau khi kiểm soát NLL/entropy, ensemble/dropout, OOD distance và quality-estimation scores, path residual có tăng khả năng phân biệt output đúng/sai không?
- **RQ3 — Selective use:** tại cùng coverage, residual-based gate có giảm lỗi form hơn các uncertainty baseline không? Ở cùng mức lỗi tối đa được chấp nhận, coverage có tăng không?
- **RQ4 — Typology:** gain có tập trung ở compositional patterns và mất đi/đảo chiều trên allomorphy, syncretism, reduplication hoặc feature interactions không? Đây là dự đoán quan trọng, không phải kết quả cần che giấu.

### Dataset/splits

- Bắt đầu từ UniMorph/SIGMORPHON 2022 (33 ngôn ngữ, nhiều hệ hình thái) cho inflection; dùng MultiBLiMP 1.0 (101 ngôn ngữ, subject–verb agreement) hoặc UrBLiMP (Urdu, 10 hiện tượng) làm validation sentence-level nếu điều kiện dữ liệu/annotation phù hợp. Hai benchmark mới này đồng thời làm tăng yêu cầu novelty: không được tuyên bố tạo benchmark/minimal-pair evaluation là đóng góp chính [MultiBLiMP 1.0](https://aclanthology.org/2026.tacl-1.10/), [UrBLiMP](https://aclanthology.org/2026.findings-acl.29/).
- Không coi việc downsample một corpus lớn là bằng chứng model hoàn toàn không có pretraining exposure.
- Báo riêng bốn overlap groups: lemma và feature set đã thấy; chỉ feature set đã thấy; chỉ lemma đã thấy; cả hai đều chưa thấy. Feature-held-out/compositional evaluation đã có tiền lệ, nên không claim split là mới.
- Dùng nhiều sampling seeds, nhiều model seeds, overlap-aware và frequency-aware splits. [Morphological Inflection: A Reality Check, ACL 2023](https://aclanthology.org/2023.acl-long.335/) cho thấy uniform sampling, split đơn và overlap không kiểm soát có thể làm méo so sánh; không dựa trên một điểm test.
- Data curve theo số lemma/forms được chọn sau data audit (ví dụ 50/100/250/500/1k paradigms nếu dữ liệu đủ); cố định tập item giữa mọi model. Ghi số tokens, update, FLOPs/wall time và số nhãn feature.
- Thêm một validation ngôn ngữ/cặp dịch nếu có đủ người bản ngữ. Phân biệt “parallel-data adaptation ít cặp” với “ngôn ngữ vắng mặt ở pretraining”.

### Baselines và ablations

1. Character Transformer NTP; NTP + standard deterministic JEPA; NTP + distributional/set JEPA; LLM-JEPA tái lập theo protocol task nhỏ như prior JEPA-language trực tiếp (đã có tại ICLR 2026).
2. Transition-based string transducer ([Makarov & Clematide 2018](https://aclanthology.org/C18-1008/)); paradigm completion/transduction ([Cotterell et al. 2017](https://aclanthology.org/E17-2120/), [Kann & Schütze 2018](https://aclanthology.org/D18-1363/)); morphology-aware latent generation ([Ataman et al.](https://arxiv.org/abs/1910.13890)); operator/representation precedent [INTERSENT](https://aclanthology.org/2023.emnlp-main.900/). Include StemCorrupt/data augmentation as a separately budgeted strong baseline, not as proposed answer.
3. Nếu chạy MT: NSL-MT, standard morphology/feature head, and ordinary NTP; compare without extra parallel data.
4. For risk: sequence NLL/token entropy, MC dropout, ensembles, OOD score, round-trip QE, translation confidence, and conformal generation. Morphology-specific confidence/selection already appears in low-resource inflection work; SIGMORPHON 2024 also explicitly includes confidence-triggered fallback/oracle query [task specification](https://github.com/sigmorphon/2024InflectionST).
5. Ablate: action types, valid-path mask, path loss, interaction handling, target distribution, JEPA target encoder, decoder conditioning, and risk score. Match both update count and compute; report unadjusted efficiency too.

### Outcomes/statistics

- Primary: exact-form accuracy and feature-bundle satisfaction, broken down by overlap type and morphological phenomenon.
- Reliability: AURC/risk–coverage, error detection AUROC/AUPRC, calibration error/Brier score, coverage at a pre-registered form-error ceiling; language/typology-stratified.
- If MT: chrF++/spBLEU/COMET secondary; native-speaker adequacy separate from MQM grammar/morphology, orthography, omissions and terminology. Automatic metrics alone do not establish form correctness.
- At least five training/split seeds where feasible; paired bootstrap or mixed-effects analysis over languages/items; report confidence intervals and per-language results. Native annotation should be blind and adjudicated; report agreement.

## Điều kiện go/no-go cho Q1

**Go** chỉ nếu cùng lúc có:

1. Significant exact-form gains or a clear Pareto improvement under matched data + compute, not just a new auxiliary loss.
2. Path residual adds predictive signal beyond NLL, ensembles, OOD/QE and conformity, and improves risk–coverage at useful coverage.
3. Results replicate across typologically distinct low-resource languages and multiple splits/seeds; gain/error pattern aligns with registered typological hypotheses. Có ít nhất một external sentence-level grammaticality test, không chỉ inflection table.
4. Human validation confirms the automatic form metric tracks genuine linguistic errors.
5. A nontrivial formal result about when sparse action-path evidence identifies a valid target form, or a sufficiently broad empirical contribution that survives direct baseline review.

**No-go/reframe** if gain is only on one synthetic split, disappears against transition/paradigm baselines, relies on more feature labels or compute, or residual is just another confidence proxy. The existing 2022/2023/2024 literature makes this an intentionally high bar. Q1 quartile depends on venue and a completed empirical paper; no literature proposal can guarantee it.

## Prior-art anchors to keep in the paper

- JEPA + autoregressive objective: [LLM-JEPA, ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/ac818ec2da1c976b267de32f59709c69-Abstract-Conference.html). Vì vậy novelty không thể chỉ là thêm JEPA loss vào decoder Transformer.
- Morphosyntactic minimal-pair evaluation: [MultiBLiMP 1.0, TACL 2026](https://aclanthology.org/2026.tacl-1.10/), [UrBLiMP, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.29/); counterfactual GEC augmentation đã có [COCOGEC, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.195/), nên counterfactual augmentation tự thân cũng không phải novelty.
- Linguistic latent transformations: [RISE, ICLR 2026 Poster](https://iclr.cc/virtual/2026/poster/10007262); latent operators with decoder: [INTERSENT, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.900/).
- Low-resource grammar penalties: [NSL-MT, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.465/).
- Sparse morphological transduction: [Makarov & Clematide, COLING 2018](https://aclanthology.org/C18-1008/); paradigmatic relations: [Cotterell et al., EACL 2017](https://aclanthology.org/E17-2120/), [Kann & Schütze, EMNLP 2018](https://aclanthology.org/D18-1363/).
- Evaluation pitfalls: [SIGMORPHON–UniMorph 2022](https://aclanthology.org/2022.sigmorphon-1.19/); [Morphological Inflection: A Reality Check, ACL 2023](https://aclanthology.org/2023.acl-long.335/).
- Active learning/confidence: [Muradoglu & Hulden, EMNLP 2022](https://aclanthology.org/2022.emnlp-main.492/); [SIGMORPHON 2024 task](https://github.com/sigmorphon/2024InflectionST).
- Selective/conformal generation: [Ren et al., ICLR 2023](https://openreview.net/forum?id=kJUS5nD0vPB); [Deutschmann et al., AAAI 2024](https://ojs.aaai.org/index.php/AAAI/article/view/29062); [Ulmer et al., Findings EACL 2024](https://aclanthology.org/2024.findings-eacl.129/).

## Open work proposed in this historical prospectus

This prospectus still lacks empirical results, an identified language set after corpus audit, and a proof of a nontrivial identifiability theorem. The direct next step is not writing an “Introduction” that overclaims. It is (1) implement the NTP / JEPA / path-score baselines on 3–5 SIGMORPHON languages; (2) run the held-out-feature/path residual pilot; (3) decide go/no-go using the criteria above; and only then lock the paper claim and target venue.

