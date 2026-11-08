# Contributing

Corrections and additions welcome via issue or pull request.

## Principles

- **Mint only genuine gaps.** A body that already holds an identifier in a standard register (GB-GOR, Companies House, Charity Commission) is referenced to it, never given a new code. ROR identifiers do not count.
- **Codes are permanent.** Never renumber or reissue. New bodies append the next number in `source/code_assignments.csv`. A withdrawn code is retained there and never reused.
- **Authoritative sources only.** police.uk `/forces`, ONS geography, and the GB-GOR register over secondary lists. Cite the source for any change.

## Adding or changing a body

1. Add the force to `source/additional_forces.json` (if not on police.uk `/forces`).
2. Check it against `source/gb_gor_government-organisation.csv` — if it already holds a code, reference it; otherwise mint.
3. Add its frozen code to `source/code_assignments.csv` (next number for a mint; the external id for a reference).
4. Regenerate both registers with `build_register.py` and verify.
