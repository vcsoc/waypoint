# Upstream baseline

Review date: 2026-10-09

The inspected fork baseline is `5d207d85ee547bc323d704bc6aaab901aa0be8b6`, retrieved through the existing checkout and confirmed through the upstream GitHub commit API. Source: https://github.com/BerriAI/litellm/commit/5d207d85ee547bc323d704bc6aaab901aa0be8b6. GitHub records the commit date as 2026-10-08T22:38:38Z

The local branch tip before uncommitted licensing work is `085b721ec41ffa24565bc941b2843b1b216127f6`. It includes the local ChatGPT Compose stack and host database mount. Licensing changes are additional uncommitted development work. The specification's research SHA is a separate historical reference, not this checkout's baseline

This baseline is chosen to document the current working installation, not as a supported production release recommendation. Selecting and validating a production baseline is still pending P0

| License file at baseline | SHA-256 |
| --- | --- |
| LICENSE | b170d6bf8e8835dd357e011681db028f4d51e2fb0ea892058f56e01fb39b8273 |
| enterprise/LICENSE.md | a3160d1176cb556447255ca8652855486d681f8025550291828796a439e1b2f9 |

The root license gives MIT terms to content outside its enterprise exclusion. The actual enterprise license file restricts production and redistribution; the root reference to a different filename does not remove those terms

Current development build inputs are `Dockerfile`, `pyproject.toml`, `uv.lock`, the enterprise and proxy-extras workspace packages, the dashboard package lock/source, and the embedded LiteAdmin build inputs. Their base image digests and download hashes are recorded in those files. The development image still contains mixed-license components and is not an approved Waypoint release artifact

Required remaining evidence: complete source/dependency/asset classification, supported baseline rationale, approved build inputs, final image/wheel inspection, release SBOM and reproducible artifact manifest
