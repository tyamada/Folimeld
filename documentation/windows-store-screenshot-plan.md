# Store screenshot capture plan

[日本語](windows-store-screenshot-plan_ja.md) | [English](windows-store-screenshot-plan.md)

Status: planning only; no captures or uploads yet. After the test Dynabook arrives and normal operation passes, capture Japanese and English interfaces separately. Restart the app after changing its language. Aim for five images per language initially.

| Order / filename | State to capture | Japanese caption | English caption |
| --- | --- | --- | --- |
| 01-overview.png | Open the generated three-page PDF; show thumbnails and toolbar | ページを見ながらPDFを整理 | Organize PDF pages visually |
| 02-page-editing.png | Show multiple selection and rotation/reordering results on a PDF copy | 複数ページを選んで移動・回転 | Move and rotate selected pages |
| 03-image-import.png | Image-folder dialog with order and page-size choices visible | 画像フォルダーからPDFを作成 | Create a PDF from an image folder |
| 04-properties.png | Document properties, Details tab | PDFのレイアウトと綴じ方向を設定 | Adjust PDF layout and binding direction |
| 05-password.png | PDF opening-password settings; input empty or masked | PDFを開くためのパスワードを設定 | Set a password for opening a PDF |

Use copies of the generated test ZIP fixtures. Do not use manga under `testdata/`, third-party documents, personal files or purchaser information. Select `fixtures/` for image import and use its PNG/JPEG/TIFF files; PDFs are excluded from the image list.

## Capture conditions and storage

- Current Microsoft Desktop requirements are PNG, at least 1366×768, no larger than 50 MB each. Prefer actual 1920×1080 captures where available; do not upscale to meet dimensions. Use another display if necessary.
- Save Japanese captures under `build/store-listing/screenshots/ja-JP/` and English under `build/store-listing/screenshots/en-US/`. Add only approved images to the repository/listing later.
- Use the same candidate, window size and scaling. Record app version, package SHA-256, OS build, language, resolution/scaling, date and fixture hashes in `capture-record.json`.
- Capture actual UI; do not add marketing messages/logos or composite unimplemented screens. Exclude notifications, account names, personal paths, passwords and errors.
- Verify display/save results for properties/password changes before capture. Exclude supporter purchases because actual Store behavior remains unverified.
- Recapture using the final submission candidate or verify no UI/feature differences. Development-package screenshots do not establish Store-delivered behavior.

Captions in both languages are under 200 characters. Upload images/captions separately for each listing language. Recheck current requirements before publication. [Microsoft image requirements](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/screenshots-and-images)
