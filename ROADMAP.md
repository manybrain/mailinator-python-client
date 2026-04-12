# Roadmap

This roadmap tracks the Python SDK modernization work in strict sequence.

## Sequence

- [ ] Define Python support policy (supported Python versions and test matrix).
- [ ] Add CI quality gates (lint, tests, build, install smoke test).
- [ ] Document Python release mechanics (build, twine, TestPyPI/PyPI workflow, credentials).
- [ ] Update outdated dependencies.
- [ ] Update version number.
- [ ] Publish these documentation/dependency/version updates as a minor release.
- [ ] Define a repeatable gap-analysis report format (missing operations, URL mismatches, query/model gaps, planned fixes).
- [ ] Run gap analysis against the OpenAPI specification and produce a prioritized implementation plan.
- [ ] Fix URL path inconsistencies between the SDK and OpenAPI specification.
- [ ] Implement Streaming Messages endpoint support (`/domains/private/stream/` and `/domains/private/stream/{inbox}`) with documented query parameters.
- [ ] Document compatibility/migration notes in `CHANGELOG.md` and README for endpoint/deprecation changes.
- [ ] Publish the API-alignment changes.
