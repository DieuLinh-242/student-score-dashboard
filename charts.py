from io import BytesIO

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from data_service import CLASSIFICATION_ORDER, SCORE_COLUMNS

try:  # Plotly được import muộn để lỗi thiếu thư viện hiện rõ nguyên nhân
    import plotly.express as px
except ImportError:  # pragma: no cover
    px = None


def _to_png(fig) -> BytesIO:
    fig.tight_layout()
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=140)
    plt.close(fig)  # luôn đóng figure để không rò rỉ bộ nhớ
    buffer.seek(0)
    return buffer


def _empty_png(message: str) -> BytesIO:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=14)
    ax.axis("off")
    return _to_png(fig)


def distribution_png(df) -> BytesIO:
    if df.empty:
        return _empty_png("Không có dữ liệu")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.histplot(data=df, x="total_score", bins=10, kde=len(df) > 1,
                 color="#2563eb", ax=ax)
    ax.set(title="Phân phối điểm tổng kết",
           xlabel="Điểm tổng kết", ylabel="Số sinh viên")
    return _to_png(fig)


def correlation_png(df) -> BytesIO:
    """Heatmap tương quan giữa các điểm thành phần và điểm tổng kết."""
    if len(df) < 2:
        return _empty_png("Cần ít nhất 2 sinh viên để tính tương quan")
    fig, ax = plt.subplots(figsize=(6, 4.5))
    corr = df[SCORE_COLUMNS + ["total_score"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
                vmin=-1, vmax=1, ax=ax)
    ax.set_title("Tương quan giữa các điểm")
    return _to_png(fig)


def classification_chart_html(df) -> str:
    counts = (
        df["classification"].astype(str)
        .value_counts()
        .reindex(CLASSIFICATION_ORDER, fill_value=0)
        .rename_axis("classification")
        .reset_index(name="count")
    )
    fig = px.bar(
        counts, x="classification", y="count",
        color="classification",
        title="Số sinh viên theo xếp loại",
        labels={"classification": "Xếp loại", "count": "Số sinh viên"},
    )
    fig.update_layout(showlegend=False, height=420)
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def scatter_chart_html(df) -> str:
    fig = px.scatter(
        df, x="midterm", y="final",
        color="class_name", hover_name="full_name",
        title="Điểm giữa kỳ và cuối kỳ",
        labels={"midterm": "Giữa kỳ", "final": "Cuối kỳ",
                "class_name": "Lớp"},
    )
    fig.update_traces(marker={"size": 11})
    fig.update_layout(height=420, xaxis_range=[0, 10], yaxis_range=[0, 10])
    return fig.to_html(full_html=False, include_plotlyjs=False)
