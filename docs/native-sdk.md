# Native host SDK admission

Native records have three explicit schema/SDK profiles. The schema is a
transport contract, not the application's paper version.

| Native schema | Exact SDK Git selection | SDK version in the profile | New production |
|---|---|---|---|
| 1 | `45171a099a6a658c52ab689501de646a28485653` | 0.5.0 | Refused; retained records remain readable |
| 2 | `d34876e021a8f2e654b96f1c23f7ec43d8d958c2` | 0.6.0 | Refused; retained records remain readable |
| 3 | `263d7c83abe6f1309a64af3285a683c1b7672269` | 0.7.0 | Current production profile |

[The source registry](../src/blakean_entomology/publication_profiles.py) owns
these immutable pairs. Booleans, unsupported future schemas and crossed
schema/pin pairs refuse. Current `pyproject.toml`, `uv.lock` and the actual
normal installation must agree with profile 3. Historical records retain their
original evidence; a declared profile supplies no retroactive installed proof.

The schema-1 table records the registry's declared version 0.5.0. The original
installed receipt at that Git selection observed Blake 0.4.0, as retained in
[project lineage](project-lineage.md) and the
[earlier native qualification](../research/template-native-20261030.json).
Keep declared legacy profile metadata separate from the observed historical
producer; neither is a new installation claim. Current schema 3 is unchanged.

## Host admission

Before producer input access or output reservation, application policy calls
public `blake.methods.installed.verify_installed_git`. That reusable verifier
checks actual Git installation metadata, complete package RECORD bytes and
imported-module origins. Entomology owns the allowed profile and staging policy.
Editable installs and source overlays cannot qualify this production boundary.

After locked installation, the bounded host check is:

~~~bash
uv run --locked python -c 'from blake.methods.installed import verify_installed_git; from blakean_entomology.publication_profiles import CURRENT_SDK_COMMIT; print(verify_installed_git("blake", CURRENT_SDK_COMMIT).model_dump_json())'
~~~

A new stage needs a freshly source-pinned **schema-3 request**, unused private
output epoch and applicable supported admission. `prepare_native_stage`
checks the SDK before inputs and again before closing the stage, writes
`installed-sdk.json`, and binds the exact request, host receipt and stage in
the transport inventory. Missing/malformed members or identity changes refuse;
failed epochs stay retained.

The staging policy compares complete before/after SDK observations, including
the imported-module set. A larger import footprint conservatively refuses that
stage; it does not prove package bytes changed. A later SDK adoption requires a
new explicit profile and qualification, preserving all preceding profiles.

## Separate template runtime

The selected template worker intentionally imports neither Blake nor Pydantic.
Its stdlib transport receives the exact schema, checks the profile and verifies
the host receipt's membership, size, bytes, version and pin. Schemas 2 and 3
require their own selected installed receipt. Schema 1 has no host receipt and
earns no inferred host verification.

The template source is separately pinned at
`efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8`.
Actual writer runtime prefixes and imported-template sources are distinct from
host-SDK evidence. The result records the declared and observed SDK selections,
actual writers, resolved metadata, input checks and output hashes.

Git metadata and RECORD establish local consistency, not authenticated remote
tree identity or protection from a malicious same-user writer. Installed-source
equality against reviewed Git bytes is a separate check. Host admission does
not qualify future imports, PDF/HTML layout, scientific interpretation,
accessibility, rights or release readiness.

## Current and retained qualifications

Current software and its normal installed qualification are identified by
[project status](PROJECT_STATUS.md) and
[the canonical installed record](../research/visual-installed-20261102.json).

The retained 0.7.0 normal installation passed 436 tests and the separate
application/tool floors. Its
[preserved status](../research/history/visual-revision-20261102/PROJECT_STATUS.md)
and [methods/manuscript record](../research/methods-manuscript-20261101.json)
identify that exact epoch. Installed admission and shadow-import/crossed-profile
refusals remain separate controls.

The [0.6.0 qualification](../research/native-sdk-admission-20261031.json)
retains its exact schema-2 source selection, installation, 353 tests and
refusing controls. Earlier schema-1 paper and producer records remain unchanged.
None is relabelled as profile 3.

For a replacement paper, follow [native production](manuscript/README.md):
prepare a new closed article, declare all nine pinned native inputs, execute the
actual template API, and obtain complete physical-page and HTML acceptance.
A software pass or an old one-shot admission does not authorize or qualify a
new native epoch. Downloads replacement and private-main publication have
separate exact-byte delivery records.
