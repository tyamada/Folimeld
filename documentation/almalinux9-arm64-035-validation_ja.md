# AlmaLinux 9 ARM64 0.3.5-2 RPM 検証記録

# Folimeld0.3.5 AlmaLinux9 ARM64 RPM preview

日本語: AlmaLinux9.8 aarch64向け0.3.5-2 RPM試験版です。既存公開物とlatestを保持します。

`folimeld-0.3.5-2.alma9_8.aarch64.rpm` (84,706,160bytes), SHA256 `ac05b323d271bccbd59c3b461841c576077bed372ca4ae510b8d837771bace14`

内蔵Mac上のAlmaLinux9.8 ARM64 VM、一般ユーザーXorg/Mutter、SELinux Enforcingで新規導入、回転・Undo/Redo・移動・白紙挿入/削除・別名保存・日本語パス再読込・画像PDF作成保存を確認。完全削除と同じ候補の再導入後も文書・設定を保持し保存PDFを表示。GUI3回終了0、残存プロセスなし。保存ページ順2→1→3、回転0→90→0、画像と元PNGの画素一致。410passed/9skipped/69subtests、ruff成功。2ビルド先でELF一致（同一Qt SDK、RPM時刻は異なる）。新しい最小依存構成でもUID1000 offscreen15秒継続。

本体ソース `44dee9d0543f5003160284f21aa458acbe13faa9`、ZIP SHA256 `50fcf81a945c9d9bf28e0ad7e4cd7d5968e81307c2ba5fe29a6706a17d542c3e`、全994入力をGit/ZIP/埋込記録で照合。163 ARM64 ELFは公式wheel25・自前Qt/PySide41・Alma RPM由来97を完全バイト照合。42署名付きバイナリRPMに対応する39署名付きSRPMを添付。RPATH変更は元ファイルへの同じ処理を再現して一致確認。公式PyInstaller起動部の元セクションも一致。

```bash
sudo dnf install ./folimeld-0.3.5-2.alma9_8.aarch64.rpm
```

公式Qt/PySide6.11.2 ARM wheelのglibc2.39要件を避けるため、版を下げずAlma9 glibc2.34上でQtbase/qtsvg/PySideをソースビルドしました。Core/Gui/Widgets/PrintSupport/Svgのみ。QML/Designer等の未使用機能とQt標準翻訳カタログは含まず、アプリ独自翻訳は含みます。上流変更は未構築の任意機能の梱包を省く記録済みパッチ1件。28,100元ソースファイル照合。依存ソースは共通0.3.4 TAR、Pillow補足、今回のAlma39SRPM補足、構成・パッチ・告知・provenanceを組み合わせてください。履歴NOT INCLUDED記載は別添ソースで補完します。

GitHub配布の未署名RPM、Alma公式パッケージではありません。glibc2.34以上、今回の受入は9.8 ARM64のみ。初回候補のlibOpenGL不足はrevision2で修正し新規最小環境で再検証。実機ARM、GNOME/Wayland、IME、暗号化/フォームGUI、関連付け、旧版更新は未試験。日本語名はシェル作成コピーの再読込。合成素材のUbuntu/Debian表記や旧amd64等の記録をAlma合格結果として使っていません。通常ユーザードメインでSnap同様の制限はありません。詳細はBUILD/KNOWN-LIMITATIONS/検証ZIPをご覧ください。

English: AlmaLinux9.8 aarch64 RPM0.3.5-2 preview. Fresh internal-Mac QEMU HVF, normal UID1000 Xorg/Mutter, SELinux Enforcing. Fresh install, edit/undo/redo/move/blank operations, Save As, Japanese-path reopen, image conversion/save and full removal/same-candidate reinstall passed. Documents/settings hashes preserved;3GUI exits0 and no remaining processes. Saved page order/rotation and PNG pixels verified.410tests/9skips/69subtests,ruff passed. Two clean app roots sharing one custom Qt SDK produced identical ELF; RPM times differ. Minimum dependency root ran UID1000 offscreen15seconds (timeout124 is liveness, not GUI completion).

Exact clean source commit/ZIP above,994inputs checked against Git/embedded manifest.163 AArch64 ELF:25official wheel,41locally source-built Qt/PySide,97AlmaRPM-derived;42signed binary RPMs map to39exact signed SRPMs attached. RPATH transformations replayed and full bytes matched. Original PyInstaller bootloader sections match. Qtbase/qtsvg/PySide6.11.2 built locally on glibc2.34 because official Qt/PySide ARM wheels need2.39. Core/Gui/Widgets/PrintSupport/Svg subset; app translations included, Qt standard catalogs and unused QML/Designer omitted. One recorded optional-artifact packaging patch;28,100original source files verified. Combine common upstream0.3.4 source TAR, Pillow supplement, current Alma39SRPM supplement, patch/configuration/provenance and current notices. Extra historical sources/tests are not Alma acceptance; historical embedded NOT INCLUDED is supplemented separately.

Unsigned local GitHub RPM, not official Alma repository submission; glibc>=2.34, accepted only on9.8 ARM64. Revision1 missing OpenGL fixed in revision2 and fresh minimum root retested. No physical ARM/full GNOME/Wayland/IME/encryption/forms GUI/associations/older9minor/cross-version upgrade accepted. Japanese-path copy created via shell; synthetic labels historical. SELinux normal unconfined user domain, no Snap-style app boundary. No independent second-VM Qt build. See limitations/build/evidence. Existing releases/latest preserved.


制限の全文:

AlmaLinux9.8 aarch64 RPM preview on GitHub, not an official AlmaLinux repository package. Application RPM unsigned. glibc>=2.34, tested on9.8 only; earlier9.x minors/other RHEL derivatives not accepted. Official OS dependency binary/source RPM signatures verified with the full-fingerprint checked AlmaLinux9 key.
Official Qt/PySide6.11.2 ARM wheel requires glibc2.39, so Qtbase6.11.2/qtsvg6.11.2 and PySide/Shiboken6.11.2 were built locally on AlmaLinux9.8 Python3.12.15/GCC11.5/Clang21.1.8. No dependency version downgrade. Modules Core,Gui,Widgets,PrintSupport,Svg only; QML/Designer/WebEngine/QtPdf omitted. Qt standard translation catalogs not built; app's own translations included. One recorded upstream Linux packaging patch skips absent optional artifacts; 28,100 original source files verified. Generated cp37-abi3 wheel tag is upstream limited-API naming, not Python3.7 acceptance; Python3.12.15 was actually used.
Fresh normal-user UID1000 Xorg/Mutter GUI on an internal Mac QEMU HVF VM, SELinux Enforcing in normal unconfined user domain. No Snap-style app boundary. All3GUI runs exit0; full removal/same-candidate reinstall preserves recorded Documents/settings hashes. No cross-version upgrade/rollback acceptance. No physical ARM, full GNOME/Wayland, IME composition, encryption/forms GUI, file-manager associations, older Alma minors or other OS acceptance. Japanese-path copy created in shell, then reopened. fitz deprecation and offscreen UTF-8/plugin warnings retained. Synthetic fixture page labels mention Ubuntu/Debian; actual execution here is new AlmaLinux, not inherited acceptance.
410tests passed,9skipped,69subtests; ruff passed. Two separate application output roots share the same fixed locally built Qt/PySide SDK and yield identical ELF; RPM header time differs. No full independently provisioned second-VM build of the Qt stack.
Revision1 private candidate failed minimum-root startup for missing libOpenGL.so.0. Revision2 declares it and passed a new official-dependency-only installroot with weak dependencies disabled; UID1000 offscreen alive15seconds timeout124 is liveness, not normal GUI completion. Private failed candidate and logs retained separately, not released.
163 AArch64 ELF mapped:25 official-wheel members,41 locally source-built Qt/PySide,97 OS-derived members from42 signed binary RPMs mapping to39 exact signed SRPMs. Three ICU OS payloads have PySide standalone RPATH changes; replaying exact patchelf onto original OS files matches complete bytes. Qt SDK transformations likewise replayed and complete-byte verified. Missing libxcb/keysyms legal texts resolved from exact signed SRPM source/header. Official PyInstaller bootloader original sections match. Other third-party wheels not independently rebuilt.
Source ZIP994inputs matches exact clean Git/ZIP/embedded manifest. Common0.3.4 third-party TAR supplies unchanged original sources including Qtbase/qtsvg/PySide; add current Alma39SRPM supplement, Qt source-build patch/config/provenance, Pillow source/notice supplement and current notices. Current cp312 Pillow codec SBOM component/version/source hashes and license independently matched. Extra old Ubuntu/Fedora/amd64 records are historical, not Alma mapping. Historical embedded NOT INCLUDED is resolved by separate sources, not erased. Recipe needs official Alma repositories/bootstrap packages; not a fully offline toolchain image.
