import json, csv, sys, os
SCHEME = "force"
SRC = sys.argv[1] if len(sys.argv) > 1 else "source/police_uk_forces.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "data/register.csv"
SDIR = os.path.dirname(SRC) or "."
PFA = os.path.join(SDIR, "pfa_names_codes_2025.csv")
ADD = os.path.join(SDIR, "additional_forces.json")
CODES = os.path.join(SDIR, "code_assignments.csv")
TODAY = "2026-11-08"

forces = json.load(open(SRC))
if os.path.exists(ADD): forces = forces + json.load(open(ADD))
assign = {r["force_id"]: {"gb_pol": r["gb_pol"], "gb_opcc": r["gb_opcc"]} for r in csv.DictReader(open(CODES))}

def norm(s): return " ".join(s.lower().replace("&", "and").split())
pfa_by_name = {norm(r["PFA25NM"]): r["PFA25CD"] for r in csv.DictReader(open(PFA))}
PFA_ALIAS = {"metropolitan police district":"Metropolitan Police","city of london":"London, City of",
             "devon and cornwall":"Devon & Cornwall","northern ireland":"Police Service of Northern Ireland","scotland":"Scotland"}
def pfa_code(area): return pfa_by_name.get(norm(PFA_ALIAS.get(norm(area), area)), "")

AREA = {"metropolitan":"Metropolitan Police District","city-of-london":"City of London",
        "northern-ireland":"Northern Ireland","devon-and-cornwall":"Devon and Cornwall"}
def area_of(f):
    if f.get("area"): return f["area"]
    fid, name = f["id"], f["name"]
    if fid in AREA: return AREA[fid]
    for suf in (" Constabulary", " Police Service", " Police"):
        if name.endswith(suf): return name[:-len(suf)]
    return name

SPECIAL = {
 "metropolitan":("Mayor's Office for Policing and Crime (MOPAC)",True,"Mayor of London",""),
 "city-of-london":("City of London Corporation (Court of Common Council)",False,"City of London Corporation","GB-LAE-LND"),
 "greater-manchester":("Greater Manchester Combined Authority",False,"Mayor of Greater Manchester","GB-LAE-GMCA"),
 "west-yorkshire":("West Yorkshire Combined Authority",False,"Mayor of West Yorkshire","GB-UKLA-WYCA"),
 "south-yorkshire":("South Yorkshire Mayoral Combined Authority",False,"Mayor of South Yorkshire","GB-LAE-SCR"),
 "north-yorkshire":("York and North Yorkshire Combined Authority",False,"Mayor of York and North Yorkshire","GB-UKLA-YNYC"),
 "northern-ireland":("Northern Ireland Policing Board",False,"NI Policing Board / Department of Justice","GB-GOR-OT649"),
 "police-scotland":("Scottish Police Authority",True,"Scottish Police Authority",""),
 "civil-nuclear":("Civil Nuclear Police Authority",False,"Civil Nuclear Police Authority","GB-GOR-PB194"),
 "british-transport":("British Transport Police Authority",False,"British Transport Police Authority","GB-GOR-PB461"),
}
HDR = ["org_id","name","body_type","police_force_area","ons_police_force_area_code","paired_id",
       "pcc_function_held_by","status","issued_by","date_issued","evidence","notes"]

def polnum(code): return int(code.split("-")[-1]) if code.startswith("GB-POL-") else 10**6
ordered = sorted(forces, key=lambda f: (polnum(assign.get(f["id"],{}).get("gb_pol","")), area_of(f).lower()))

force_rows=[]; opcc_rows=[]
for f in ordered:
    fid=f["id"]; fname=f["name"]; area=area_of(f)
    code = "" if f.get("non_territorial") else pfa_code(area)
    pol_id = assign.get(fid,{}).get("gb_pol","")
    pol_ref = not pol_id.startswith("GB-POL-")
    opcc_name, mint, holder, ext_id = SPECIAL.get(fid,
        (f"Office of the Police and Crime Commissioner for {area}", True, "Police and Crime Commissioner", ""))
    opcc_id = (assign.get(fid,{}).get("gb_opcc","") if mint else ext_id)
    fpaired = opcc_id or "(see paired OPCC row)"
    if pol_ref:
        fevid = f"{fname}; existing identifier {pol_id}; non-territorial GB-wide force."
        fnote = f"Referenced, not minted: holds {pol_id}. Oversight: {opcc_name} ({opcc_id})."
    elif f.get("non_territorial"):
        fevid = f"Non-territorial GB-wide police force. RCVDA-minted {pol_id} (no separate register identity; genuine gap)."
        fnote = f"RCVDA-minted: non-territorial force. Oversight: {opcc_name} ({opcc_id})."
    elif fid == "police-scotland":
        fevid = f"Territorial national force for Scotland (Police Scotland, since 2013). ONS PFA {code} (Dec 2025)."
        fnote = "Scotland jurisdiction; single national force."
    else:
        fevid = f"Territorial police force (police.uk /forces, authoritative). ONS PFA {code} (Dec 2025)."
        fnote = "PSNI = Northern Ireland jurisdiction" if fid=="northern-ireland" else ""
    force_rows.append([pol_id, fname, "force", area, code, fpaired, holder, "Active", "RCVDA", TODAY, fevid, fnote])

    if mint:
        if fid=="metropolitan":
            onote="RCVDA-minted: London OPCC-equivalent (MOPAC), corporation sole, no register ID (genuine gap)."
        elif fid=="police-scotland":
            onote="RCVDA-minted: Scotland's police governance body (Scottish Police Authority); statutory body, no company/charity/GB-GOR ID (genuine gap)."
        else:
            onote="RCVDA-minted: statutory corporation sole, no company/charity register ID (genuine gap)."
        oevid=f"PCC/OPCC for {area}; no charity/company/GB-GOR registration; keyed by RCVDA."+((" ONS PFA "+code+" (Dec 2025).") if code else "")
    else:
        onote=f"NOT minted: governance held by {opcc_name}, an existing identifiable body; keyed to its own ID {opcc_id}."
        oevid=f"Police governance for {area} held by {holder}; keyed to {opcc_name} ({opcc_id})."+((" ONS PFA "+code+" (Dec 2025).") if code else "")
    opcc_rows.append([opcc_id, opcc_name, "opcc", area, code, pol_id, holder, "Active", "RCVDA", TODAY, oevid, onote])

out_rows = force_rows if SCHEME=="force" else opcc_rows
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT,"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(HDR); w.writerows(out_rows)
if SCHEME=="force":
    m=sum(1 for r in out_rows if str(r[0]).startswith("GB-POL-")); rf=len(out_rows)-m
    print(f"rows:{len(out_rows)} GB-POL minted:{m} referenced:{rf}")
else:
    m=sum(1 for r in out_rows if str(r[0]).startswith("GB-OPCC-")); rf=sum(1 for r in out_rows if r[0] and not str(r[0]).startswith("GB-OPCC-"))
    print(f"rows:{len(out_rows)} GB-OPCC minted:{m} referenced:{rf}")
