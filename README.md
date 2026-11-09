# UK Police Forces — Names and Codes (GB-POL)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24063717.svg)](https://doi.org/10.5281/zenodo.24063717)

An open, coded register of **UK police forces** — the 43 territorial forces of England & Wales, Police Scotland, the Police Service of Northern Ireland, and the UK-wide non-territorial forces — with an identifier for each body that has no usable identifier of its own.

> **Status: work in progress.** The `GB-POL` scheme is **not yet registered** with [org-id.guide](https://org-id.guide). See [Roadmap](#roadmap).

## Why this exists

A territorial police force (since 2011 the Chief Constable is a corporation sole) has no charity number, no company number, and — for most forces — no clean government-organisation code. They fall through the gap of the national identifier schemes, exactly the condition this register fills. It is the direct parallel of RCVDA's parish-council register (`GB-PCE`) and is built on the same principles as mySociety's `uk_local_authority_names_and_codes`.

Police and Crime Commissioners / OPCCs are a distinct class of body and live in the sibling register, **[opcc-names-and-codes](../opcc-names-and-codes)** (`GB-OPCC`). Each force row cross-references its governance body via `paired_id`.

## Mint only genuine gaps

A `GB-POL` code is minted **only** where a force has no usable existing identifier. A force that already holds an identifier in a standard register is **referenced**, not minted:

- **Police Service of Northern Ireland** → referenced `GB-GOR-OT657` (holds a government-organisation code).
- **Civil Nuclear Constabulary** → referenced `GB-GOR-OT1063`.

ROR (Research Organization Registry) identifiers are **not** treated as a usable principal identifier for this purpose: several forces carry a `XI-ROR` id incidentally, but ROR is an international research-sector registry, not a UK statutory/principal register, so those forces are still minted.

## Coverage

All 43 England & Wales territorial forces, Police Scotland, PSNI, plus the UK-wide non-territorial forces (British Transport Police, Civil Nuclear Constabulary, Ministry of Defence Police). 46 `GB-POL` mints, 2 referenced forces.

## Data

| File | What it is |
|------|-----------|
| [`data/register.csv`](data/register.csv) | The register: one row per force, with its `GB-POL` code (or the referenced external id), area, ONS PFA code, and paired governance body. |
| [`source/police_uk_forces.json`](source/police_uk_forces.json) | The authoritative force list, from the police.uk `/forces` API. |
| [`source/additional_forces.json`](source/additional_forces.json) | Forces not on police.uk `/forces` (Police Scotland, BTP, Civil Nuclear, MoD Police). |
| [`source/pfa_names_codes_2025.csv`](source/pfa_names_codes_2025.csv) | ONS Police Force Areas (December 2025) Names and Codes. |
| [`source/code_assignments.csv`](source/code_assignments.csv) | The permanence ledger — the frozen code assigned to each body. Codes are never reissued or renumbered; a withdrawn code (e.g. `GB-POL-00030`, PSNI before it was referenced) is retained here and never reused. |
| [`source/gb_gor_government-organisation.csv`](source/gb_gor_government-organisation.csv) | Held copy of the GB-GOR government-organisation register, used to cross-check that no mint duplicates an existing identifier. |

## How the data is built

`build_register.py` reads the sources, joins the ONS PFA code by area name, applies the mint-vs-reference rule, and reads the frozen codes from `code_assignments.csv`. See [METHODOLOGY.md](METHODOLOGY.md). Codes are **allocated once and frozen** — see [CODESCHEME.md](CODESCHEME.md).

To regenerate:

```
python3 source/build_register.py source/police_uk_forces.json data/register.csv
```

## Licence

Open Government Licence v3.0 — see [LICENSE](LICENSE).

## Roadmap

1. Hold and maintain the register (done).
2. Register the `GB-POL` scheme with [org-id.guide](https://org-id.guide) once coverage and maintenance are settled.

Note: the January 2026 police reform White Paper ("From local to national") proposes merging forces into ~12 regional bodies and creating a National Police Service. If enacted, superseded forces will be retired (code kept, status updated) and new bodies minted or referenced; nothing is renumbered.

## Author and maintainer

Created and maintained by Peter Neal at Redcar & Cleveland Voluntary Development Agency (RCVDA). Corrections welcome via issues/PRs.
