# Native host SDK admission

The native workflow has two explicit profiles. Archived schema-1 requests,
stages and transports retain SDK `45171a099a6a658c52ab689501de646a28485653`.
They remain readable for custody, while the current staging API refuses new
production from that historical request before reading inputs or writing output.
Schema 2 is bound to this release's current Git pin in `publication_wire.CURRENT_SDK_COMMIT`,
which must agree with `pyproject.toml`, `uv.lock` and the actual normal install.
Crossed schema/pin pairs refuse.

Before a new stage, application policy calls public
`blake.methods.installed.verify_installed_git`. The shared verifier checks the
actual Git installation metadata, complete package RECORD bytes and imported
module origins. Entomology owns the allowed pin and stage policy; no generic
provenance algorithm is duplicated here. Editable installs and source overlays
cannot qualify this production boundary.

After locked installation, the bounded host check is:

```bash
uv run --locked python -c 'from blake.methods.installed import verify_installed_git; from blakean_entomology.publication_wire import CURRENT_SDK_COMMIT; print(verify_installed_git("blake", CURRENT_SDK_COMMIT).model_dump_json())'
```

This command checks software identity only. A new stage requires a freshly
source-pinned schema-2 request, an unused private output epoch and supported
admission. `prepare_native_stage` checks the SDK before touching producer inputs,
rechecks it before closing the stage, writes `installed-sdk.json`, and carries
the request's selected pin and exact host receipt into `native-stage.json` and
the hash-bound transport inventory. An identity change or malformed/missing
transport member refuses; failed epochs remain retained.

The staging policy compares complete before/after SDK observations, including the imported-module set. A larger import footprint conservatively refuses that stage; this is not a claim that package bytes changed. A later SDK adoption must introduce another explicit profile while retaining prior profile bindings.

The separately selected template runtime intentionally imports neither Blake
nor Pydantic. Its stdlib transport verifies the host receipt's bound membership,
size and bytes, while existing template/source checks remain in force. The
native result distinguishes the declared SDK selection from observed host-SDK
evidence. Schema 1 has no installed host receipt and earns no inferred host
verification. The template worker's own runtime/imported-template checks are
separate evidence.

Git metadata and RECORD supply local consistency, not authenticated proof of a
remote tree or protection from a malicious same-user writer. Installed-source
equality is qualified separately against the reviewed Git source. A host check
does not qualify future imports, graphical output, PDF/HTML, scientific claims, rights or release readiness.

This software change preserves the five authored native inputs and retained
40-page PDF byte-for-byte. It invokes no native writer, renews no consumed grant
and does not relabel that edition's producer. The next current-SDK render must
have its own request/admission/output epoch, actual pinned template API run and
independent complete PDF/HTML acceptance before any replacement in Downloads.
See the [render guide](manuscript/README.md) and [current status](PROJECT_STATUS.md).

The [0.6.0 software qualification](../research/native-sdk-admission-20261031.json)
records the exact published Git selection, fresh normal installation and 353
tests. Actual installed admission succeeds; a real shadow-import child and
crossed request/stage/receipt profiles refuse. These checks close E-N01, while a
current-SDK render and physical/browser acceptance remain E-N02.
