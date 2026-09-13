# AGENTS.md — legal

Repo này thuộc hệ thống **Lock.R** (org [LockR-Tech](https://github.com/LockR-Tech)). Tiến độ, luật và sơ đồ nằm ở repo [**docs**](https://github.com/LockR-Tech/docs) (`../docs/AGENTS.md`, `../docs/STATUS.md`).

## Riêng repo này

- Trang tĩnh phục vụ yêu cầu của Google Play và Facebook Login:
  - `privacy-policy.html` → `https://lockr-tech.github.io/legal/privacy-policy.html`
  - `data-deletion.html` → `https://lockr-tech.github.io/legal/data-deletion.html`
- **Repo public** vì GitHub Pages không chạy trên repo private ở gói Free. Không đưa bất cứ thứ gì nội bộ vào đây.
- Merge `main` ⇒ GitHub Pages tự build lại trong ~1 phút. Không có `index.html` nên URL gốc `/legal/` trả 404 — đó là bình thường.
- Đổi đường dẫn file ⇒ phải cập nhật URL đã khai trên Google Play Console và Facebook Developer.
- Nội dung chính sách phải khớp với `mobile/assets/markdown/privacy_policy.md` và `terms_of_service.md` trong app.
- Không push thẳng `main`; commit theo Conventional Commits (scope `privacy`, `data-deletion`). Không thêm trailer `Co-Authored-By` của công cụ AI.
