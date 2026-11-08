# The GB-POL code scheme

`GB-POL` = **GB** (ISO 3166 — the United Kingdom, including Northern Ireland) **POL**ice forces. (Proposed org-id.guide scheme prefix; not yet registered.)

## What gets a code

A police **force** is the entity. A `GB-POL` code is minted for every force that has **no usable existing identifier**. A force that already holds an identifier in a standard register (the government-organisation register `GB-GOR`, Companies House, the Charity Commission, etc.) is **referenced** to that identifier, not minted — its `org_id` is the external code, not a `GB-POL` number. ROR (`XI-ROR`) identifiers do not count as a usable principal identifier (see README).

## Code format

```
GB-POL-#####
```

Five-digit, zero-padded sequence. Codes are:

- **Opaque.** They carry no geographic or alphabetical meaning. The ONS Police Force Area code (`PFA25CD`, e.g. `E23000013`) is carried alongside in `ons_police_force_area_code` as a lookup, never as the identifier.
- **Permanent and frozen.** The assignment lives in [`source/code_assignments.csv`](source/code_assignments.csv). A code, once issued, is never reissued or renumbered — even if a force is renamed, merged or dissolved. The builder reads the frozen ledger; new forces append the next number. Adding a force never reshuffles existing codes.
- **Withdrawn codes are retained.** `GB-POL-00030` was issued to PSNI, then withdrawn when PSNI was found to hold `GB-GOR-OT657` and re-keyed as a reference. `00030` is kept in the ledger as withdrawn and is never reused; the sequence carries a deliberate gap.

## Referenced forces (not minted)

| Force | Keyed to |
|---|---|
| Police Service of Northern Ireland | `GB-GOR-OT657` |
| Civil Nuclear Constabulary | `GB-GOR-OT1063` |

## Relationship to other schemes

- **Sideways:** `ons_police_force_area_code` links to ONS Police Force Area geography (`PFA25CD`).
- **Governance:** `paired_id` links each force to its OPCC / police-governance body in the `GB-OPCC` register (or to that body's external id where referenced).

## Fields (`data/register.csv`)

`org_id`, `name`, `body_type` (`force`), `police_force_area`, `ons_police_force_area_code`, `paired_id`, `pcc_function_held_by`, `status`, `issued_by`, `date_issued`, `evidence`, `notes`.
