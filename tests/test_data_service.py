import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from data_service import (clean_scores, enrich_scores, filter_scores,
                          load_scores, summarize)


def get():
    return enrich_scores(clean_scores(load_scores()))


def test_total_score_sv001():
    # 0.1*9 + 0.2*8 + 0.3*7.5 + 0.4*8 = 0.9 + 1.6 + 2.25 + 3.2 = 7.95
    row = get().set_index("student_id").loc["SV001"]
    assert row["total_score"] == 7.95
    assert row["classification"] == "Khá"


def test_classification_boundaries():
    df = pd.DataFrame({"total_score": [3.99, 4.0, 5.5, 7.0, 8.5, 10.0]})
    from data_service import CLASSIFICATION_ORDER
    labels = pd.cut(df["total_score"], [-0.01, 4.0, 5.5, 7.0, 8.5, 10.01],
                    labels=CLASSIFICATION_ORDER, right=False).astype(str).tolist()
    assert labels == ["Kém", "Yếu", "Trung bình", "Khá", "Giỏi", "Giỏi"]


def test_clean_removes_invalid_and_duplicates():
    raw = pd.DataFrame({
        "student_id": ["A", "A", "B", "C"],
        "full_name": ["x", "x2", "y", "z"],
        "class_name": ["L1"] * 4,
        "attendance": [5, 6, 11, None],
        "assignment": [5] * 4, "midterm": [5] * 4, "final": [5] * 4,
    })
    out = clean_scores(raw)
    assert out["student_id"].tolist() == ["A"]
    assert out.loc[0, "full_name"] == "x2"  # giữ bản ghi cuối


def test_filter_and_summary():
    data = get()
    a = filter_scores(data, "CTK46A")
    assert len(a) == 3
    s = summarize(a)
    assert s["student_count"] == 3
    assert s["pass_rate"] == round(2 / 3 * 100, 2)  # SV005 không đạt
    assert summarize(a.iloc[0:0])["student_count"] == 0
