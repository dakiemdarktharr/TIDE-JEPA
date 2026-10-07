"""Original AI-authored Vi–En controlled examples; not PhoMT or human gold.

Each tuple explicitly specifies the four meaning states (current/past x
positive/negative). Actions follow these stated meanings, not translation links.
Reviewers must examine the actual generated records before approving them.
"""

import argparse
import json
from pathlib import Path

from .data import CorpusRecord, dataset_fingerprint
from .schema import Action


# Independently authored event families. The split is fixed before model runs.
# en: current positive, current negative, past positive, past negative; then vi.
FAMILIES = {
    "train": [
        ("read", "Lan reads a book now.", "Lan does not read a book now.", "Lan read a book yesterday.", "Lan did not read a book yesterday.", "Bây giờ Lan đọc một quyển sách.", "Bây giờ Lan không đọc một quyển sách.", "Hôm qua Lan đọc một quyển sách.", "Hôm qua Lan không đọc một quyển sách."),
        ("cook", "Nam cooks rice now.", "Nam does not cook rice now.", "Nam cooked rice yesterday.", "Nam did not cook rice yesterday.", "Bây giờ Nam nấu cơm.", "Bây giờ Nam không nấu cơm.", "Hôm qua Nam nấu cơm.", "Hôm qua Nam không nấu cơm."),
        ("open", "Mai opens the door now.", "Mai does not open the door now.", "Mai opened the door yesterday.", "Mai did not open the door yesterday.", "Bây giờ Mai mở cửa.", "Bây giờ Mai không mở cửa.", "Hôm qua Mai mở cửa.", "Hôm qua Mai không mở cửa."),
        ("wash", "Minh washes a cup now.", "Minh does not wash a cup now.", "Minh washed a cup yesterday.", "Minh did not wash a cup yesterday.", "Bây giờ Minh rửa một cái cốc.", "Bây giờ Minh không rửa một cái cốc.", "Hôm qua Minh rửa một cái cốc.", "Hôm qua Minh không rửa một cái cốc."),
        ("draw", "Hoa draws a flower now.", "Hoa does not draw a flower now.", "Hoa drew a flower yesterday.", "Hoa did not draw a flower yesterday.", "Bây giờ Hoa vẽ một bông hoa.", "Bây giờ Hoa không vẽ một bông hoa.", "Hôm qua Hoa vẽ một bông hoa.", "Hôm qua Hoa không vẽ một bông hoa."),
        ("buy", "An buys bread now.", "An does not buy bread now.", "An bought bread yesterday.", "An did not buy bread yesterday.", "Bây giờ An mua bánh mì.", "Bây giờ An không mua bánh mì.", "Hôm qua An mua bánh mì.", "Hôm qua An không mua bánh mì."),
        ("drink", "Binh drinks water now.", "Binh does not drink water now.", "Binh drank water yesterday.", "Binh did not drink water yesterday.", "Bây giờ Bình uống nước.", "Bây giờ Bình không uống nước.", "Hôm qua Bình uống nước.", "Hôm qua Bình không uống nước."),
        ("carry", "Ha carries a bag now.", "Ha does not carry a bag now.", "Ha carried a bag yesterday.", "Ha did not carry a bag yesterday.", "Bây giờ Hà mang một cái túi.", "Bây giờ Hà không mang một cái túi.", "Hôm qua Hà mang một cái túi.", "Hôm qua Hà không mang một cái túi."),
        ("plant", "Dung plants a tree now.", "Dung does not plant a tree now.", "Dung planted a tree yesterday.", "Dung did not plant a tree yesterday.", "Bây giờ Dũng trồng một cái cây.", "Bây giờ Dũng không trồng một cái cây.", "Hôm qua Dũng trồng một cái cây.", "Hôm qua Dũng không trồng một cái cây."),
        ("clean", "Linh cleans the table now.", "Linh does not clean the table now.", "Linh cleaned the table yesterday.", "Linh did not clean the table yesterday.", "Bây giờ Linh lau bàn.", "Bây giờ Linh không lau bàn.", "Hôm qua Linh lau bàn.", "Hôm qua Linh không lau bàn."),
        ("write", "Thu writes a letter now.", "Thu does not write a letter now.", "Thu wrote a letter yesterday.", "Thu did not write a letter yesterday.", "Bây giờ Thu viết một lá thư.", "Bây giờ Thu không viết một lá thư.", "Hôm qua Thu viết một lá thư.", "Hôm qua Thu không viết một lá thư."),
        ("close", "Son closes the window now.", "Son does not close the window now.", "Son closed the window yesterday.", "Son did not close the window yesterday.", "Bây giờ Sơn đóng cửa sổ.", "Bây giờ Sơn không đóng cửa sổ.", "Hôm qua Sơn đóng cửa sổ.", "Hôm qua Sơn không đóng cửa sổ."),
    ],
    "validation": [
        ("fix", "Tuan fixes a bicycle now.", "Tuan does not fix a bicycle now.", "Tuan fixed a bicycle yesterday.", "Tuan did not fix a bicycle yesterday.", "Bây giờ Tuấn sửa một chiếc xe đạp.", "Bây giờ Tuấn không sửa một chiếc xe đạp.", "Hôm qua Tuấn sửa một chiếc xe đạp.", "Hôm qua Tuấn không sửa một chiếc xe đạp."),
        ("sell", "Nga sells fruit now.", "Nga does not sell fruit now.", "Nga sold fruit yesterday.", "Nga did not sell fruit yesterday.", "Bây giờ Nga bán trái cây.", "Bây giờ Nga không bán trái cây.", "Hôm qua Nga bán trái cây.", "Hôm qua Nga không bán trái cây."),
        ("listen", "Phuc listens to music now.", "Phuc does not listen to music now.", "Phuc listened to music yesterday.", "Phuc did not listen to music yesterday.", "Bây giờ Phúc nghe nhạc.", "Bây giờ Phúc không nghe nhạc.", "Hôm qua Phúc nghe nhạc.", "Hôm qua Phúc không nghe nhạc."),
        ("feed", "Vy feeds a cat now.", "Vy does not feed a cat now.", "Vy fed a cat yesterday.", "Vy did not feed a cat yesterday.", "Bây giờ Vy cho một con mèo ăn.", "Bây giờ Vy không cho một con mèo ăn.", "Hôm qua Vy cho một con mèo ăn.", "Hôm qua Vy không cho một con mèo ăn."),
    ],
    "test": [
        ("paint", "Huy paints a wall now.", "Huy does not paint a wall now.", "Huy painted a wall yesterday.", "Huy did not paint a wall yesterday.", "Bây giờ Huy sơn một bức tường.", "Bây giờ Huy không sơn một bức tường.", "Hôm qua Huy sơn một bức tường.", "Hôm qua Huy không sơn một bức tường."),
        ("find", "My finds a key now.", "My does not find a key now.", "My found a key yesterday.", "My did not find a key yesterday.", "Bây giờ My tìm thấy một chiếc chìa khóa.", "Bây giờ My không tìm thấy một chiếc chìa khóa.", "Hôm qua My tìm thấy một chiếc chìa khóa.", "Hôm qua My không tìm thấy một chiếc chìa khóa."),
        ("learn", "Khanh learns a song now.", "Khanh does not learn a song now.", "Khanh learned a song yesterday.", "Khanh did not learn a song yesterday.", "Bây giờ Khánh học một bài hát.", "Bây giờ Khánh không học một bài hát.", "Hôm qua Khánh học một bài hát.", "Hôm qua Khánh không học một bài hát."),
        ("send", "Quynh sends a message now.", "Quynh does not send a message now.", "Quynh sent a message yesterday.", "Quynh did not send a message yesterday.", "Bây giờ Quỳnh gửi một tin nhắn.", "Bây giờ Quỳnh không gửi một tin nhắn.", "Hôm qua Quỳnh gửi một tin nhắn.", "Hôm qua Quỳnh không gửi một tin nhắn."),
    ],
}

# V4 is a new, same-language synthetic corpus with disjoint event families
# from v3 and two independently rendered surface forms for each meaning state.
# Tuple fields: event, EN agent/base/present/past/patient, VI agent/verb/patient.
FAMILIES_V4 = {
    "train": [
        ("borrow", "Phuong", "borrow", "borrows", "borrowed", "a pen", "Phương", "mượn", "một cây bút"),
        ("bake", "Khoa", "bake", "bakes", "baked", "a cake", "Khoa", "nướng", "một chiếc bánh"),
        ("fold", "Trang", "fold", "folds", "folded", "a shirt", "Trang", "gấp", "một chiếc áo"),
        ("kick", "Long", "kick", "kicks", "kicked", "a ball", "Long", "đá", "một quả bóng"),
        ("pour", "Diep", "pour", "pours", "poured", "tea", "Diệp", "rót", "trà"),
        ("mail", "Nhi", "mail", "mails", "mailed", "a letter", "Nhi", "gửi", "một lá thư"),
        ("row", "Tuan", "row", "rows", "rowed", "a boat", "Tuấn", "chèo", "một chiếc thuyền"),
        ("lift", "Vy", "lift", "lifts", "lifted", "a box", "Vy", "nhấc", "một cái hộp"),
        ("sweep", "Hieu", "sweep", "sweeps", "swept", "the floor", "Hiếu", "quét", "sàn nhà"),
        ("sew", "My", "sew", "sews", "sewed", "a button", "Mỹ", "khâu", "một chiếc cúc áo"),
        ("chop", "Quang", "chop", "chops", "chopped", "vegetables", "Quang", "băm", "rau củ"),
        ("stir", "Lan Anh", "stir", "stirs", "stirred", "the soup", "Lan Anh", "khuấy", "nồi súp"),
    ],
    "validation": [
        ("catch", "Bao", "catch", "catches", "caught", "a fish", "Bảo", "bắt", "một con cá"),
        ("polish", "Kim", "polish", "polishes", "polished", "the shoes", "Kim", "đánh bóng", "đôi giày"),
        ("pack", "Son", "pack", "packs", "packed", "a suitcase", "Sơn", "đóng gói", "một chiếc va li"),
        ("water", "Thao", "water", "waters", "watered", "the flowers", "Thảo", "tưới", "những bông hoa"),
    ],
    "test": [
        ("measure", "Duy", "measure", "measures", "measured", "the table", "Duy", "đo", "chiếc bàn"),
        ("unlock", "Nga", "unlock", "unlocks", "unlocked", "the gate", "Nga", "mở khóa", "cánh cổng"),
        ("mix", "Phuc", "mix", "mixes", "mixed", "the batter", "Phúc", "trộn", "bột bánh"),
        ("count", "Yen", "count", "counts", "counted", "the coins", "Yến", "đếm", "những đồng xu"),
    ],
}


def author_seed(output_dir):
    output = Path(output_dir)
    if output.exists():
        raise FileExistsError("seed output already exists; do not overwrite a reviewed corpus")
    rows, edges, paths, groups = [], [], [], {}
    single_edges = [(0, 2, "TIME", "PAST"), (2, 0, "TIME", "NOW"),
                    (0, 1, "POLARITY", "NEGATIVE"), (1, 0, "POLARITY", "POSITIVE"),
                    (2, 3, "POLARITY", "NEGATIVE"), (3, 2, "POLARITY", "POSITIVE"),
                    (1, 3, "TIME", "PAST"), (3, 1, "TIME", "NOW")]
    for split, families in FAMILIES.items():
        for family in families:
            event, *texts = family
            group = f"authored-{event}"
            groups[group] = split
            # Test paths intentionally reverse the action order used in train
            # and validation; v4.17 discloses this as a secondary holdout axis.
            path_edges = ([(0, 2, "TIME", "PAST"), (2, 3, "POLARITY", "NEGATIVE")]
                          if split == "test" else
                          [(0, 1, "POLARITY", "NEGATIVE"), (1, 3, "TIME", "PAST")])
            for language, state_texts in (("en", texts[:4]), ("vi", texts[4:])):
                for index, (source, target, kind, value) in enumerate(single_edges + path_edges):
                    is_path = index >= len(single_edges)
                    rows.append(CorpusRecord(
                        record_id=f"{group}-{language}-{index}", split_group_id=group,
                        language=language, source_text=state_texts[source], target_text=state_texts[target],
                        source_frame_id=f"{group}-state-{source}", target_frame_id=f"{group}-state-{target}",
                        action=Action(kind, value), provenance_ref="tide_jepa/pilot_seed.py:original-ai-authored-v1",
                        license_ref="original-ai-authored-internal-research; no-PhoMT-content",
                        approval_status="pending", path_id=f"{group}-path" if is_path else None,
                        path_step=index - len(single_edges) if is_path else None,
                    ))
            for index in range(10):
                edges.append({"left_record_id": f"{group}-en-{index}", "right_record_id": f"{group}-vi-{index}", "relation": "same_event"})
            paths.append({"left_path_id": f"{group}-path", "left_language": "en", "right_path_id": f"{group}-path", "right_language": "vi", "relation": "same_event"})
    actions = [{"kind": kind, "value": value} for kind, value in (("TIME", "NOW"), ("TIME", "PAST"), ("POLARITY", "POSITIVE"), ("POLARITY", "NEGATIVE"))]
    output.mkdir(parents=True)
    (output / "corpus.draft.jsonl").write_text("".join(json.dumps(row.to_dict(), ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    files = {
        "inventory.draft.json": {"actions": actions, "approved_by_language": {"en": [], "vi": [], "cham_phan_rang": []}, "proposed_by_language": {"en": actions, "vi": actions}},
        "alignments.draft.json": {"edge_pairs": edges, "path_pairs": paths},
        "groups.json": groups,
        "data_statement.json": {"source": "original AI-authored synthetic controlled-language pilot", "phomt_used": False,
                                "human_validated": False, "languages": ["en", "vi"], "event_families": len(groups),
                                "records": len(rows), "draft_sha256": dataset_fingerprint(rows),
                                "split_policy": "Disjoint event/predicate families; fixed before training. Shared sentence templates occur in all partitions; this is NOT template- or domain-generalization evidence.",
                                "held_out_path": "TIME=PAST -> POLARITY=NEGATIVE is absent from train/validation paths; single actions remain in train.",
                                "limitations": ["AI-authored and AI-reviewed only", "Small repetitive templates", "Single accepted target per state", "No natural-corpus or human-language efficacy claim"]},
    }
    frames = {}
    for split, families in FAMILIES.items():
        for family in families:
            event, *texts = family
            for index in range(4):
                frames[f"authored-{event}-state-{index}"] = {"event": event, "state_index": index,
                    "time": "past" if index >= 2 else "present", "polarity": "negative" if index in (1, 3) else "positive",
                    "context": "same synthetic event; only declared time and polarity change"}
    files["semantic_frames.draft.json"] = frames
    for name, value in files.items():
        (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return files["data_statement.json"]


# Fresh synthetic event families for a source-attention model iteration.
# Splits are fixed at 20/6/6 families before any v4.2 training run.
FAMILIES_V42 = {
    "train": [
        ("squeeze", "Thuy", "squeeze", "squeezes", "squeezed", "a lemon", "Thủy", "vắt", "một quả chanh"),
        ("peel", "Bao Chau", "peel", "peels", "peeled", "an orange", "Bảo Châu", "gọt vỏ", "một quả cam"),
        ("grill", "Quoc", "grill", "grills", "grilled", "a fish", "Quốc", "nướng", "một con cá"),
        ("slice", "Ha My", "slice", "slices", "sliced", "bread", "Hà My", "cắt lát", "bánh mì"),
        ("mix", "Tung", "mix", "mixes", "mixed", "paint", "Tùng", "pha", "sơn"),
        ("hang_coat", "Ngoc", "hang", "hangs", "hung", "a coat", "Ngọc", "treo", "một chiếc áo khoác"),
        ("lock_gate", "Viet", "lock", "locks", "locked", "a gate", "Việt", "khóa", "một cánh cổng"),
        ("unlock_gate", "Phuc An", "unlock", "unlocks", "unlocked", "a gate", "Phúc An", "mở khóa", "một cánh cổng"),
        ("pack_lunch", "Mai Anh", "pack", "packs", "packed", "a lunch", "Mai Anh", "chuẩn bị", "một phần ăn trưa"),
        ("unpack_box", "Gia Bao", "unpack", "unpacks", "unpacked", "a box", "Gia Bảo", "mở", "một chiếc hộp"),
        ("climb_ladder", "Ngan", "climb", "climbs", "climbed", "a ladder", "Ngân", "leo lên", "một chiếc thang"),
        ("push_cart", "Kiet", "push", "pushes", "pushed", "a cart", "Kiệt", "đẩy", "một chiếc xe đẩy"),
        ("pull_wagon", "Thao Vy", "pull", "pulls", "pulled", "a wagon", "Thảo Vy", "kéo", "một chiếc xe kéo"),
        ("repair_clock", "Dat", "repair", "repairs", "repaired", "a clock", "Đạt", "sửa", "một chiếc đồng hồ"),
        ("deliver_package", "Quynh Anh", "deliver", "delivers", "delivered", "a package", "Quỳnh Anh", "giao", "một bưu kiện"),
        ("wipe_mirror", "Trinh", "wipe", "wipes", "wiped", "a mirror", "Trinh", "lau", "một chiếc gương"),
        ("fill_bottle", "Duc", "fill", "fills", "filled", "a bottle", "Đức", "rót đầy", "một chai nước"),
        ("empty_basket", "Khanh Linh", "empty", "empties", "emptied", "a basket", "Khánh Linh", "đổ hết", "một chiếc giỏ"),
        ("wrap_gift", "Minh Chau", "wrap", "wraps", "wrapped", "a gift", "Minh Châu", "gói", "một món quà"),
        ("untie_knot", "Hanh", "untie", "unties", "untied", "a knot", "Hạnh", "tháo", "một nút thắt"),
    ],
    "validation": [
        ("cut_cloth", "Thu Nhi", "cut", "cuts", "cut", "cloth", "Thu Nhi", "cắt", "vải"),
        ("grind_coffee", "Thanh", "grind", "grinds", "ground", "coffee", "Thanh", "xay", "cà phê"),
        ("light_candle", "Quang Minh", "light", "lights", "lit", "a candle", "Quang Minh", "thắp", "một ngọn nến"),
        ("extinguish_candle", "Diem", "extinguish", "extinguishes", "extinguished", "a candle", "Diễm", "thổi tắt", "một ngọn nến"),
        ("raise_flag", "Bao Ngoc", "raise", "raises", "raised", "a flag", "Bảo Ngọc", "kéo lên", "một lá cờ"),
        ("lower_flag", "Anh Khoa", "lower", "lowers", "lowered", "a flag", "Anh Khoa", "hạ xuống", "một lá cờ"),
    ],
    "test": [
        ("assemble_shelf", "Manh", "assemble", "assembles", "assembled", "a shelf", "Mạnh", "lắp ráp", "một chiếc kệ"),
        ("braid_hair", "Yen", "braid", "braids", "braided", "hair", "Yến", "tết", "tóc"),
        ("drain_pasta", "Hieu Minh", "drain", "drains", "drained", "the pasta", "Hiếu Minh", "để ráo", "mì ống"),
        ("fasten_belt", "Thien", "fasten", "fastens", "fastened", "a belt", "Thiện", "thắt", "một chiếc thắt lưng"),
        ("sharpen_pencil", "Ly", "sharpen", "sharpens", "sharpened", "a pencil", "Ly", "gọt", "một cây bút chì"),
        ("tie_ribbon", "Hoai", "tie", "ties", "tied", "a ribbon", "Hoài", "buộc", "một dải ruy băng"),
    ],
}

# v4.3 is a fresh compositional probe. Every agent, verb lemma and object phrase
# occurs in training, while the event-frame triples assigned to validation and
# release holdout are new combinations. This directly tests recombination of
# known lexical material instead of holding out every word with each event.
_V43_AGENTS = (
    ("Lan", "Lan"), ("Nam", "Nam"), ("Mai", "Mai"), ("Minh", "Minh"),
    ("Hoa", "Hoa"), ("An", "An"), ("Binh", "Bình"), ("Linh", "Linh"),
)
_V43_VERBS = (
    ("read", "reads", "read", "đọc"), ("wash", "washes", "washed", "rửa"),
    ("open", "opens", "opened", "mở"), ("draw", "draws", "drew", "vẽ"),
    ("carry", "carries", "carried", "mang"), ("cook", "cooks", "cooked", "nấu"),
    ("write", "writes", "wrote", "viết"), ("buy", "buys", "bought", "mua"),
)
_V43_PATIENTS = (
    ("a book", "một quyển sách"), ("a cup", "một cái cốc"),
    ("the door", "cánh cửa"), ("a flower", "một bông hoa"),
    ("a bag", "một cái túi"), ("rice", "cơm"),
    ("a letter", "một lá thư"), ("bread", "bánh mì"),
)


def _compose_v43_families():
    partitions = {"train": [], "validation": [], "test": []}
    for b in range(4):
        for a in range(8):
            if b < 2 or (b == 2 and a < 4):
                split = "train"
            elif (b == 2 and a < 8) or (b == 3 and a < 2):
                split = "validation"
            else:
                split = "test"
            verb_en, present, past, verb_vi = _V43_VERBS[(a + b) % len(_V43_VERBS)]
            patient_en, patient_vi = _V43_PATIENTS[(3 * a + b) % len(_V43_PATIENTS)]
            agent_en, agent_vi = _V43_AGENTS[a]
            partitions[split].append((f"compose_{a}_{b}", agent_en, verb_en, present, past,
                                      patient_en, agent_vi, verb_vi, patient_vi))
    return partitions


FAMILIES_V43 = _compose_v43_families()

# v4.4 increases compositional coverage while holding optimizer updates constant.
# All lexical factors are shared, broad-compatibility transitive actions and
# objects reduce semantic oddities in the recombined event frames.
_V44_AGENTS = _V43_AGENTS
_V44_VERBS = (
    ("move", "moves", "moved", "di chuyển"), ("carry", "carries", "carried", "mang"),
    ("find", "finds", "found", "tìm thấy"), ("bring", "brings", "brought", "mang đến"),
    ("photograph", "photographs", "photographed", "chụp ảnh"),
    ("wrap", "wraps", "wrapped", "gói"), ("buy", "buys", "bought", "mua"),
    ("pack", "packs", "packed", "đóng gói"),
)
_V44_PATIENTS = (
    ("a package", "một bưu kiện"), ("a box", "một chiếc hộp"),
    ("a book", "một quyển sách"), ("a bag", "một cái túi"),
    ("a gift", "một món quà"), ("a letter", "một lá thư"),
    ("a basket", "một cái giỏ"), ("a suitcase", "một chiếc va li"),
)
_V49_AGENTS = (("Kieu", "Kiều"), ("Thien", "Thiện"), ("Oanh", "Oanh"))
_V410_AGENTS = (("Nhu", "Như"), ("Tuyen", "Tuyền"), ("Loc", "Lộc"))
_V411_AGENTS = (("Kha My", "Khả My"), ("Tuan Kiet", "Tuấn Kiệt"), ("An Vy", "An Vy"))
_V412_AGENTS = (("My Dung", "Mỹ Dung"), ("Quoc Bao", "Quốc Bảo"), ("Thao Nhi", "Thảo Nhi"))
_V413_AGENTS = (("Bao Tram", "Bảo Trâm"), ("Huu Phuoc", "Hữu Phước"), ("Gia Han", "Gia Hân"))
_V414_AGENTS = (("Ngoc Mai", "Ngọc Mai"), ("Tuan Anh", "Tuấn Anh"), ("Khanh Vy", "Khánh Vy"))
_V415_AGENTS = (("Bao Nguyen", "Bảo Nguyễn"), ("Mai Pham", "Mai Phạm"), ("Duc Tran", "Đức Trần"))
_V416_AGENTS = (("Quoc Minh", "Quốc Minh"), ("Linh Chi", "Linh Chi"), ("Thanh Binh", "Thanh Bình"))
_V417_AGENTS = (("Hai Yen", "Hải Yến"), ("Tuan Kiet", "Tuấn Kiệt"), ("Nhu Quynh", "Như Quỳnh"))
_V418_AGENTS = (("Minh Tam", "Minh Tâm"), ("Bao Chau", "Bảo Châu"), ("Le Anh", "Lê Anh"))
_V419_AGENTS = (("Thanh Ha", "Thanh Hà"), ("Dinh Bao", "Đình Bảo"), ("Hoang Linh", "Hoàng Linh"))
_V420_AGENTS = (("Tuyet Mai", "Tuyết Mai"), ("Nhat Khang", "Nhật Khang"), ("Viet Anh", "Việt Anh"))
_V421_AGENTS = (("Hoai An", "Hoài An"), ("Bao Long", "Bảo Long"), ("Minh Quan", "Minh Quân"))
_V422_AGENTS = (("Gia Huy", "Gia Huy"), ("Thao My", "Thảo My"), ("Quoc Bao", "Quốc Bảo"))
_V423_AGENTS = (("Khanh Linh", "Khánh Linh"), ("Duc Minh", "Đức Minh"), ("Ngoc Mai", "Ngọc Mai"))
_V424_AGENTS = (("Thanh Truc", "Thanh Trúc"), ("Hoang Nam", "Hoàng Nam"), ("Mai Phuong", "Mai Phương"))
_V425_AGENTS = (("Bich Ngoc", "Bích Ngọc"), ("Phan Minh", "Phan Minh"), ("Thu Trang", "Thu Trang"))
_V426_AGENTS = (("Bao Chau", "Bảo Châu"), ("Duc Anh", "Đức Anh"), ("Gia Han", "Gia Hân"))
_V427_AGENTS = (("Tuan Phuc", "Tuấn Phúc"), ("Ngoc Bich", "Ngọc Bích"), ("Hoang Duy", "Hoàng Duy"))
_V428_AGENTS = (("Bao Ngan", "Bảo Ngân"), ("Quoc Bao", "Quốc Bảo"), ("Thao Vy", "Thảo Vy"))
_V429_AGENTS = (("Duc Anh", "Đức Anh"), ("Ngoc Han", "Ngọc Hân"), ("Minh Kiet", "Minh Kiệt"))
_V430_AGENTS = (("Thu Ha", "Thu Hà"), ("Tuan Huy", "Tuấn Huy"), ("Lan Anh", "Lan Anh"))


def _compose_v44_families():
    import random

    covered = []
    for block in range(8):
        for agent in range(8):
            covered.append((agent, (agent + block) % 8, (3 * agent + block) % 8))
    all_combinations = [(agent, verb, patient)
                        for agent in range(8) for verb in range(8) for patient in range(8)]
    selected = set(covered)
    for triple in all_combinations:
        if len(covered) == 80:
            break
        if triple not in selected:
            covered.append(triple)
            selected.add(triple)
    remaining = [triple for triple in all_combinations if triple not in selected]
    random.Random(20261002).shuffle(remaining)
    validation, test = remaining[:12], remaining[12:24]
    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", covered), ("validation", validation), ("test", test)):
        for index, (agent, verb, patient) in enumerate(combinations):
            agent_en, agent_vi = _V44_AGENTS[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            result[split].append((f"compose_{agent}_{verb}_{patient}", agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V44 = _compose_v44_families()

# v4.5 is disjoint from every v4.4 frame combination, including its sealed
# release holdout. The split is sampled from the remaining compositional space
# while train is guaranteed to cover every agent, verb and patient.
def _compose_v45_families():
    import random

    previously_used = {tuple(map(int, row[0].removeprefix("compose_").split("_")))
                       for split in FAMILIES_V44.values() for row in split}
    remaining = [(agent, verb, patient)
                 for agent in range(8) for verb in range(8) for patient in range(8)
                 if (agent, verb, patient) not in previously_used]
    random.Random(20261003).shuffle(remaining)
    train = []
    agents, verbs, patients = set(), set(), set()
    while remaining and (len(agents) < 8 or len(verbs) < 8 or len(patients) < 8):
        triple = remaining.pop()
        train.append(triple)
        agents.add(triple[0])
        verbs.add(triple[1])
        patients.add(triple[2])
    train.extend(remaining[:80 - len(train)])
    selected = set(train)
    held_out = [triple for triple in remaining[80 - len(train):] if triple not in selected]
    validation, test = held_out[:12], held_out[12:24]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = _V44_AGENTS[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose45_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V45 = _compose_v45_families()


_V46_PROGRESSIVE = {
    "move": "moving", "carry": "carrying", "find": "finding", "search for": "searching for", "bring": "bringing",
    "photograph": "photographing", "wrap": "wrapping", "buy": "buying", "pack": "packing",
}


def _compose_v46_families():
    import random

    previously_used = set()
    for family_map, prefix in ((FAMILIES_V44, "compose_"), (FAMILIES_V45, "compose45_")):
        previously_used.update(tuple(map(int, row[0].removeprefix(prefix).split("_")))
                               for split in family_map.values() for row in split)
    remaining = [(agent, verb, patient)
                 for agent in range(8) for verb in range(8) for patient in range(8)
                 if (agent, verb, patient) not in previously_used]
    random.Random(20261004).shuffle(remaining)
    train = []
    agents, verbs, patients = set(), set(), set()
    while remaining and (len(agents) < 8 or len(verbs) < 8 or len(patients) < 8):
        triple = remaining.pop()
        train.append(triple)
        agents.add(triple[0])
        verbs.add(triple[1])
        patients.add(triple[2])
    train.extend(remaining[:80 - len(train)])
    selected = set(train)
    held_out = [triple for triple in remaining[80 - len(train):] if triple not in selected]
    validation, test = held_out[:12], held_out[12:24]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = _V44_AGENTS[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            result[split].append((f"compose46_{agent}_{verb}_{patient}", agent_en, base,
                                  present, past, _V44_PATIENTS[patient][0], agent_vi,
                                  verb_vi, _V44_PATIENTS[patient][1]))
    return result


FAMILIES_V46 = _compose_v46_families()


def _compose_v47_families():
    """Build fresh triples whose held-out pairwise factors are all trained."""
    import random

    previously_used = set()
    for family_map, prefix in ((FAMILIES_V44, "compose_"),
                               (FAMILIES_V45, "compose45_"),
                               (FAMILIES_V46, "compose46_")):
        previously_used.update(tuple(map(int, row[0].removeprefix(prefix).split("_")))
                               for split in family_map.values() for row in split)
    remaining = [(agent, verb, patient)
                 for agent in range(8) for verb in range(8) for patient in range(8)
                 if (agent, verb, patient) not in previously_used]
    if len(remaining) != 200:
        raise ValueError("v4.7 requires the expected fresh compositional pool")

    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 120:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.7 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261005).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]
    if len(remaining) != 80:
        raise ValueError("v4.7 requires 40 validation and 40 release-holdout triples")

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = _V44_AGENTS[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            result[split].append((f"compose47_{agent}_{verb}_{patient}", agent_en, base,
                                  present, past, patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V47 = _compose_v47_families()


def _compose_v48_families():
    """Create a fresh agent-factor generalization split with covered pairs."""
    import random

    agents = _V44_AGENTS + (("Khanh", "Khánh"), ("Quynh", "Quỳnh"), ("Hai", "Hải"))
    previously_used = set()
    for family_map, prefix in ((FAMILIES_V44, "compose_"),
                               (FAMILIES_V45, "compose45_"),
                               (FAMILIES_V46, "compose46_"),
                               (FAMILIES_V47, "compose47_")):
        previously_used.update(tuple(map(int, row[0].removeprefix(prefix).split("_")))
                               for split in family_map.values() for row in split)
    remaining = [(agent, verb, patient)
                 for agent in range(len(agents)) for verb in range(len(_V44_VERBS))
                 for patient in range(len(_V44_PATIENTS))
                 if (agent, verb, patient) not in previously_used]
    if len(remaining) != 192:
        raise ValueError("v4.8 requires the expected unseen agent-factor pool")

    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.8 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261006).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]
    if len(remaining) != 80:
        raise ValueError("v4.8 requires 40 validation and 40 release-holdout triples")

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose48_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V48 = _compose_v48_families()


def _compose_v49_families():
    """Author a fresh agent-composition pool and split for v4.9."""
    import random

    agents = _V44_AGENTS + _V49_AGENTS
    # The new agents create a fresh 3 x 8 x 8 combination pool. The training
    # partition covers every factor pair that appears in validation or test.
    remaining = [(agent, verb, patient)
                 for agent in range(8, 11) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.9 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261008).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose49_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V49 = _compose_v49_families()


def _compose_v410_families():
    """Author another fresh agent-composition pool with a new holdout."""
    import random

    agents = _V44_AGENTS + _V49_AGENTS + _V410_AGENTS
    remaining = [(agent, verb, patient)
                 for agent in range(11, 14) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.10 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261009).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose410_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V410 = _compose_v410_families()


def _compose_v411_families():
    """Author a fresh agent-composition pool and unopened holdout for v4.11."""
    import random

    agents = _V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS
    remaining = [(agent, verb, patient)
                 for agent in range(14, 17) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.11 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261010).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose411_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V411 = _compose_v411_families()


def _compose_v412_families():
    """Author a fresh factor pool for the copy-loss ablation and new holdout."""
    import random

    agents = _V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
    remaining = [(agent, verb, patient)
                 for agent in range(17, 20) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.12 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261011).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose412_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V412 = _compose_v412_families()


def _compose_v413_families():
    """Author fresh agent combinations for a copy-loss dose-response pilot."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS
              + _V412_AGENTS + _V413_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(20, 23) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.13 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261012).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose413_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V413 = _compose_v413_families()


def _compose_v414_families():
    """Use a fresh agent pool and split for the balanced-context pilot."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS
              + _V412_AGENTS + _V413_AGENTS + _V414_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(23, 26) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.14 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261013).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose414_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V414 = _compose_v414_families()


def _compose_v415_families():
    """Use a fresh agent pool while preserving v4.14's balanced surface design."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS
              + _V412_AGENTS + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(26, 29) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.15 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261015).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose415_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V415 = _compose_v415_families()


def _compose_v416_families():
    """Use fresh agent factors for a lower latent-objective-dose study."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS
              + _V412_AGENTS + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(29, 32) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.16 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261017).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose416_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V416 = _compose_v416_families()


def _compose_v417_families():
    """Use fresh agent factors for a preregistered row-exposure balance study."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS
              + _V412_AGENTS + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS
              + _V416_AGENTS + _V417_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(32, 35) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.17 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261018).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]
    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose417_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V417 = _compose_v417_families()


def _compose_v418_families():
    """Use fresh agent factors and a matched path order for the 2x2 objective study."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS
              + _V412_AGENTS + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS
              + _V416_AGENTS + _V417_AGENTS + _V418_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(35, 38) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.18 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261019).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose418_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V418 = _compose_v418_families()


def _compose_v419_families():
    """Use fresh agent factors and the v4.18 matched path-order design."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
              + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS + _V417_AGENTS
              + _V418_AGENTS + _V419_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(38, 41) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.19 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261020).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose419_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V419 = _compose_v419_families()


def _compose_v420_families():
    """Use a fresh agent pool for the preregistered decoder comparison."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
              + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS + _V417_AGENTS
              + _V418_AGENTS + _V419_AGENTS + _V420_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(41, 44) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.20 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261021).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose420_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V420 = _compose_v420_families()


def _compose_v421_families():
    """Make a fresh, pairwise-covered split for the copy × decoder study."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
              + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS + _V417_AGENTS
              + _V418_AGENTS + _V419_AGENTS + _V420_AGENTS + _V421_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(44, 47) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.21 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261022).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose421_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V421 = _compose_v421_families()


def _compose_v422_families():
    """Use fresh agent factors and a new fixed split for the checker-repair rerun."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
              + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS + _V417_AGENTS
              + _V418_AGENTS + _V419_AGENTS + _V420_AGENTS + _V421_AGENTS + _V422_AGENTS)
    remaining = [(agent, verb, patient)
                 for agent in range(47, 50) for verb in range(8) for patient in range(8)]
    train = []
    pair_sets = (set(), set(), set())
    while len(train) < 112:
        best = max(
            remaining,
            key=lambda triple: (
                sum(pair not in known for pair, known in zip(
                    ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])),
                    pair_sets)),
                tuple(-value for value in triple)),
        )
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.22 held-out triples must reuse only training-seen factor pairs")
    random.Random(20261023).shuffle(remaining)
    validation, test = remaining[:40], remaining[40:80]

    result = {"train": [], "validation": [], "test": []}
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = _V44_VERBS[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose422_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V422 = _compose_v422_families()


def _compose_v423_families():
    """Balance fresh factor marginals while retaining pairwise-covered holdouts."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
              + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS + _V417_AGENTS
              + _V418_AGENTS + _V419_AGENTS + _V420_AGENTS + _V421_AGENTS + _V422_AGENTS
              + _V423_AGENTS)
    remaining = {(agent, verb, patient)
                 for agent in range(50, 53) for verb in range(8) for patient in range(8)}
    train = []
    pair_sets = (set(), set(), set())
    marginals = ({}, {}, {})
    rng = random.Random(20261024)
    while len(train) < 112:
        candidates = list(remaining)
        rng.shuffle(candidates)

        def score(triple):
            pairs = ((triple[0], triple[1]), (triple[0], triple[2]),
                     (triple[1], triple[2]))
            novelty = sum(pair not in known for pair, known in zip(pairs, pair_sets))
            balance_cost = sum((marginals[index].get(value, 0) + 1) ** 2
                               - marginals[index].get(value, 0) ** 2
                               for index, value in enumerate(triple))
            return novelty, -balance_cost

        best = max(candidates, key=score)
        train.append(best)
        remaining.remove(best)
        for pair, known in zip(((best[0], best[1]), (best[0], best[2]),
                                (best[1], best[2])), pair_sets):
            known.add(pair)
        for index, value in enumerate(best):
            marginals[index][value] = marginals[index].get(value, 0) + 1
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])), pair_sets))
           for triple in remaining):
        raise ValueError("v4.24 held-out triples must reuse only training-seen factor pairs")

    def take_balanced(count):
        chosen, counts = [], ({}, {}, {})
        for _ in range(count):
            candidates = list(remaining)
            rng.shuffle(candidates)
            def cost(triple):
                return sum((counts[index].get(value, 0) + 1) ** 2
                           - counts[index].get(value, 0) ** 2
                           for index, value in enumerate(triple))
            best = min(candidates, key=cost)
            chosen.append(best)
            remaining.remove(best)
            for index, value in enumerate(best):
                counts[index][value] = counts[index].get(value, 0) + 1
        return chosen

    validation, test = take_balanced(40), take_balanced(40)
    result = {"train": [], "validation": [], "test": []}
    verbs = _V44_VERBS[:2] + (("search for", "searches for", "searched for", "tìm kiếm"),) + _V44_VERBS[3:]
    for split, combinations in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in combinations:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = verbs[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose423_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V423 = _compose_v423_families()


def _compose_v424_families():
    """Allocate fresh balanced factor combinations for the capacity study."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
              + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS + _V417_AGENTS
              + _V418_AGENTS + _V419_AGENTS + _V420_AGENTS + _V421_AGENTS + _V422_AGENTS
              + _V423_AGENTS + _V424_AGENTS)
    remaining = {(agent, verb, patient)
                 for agent in range(53, 56) for verb in range(8) for patient in range(8)}
    train = []
    pair_sets = (set(), set(), set())
    marginals = ({}, {}, {})
    rng = random.Random(20261027)
    while len(train) < 112:
        candidates = list(remaining)
        rng.shuffle(candidates)

        def score(triple):
            pairs = ((triple[0], triple[1]), (triple[0], triple[2]),
                     (triple[1], triple[2]))
            novelty = sum(pair not in known for pair, known in zip(pairs, pair_sets))
            imbalance = sum((marginals[i].get(value, 0) + 1) ** 2
                            - marginals[i].get(value, 0) ** 2
                            for i, value in enumerate(triple))
            return novelty, -imbalance

        chosen = max(candidates, key=score)
        train.append(chosen)
        remaining.remove(chosen)
        for pair, known in zip(((chosen[0], chosen[1]), (chosen[0], chosen[2]),
                                (chosen[1], chosen[2])), pair_sets):
            known.add(pair)
        for i, value in enumerate(chosen):
            marginals[i][value] = marginals[i].get(value, 0) + 1
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]),
             (triple[1], triple[2])), pair_sets)) for triple in remaining):
        raise ValueError("v4.24 held-out triples must reuse only training-seen factor pairs")

    def take_balanced(count):
        selected, counts = [], ({}, {}, {})
        for _ in range(count):
            candidates = list(remaining)
            rng.shuffle(candidates)

            def imbalance(triple):
                return sum((counts[i].get(value, 0) + 1) ** 2 - counts[i].get(value, 0) ** 2
                            for i, value in enumerate(triple))

            chosen = min(candidates, key=imbalance)
            selected.append(chosen)
            remaining.remove(chosen)
            for i, value in enumerate(chosen):
                counts[i][value] = counts[i].get(value, 0) + 1
        return selected

    validation, test = take_balanced(40), take_balanced(40)
    result = {"train": [], "validation": [], "test": []}
    verbs = _V44_VERBS[:2] + (("search for", "searches for", "searched for", "tìm kiếm"),) + _V44_VERBS[3:]
    for split, triples in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in triples:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = verbs[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose424_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V424 = _compose_v424_families()


def _compose_v425_families():
    """Allocate fresh held-out triples for the self-feeding diagnostic."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
              + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS + _V417_AGENTS
              + _V418_AGENTS + _V419_AGENTS + _V420_AGENTS + _V421_AGENTS + _V422_AGENTS
              + _V423_AGENTS + _V424_AGENTS + _V425_AGENTS)
    remaining = {(agent, verb, patient)
                 for agent in range(56, 59) for verb in range(8) for patient in range(8)}
    train = []
    pair_sets = (set(), set(), set())
    marginals = ({}, {}, {})
    rng = random.Random(20261028)
    while len(train) < 112:
        candidates = sorted(remaining)
        rng.shuffle(candidates)

        def score(triple):
            pairs = ((triple[0], triple[1]), (triple[0], triple[2]),
                     (triple[1], triple[2]))
            novelty = sum(pair not in known for pair, known in zip(pairs, pair_sets))
            imbalance = sum((marginals[i].get(value, 0) + 1) ** 2
                            - marginals[i].get(value, 0) ** 2
                            for i, value in enumerate(triple))
            return novelty, -imbalance

        chosen = max(candidates, key=score)
        train.append(chosen)
        remaining.remove(chosen)
        for pair, known in zip(((chosen[0], chosen[1]), (chosen[0], chosen[2]),
                                (chosen[1], chosen[2])), pair_sets):
            known.add(pair)
        for i, value in enumerate(chosen):
            marginals[i][value] = marginals[i].get(value, 0) + 1
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]),
             (triple[1], triple[2])), pair_sets)) for triple in remaining):
        raise ValueError("v4.25 held-out triples must reuse only training-seen factor pairs")

    def take_balanced(count):
        selected, counts = [], ({}, {}, {})
        for _ in range(count):
            candidates = sorted(remaining)
            rng.shuffle(candidates)

            def imbalance(triple):
                return sum((counts[i].get(value, 0) + 1) ** 2 - counts[i].get(value, 0) ** 2
                           for i, value in enumerate(triple))

            chosen = min(candidates, key=imbalance)
            selected.append(chosen)
            remaining.remove(chosen)
            for i, value in enumerate(chosen):
                counts[i][value] = counts[i].get(value, 0) + 1
        return selected

    validation, test = take_balanced(40), take_balanced(40)
    result = {"train": [], "validation": [], "test": []}
    verbs = _V44_VERBS[:2] + (("search for", "searches for", "searched for", "tìm kiếm"),) + _V44_VERBS[3:]
    for split, triples in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in triples:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = verbs[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose425_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V425 = _compose_v425_families()


def _compose_v426_families():
    """Allocate a fresh agent block and split for the low-dose copy study."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
              + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS + _V417_AGENTS
              + _V418_AGENTS + _V419_AGENTS + _V420_AGENTS + _V421_AGENTS + _V422_AGENTS
              + _V423_AGENTS + _V424_AGENTS + _V425_AGENTS + _V426_AGENTS)
    remaining = {(agent, verb, patient)
                 for agent in range(59, 62) for verb in range(8) for patient in range(8)}
    train = []
    pair_sets = (set(), set(), set())
    marginals = ({}, {}, {})
    rng = random.Random(20261029)
    while len(train) < 112:
        candidates = sorted(remaining)
        rng.shuffle(candidates)

        def score(triple):
            pairs = ((triple[0], triple[1]), (triple[0], triple[2]),
                     (triple[1], triple[2]))
            novelty = sum(pair not in known for pair, known in zip(pairs, pair_sets))
            imbalance = sum((marginals[i].get(value, 0) + 1) ** 2
                            - marginals[i].get(value, 0) ** 2
                            for i, value in enumerate(triple))
            return novelty, -imbalance

        chosen = max(candidates, key=score)
        train.append(chosen)
        remaining.remove(chosen)
        for pair, known in zip(((chosen[0], chosen[1]), (chosen[0], chosen[2]),
                                (chosen[1], chosen[2])), pair_sets):
            known.add(pair)
        for i, value in enumerate(chosen):
            marginals[i][value] = marginals[i].get(value, 0) + 1
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]),
             (triple[1], triple[2])), pair_sets)) for triple in remaining):
        raise ValueError("v4.26 held-out triples must reuse only training-seen factor pairs")

    def take_balanced(count):
        selected, counts = [], ({}, {}, {})
        for _ in range(count):
            candidates = sorted(remaining)
            rng.shuffle(candidates)

            def imbalance(triple):
                return sum((counts[i].get(value, 0) + 1) ** 2 - counts[i].get(value, 0) ** 2
                           for i, value in enumerate(triple))

            chosen = min(candidates, key=imbalance)
            selected.append(chosen)
            remaining.remove(chosen)
            for i, value in enumerate(chosen):
                counts[i][value] = counts[i].get(value, 0) + 1
        return selected

    validation, test = take_balanced(40), take_balanced(40)
    result = {"train": [], "validation": [], "test": []}
    verbs = _V44_VERBS[:2] + (("search for", "searches for", "searched for", "tìm kiếm"),) + _V44_VERBS[3:]
    for split, triples in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in triples:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = verbs[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"compose426_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V426 = _compose_v426_families()


def _compose_v4x_families(agent_start, split_seed, event_prefix):
    """Allocate a fresh balanced factor block for a versioned diagnostic split."""
    import random

    agents = (_V44_AGENTS + _V49_AGENTS + _V410_AGENTS + _V411_AGENTS + _V412_AGENTS
              + _V413_AGENTS + _V414_AGENTS + _V415_AGENTS + _V416_AGENTS + _V417_AGENTS
              + _V418_AGENTS + _V419_AGENTS + _V420_AGENTS + _V421_AGENTS + _V422_AGENTS
              + _V423_AGENTS + _V424_AGENTS + _V425_AGENTS + _V426_AGENTS + _V427_AGENTS + _V428_AGENTS
              + _V429_AGENTS + _V430_AGENTS)
    remaining = {(agent, verb, patient)
                 for agent in range(agent_start, agent_start + 3) for verb in range(8) for patient in range(8)}
    train = []
    pair_sets = (set(), set(), set())
    marginals = ({}, {}, {})
    rng = random.Random(split_seed)
    while len(train) < 112:
        candidates = sorted(remaining)
        rng.shuffle(candidates)

        def score(triple):
            pairs = ((triple[0], triple[1]), (triple[0], triple[2]),
                     (triple[1], triple[2]))
            novelty = sum(pair not in known for pair, known in zip(pairs, pair_sets))
            imbalance = sum((marginals[i].get(value, 0) + 1) ** 2
                            - marginals[i].get(value, 0) ** 2
                            for i, value in enumerate(triple))
            return novelty, -imbalance

        chosen = max(candidates, key=score)
        train.append(chosen)
        remaining.remove(chosen)
        for pair, known in zip(((chosen[0], chosen[1]), (chosen[0], chosen[2]),
                                (chosen[1], chosen[2])), pair_sets):
            known.add(pair)
        for i, value in enumerate(chosen):
            marginals[i][value] = marginals[i].get(value, 0) + 1
    if any(not all(pair in known for pair, known in zip(
            ((triple[0], triple[1]), (triple[0], triple[2]),
             (triple[1], triple[2])), pair_sets)) for triple in remaining):
        raise ValueError("v4.27 held-out triples must reuse only training-seen factor pairs")

    def take_balanced(count):
        selected, counts = [], ({}, {}, {})
        for _ in range(count):
            candidates = sorted(remaining)
            rng.shuffle(candidates)

            def imbalance(triple):
                return sum((counts[i].get(value, 0) + 1) ** 2 - counts[i].get(value, 0) ** 2
                           for i, value in enumerate(triple))

            chosen = min(candidates, key=imbalance)
            selected.append(chosen)
            remaining.remove(chosen)
            for i, value in enumerate(chosen):
                counts[i][value] = counts[i].get(value, 0) + 1
        return selected

    validation, test = take_balanced(40), take_balanced(40)
    result = {"train": [], "validation": [], "test": []}
    verbs = _V44_VERBS[:2] + (("search for", "searches for", "searched for", "tìm kiếm"),) + _V44_VERBS[3:]
    for split, triples in (("train", train), ("validation", validation), ("test", test)):
        for agent, verb, patient in triples:
            agent_en, agent_vi = agents[agent]
            base, present, past, verb_vi = verbs[verb]
            patient_en, patient_vi = _V44_PATIENTS[patient]
            event = f"{event_prefix}_{agent}_{verb}_{patient}"
            result[split].append((event, agent_en, base, present, past,
                                  patient_en, agent_vi, verb_vi, patient_vi))
    return result


FAMILIES_V427 = _compose_v4x_families(62, 20261030, "compose427")
FAMILIES_V428 = _compose_v4x_families(65, 20261031, "compose428")
FAMILIES_V429 = _compose_v4x_families(68, 20261032, "compose429")
FAMILIES_V430 = _compose_v4x_families(71, 20261033, "compose430")


def author_seed_v4(output_dir, *, version="v4"):
    """Create a new AI-authored v4-family draft with explicit bilingual frames."""
    output = Path(output_dir)
    if output.exists():
        raise FileExistsError("seed output already exists; preserve prior evidence and use a new version")
    rows, edge_pairs, path_pairs, groups, frames = [], [], [], {}, {}
    single_edges = [(0, 2, "TIME", "PAST"), (2, 0, "TIME", "NOW"),
                    (0, 1, "POLARITY", "NEGATIVE"), (1, 0, "POLARITY", "POSITIVE"),
                    (2, 3, "POLARITY", "NEGATIVE"), (3, 2, "POLARITY", "POSITIVE"),
                    (1, 3, "TIME", "PAST"), (3, 1, "TIME", "NOW")]
    actions = [{"kind": kind, "value": value} for kind, value in
               (("TIME", "NOW"), ("TIME", "PAST"), ("POLARITY", "POSITIVE"), ("POLARITY", "NEGATIVE"))]
    family_map = (FAMILIES_V42 if version == "v4.2" else
                  FAMILIES_V43 if version == "v4.3" else
                  FAMILIES_V44 if version == "v4.4" else
                  FAMILIES_V45 if version == "v4.5" else
                  FAMILIES_V414 if version == "v4.14" else
                  FAMILIES_V430 if version == "v4.30" else
                  FAMILIES_V429 if version == "v4.29" else
                  FAMILIES_V428 if version in ("v4.28", "v4.29", "v4.30") else
                  FAMILIES_V427 if version == "v4.27" else
                  FAMILIES_V426 if version == "v4.26" else
                  FAMILIES_V425 if version == "v4.25" else
                  FAMILIES_V424 if version == "v4.24" else
                  FAMILIES_V423 if version == "v4.23" else
                  FAMILIES_V422 if version == "v4.22" else
                  FAMILIES_V421 if version == "v4.21" else
                  FAMILIES_V420 if version == "v4.20" else
                  FAMILIES_V419 if version == "v4.19" else
                  FAMILIES_V418 if version == "v4.18" else
                  FAMILIES_V417 if version == "v4.17" else
                  FAMILIES_V416 if version == "v4.16" else
                  FAMILIES_V415 if version == "v4.15" else
                  FAMILIES_V413 if version == "v4.13" else
                  FAMILIES_V412 if version == "v4.12" else
                  FAMILIES_V411 if version == "v4.11" else
                  FAMILIES_V410 if version == "v4.10" else
                  FAMILIES_V49 if version == "v4.9" else
                  FAMILIES_V48 if version == "v4.8" else
                  FAMILIES_V47 if version == "v4.7" else
                  FAMILIES_V46 if version == "v4.6" else FAMILIES_V4)
    for split, families in family_map.items():
        for definition in families:
            event, en_agent, en_base, en_present, en_past, en_patient, vi_agent, vi_verb, vi_patient = definition
            group = f"{version}-{event}"
            groups[group] = split
            for index in range(4):
                past, negative = index >= 2, index in (1, 3)
                time = "past" if past else "present"
                polarity = "negative" if negative else "positive"
                frame = {"event": event, "time": time, "polarity": polarity,
                         "agent_en": en_agent, "agent_vi": vi_agent,
                         "predicate_en": en_base, "predicate_vi": vi_verb,
                         "predicate_en_present": en_present, "predicate_en_past": en_past,
                         "patient_en": en_patient, "patient_vi": vi_patient,
                         "context": "same event; requested action changes time or polarity only"}
                progressive_vi = (version in ("v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30")
                                  and (not negative or version != "v4.23"))
                frame["predicate_vi_present"] = (("đang " if progressive_vi else "")
                                                   + ("không " if negative else "") + vi_verb)
                if version in ("v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30"):
                    frame.update({"place_en": "in the workshop", "place_vi": "trong xưởng",
                                  "context": "same event in the same workshop; only time or polarity changes"})
                if version in ("v4.6", "v4.7", "v4.8", "v4.9", "v4.10", "v4.11", "v4.12", "v4.13", "v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30"):
                    frame["predicate_en_progressive"] = _V46_PROGRESSIVE[en_base]
                frames[f"{group}-state-{index}"] = frame
            path_edges = ([(0, 2, "TIME", "PAST"), (2, 3, "POLARITY", "NEGATIVE")]
                          if split == "test" and version == "v4.17" else
                          [(0, 1, "POLARITY", "NEGATIVE"), (1, 3, "TIME", "PAST")])
            for language in ("en", "vi"):
                for variant in range(4 if version in ("v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30") else 2):
                    state_forms_v4_6 = None
                    if version in ("v4.6", "v4.7", "v4.8", "v4.9", "v4.10", "v4.11", "v4.12", "v4.13", "v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30"):
                        progressive = _V46_PROGRESSIVE[en_base]
                        vi_now_verb = f"đang {vi_verb}" if version in ("v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30") else vi_verb
                        vi_now_negative = (f"đang không {vi_verb}" if version in ("v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30")
                                           else f"không {vi_verb}")
                        state_forms_v4_6 = {
                            "en": ((f"Right now, {en_agent} is {progressive} {en_patient}.",
                                    f"{en_agent} is {progressive} {en_patient} right now."),
                                   (f"Right now, {en_agent} is not {progressive} {en_patient}.",
                                    f"{en_agent} is not {progressive} {en_patient} right now.")),
                            "vi": ((f"Bây giờ, {vi_agent} {vi_verb} {vi_patient}.",
                                    f"{vi_agent} {vi_verb} {vi_patient} bây giờ."),
                                   (f"Bây giờ, {vi_agent} không {vi_verb} {vi_patient}.",
                                    f"{vi_agent} không {vi_verb} {vi_patient} bây giờ.")),
                        }
                        if version in ("v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30"):
                            state_forms_v4_6 = {
                                "en": ((f"In the workshop, {en_agent} is {progressive} {en_patient} right now.",
                                        f"Right now, {en_agent} is {progressive} {en_patient} in the workshop.",
                                        f"{en_agent} is {progressive} {en_patient} right now, in the workshop.",
                                        f"{en_agent} is {progressive} {en_patient} in the workshop right now."),
                                       (f"In the workshop, {en_agent} is not {progressive} {en_patient} right now.",
                                        f"Right now, {en_agent} is not {progressive} {en_patient} in the workshop.",
                                        f"{en_agent} is not {progressive} {en_patient} right now, in the workshop.",
                                        f"{en_agent} is not {progressive} {en_patient} in the workshop right now."),
                                       (f"In the workshop, {en_agent} {en_past} {en_patient} yesterday.",
                                        f"Yesterday, {en_agent} {en_past} {en_patient} in the workshop.",
                                        f"{en_agent} {en_past} {en_patient} yesterday, in the workshop.",
                                        f"{en_agent} {en_past} {en_patient} in the workshop yesterday."),
                                       (f"In the workshop, {en_agent} did not {en_base} {en_patient} yesterday.",
                                        f"Yesterday, {en_agent} did not {en_base} {en_patient} in the workshop.",
                                        f"{en_agent} did not {en_base} {en_patient} yesterday, in the workshop.",
                                        f"{en_agent} did not {en_base} {en_patient} in the workshop yesterday.")),
                                "vi": ((f"Trong xưởng, {vi_agent} {vi_now_verb} {vi_patient} bây giờ.",
                                        f"Bây giờ, {vi_agent} {vi_now_verb} {vi_patient} trong xưởng.",
                                        f"{vi_agent} {vi_now_verb} {vi_patient} bây giờ, trong xưởng.",
                                        f"{vi_agent} {vi_now_verb} {vi_patient} trong xưởng bây giờ."),
                                       (f"Trong xưởng, {vi_agent} {vi_now_negative} {vi_patient} bây giờ.",
                                        f"Bây giờ, {vi_agent} {vi_now_negative} {vi_patient} trong xưởng.",
                                        f"{vi_agent} {vi_now_negative} {vi_patient} bây giờ, trong xưởng.",
                                        f"{vi_agent} {vi_now_negative} {vi_patient} trong xưởng bây giờ."),
                                       (f"Trong xưởng, {vi_agent} đã {vi_verb} {vi_patient} hôm qua.",
                                        f"Hôm qua, {vi_agent} đã {vi_verb} {vi_patient} trong xưởng.",
                                        f"{vi_agent} đã {vi_verb} {vi_patient} hôm qua, trong xưởng.",
                                        f"{vi_agent} đã {vi_verb} {vi_patient} trong xưởng hôm qua."),
                                       (f"Trong xưởng, {vi_agent} không {vi_verb} {vi_patient} hôm qua.",
                                        f"Hôm qua, {vi_agent} không {vi_verb} {vi_patient} trong xưởng.",
                                        f"{vi_agent} không {vi_verb} {vi_patient} hôm qua, trong xưởng.",
                                        f"{vi_agent} không {vi_verb} {vi_patient} trong xưởng hôm qua."))}
                    if version in ("v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30"):
                        realized = [state_forms_v4_6[language][state_index][variant]
                                    for state_index in range(4)]
                    else:
                        realized = [state[language][variant] for state in
                                    [{"en": (f"Right now, {en_agent} {en_present} {en_patient}.", f"{en_agent} {en_present} {en_patient} right now."),
                                      "vi": (f"Bây giờ, {vi_agent} {vi_verb} {vi_patient}.", f"{vi_agent} {vi_verb} {vi_patient} bây giờ.")},
                                     {"en": (f"Right now, {en_agent} does not {en_base} {en_patient}.", f"{en_agent} does not {en_base} {en_patient} right now."),
                                      "vi": (f"Bây giờ, {vi_agent} không {vi_verb} {vi_patient}.", f"{vi_agent} không {vi_verb} {vi_patient} bây giờ.")},
                                     {"en": (f"Yesterday, {en_agent} {en_past} {en_patient}.", f"{en_agent} {en_past} {en_patient} yesterday."),
                                      "vi": (f"Hôm qua, {vi_agent} đã {vi_verb} {vi_patient}.", f"{vi_agent} đã {vi_verb} {vi_patient} hôm qua.")},
                                     {"en": (f"Yesterday, {en_agent} did not {en_base} {en_patient}.", f"{en_agent} did not {en_base} {en_patient} yesterday."),
                                      "vi": (f"Hôm qua, {vi_agent} không {vi_verb} {vi_patient}.", f"{vi_agent} không {vi_verb} {vi_patient} hôm qua.")}]]
                    if state_forms_v4_6 is not None and version not in ("v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30"):
                        realized[0] = state_forms_v4_6[language][0][variant]
                        realized[1] = state_forms_v4_6[language][1][variant]
                    for edge_index, (source, target, kind, value) in enumerate(single_edges + path_edges):
                        is_path = edge_index >= len(single_edges)
                        rows.append(CorpusRecord(
                            record_id=f"{group}-{language}-v{variant}-e{edge_index}", split_group_id=group,
                            language=language, source_text=realized[source], target_text=realized[target],
                            source_frame_id=f"{group}-state-{source}", target_frame_id=f"{group}-state-{target}",
                            action=Action(kind, value), provenance_ref=f"tide_jepa/pilot_seed.py:original-ai-authored-{version}",
                            license_ref="original-ai-authored-internal-research; no-PhoMT-content",
                            approval_status="pending", path_id=f"{group}-path-v{variant}" if is_path else None,
                            path_step=edge_index - len(single_edges) if is_path else None))
                    # Emit each bilingual alignment once. This block sits inside
                    # the language loop to keep row realization construction
                    # together, so only its English pass owns the pair records.
                    if language == "en":
                        for index in range(10):
                            edge_pairs.append({"left_record_id": f"{group}-en-v{variant}-e{index}",
                                               "right_record_id": f"{group}-vi-v{variant}-e{index}",
                                               "relation": "same_event"})
                        path_pairs.append({"left_path_id": f"{group}-path-v{variant}", "left_language": "en",
                                           "right_path_id": f"{group}-path-v{variant}", "right_language": "vi",
                                           "relation": "same_event"})
    output.mkdir(parents=True)
    (output / "corpus.draft.jsonl").write_text("".join(json.dumps(row.to_dict(), ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    artifacts = {
        "inventory.draft.json": {"actions": actions, "approved_by_language": {"en": [], "vi": [], "cham_phan_rang": []},
                                  "proposed_by_language": {"en": actions, "vi": actions}},
        "alignments.draft.json": {"edge_pairs": edge_pairs, "path_pairs": path_pairs},
        "groups.json": groups,
        "data_statement.json": {"version": f"vi-en-ai-{version}", "source": "original AI-authored synthetic controlled-language pilot",
                                "phomt_used": False, "human_validated": False, "languages": ["en", "vi"],
                                "event_families": len(groups), "records": len(rows),
                                **({"review_scope": "train-validation-only",
                                    "reviewed_records": sum(groups[row.split_group_id] != "test" for row in rows)}
                                   if version in ("v4.28", "v4.29", "v4.30") else {}),
                                **({"review_bundle_dir": "review_bundle"}
                                   if version in ("v4.29", "v4.30") else {}),
                                **({"context_checker_scope": "The shared workshop context is checked as the declared English/Vietnamese place marker only; broader discourse context is not evaluated.",
                                    "action_frame_mapping": {"TIME": {"NOW": "target frame time is present", "PAST": "target frame time is past"},
                                                             "POLARITY": {"POSITIVE": "target frame polarity is positive", "NEGATIVE": "target frame polarity is negative"}}}
                                   if version in ("v4.29", "v4.30") else {}),
                                "draft_sha256": dataset_fingerprint(rows),
                                "split_policy": ("20 train, 6 validation, 6 release-holdout event families, fixed before model selection; fresh families not used in prior versions"
                                                 if version == "v4.2" else
                                                 "20 train, 6 validation, 6 release-holdout event combinations; every agent, verb lemma and patient phrase occurs in training; all combinations are frame/group-disjoint; test path order is held out"
                                                 if version == "v4.3" else
                                                 "80 train, 12 validation, 12 release-holdout event combinations; every agent, verb lemma and patient phrase occurs in training; frame/group-disjoint combinations built from broadly compatible actions and objects; test path order is held out"
                                                 if version == "v4.4" else
                                                 "80 train, 12 validation, 12 release-holdout event combinations sampled outside every v4.4 combination; all agent, verb lemma, and patient phrase values occur in training; new holdout combinations are not reused from the prior version"
                                                 if version == "v4.5" else
                                                 "80 train, 12 validation, 12 release-holdout event combinations sampled outside every v4.4 and v4.5 combination; all agent, verb lemma, and patient phrase values occur in training; English NOW uses present progressive; new holdout combinations are unused by prior versions"
                                                 if version == "v4.6" else
                                                 "120 train, 40 validation, 40 release-holdout event combinations sampled outside every v4.4-v4.6 combination; all agent, verb lemma, and patient phrase values occur in training; every validation and release-holdout triple uses only factor pairs represented in training; English NOW uses present progressive"
                                                 if version == "v4.7" else
                                                 "112 train, 40 validation, 40 release-holdout event combinations using three new agents; every held-out agent-verb, agent-patient, and verb-patient pair is represented in training; held-out combinations are disjoint from v4.4-v4.7; English NOW uses present progressive"
                                                 if version == "v4.8" else
                                                 "112 train, 40 validation, 40 release-holdout combinations (stored with schema split label test) from three new agents; every held-out factor pair is represented in training; English NOW uses present progressive"
                                                 if version == "v4.9" else
                                                 "112 train, 40 validation, 40 release-holdout combinations (schema split label test) from three new agents; every held-out factor pair is represented in training; English NOW uses present progressive"
                                                 if version == "v4.10" else
                                                 "112 train, 40 validation, 40 release-holdout combinations (schema split label test) from three agents not used in prior pilot pools; every held-out factor pair is represented in training; English NOW uses present progressive"
                                                 if version == "v4.11" else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three new agents; every held-out factor pair is represented in training; English NOW uses present progressive; fresh factors and holdout for matched source-copy ablation"
                                                 if version == "v4.12" else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; fresh split and sealed holdout for a source-copy dose-response ablation"
                                                 if version == "v4.13" else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; fresh sealed holdout for an exposure-diversity test"
                                if version in ("v4.14", "v4.15") else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; fresh split and sealed holdout for a lower latent-objective-dose study"
                                                 if version == "v4.16" else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; fresh split and sealed holdout for a unique-transition row-exposure balance study. Train/validation paths apply negative polarity then past time; test paths reverse this order, so the sealed holdout also probes action-order recombination and is not a matched measure of the weighting contrast"
                                                 if version == "v4.17" else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; train, validation, and sealed holdout use the same action order; fresh split for a 2x2 TIDE-auxiliary/source-copy supervision factorial"
                                                 if version == "v4.18" else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; action order matches across all splits; fresh split for a TIDE copy-weight (0/1.5) × latent-dose (0/0.1) study with matched loss computation and fixed-final-epoch evaluation"
                                                 if version == "v4.19" else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; action order matches across all splits; fresh split for a TIDE vocabulary-softmax versus source-pointer decoder comparison with fixed-final-epoch evaluation"
                                                 if version == "v4.20" else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; action order matches across all splits; fresh split for a fixed-final-epoch 2x2 TIDE source-copy-weight (0/1.5) × decoder (vocabulary/source-pointer) factorial"
                                                 if version == "v4.21" else
                                                 "112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; action order matches across splits; new corpus, split, reviews, protocol, and sealed holdout for the v4.21 checker-coverage repair rerun of the fixed-final-epoch 2x2 TIDE copy-loss-weight × decoder factorial"
                                                 if version == "v4.22" else
                                                 "112/40/40 event combinations from three fresh agents × eight verbs × eight patients; balanced factor marginals and pairwise-covered held-out combinations; English progressive NOW aligns with Vietnamese đang, including đang không in Vietnamese NOW-negative forms; same path order in all splits; sentence-template families are shared across partitions, so this is a preliminary compositional pilot and not a template/domain-generalization benchmark"
                                                 if version == "v4.23" else
                                                 "112/40/40 event combinations from three fresh agents × eight verbs × eight patients; pairwise-covered held-out combinations, fixed deterministic split seed; shared four-form realization grammar and action order; fresh synthetic split for a 64-width/two-layer TIDE capacity profile and source-copy weight 0/1.5 comparison with fixed-final-epoch evaluation"
                                                 if version == "v4.24" else
                                                 "112/40/40 event combinations from three fresh agents × eight verbs × eight patients; pairwise-covered held-out combinations, fixed deterministic split seed, English progressive NOW aligned with Vietnamese đang (including đang không for negative NOW), shared four-form realization grammar and action order; fresh synthetic corpus and release holdout to test one-pass 0.2 self-feeding against teacher forcing at fixed 64-width/two-layer TIDE capacity; the extra proposal forward costs more compute, so no matched-compute claim; preliminary exposure-mismatch hypothesis test only"
                                                 if version == "v4.25" else
                                                 "112/40/40 event combinations from three fresh agents × eight verbs × eight patients; pairwise-covered held-out combinations, fixed deterministic split seed; shared four-form realization grammar and action order; fresh synthetic corpus and sealed release holdout for low-dose source-copy supervision (0/0.25) at fixed 64-width/two-layer TIDE capacity and final-epoch evaluation"
                                                 if version == "v4.26" else
                                                 "112/40/40 event combinations from three fresh agents × eight verbs × eight patients; pairwise-covered held-out combinations, fixed deterministic split seed, English progressive NOW aligned with Vietnamese đang (including đang không for negative NOW), shared four-form realization grammar and action order; fresh synthetic corpus and release holdout for equal-language-balanced token CE versus global byte-token CE at fixed 64-width/two-layer TIDE capacity and source-copy weight 0; preliminary optimization diagnostic only"
                                                 if version == "v4.27" else
                                                 "112/40/40 event combinations from a fresh three-agent factor block, eight verbs, and eight patients; new deterministic split seed, pairwise-covered held-out combinations, same four-form grammar and action order; fresh corpus and release holdout for the base per-edge language-balanced token CE contrast; reviewers inspect train and validation only, while test-split text remains sealed until all validation gates pass"
                                                 if version == "v4.28" else
                                                 "112/40/40 event combinations from a fresh three-agent factor block with a new deterministic split seed; the release holdout is separate from v4.28 and only train/validation records, frames, groups, and alignments enter the reviewer bundle; the shared workshop context is checked through the declared place marker"
                                                 if version == "v4.29" else
                                                 "112/40/40 combinations from agents 71–73 × eight verbs × eight patients on a fresh split, with the shared four-form grammar and action order; train/validation-only review package and sealed release holdout for a TIDE vocabulary-versus-source-pointer decoder comparison at source-copy weight 0"
                                                 if version == "v4.30" else
                                                 "12 train, 4 validation, 4 release-holdout event families, fixed before model selection; new events not used in v3"),
                                "surface_realizations_per_state": 4 if version in ("v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30") else 2,
                                **({"transition_weighting_note": (
                                    "There are 3072 duplicated path-step rows across the full split: 1792 in "
                                    "training, 640 in validation, and 640 in the sealed release holdout. Each "
                                    "logical path-step transition has one standalone single-edge record and one "
                                    "path-linked record. In training this adds 1792 record exposures, so those "
                                    "path-selected transitions contribute twice the row-wise token/edge exposure. "
                                    "Validation and holdout duplicates are evaluation records, not training "
                                    "exposure. " + ("The v4.17 protocol crosses uniform row weighting with a "
                                    "unique-transition condition assigning 0.5 weight to each standalone/path-linked "
                                    "representation in base per-edge losses; path-composition losses are unchanged. "
                                    "This is an aggregate weighting contrast, not removal of either record."
                                    if version == "v4.17" else
                                    "The representation is fixed identically across conditions; results describe a "
                                    "path-enriched training distribution, not uniform weighting over unique transitions."))}
                                    if version in ("v4.15", "v4.16", "v4.17", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30") else {}),
                                **({"registered_hypotheses": {
                                    "source_copy_supervision": "Within each TIDE auxiliary multiplier, weight 1.5 is hypothesized to improve source-slot preservation versus weight 0 without reducing action fidelity by more than 5 percentage points.",
                                    "tide_auxiliary": "At fixed source-copy weight, TIDE auxiliary multiplier 0.1 is hypothesized to improve the joint action-and-preservation outcome versus multiplier 0.",
                                    "primary_quality_gate": "Every cell, seed, and language/action bucket must pass frozen Unicode, action-fidelity, and preservation thresholds before the release holdout can be opened.",
                                    "interpretation": "Report cell-wise outcomes and the copy × TIDE interaction descriptively; three seeds do not establish population-level statistical certainty."}}
                                    if version == "v4.18" else
                                    {"registered_hypotheses": {
                                     "source_copy_supervision": "At each latent multiplier, weight 1.5 is hypothesized to improve source-slot preservation versus weight 0 without reducing action fidelity by more than 5 percentage points.",
                                     "tide_auxiliary": "At fixed source-copy weight, latent multiplier 0.1 is hypothesized to improve the joint action-and-preservation outcome versus multiplier 0.",
                                     "checkpoint_selection": "A preregistered final-epoch checkpoint is hypothesized to reduce validation-based checkpoint-selection bias; all conditions run the same fixed epoch count.",
                                     "matched_compute": "All TIDE cells compute the same model and loss terms; source-copy loss is evaluated in every cell, while registered multipliers alone determine its gradient contribution.",
                                     "primary_quality_gate": "Every cell, seed, and language/action bucket must pass frozen Unicode, action-fidelity, and preservation thresholds before the release holdout can be opened.",
                                     "interpretation": "Report cell-wise outcomes and the copy × latent-dose interaction descriptively; three seeds do not establish population-level statistical certainty."}}
                                    if version == "v4.19" else {}),
                                **({"registered_hypotheses": {
                                    "source_pointer_decoder": "At fixed TIDE objective, data, split, seeds, training schedule, and validation protocol, a source-pointer mixture decoder is hypothesized to improve source-slot preservation over the vocabulary-only decoder without reducing action fidelity by more than 5 percentage points.",
                                    "primary_quality_gate": "Every decoder condition, seed, and language/action bucket must pass the frozen Unicode, action-fidelity, and preservation thresholds before the release holdout can be opened.",
                                    "compute_interpretation": "Decoder variants differ in parameter count and per-token operations; record updates, tokens, wall time, and throughput, and make no matched-FLOP claim.",
                                    "interpretation": "Report decoder contrasts descriptively across three seeds; synthetic references and three seeds do not establish natural-language efficacy or population-level statistical certainty."}}
                                    if version == "v4.20" else
                                    {"registered_hypotheses": {
                                     "copy_decoder_interaction": "The combination of positive source-copy supervision (1.5) and a source-pointer decoder is hypothesized to improve joint source-slot preservation and action fidelity over either component alone; effects are descriptive across three seeds.",
                                     "primary_quality_gate": "Every registered cell, seed, and language/action bucket must pass the frozen Unicode, action-fidelity, and preservation thresholds before the release holdout can be opened.",
                                     "compute_interpretation": "The 2x2 copy-weight × decoder factorial computes the source-copy term in every cell; only its multiplier and decoder mode vary. Decoder variants differ in parameter count and operations, so no matched-FLOP claim is made.",
                                     "interpretation": "Report all four cells separately and describe the interaction without population-level claims; the benchmark is synthetic and has three seeds."}}
                                    if version in ("v4.21", "v4.22", "v4.23") else
                                    {"registered_hypotheses": {
                                     "source_copy_supervision": "At fixed 64-width/two-layer TIDE capacity, source-copy weight 1.5 is hypothesized to improve role preservation over weight 0 without reducing action fidelity by more than five percentage points.",
                                     "capacity_scope": "This version uses a larger fixed model than v4.23 but a fresh corpus and split; the cross-version comparison is descriptive and does not isolate model capacity causally.",
                                     "primary_quality_gate": "Every source-copy condition, seed, and language/action bucket must pass frozen Unicode, action-fidelity, and preservation thresholds before the release holdout can be opened.",
                                     "interpretation": "Report the copy-weight contrast descriptively across three seeds; this synthetic pilot does not establish natural-language efficacy or population-level certainty."}}
                                    if version == "v4.24" else
                                    {"registered_hypotheses": {
                                     "one_pass_self_feeding": "At fixed model, corpus, split, and updates, one-pass self-feeding at rate 0.2 is hypothesized to improve validation role preservation compared with teacher forcing without reducing action fidelity by more than five percentage points.",
                                     "method_scope": "Training replaces a sampled share of decoder inputs with argmax tokens proposed from the preceding teacher-forced context; it is one-pass self-feeding, not recursive scheduled sampling.",
                                     "compute_interpretation": "Positive-rate conditions run an additional no-gradient proposal forward and then the training forward, so conditions are not compute matched; report updates, tokens, wall time, and throughput.",
                                     "primary_quality_gate": "Every condition, seed, and language/action bucket must pass frozen Unicode, action-fidelity, and preservation thresholds before the release holdout can be opened.",
                                     "interpretation": "Three seeds and a narrow synthetic grammar support only a preliminary diagnostic; the contrast cannot establish the cause of earlier failures or natural-language efficacy."}}
                                    if version == "v4.25" else
                                    {"registered_hypotheses": {
                                     "low_dose_source_copy": "At fixed TIDE model, corpus, split, and updates, source-copy weight 0.25 is hypothesized to improve entity/role preservation versus weight 0 without reducing action fidelity by more than five percentage points.",
                                     "compute_interpretation": "Both conditions compute the aligned source-copy token loss; only the registered multiplier differs, so updates and examples are matched, while wall time is reported.",
                                     "primary_quality_gate": "Every condition, seed, and language/action bucket must pass frozen Unicode, action-fidelity, and preservation thresholds before the release holdout can be opened.",
                                     "interpretation": "This fresh synthetic corpus and three-seed contrast support only preliminary diagnostic evidence, not human or natural-language validation."}}
                                    if version == "v4.26" else
                                    {"registered_hypotheses": {
                                     "language_balanced_token_loss": "At fixed TIDE model, source-copy weight 0, corpus size, split, and updates, replacing the global base per-edge byte-token CE with an equal mean of per-example normalized token CE within each language and then equally across English/Vietnamese is hypothesized to improve English patient/predicate preservation without reducing action fidelity or Vietnamese preservation.",
                                     "mechanism": "Training records are balanced by language count, but target UTF-8 byte counts differ. The treatment tests whether global byte-token normalization gives Vietnamese more gradient mass in the base per-edge token term. Both conditions compute both summaries; only interpolation weight 0 versus 1 changes that term. Composed path-token CE and auxiliary terms remain identical across arms.",
                                     "primary_quality_gate": "Every condition, seed, and language/action bucket must pass the frozen Unicode, action-fidelity, and preservation thresholds before the release holdout can be opened.",
                                     "interpretation": "Three seeds on a fresh synthetic corpus support only a preliminary optimization diagnostic, not human or natural-language efficacy."}}
                                     if version in ("v4.27", "v4.28", "v4.29") else
                                    {"registered_hypotheses": {
                                     "source_pointer_preservation": "At fixed TIDE objective, source-copy weight 0, corpus, split, and updates, a source-pointer decoder is hypothesized to improve source-slot preservation over the vocabulary decoder without reducing action fidelity by more than five percentage points.",
                                     "compute_interpretation": "The pointer decoder adds a source-memory distribution and learned mixture gate; report updates, tokens, wall time, and throughput. This is not a matched-FLOP comparison.",
                                     "primary_quality_gate": "Every decoder condition, seed, and language/action bucket must pass the frozen Unicode, action-fidelity, and preservation thresholds before the release holdout can be opened.",
                                     "interpretation": "This fresh synthetic three-seed replication is descriptive; prior decoder results remain preserved and no natural-language efficacy is claimed."}}
                                     if version == "v4.30" else {}),
                                "limitations": ["AI-authored; independent AI review is preliminary", "synthetic shared grammar; no domain-generalization claim",
                                                "single deterministic reference per realization", "no human evaluation or natural-corpus efficacy"]},
        "semantic_frames.draft.json": frames,
    }
    for name, value in artifacts.items():
        (output / name).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if version in ("v4.29", "v4.30"):
        import hashlib
        review_rows = [row for row in rows if groups[row.split_group_id] != "test"]
        review_record_ids = {row.record_id for row in review_rows}
        review_frame_ids = {frame for row in review_rows for frame in (row.source_frame_id, row.target_frame_id)}
        review_path_ids = {row.path_id for row in review_rows if row.path_id is not None}
        bundle = output / "review_bundle"
        bundle.mkdir()
        (bundle / "records.jsonl").write_text(
            "".join(json.dumps(row.to_dict(), ensure_ascii=False) + "\n" for row in review_rows),
            encoding="utf-8")
        (bundle / "semantic_frames.json").write_text(
            json.dumps({key: value for key, value in frames.items() if key in review_frame_ids},
                       ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        (bundle / "groups.json").write_text(
            json.dumps({key: value for key, value in groups.items() if value != "test"},
                       ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        scoped_alignments = {
            "edge_pairs": [pair for pair in edge_pairs
                           if pair["left_record_id"] in review_record_ids
                           and pair["right_record_id"] in review_record_ids],
            "path_pairs": [pair for pair in path_pairs
                           if pair["left_path_id"] in review_path_ids
                           and pair["right_path_id"] in review_path_ids],
        }
        (bundle / "alignments.json").write_text(
            json.dumps(scoped_alignments, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8")
        (bundle / "inventory.json").write_text(
            json.dumps(artifacts["inventory.draft.json"], ensure_ascii=False,
                       sort_keys=True, indent=2) + "\n", encoding="utf-8")
        (bundle / "statement.json").write_text(
            json.dumps({"version": f"vi-en-ai-{version}", "source": "original AI-authored synthetic pilot",
                        "phomt_used": False, "human_validated": False,
                        "review_scope": "train-validation-only", "reviewed_records": len(review_rows),
                        "languages": ["en", "vi"],
                        "draft_stage": "all records remain pending until both preliminary AI reviews and adjudication approve freeze",
                        "action_frame_mapping": {"TIME": {"NOW": "target frame time is present", "PAST": "target frame time is past"},
                                                 "POLARITY": {"POSITIVE": "target frame polarity is positive", "NEGATIVE": "target frame polarity is negative"}},
                        "standalone_records": "Rows with path_id=null and path_step=null are single-edge records; composed-path rows have path_step 0 or 1 and a path_id. Null path fields are intentional.",
                        "context_checker_scope": "The shared workshop context is checked as the declared English/Vietnamese place marker only; broader discourse context is not evaluated."}, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8")
        bundle_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in sorted(bundle.iterdir()) if path.is_file()}
        bundle_manifest = {"review_scope": "train-validation-only",
                           "reviewed_records": len(review_rows), "files_sha256": bundle_hashes}
        (bundle / "manifest.json").write_text(
            json.dumps(bundle_manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8")
        artifacts["data_statement.json"]["review_bundle_sha256"] = hashlib.sha256(
            (bundle / "manifest.json").read_bytes()).hexdigest()
        (output / "data_statement.json").write_text(
            json.dumps(artifacts["data_statement.json"], ensure_ascii=False,
                       sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return artifacts["data_statement.json"]


def main():
    parser = argparse.ArgumentParser(description="Author a pending original synthetic Vi–En pilot for review")
    parser.add_argument("output_dir")
    parser.add_argument("--pilot-version", choices=("v3", "v4", "v4.1", "v4.2", "v4.3", "v4.4", "v4.5", "v4.6", "v4.7", "v4.8", "v4.9", "v4.10", "v4.11", "v4.12", "v4.13", "v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23", "v4.24", "v4.25", "v4.26", "v4.27", "v4.28", "v4.29", "v4.30"), default="v3")
    args = parser.parse_args()
    result = (author_seed(args.output_dir) if args.pilot_version == "v3"
              else author_seed_v4(args.output_dir, version=args.pilot_version))
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
