# Dashboard quản lí điểm sinh viên (FastAPI + Pandas + Seaborn + Plotly)

## Chạy cục bộ
```bash
python -m venv .venv
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# macOS/Linux:         source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
- Dashboard: http://127.0.0.1:8000/   (lọc lớp: `/?class_name=CTK46A`)
- Swagger UI: /docs · API: /api/summary, /api/students · Kiểm tra: /health

## Kiểm thử
```bash
pip install pytest
pytest -q tests
```

## Đưa lên GitHub và Render
```bash
git init
git add .
git commit -m "Initial student score dashboard"
git branch -M main
git remote add origin https://github.com/USERNAME/student-score-dashboard.git
git push -u origin main
```
Render: New > Web Service > chọn repo > Python
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Điểm tổng kết
10% chuyên cần + 20% bài tập + 30% giữa kỳ + 40% cuối kỳ.
Xếp loại: <4 Kém · 4–<5,5 Yếu · 5,5–<7 Trung bình · 7–<8,5 Khá · ≥8,5 Giỏi.
