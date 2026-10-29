# Store publication decision register

[日本語](windows-store-publication-decisions_ja.md) | [English](windows-store-publication-decisions.md)

Status: pre-publication. Retain the existing registration/name reservation. This register tracks decisions; it does not update Partner Center, send mail or publish websites. Apply user decisions to both languages only after receiving answers/evidence.

| Item | Current state | Required decision/evidence | Destination |
| --- | --- | --- | --- |
| Product name / actual identity | Folimeld MSIX name transfer awaits Microsoft | Official process and three identity values | Store configuration, final manifest, listing |
| Official publisher | Undecided; development manifest display name is not authoritative | User-selected public name consistent with Partner Center | Policy, listing |
| Support contact | Undecided | Public email/URL, supported languages and operator | Policy, Store contact |
| Support information handling | Undecided | Retention, storage and deletion; review a default of not requesting documents/passwords | Policy, support guidance |
| Privacy policy URL | Japanese/English drafts exist; destination undecided | Hosting choice, contact/effective date and final-package consistency | Store information, both policies |
| Support/product website | Undecided | A user-controlled public destination; decide how reserved `docs/` is used if choosing GitHub Pages | Store URLs |
| Corresponding source publication | Build ZIPs/association JSON and dependency sources saved locally | Final-artifact sources hosted, download/hash verification and overall dependency review | Releases, licensing guidance |
| App price / supporter purchases | Editing is not gated by in-app purchase; app price/initial purchase offering undecided | User's sales policy; actual Store tests if included, otherwise align entry points and listing | App, add-on, listing |
| Markets / category / age rating | Undecided; Productivity is a candidate | User's markets and answers to actual rating questionnaire | Partner Center |
| Supported platform | Initially Windows 11 x64 | Dynabook tests, final MSIX acceptance/WACK; ARM64 needs separate hardware evidence | Listing, release plan |
| Release date | Undecided; PC delivery expected 2026-10-30 is not a release date | Microsoft response, decisions, tests and dependency review completed | Publication settings, announcement |

Bundle the first decision request around four items: official publisher, public support contact, app price/supporter policy and hosting destination. Continue copy/procedure preparation while answers are pending. Do not automatically repurpose the migration inquiry's sender as the public contact.

Related: [release plan](windows-store-release-plan.md), [listing](windows-store-listing.md), [privacy draft](privacy-policy.md), [license/distribution](license-distribution_ja.md).
