## Proposed list: GB-POL — UK Police Forces

### Proposed list code
`GB-POL` — jurisdiction `GB` (ISO 3166, the United Kingdom incl. Northern Ireland) + list-name code `POL`.

### Name
UK Police Forces (RCVDA register)

### Managed by
Redcar & Cleveland Voluntary Development Agency (RCVDA), a UK charity (Charity No. 1135959). Published openly on GitHub.

### Description
Open identifiers for UK police forces — the 43 territorial forces of England & Wales, Police Scotland, the Police Service of Northern Ireland, and the UK-wide non-territorial forces (British Transport Police, Civil Nuclear Constabulary, Ministry of Defence Police). A `GB-POL` code is minted **only** where a force has no usable existing identifier; a force that already holds one is **referenced** to it, not minted (e.g. PSNI → `GB-GOR-OT657`, Civil Nuclear Constabulary → `GB-GOR-OT1063`). Territorial police forces are statutory bodies / corporations sole with no charity number, company number, or (for most) government-organisation code, so they otherwise fall through the gap of the existing identifier schemes.

### Geographic coverage
GB (the United Kingdom, including Northern Ireland).

### Legal structure
Statutory body / corporation sole.

### Sector
Policing.

### List type
Third-party.

### Information about the list
https://github.com/rcvda/police-force-names-and-codes

### Looking up identifiers / open-data copy
Open CSV: https://github.com/rcvda/police-force-names-and-codes/blob/main/data/register.csv — look up the force by name/area; the `org_id` column holds the `GB-POL` code. Archived with a DOI: https://doi.org/10.5281/zenodo.24063717

### Licence
Open Government Licence v3.0 (the data derives from the police.uk `/forces` API and ONS, both OGL).

### Example identifier (verified)
`GB-POL-00006` — Cleveland Police. Minted by RCVDA; Cleveland Police has no charity number, company number, or government-organisation (GB-GOR) code — a genuine identifier gap. Also recorded in RCVDA's CRM.

### Relevance
Used for linking UK voluntary-sector and public-sector organisation data, in the same ecosystem as Find That Charity and 360Giving. Sibling to RCVDA's police & crime commissioner register (proposed `GB-OPCC`, submitted alongside this one), and modelled on mySociety's `uk_local_authority_names_and_codes`.
