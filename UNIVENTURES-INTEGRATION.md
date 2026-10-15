# Local Agent integration: n1.dev

This host-specific candidate merges upstream0d1568b6c1796d190d37b925029958983e94047a onto preserve/2026-10-15/n1.dev. Its historical source ref is unchanged. This branch is not a common fleet release and must not be deployed to other hosts by default.

Ordinary backups accept nested auth.ENDPOINT_URL and legacy outer endpoint_url, preserving region and credentials. Native build preparation includes the cached-app helper used by the paired Press Dockerfile. f2/f3 additionally retain archive-upload compatibility in a separate legacy builder module. Existing host-specific Redis, container, Code Server, grants, TLS, SSH and branding patches remain scoped to their original variants. Upstream already provides safe list/dict timeout parsing, replacing f21's older workaround.

Historical adjacent backups are retained in preservation history and omitted from this runtime tree. These commits remain local and unpushed. Source parses and focused method contracts are tested in the paired Press integration. No full Linux Agent dependency install, real Docker build, remote provisioning or host upgrade is certified by those checks. See the paired Press UNIVENTURES-UPSTREAM-INTEGRATION.md and workspace inventory/upstream-integration-20261015 for compatibility boundaries and release gates. Production unchanged; release HOLD.
