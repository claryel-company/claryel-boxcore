# Prepared self-hosted runner migration

Status: prepared, not deployed.

Target runner groups: `claryel-build` for trusted branches and `claryel-public-safe` or GitHub-hosted runners for untrusted public pull requests.

Activation will add path filters, concurrency cancellation and short artifact retention while preventing public pull-request code from reaching production secrets or the local network.

No workflow on `main` is changed by this branch.
