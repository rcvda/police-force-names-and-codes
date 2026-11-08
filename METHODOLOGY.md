# Methodology

How the registers are built. Every row is reproducible from authoritative, openly-licensed sources, not hand-keyed.

## Sources

1. **police.uk `/forces` API** — the authoritative list of the 43 England & Wales territorial forces plus PSNI. Pulled into `source/police_uk_forces.json`.
2. **Forces not on that list** — Police Scotland, British Transport Police, Civil Nuclear Constabulary, Ministry of Defence Police — held in `source/additional_forces.json` (policing is devolved in Scotland, so Police Scotland is not on police.uk; the others are UK-wide non-territorial forces).
3. **ONS Police Force Areas (December 2025) Names and Codes** (Open Geography Portal) — `PFA25CD` / `PFA25NM`, held in `source/pfa_names_codes_2025.csv`. Provides the `ons_police_force_area_code`. Vintage changes annually.
4. **UK government-organisation register (GB-GOR)** — held in `source/gb_gor_government-organisation.csv`, used to (a) reference bodies that already have a code and (b) cross-check that no mint duplicates an existing identifier.

## Build

`build_register.py` reads the sources, derives each force area, joins the ONS PFA code by area name (with a small alias map: Metropolitan Police District, City of London, Devon & Cornwall, Northern Ireland, Scotland), applies the mint-vs-reference rule, and reads the frozen codes from `source/code_assignments.csv`. The forces register emits `body_type=force` rows; the OPCC register emits `body_type=opcc` rows. Both are produced by the same script.

Reproduce:

```
python3 source/build_register.py source/police_uk_forces.json data/register.csv
```

## GB-GOR cross-check

Every mint was checked against the GB-GOR register (held in `source/`). Findings applied: PSNI holds `GB-GOR-OT657` → referenced, not minted (`GB-POL-00030` withdrawn); British Transport Police Authority (`GB-GOR-PB461`), Civil Nuclear Constabulary (`GB-GOR-OT1063`) and Civil Nuclear Police Authority (`GB-GOR-PB194`) referenced. ROR (`XI-ROR`) matches are not treated as usable principal identifiers. The Ministry of Defence Police has only a defunct code (`GB-GOR-EA693`, the MoD Police and Guarding Agency, removed 2013), so the current force is minted as a genuine gap.
