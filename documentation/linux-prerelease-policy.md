# Linux prerelease policy and publication checklist

[日本語](linux-prerelease-policy_ja.md)

Current policy from 2026-11-17: **all Folimeld Linux distributions, including older versions, are prereleases (test distributions).** This covers DEB, RPM and Snap, amd64 and ARM64, and Releases shared by both CPUs. Do not promote them to stable releases or GitHub Latest. This policy does not change Windows, macOS or BSD classifications.

The shared `linux-v0.3.3` and `linux-v0.3.4` Releases have already been marked as prereleases; do not repeat that classification change. Classification alone does not call for rebuilds, VM retesting, or overwriting, deleting or re-uploading existing assets. Preserve historical release text, build records and original attachments, including their use of “stable”. A Snap's build-time `grade: stable` does not designate a stable GitHub Release.

## User guidance and supported systems

Both READMEs must describe all Linux versions as test distributions. Read each Release and CPU-specific verification record for OS versions, CPU, format, package revision, dependencies and tested scope. Do not apply amd64 results to ARM64.

Kali amd64 0.3.5 uses the [shared Ubuntu/Debian/Kali DEB](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-amd64-v0.3.5). The absence of a Kali-specific amd64 tag does not mean it is unpublished. It is separate from the [Kali ARM64 Release](https://github.com/tyamada/Folimeld/releases/tag/kali-arm64-v0.3.5).

## Future Linux publication: required settings on every route

These instructions apply only after separate publication authorization. Adding this document does not execute creation, editing or publication.

1. Review the branch, uncommitted changes and AGENTS.md; preserve other work. Finalize the tag's source commit, release text, CPU-specific records, explicit asset list and SHA-256 hashes.
2. Create a new Linux Release as **Draft and Pre-release, not Latest** from the beginning. Tags without `preview` are not exceptions. For CLI creation, use `--verify-tag` to avoid implicit tag creation.
3. For CLI creation specify `gh release create <tag> --verify-tag --draft --prerelease --latest=false ...`; when publishing also specify `gh release edit <tag> --draft=false --prerelease --latest=false`. These are not commands to reapply mechanically to existing public Releases.
4. REST API creation/publication requests must explicitly include `prerelease: true` and `make_latest: "false"`. Use `draft: false` only when publishing the draft. Do not rely on omitted options, `legacy`, or automatic Latest selection.
5. In the browser, select Pre-release, do not select Latest, and review both settings immediately before saving. Draft alone does not imply prerelease classification.
6. Immediately before and after publication, verify `prerelease=true`, the appropriate `draft` value, tag, asset names/sizes/SHA-256 hashes and unchanged existing Latest using the API or equivalent. Record verification from the actual public URLs before announcing availability in README. Stop and report discrepancies; do not correct settings or re-upload without authorization.
7. Do not modify other CPU/OS Releases, existing assets, publication dates, text or tags. Preserve historical originals and describe current policy here and in README.

See the official [CLI creation](https://cli.github.com/manual/gh_release_create) and [CLI editing](https://cli.github.com/manual/gh_release_edit) references.

## Limits of local preparation tools

`tools/prepare_linux_release.py` verifies existing assets and creates a local migration plan; it does not create GitHub Releases. Its output does not enforce prerelease/Latest fields, so any future API, CLI or UI publisher consuming it must apply the settings above. Do not retroactively rewrite historical plan JSON or original attachments.

The current `.github/workflows/checks.yml` performs checks and uploads Actions artifacts, not GitHub Releases. Any new publication automation needs Linux-scoped guards for prerelease classification and unchanged Latest. This policy is not a claim that all external or temporary scripts are technically constrained today.
