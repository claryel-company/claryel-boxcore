# Publish CLARYEL project knowledge

This composite action publishes one active CLARYEL repository into the local knowledge plane on CLARYEL01.

## Security model

The caller uses its own short-lived repository-scoped `GITHUB_TOKEN`. No organization-wide personal access token is stored on the server. The action checks out and reads only the calling repository, then uses the already governed Agent Fabric container to reach the authenticated local Knowledge API and PostgreSQL.

The publisher excludes archived repositories, secret-bearing paths, environment files, private keys, model weights, dependency trees, generated build output and oversized files. Probable inline credentials are redacted before indexing. Source text, extracted chunks, generated answers and credential values are not retained in workflow evidence.

## Published sources

The collector includes repository documentation, instructions, ADRs, architecture, decisions, RFCs, runbooks, plans, roadmaps, policies, schema and migration descriptions, OpenAPI definitions, Compose manifests and governed workflow files. Unsupported text formats are wrapped in Markdown with source path, revision and SHA-256 metadata. PDF, DOCX and XLSX documents are passed to the native Knowledge API extractors.

Repository metadata, the 100 most recently updated issues, pull requests and releases are rendered as separate governed documents. Open issues are deterministically projected into `next_steps`. Architecture and decision files are projected into `architecture_records`; migrations and interface descriptions into `schema_assets`; repository purpose into `repository_contexts`.

## Versioning

Each logical source has a stable `knowledge_sources.source_key`. An unchanged source SHA-256 updates `last_seen_at` without re-embedding. A changed source is scanned, encrypted, parsed and embedded before PostgreSQL switches the current source version. The previous vector is removed only after the new version is accepted. Historical encrypted objects remain available for controlled audit unless a separate purge policy applies.

A complete authoritative run marks disappeared files as missing and removes their current vectors while retaining source history. Per-source failure leaves the previous accepted version current.

## Caller example

```yaml
permissions:
  contents: read
  issues: read
  pull-requests: read

jobs:
  publish:
    runs-on: [self-hosted, linux, x64, claryel-deploy]
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - uses: claryel-company/claryel-boxcore/.github/actions/publish-project-knowledge@<PINNED_COMMIT>
        with:
          github-token: ${{ github.token }}
          repository: ${{ github.repository }}
          revision: ${{ github.sha }}
          default-branch: ${{ github.event.repository.default_branch }}
          visibility: private
          trigger-kind: push
```

The caller must pin an exact accepted commit. Repository workflows run on default-branch pushes, once daily for reconciliation, and manually on demand.
