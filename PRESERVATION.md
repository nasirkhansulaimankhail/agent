# UniVentures Agent source preservation

Captured 15 October 2026. This fork preserves deployed source without upgrading it or changing production remotes. Snapshot branches retain their original upstream parents, tracked changes and untracked source backup files, byte for byte. File modes and SHA256 values were verified before push.

This landing branch uses the f3 builder snapshot and adds documentation. It is NOT a unified Agent release: other hosts have different bases and patches. Use the per-host branches to inspect their exact source. Do not deploy this landing branch across the fleet.

| Host | Snapshot branch | Upstream base | Snapshot commit | Changed paths |
| --- | --- | --- | --- | --- |
| f1.dev.univenturescloud.com | `preserve/2026-10-15/f1.dev` | `185054c73be9` | `4195c50c2869` | 14 |
| f1.univenturescloud.com | `preserve/2026-10-15/f1` | `38bdef47c385` | `0fdfecf18d68` | 14 |
| f2.univenturescloud.com | `preserve/2026-10-15/f2` | `bfc93524151d` | `a951ebc688ad` | 14 |
| f21.univenturescloud.com | `preserve/2026-10-15/f21` | `2a412bc2b129` | `1926599b4823` | 9 |
| f3.univenturescloud.com | `preserve/2026-10-15/f3` | `bfc93524151d` | `e4960322fb12` | 15 |
| l1.univenturescloud.com | `preserve/2026-10-15/l1` | `cc3f61b8d042` | `cc3f61b8d042` | 0 |
| m1.dev.univenturescloud.com | `preserve/2026-10-15/m1.dev` | `185054c73be9` | `0b4ed06b04c7` | 1 |
| m1.univenturescloud.com | `preserve/2026-10-15/m1` | `38bdef47c385` | `dd7cbd8e1ea6` | 2 |
| m2.univenturescloud.com | `preserve/2026-10-15/m2` | `bfc93524151d` | `61f74b0d84ed` | 8 |
| ms1.univenturescloud.com | `preserve/2026-10-15/ms1` | `38bdef47c385` | `38bdef47c385` | 0 |
| n1.dev.univenturescloud.com | `preserve/2026-10-15/n1.dev` | `185054c73be9` | `401e58590ddd` | 3 |
| n1.univenturescloud.com | `preserve/2026-10-15/n1` | `38bdef47c385` | `be4a1f6715cc` | 2 |
| n2.univenturescloud.com | `preserve/2026-10-15/n2` | `bfc93524151d` | `7636769e065a` | 14 |
| naya-f1.univenturescloud.com | `preserve/2026-10-15/naya-f1` | `185054c73be9` | `4c7b1666a5d7` | 5 |
| naya-n1.univenturescloud.com | `preserve/2026-10-15/naya-n1` | `185054c73be9` | `06a360f124bc` | 1 |
| r2.univenturescloud.com | `preserve/2026-10-15/r2` | `bfc93524151d` | `3999d213cb7f` | 8 |

Machine-readable file hashes and provenance are in `preservation/snapshots.json`. Clean Agent hosts point directly at their deployed base commit.

## Preservation scope

Includes all Git-tracked modifications/deletions and all untracked files reported by Git at capture time, including adjacent historical source backups. The production repositories were only read. Files ignored by Git, databases, credentials, site configuration, certificates, containers, Code Server runtime caches and host configuration are not included. These require protected backups through the separate pre-upgrade process. This source snapshot is not a complete production backup.

## Future work

Keep snapshot branches as historical records. Extract suitable business behavior into a custom Frappe app and maintain focused integration commits in these forks. Resolve upstream compatibility and complete isolated staging before creating any deployable upgrade release. No deployment or update automation was enabled for preservation.
