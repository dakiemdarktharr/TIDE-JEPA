> **RESEARCH BACKGROUND, NOT THE ACTIVE SPECIFICATION.** Current model: **TIDE-JEPA**; languages: **Vietnamese, English, and Phan Rang Cham**. See [the active specification](tide_jepa_spec.md). Literature and earlier possibilities below remain useful research notes; language lists, draft designs, time-sensitive facts, and linked evidence require reconciliation or verification before reuse. They do not approve any Phan Rang Cham grammar, orthography, action inventory, or data source.
# JEPA cho sinh ngôn ngữ ít tài nguyên: research note

Ngày rà soát: 28-09-2026  
Trạng thái: định vị và giả thuyết nghiên cứu; chưa phải kết quả thực nghiệm hoặc claim đã được xác nhận là mới.

## 1. Bối cảnh Hackathon

Trang chính thức mô tả ba chủ đề Security, Generative AI và Low-Resource Languages, chạy trên Kaggle. Bốn nhiệm vụ cụ thể chỉ được công bố trong ngày thi; trang hiện không chốt cặp ngôn ngữ hoặc loại lỗi cần giải quyết. Vì vậy, paper không nên phụ thuộc vào giả định rằng đề thi là machine translation, tiếng Việt, hay một loại hình thái cụ thể. Có thể chuẩn bị trước phương pháp và benchmark kiểm soát, rồi ánh xạ sang task thật sau khi công bố.

Nguồn: [RMIT Hackathon 2026](https://rmit-hackathon.com/).

## 2. Lập luận nghiên cứu

Không nên định nghĩa vấn đề là “mô hình cần biết thêm từ”. “Inaccuracy ngôn ngữ” gộp ít nhất hai lỗi khác nhau:

1. **Sai nội dung**: nghĩa, quan hệ, phủ định, số lượng, thực thể hoặc thuật ngữ không đúng.
2. **Sai cách hiện thực hóa**: dấu/chữ, cách viết, ranh giới từ, hình thái, hòa hợp hoặc cấu trúc câu không tự nhiên.

Các lỗi đó cần được đo riêng. Một latent liên ngôn ngữ tốt có thể giúp giữ nghĩa, nhưng nếu nó bỏ qua các khác biệt bề mặt thì vẫn có thể sinh câu sai ngôn ngữ.

JEPA không phải backbone sinh từ ngữ. Nó là mục tiêu học latent. Nếu dùng squared-error để dự đoán một target latent duy nhất, nghiệm population là conditional mean. Khi một ngữ cảnh cho phép nhiều realization hợp lệ ở những cụm latent tách biệt, conditional mean có thể nằm ngoài các cụm hợp lệ. Khi đó model hoặc dự đoán một “điểm giữa” không biểu đạt realization hợp lệ, hoặc làm các target khác nhau co cụm để giảm loss.

Đây không phải khoảng trống mới do đề tài này phát hiện. Bản preprint [The JEPA Paradox in Language](https://arxiv.org/html/2607.23531) ngày 26-07-2026 đã trực tiếp phân tích conditional concentration, centroid degeneracy và collapse của JEPA xác định trên text. Paper này chưa xác minh được venue peer-reviewed trong lượt rà soát này. Do đó, đề tài không được tuyên bố “phát hiện JEPA thất bại trên ngôn ngữ” hay chỉ đề nghị mixture prediction.

## 3. Những novelty claim phải loại bỏ

| Claim không đủ mới | Bằng chứng prior art |
|---|---|
| “Tách semantic latent khỏi form/morphology latent” | [Ataman et al., ICLR 2020](https://arxiv.org/abs/1910.13890) đã kết hợp lexical-semantic latent liên tục với đặc trưng morphosyntax khi sinh từ cho Arabic/Czech/Turkish; [Bu et al., Findings ACL 2024](https://aclanthology.org/2024.findings-acl.620/) tách semantic/language-specific features và dùng chúng khi sinh bản dịch. |
| “JEPA cộng với token-generation loss” | [LLM-JEPA, ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/file/ac818ec2da1c976b267de32f59709c69-Paper-Conference.pdf) giữ loss sinh và thêm JEPA giữa các view; nhiệm vụ gồm SQL/regex/math, nhưng không đo sinh target-language ít tài nguyên hay fidelity hình thái/chính tả. |
| “JEPA + latent reasoner + Talker” | [JEPA-Reasoner](https://arxiv.org/html/2512.19171v3) đã tách latent reasoning và tái tạo text; hiện là preprint theo hồ sơ được rà soát, với thí nghiệm chính về reasoning và nhiễu, không phải linguistic fidelity. |
| “Thêm objective tự giám sát giúp hình thái low-resource” | [Wiemerslage & von der Wense, ACL 2025](https://aclanthology.org/2025.acl-long.1195/) so sánh 13 objective trên 19 ngôn ngữ; autoencoding tốt khi lexicon rất nhỏ, CMLM tốt hơn khi unlabeled corpus lớn hơn, masking theo morpheme là hướng có kết quả tích cực. |
| “Chỉ cần thay Transformer bằng Mamba” | [Pitorro et al., WMT 2024](https://aclanthology.org/2024.wmt-1.111/) cho thấy Mamba cạnh tranh, còn đưa attention vào Mamba cải thiện chất lượng dịch, extrapolation và recall named entity. |
| “Predict latent difference dưới linguistic edit” | [DiffCSE, NAACL 2022](https://aclanthology.org/2022.naacl-main.311/) đã học sentence representations nhạy với khác biệt do MLM-edit; [ESCL, ICASSP 2023](https://doi.org/10.1109/ICASSP49357.2023.10096142) dùng invariant/equivariant tasks và relative-difference loss; [RISE, ICLR 2026 Poster](https://openreview.net/forum?id=qEmKKvYr07) ánh xạ negation/conditionality/politeness thành phép quay trong embedding đa ngôn ngữ trên 7 ngôn ngữ. Chúng không chứng minh target-language generation ít tài nguyên, nhưng đủ để preempt novelty tổng quát về equivariance/latent delta. |
| “Học linguistic operators trong latent rồi thêm decoder” | [INTERSENT, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.900/) học compositional sentence operators cùng bottleneck encoder-decoder và loss contrastive + generative; [STAFFNET, 2018](https://aclanthology.org/W18-2901/) biểu diễn affix như hàm trên stem; [Vocab Diet, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1618/) học vector base + transformation cho morphology. Đây là prior art thêm chống lại tuyên bố rộng rằng operator latent + text decoder là mới. |
| “Counterfactual edits tạo quan hệ source→target mới” | [Counterfactual Data Augmentation for NMT, NAACL 2021](https://aclanthology.org/2021.naacl-main.18/) đã tạo paired edits ở source và aligned target để đo robustness/generalization; [Equivariant Transduction through Invariant Alignment, COLING 2022](https://aclanthology.org/2022.coling-1.412/) học equivariant sequence transduction trên SCAN; [Zmigrod et al., ACL 2019](https://aclanthology.org/P19-1161/) áp dụng gender counterfactual và agreement edits cho morphology. Do đó, “edit cặp câu rồi học hướng đổi” cũng không đủ mới. |
| “Dạy tránh lỗi ngôn ngữ bằng hard negatives” | [NSL-MT, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.465/) dùng vi phạm morphology/syntax/lexicon có severity weights và phạt xác suất bản dịch sai; báo cáo gain trên nhiều backbone và ngân sách bitext nhỏ. Đây là baseline rất gần bài toán; khác biệt của nó là negative ở mức sequence và phụ thuộc rule-based violation generators, không có JEPA latent dynamics. Human eval của paper chỉ báo hai ngôn ngữ (Zarma/Bambara), 50 mẫu/ngôn ngữ, cần mở rộng trong nghiên cứu tiếp theo. |
| “Tokenizer theo morpheme tự nó sẽ sửa lỗi hình thái” | [The Token Tax (AfricaNLP 2026)](https://aclanthology.org/2026.africanlp-main.10/) tìm thấy token fertility dự đoán accuracy trên 10 LLM và 16 ngôn ngữ châu Phi; ngược lại, [Morphemes without Borders (LREC 2026)](https://aclanthology.org/2026.lrec-1.923/) cho thấy morphological alignment của tokenizer không cần thiết cũng không đủ cho khả năng sinh morphology Arabic. Kết luận: tokenization là biến kiểm soát/ablation, không phải lời giải trung tâm. |

Các kết quả của Bu et al. và Ataman et al. phải được đưa vào baseline; morphology-aware objectives và tokenization cũng phải được ablate riêng, nếu không không thể biết JEPA tạo thêm ích lợi gì.

## 4. Chuỗi suy luận → lý thuyết thiết kế → thuật toán (ứng viên cũ bị bác bỏ)

**Kết quả red-team:** phiên bản tổng quát “JEPA + invariant/equivariant latent delta + language feature margin” không đủ cơ sở làm novelty claim. DiffCSE/ESCL preempt cơ chế equivariance trong sentence representation; RISE preempt biến đổi ngôn ngữ thành hình học latent đa ngôn ngữ; NSL-MT preempt negative linguistic constraints cho low-resource generation. Ý tưởng “ghép các action latent rồi tổng quát hóa sang tổ hợp hình thái chưa thấy” cũng đã bị hạ xuống: transition-based string transduction, paradigm completion/transduction và các benchmark compositional generalization đã có tiền lệ. Cả action-conditioned multi-step latent prediction cũng đã có trong JEPA/RL ngoài NLP. Phần dưới của mục này ghi lại ứng viên cũ làm đối chứng, không phải đóng góp mới.

### Lập luận bằng lời

Sai ngôn ngữ không đồng nghĩa sai nghĩa: hai câu có thể tương đương về nội dung nhưng khác nhau ở phủ định, vai nghĩa, hòa hợp, dấu, cách viết, hoặc có thể đúng ngữ pháp nhưng mang nghĩa khác. Vì vậy, loss chỉ đo semantic similarity không đảm bảo đúng; loss chỉ đo token tiếp theo cũng có thể học shortcut theo tokenization/thứ tiếng liên quan. Các nghiên cứu morphology-aware đã tách latent semantic khỏi feature hình thái hoặc dự đoán morphology tường minh; đó là baseline có thật, không thể gọi lại là novelty.

Điểm đặc biệt với JEPA là dự đoán latent duy nhất bằng MSE tối ưu conditional mean. Ngôn ngữ có nhiều realization hợp lệ, nên mean có thể không là một realization hợp lệ; preprint JEPA Paradox đã phân tích và thực nghiệm nguy cơ này. Chỉ thay MSE bằng mixture cũng không thành contribution mới. Thay vào đó cần xác định *những phân biệt nào quyết định đúng/sai cho task*, rồi buộc representation dự đoán quan hệ giữa các trạng thái đối chứng ấy.

### Lý thuyết thiết kế (chưa phải định lý mới)

Định nghĩa mỗi ví dụ có nội dung ngữ nghĩa `s` và một vector quyết định ngôn ngữ `a` (ví dụ negation, tense, number, agreement, diacritic/Unicode, entity/term). Các câu cùng nội dung có thể đổi surface form mà giữ `s`; một can thiệp ngôn ngữ có thể đổi một thành phần `a_j` và phải tạo ra thay đổi có kiểm soát trong representation. Do đó, representation đích không nên chỉ bất biến theo nghĩa, mà cần *equivariant theo feature intervention*: giữ ổn định khi thay đổi không liên quan, nhưng dịch chuyển có định hướng khi feature có ý nghĩa bị đổi.

Một design principle có thể kiểm chứng là decision-boundary preservation: nếu feature classifier trên target latent có margin `m` và Lipschitz constant `L`, thì latent prediction error nhỏ hơn `m/(2L)` giữ nguyên quyết định feature. Theo Markov bound, xác suất vượt ngưỡng bị chặn bởi `4 L² E[||z_hat-z||²] / m²`. Bound này là hệ quả margin chuẩn, **không** tự nó là đóng góp lý thuyết mới. Nó chỉ biện minh vì sao nên học margin/quan hệ feature thay vì tối ưu khoảng cách semantic trung bình; novelty phải đến từ objective/setting mới và kết quả có thể tái lập.

### Thuật toán ứng viên: Decision-Boundary / Equivariant JEPA

1. Dùng pretrained multilingual encoder-decoder làm nền, giữ loss sinh token để model vẫn sinh được chuỗi. Encoder có một latent nội dung `z_s` và một latent ngôn ngữ có cấu trúc `z_a`; ngôn ngữ đích/task conditioning đi vào predictor và decoder.
2. Từ đúng các ví dụ hiện có, tạo *paired interventions* được kiểm tra: một view bất biến nghĩa (ví dụ Unicode canonicalization/paraphrase được xác nhận) và một view đổi đúng một feature (ví dụ contrast morphology/negation/number, chỉ với rule/analyzer đủ đáng tin). Đây là weak supervision từ phép biến đổi, không phải parallel data mới; phải báo rõ nguồn knowledge và tách điều kiện có/không có analyzer.
3. Predictor JEPA dự đoán latent nội dung, các feature anchor và **độ dịch chuyển latent** sau can thiệp. Với cặp `y, T_j(y)`, loss quan hệ có dạng `||[g(x_j)-g(x)] - stopgrad[z_a(T_j(y))-z_a(y)]||²`, cộng margin để các trạng thái có feature khác không co cụm. Cặp chỉ được dùng nếu phép biến đổi hợp lệ và source/context phản ánh đúng feature đã đổi.
4. Dùng objective theo kiểu set/distribution cho target latent khi có nhiều realization hợp lệ; không hồi quy tất cả về một centroid. Cần so sánh proper scoring loss, contrastive/set loss và deterministic MSE, không mặc định mixture là novelty.
5. Tổng loss thử nghiệm: `L = L_token + λ_s L_semantic-invariance + λ_e L_intervention-equivariance + λ_a L_feature-anchor + λ_m L_margin`. `L_semantic-invariance` bảo vệ meaning; `L_intervention-equivariance` bảo vệ quan hệ feature; `L_anchor` chấm đúng feature; `L_margin` tách các cặp tối thiểu thực sự khác nghĩa/ngữ pháp.

Đây là **candidate để kiểm tra novelty**, chưa phải thuật toán đã chứng minh mới hay hiệu quả. Câu hỏi paper phải đặt hẹp: *với cùng data, backbone và compute, có thể học latent predictive states giữ được các ranh giới quyết định ngôn ngữ tốt hơn token NLL, deterministic/distributional JEPA và morphology-aware NMT hay không?* Contribution chỉ sống nếu search sâu hơn xác nhận chưa có prior art gần trùng và matched experiments ủng hộ.

### Ứng viên mới để audit: typed partial operators + path-risk control

**Quan sát dẫn xuất từ lỗi:** trong morphology, một feature bundle không phải lúc nào cũng là phép cộng các suffix độc lập. Một feature edit chỉ xác định trên một số lớp từ/ngữ cảnh; hai edit có thể commute về cú pháp nhưng không commute ở realization do allomorphy, syncretism hoặc phonology. Vì vậy ép mọi phép biến đổi thành group action khả nghịch/giao hoán có thể tạo đúng hình học nhưng sai ngôn ngữ. Mặt khác, ép model chọn một cách hiện thực hóa khi các đường suy luận xung đột làm tăng lỗi tự tin.

**Lý thuyết thiết kế, hiện là giả thuyết:** mô hình hóa feature edits như một đồ thị chuyển trạng thái *có kiểu và một phần*. Tách latent của trạng thái morphosyntactic chuẩn hoá `z_g` khỏi latent/decoder hiện thực hóa bề mặt `z_f`. Với trạng thái ngữ cảnh/lemma `z_g` và action `a` (ví dụ đổi số hoặc thì), `T_a(z_g)` chỉ được định nghĩa khi action được ngữ pháp cho phép trong trạng thái đó. Chỉ với một “diamond” feature độc lập đã được xác nhận, hai đường `T_b(T_a(z_g))` và `T_a(T_b(z_g))` mới bị kỳ vọng hội tụ trong **canonical feature state**. Không đòi hai đường tạo cùng surface string/latent hình thái bề mặt: allomorphy, phonology và biến thể hợp lệ thuộc vào bộ giải mã hiện thực hóa. Chênh lệch ở canonical state (`path residual`) có thể báo hiệu trạng thái chưa định danh hoặc model ngoại suy; nó không được tự động diễn giải là lỗi, và chỉ trở thành risk score nếu dự báo lỗi sau calibration.

Điểm có thể là đóng góp không phải “feature composition” hay “commutativity” tự thân; đó là **dùng topology của các đường feature có điều kiện để phân biệt (i) composition có bằng chứng, (ii) interaction ngôn ngữ có thể học, (iii) realization chưa định danh được**, rồi điều khiển selective generation theo ba trạng thái ấy. Tuy nhiên selective prediction cho NLP đã được nghiên cứu ([Xin et al., ACL 2021](https://aclanthology.org/2021.acl-long.84/)); OOD detection + selective generation đã được thử trực tiếp trên summarization/MT ([Ren et al., ICLR 2023](https://openreview.net/forum?id=kJUS5nD0vPB)); composition-OOD đã dùng NLL/entropy/dropout/ensembles ([Lukovnikov et al., Findings EMNLP 2021](https://aclanthology.org/2021.findings-emnlp.54/)); conformal decoding có coverage guarantees cho sequence generation ([Deutschmann et al., AAAI 2024](https://ojs.aaai.org/index.php/AAAI/article/view/29062), [Ulmer et al., Findings EACL 2024](https://aclanthology.org/2024.findings-eacl.129/)); [Conformal Language Modeling, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/31421b112e5f7faf4fc577b74e45dab2-Abstract-Conference.html) calibrates candidate-set generation/rejection; and [Homomorphism Error](https://proceedings.mlr.press/v282/an26a.html) đo độ lệch biểu diễn, tương quan với compositional generalization trong controlled tasks. Round-trip translation consistency cũng được dùng để ước lượng chất lượng dịch ([Moon et al., EAMT 2020](https://aclanthology.org/2020.eamt-1.11/), [Zhuo et al., Findings ACL 2023](https://aclanthology.org/2023.findings-acl.22/)); learned confidence for MT also detects noisy/OOD inputs ([ACL 2022](https://aclanthology.org/2022.acl-long.167/)). Vì thế “dùng residual làm confidence” không tự thân mới; phải chứng minh partial morphology graph + path disagreement dự báo lỗi target-form vượt entropy/ensemble, OOD/QE/round-trip scores, conformal methods và structural metrics hiện có.

**Thuật toán thử nghiệm (Partial-Action JEPA, tên tạm):**

1. Giữ encoder-decoder Transformer và next-token loss làm bộ sinh/baseline; JEPA chỉ học predictor trên latent states. Tách `z_g` (canonical morphosyntactic state) và `z_f` (surface realization). Mỗi state mang lemma/context, ngôn ngữ, và feature bundle được biết/ước lượng. Mỗi action có type, điều kiện áp dụng, và nhãn support.
2. Học `T_a(z_g)` như partial conditional latent predictor; decoder autoregressive hiện thực hóa từ nội dung, `z_g`, ngôn ngữ và context thành surface string. Các target latent đa realization cần một phân phối/set predictor, không dùng MSE một điểm mặc định; giữ token loss để latent prediction không bị nhầm thành khả năng sinh chuỗi.
3. Tạo các đường feature chỉ từ bundle hợp lệ đã được annotator, lexicon/analyzer hoặc nguồn benchmark xác nhận. Với diamond actions độc lập và có cùng endpoint feature bundle, áp path-consistency loss trên `z_g`, không ép commute ở `z_f`/surface form. Với interaction đã quan sát, học residual riêng có điều kiện (không ép commute). Không tự sinh grammatical labels từ heuristic không được kiểm tra.
4. Tại suy luận, tính disagreement giữa các đường dự đoán. Hiệu chỉnh ngưỡng trên validation để quyết định generate / dùng fallback / abstain. Báo risk–coverage, không chỉ accuracy trên phần model tự tin; kiểm tra theo tỷ lệ bundle mới và lớp allomorphy.
5. Tổng loss khi huấn luyện là token NLL + latent transition prediction + path-consistency cho các đường độc lập đã xác thực + regularization thưa/điều kiện cho residual tương tác. Calibrate ngưỡng selective-risk hậu nghiệm trên validation tách biệt; không giả định một penalty huấn luyện tùy ý tự tạo ra bảo đảm calibration. Mọi thành phần phải ablate riêng, matched theo compute và số nhãn.

**Dự đoán có thể bác bỏ:** ở cùng dữ liệu ít, method chỉ nên cải thiện exact-form/feature accuracy ở các bundle có primitive actions được chứng kiến, support graph đủ nối và path residual thấp; nó nên phát hiện rủi ro cao trên bundle thiếu định danh. Nếu path disagreement không dự báo lỗi sau calibration, hoặc selective coverage thấp hơn cách dùng uncertainty chuẩn (ensemble/conformal/selective classifier), không có đóng góp đủ sức đứng riêng. Một bound cộng dồn Lipschitz/margin đơn giản sẽ là hệ quả chuẩn, không được đóng gói thành theorem mới; cần chứng minh điều kiện identifiability không tầm thường hoặc đưa bằng chứng đa ngôn ngữ mạnh.

**Status:** ứng viên này mới chỉ là hướng để audit, không phải claim Q1 đã xác nhận. Các precedent gần nhất gồm [Makarov & Clematide 2018](https://aclanthology.org/C18-1008/) về edit-action transduction low-resource, [Cotterell et al. 2017](https://aclanthology.org/E17-2120/) và [Kann & Schütze 2018](https://aclanthology.org/D18-1363/) về quan hệ giữa paradigm cells, [SIGMORPHON–UniMorph 2022](https://aclanthology.org/2022.sigmorphon-1.19/) và [SSMT 2023](https://aclanthology.org/2023.findings-acl.175/) về generalization, cùng [Samir & Silfverberg 2023](https://aclanthology.org/2023.emnlp-main.19/) về compositionality và tương quan stem–affix. Selective generation, composition-OOD scores, conformal sequence sets, round-trip quality estimation và representational homomorphism metrics là các baseline bắt buộc. Path disagreement chỉ có nghĩa trên canonical feature states của các đường có cùng endpoint và đã được xác thực; surface allomorphy/ambiguity không bị phạt. Các công trình này chưa chứng minh chính xác ứng viên đã bị preempt, nhưng cấm claim rộng dựa trên thành phần quen thuộc.

## 5. Ablation candidate: JEPA dự đoán phân phối realization

Đây là đối chứng quan trọng cho thuật toán intervention-equivariant ở mục 4, không phải đóng góp mới tự thân.

**Giả thuyết H2 (ablation):** Với cùng số lượng cặp song ngữ, JEPA dự đoán phân phối latent target có thể vượt JEPA xác định nếu các realization hợp lệ có conditional dispersion cao; đây là baseline/ablation, không phải novelty claim.

**Candidate method (chưa đặt tên cuối): Conditional Realization JEPA.** Với source/context `x`, ngôn ngữ đích `ℓ`, target `y`, encoder tạo một biểu diễn nội dung `z_s` và biểu diễn hiện thực hóa `z_f`. Predictor trả về phân phối, không trả một điểm cố định:

\[
q_\theta(z_s,z_f,m \mid x,\ell)
=q_\theta(z_s\mid x)\,q_\theta(z_f,m\mid z_s,x,\ell),
\]

trong đó `m` là bundle feature có cấu trúc, ví dụ morphology khi có analyzer/UD/UniMorph, hoặc orthography/Unicode, segmentation và entity preservation ở track phù hợp. Bộ giải mã từ-token nhận cả latent nội dung lẫn latent hiện thực hóa.

Loss thử nghiệm:

\[
\mathcal L=\mathcal L_{\text{token}}
 +\lambda_s\mathcal L_{\text{semantic-JEPA}}
 +\lambda_f\mathcal L_{\text{conditional-form}}
 +\lambda_a\mathcal L_{\text{anchor}}.
\]

- `token`: loss sinh chuẩn, giữ năng lực tạo chuỗi.
- `semantic-JEPA`: dự đoán latent nội dung giữa source/target hoặc giữa hai view ngữ nghĩa.
- `conditional-form`: proper distributional loss cho latent realization, có điều kiện theo ngôn ngữ và feature bundle; ablate so với squared-error JEPA.
- `anchor`: dự đoán/khôi phục feature cần giữ như morpheme, dấu, tên riêng và thuật ngữ.

Một biến thể có thể so sánh là **concentration-gated objective**: ước lượng độ phân tán của target latent từ các view/counterfactual hợp lệ; dùng điểm JEPA xác định chỉ khi phân tán thấp và dùng objective phân phối khi phân tán cao. Cần cẩn thận: để tạo view hình thái phải dùng bộ chuyển đổi/từ vựng hiện có hoặc annotator; phải giữ nguyên ngân sách cặp song ngữ và báo riêng mọi supervision ngoài corpus chính. Không được diễn giải phép biến đổi này thành “thêm dữ liệu miễn phí”.

Đây hiện là giả thuyết, chưa phải thuật toán có novelty đã được chứng minh. “Mixture/uncertainty-aware JEPA” đơn lẻ cũng chưa đủ mới vì paper JEPA Paradox đã nêu distributional/mixture alternatives, còn latent morphology và linguistic features đã có prior art. Đóng góp phải nằm ở quy tắc điều kiện hóa/định tuyến theo realization features, ở bảo đảm lý thuyết phi tầm thường hoặc ở bằng chứng hệ thống rõ ràng trên low-resource generation.

## 6. Mệnh đề hình thức và giới hạn

Với target latent `Z` và context `C`, loss bình phương thỏa:

\[
\mathbb E[\|Z-h(C)\|^2]
=\mathbb E[\mathrm{tr}\,\mathrm{Cov}(Z\mid C)]
 +\mathbb E[\|\mathbb E[Z\mid C]-h(C)\|^2].
\]

Do đó predictor tối ưu là conditional mean, còn conditional variance là error floor. Nếu valid realization classes là các cụm latent rời nhau, mean có thể không tương ứng realization hợp lệ. Phân rã này là công cụ biện minh cho objective, không tự nó là định lý mới; JEPA Paradox đã nêu cơ chế centroid/collapse tương tự. Để đưa ra theorem đóng góp, cần chứng minh một kết quả riêng nối sai số của posterior realization/feature với xác suất lỗi linguistic feature, dưới giả định được nêu rõ và có kiểm tra thực nghiệm.

## 7. Thiết kế đánh giá ban đầu

Chỉ chọn benchmark ngôn ngữ sau khi task hackathon được công bố. Cho bài báo độc lập, cặp khởi đầu có thể là Vietnamese + Nepali: Vietnamese đo dấu, Unicode, biên từ và entity; Nepali bổ sung feature morphology. Không gộp chúng thành một claim morphology chung.

| Trục | Thiết kế |
|---|---|
| Ngân sách | Cố định cùng 1k/5k/10k cặp song ngữ cho mọi hệ thống; tách test/dev công khai, không bổ sung parallel pairs cho method đề xuất. |
| Baselines | NMT/LLM nền; JEPA xác định + token loss; JEPA phân phối; Ataman-style morphology model; Bu et al. semantic/linguistic features; tokenization BPE/byte/morpheme; morphology-aware CMLM; Makarov transition transducer; paradigm transduction/SHIP; NSL-MT; INTERSENT-style latent operators; token NLL/entropy, ensembles/dropout, OOD/QE, round-trip QE, conformal generation. |
| Backbone | Trước hết cố định một pretrained encoder-decoder để cô lập objective. Chỉ sau đó so Transformer với Mamba-attention hybrid; không lấy kiến trúc làm contribution cùng lúc nếu thiếu compute. |
| Tổng quát | chrF++, BLEU và COMET; báo theo ngôn ngữ, seed và bootstrap confidence interval. |
| Linguistic fidelity | Contrast sets: bản đúng và bản chỉ sai một feature; exact diacritic/Unicode, word-boundary, morphology, named entity, number và terminology accuracy. |
| Human evaluation | Native raters dùng MQM theo span/category/severity: mistranslation, omission, morphology/grammar, orthography, entity/term. Báo agreement và adjudication. |
| Robustness | Phép perturb Unicode/dấu/script và prompt multilingual có kiểm soát; đo semantic preservation song song với fidelity, không gộp thành một score. |

Nguồn benchmark đáng dùng: [MultiBLiMP 1.0, TACL 2026](https://aclanthology.org/2026.tacl-1.10/) cho agreement trên 101 ngôn ngữ; [YallaMorph, EMNLP 2026](https://arxiv.org/abs/2609.10153) cho Arabic controlled morphology; [FLORES](https://aclanthology.org/D19-1632/) cho Nepali-English; [PhoMT](https://arxiv.org/html/2110.12199) cho Vietnamese, nhưng phải downsample training budget và giữ nguyên test.

## 8. Điều kiện bác bỏ

Không tiếp tục claim JEPA contribution nếu một trong các kết quả sau xảy ra:

1. Method không vượt baseline Bu/Ataman/CMLM ở fidelity khi cùng ngân sách và cùng base checkpoint.
2. Semantic adequacy tăng nhưng feature fidelity giảm, hoặc ngược lại, mà không có Pareto improvement/đánh đổi được định lượng.
3. Gain biến mất khi tokenizer, auxiliary morphology loss, extra compute và data budget được kiểm soát.
4. Conditional dispersion không dự đoán được nơi objective phân phối có ích hơn objective xác định.
5. Kết quả chỉ có trên một ngôn ngữ, một seed, hoặc một benchmark tổng hợp không được người bản ngữ xác thực.

## 9. Quyết định hiện tại và việc kế tiếp

- Không theo hướng “JEPA thay Transformer”: JEPA là objective; bộ sinh token vẫn cần. Mamba là lựa chọn backbone riêng, nên chỉ thử sau khi objective được cô lập.
- Không tuyên bố novelty cho semantic/form disentanglement, morphology anchors hoặc mixture JEPA riêng lẻ.
- Chốt dữ liệu/task sau khi RMIT công bố bốn nhiệm vụ; website hiện nói challenge details reveal trong ngày thi.
- Hạ “Decision-Boundary / Equivariant JEPA” xuống baseline nghiên cứu vì cơ chế chung đã có trong DiffCSE/ESCL/RISE và negative linguistic constraints đã có trong NSL-MT.
- Ứng viên kế tiếp cần audit, chưa claim mới: **typed partial feature transitions + path disagreement làm tín hiệu selective risk**, trong đó JEPA là predictor latent và decoder autoregressive. Feature-combination split/action model/path consistency/latent operators/selective prediction/conformal sets/OOD detection/round-trip quality estimation/representational homomorphism metrics đều có prior art; phải chứng minh phần morphology-specific thêm giá trị ngoài entropy, ensembles/dropout, OOD/QE scores, conformal risk control và baselines sinh chuỗi. So với paradigm transduction/SHIP, Makarov-style edit transducer, SSMT, NSL-MT, INTERSENT, transformer NLL, JEPA xác định/phân phối. Nếu path residual không tăng selective risk–coverage khi so sánh ghép cặp theo các score này, hoặc thiếu đa ngôn ngữ/human validation thì bỏ hướng.
- Giữ nguyên tokenizer, checkpoint, corpus pair, số update và compute trong so sánh objective JEPA/NLL; thêm NSL-MT làm baseline sequence-negative, cùng Bu/Ataman và morphology generation baselines. Đánh giá adequacy và target form tách biệt, kèm native MQM và feature contrast sets; kiểm tra contamination, split theo document/lemma, nhiều seed và learning curve.
- RMIT công bố task cụ thể trong ngày thi; không chốt benchmark hoặc ngôn ngữ trước đó. Bài báo cần nghiên cứu độc lập, nhiều ngôn ngữ/seed và kiểm định người bản ngữ; không suy ra claim Q1 từ một kết quả hackathon.


