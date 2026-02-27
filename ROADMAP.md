# Roadmap

This roadmap tracks the Python SDK modernization work in strict sequence.

## Sequence

1. Add structural docs (`ROADMAP.md`, `CHANGELOG.md`, `EXAMPLEs.md`, `AI_INSTRUCTIONS.md` updates).
2. Define Python support policy (supported Python versions and test matrix).
3. Set package/version source of truth and align SDK/package versioning.
4. Add CI quality gates (lint, tests, build, install smoke test).
5. Document Python release mechanics (build, twine, TestPyPI/PyPI workflow, credentials).
6. Rewrite `README.md` to introduce Mailinator, link docs, and provide high-level SDK usage guidance.
7. Move detailed example code out of `README.md` into `EXAMPLEs.md`.
8. Update outdated dependencies.
9. Update version number.
10. Publish these documentation/dependency/version updates as a minor release.
11. Rewrite remaining JS-specific sections in `AI_INSTRUCTIONS.md` (especially gap-analysis workflow) for Python.
12. Define a repeatable gap-analysis report format (missing operations, URL mismatches, query/model gaps, planned fixes).
13. Run gap analysis against the OpenAPI specification and produce a prioritized implementation plan.
14. Mark deprecated endpoints as deprecated in code so users are warned. ✅ Completed for rules endpoints.
15. Fix URL path inconsistencies between the SDK and OpenAPI specification.
16. Add optional `delete` query parameter to Get Inbox method.
17. Implement Streaming Messages endpoint support (`/domains/private/stream/` and `/domains/private/stream/{inbox}`) with documented query parameters.
18. Document compatibility/migration notes in `CHANGELOG.md` and README for endpoint/deprecation changes.
19. Publish the API-alignment changes.

## Current Status

- [x] Step 1 complete.
- [x] Step 3 complete.
- [x] Step 6 complete.
- [x] Step 7 complete.
- [x] Step 11 complete.
- [ ] Steps 2, 4-5 pending.
- [ ] Steps 8-10 pending.
- [ ] Steps 12-13 pending.
- [x] Step 14 complete (rules endpoints now emit deprecation warnings).
- [ ] Steps 15-19 pending.
