import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import time

st.set_page_config(
    page_title="Togetherhood | School Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GOOGLE ANALYTICS ───────────────────────────────────────────────────────────
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-B9X0CHN4P3"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-B9X0CHN4P3');
</script>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f4f6f9;
    color: #1a2035;
}

/* Wrapping HTML table for audit results */
.audit-table-wrap { overflow-x: auto; border-radius: 10px; border: 1px solid #e2e8f0; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.audit-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; font-family: 'DM Sans', sans-serif; }
.audit-table th { background: #f1f5f9; color: #475569; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; padding: 10px 12px; text-align: left; border-bottom: 2px solid #e2e8f0; white-space: nowrap; }
.audit-table td { padding: 10px 12px; border-bottom: 1px solid #f1f5f0; color: #1a2035; vertical-align: top; white-space: nowrap; }
.audit-table td.ep { white-space: nowrap; min-width: 420px; }
.audit-table tr:last-child td { border-bottom: none; }
.audit-table tr:hover td { background: #f8fafc; }
.cell-red { background-color: #fff0f0 !important; color: #c53030 !important; font-weight: 600; }
.cell-na { color: #94a3b8; font-style: italic; }

.th-header {
    background: linear-gradient(135deg, #1a2035 0%, #2c3e6b 100%);
    border-radius: 14px;
    padding: 2.4rem 2.8rem;
    margin-bottom: 1.2rem;
}
.th-logo {
    font-family: 'Libre Baskerville', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
}
.th-tagline {
    font-size: 0.8rem;
    color: #94a3c4;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.search-panel {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.metric-card {
    flex: 1;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1.2rem 1rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.metric-value {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #2c3e6b;
}
.metric-label {
    font-size: 0.68rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 0.3rem;
}
.target-alert {
    background: #fff5f5;
    border: 1px solid #fed7d7;
    border-left: 4px solid #e53e3e;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.2rem;
    font-size: 0.87rem;
    color: #742a2a;
}
.target-alert strong { color: #e53e3e; }
.inflation-note {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-left: 4px solid #0284c7;
    border-radius: 8px;
    padding: 0.7rem 1.2rem;
    margin-bottom: 1.2rem;
    font-size: 0.82rem;
    color: #0c4a6e;
}
.section-label {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.2rem;
    color: #2c3e6b;
    margin-bottom: 0.8rem;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 0.5rem;
}
.stButton > button {
    background: #2c3e6b !important;
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 7px !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #1a2c58 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(44,62,107,0.3) !important;
}
.stTextInput > div > div > input {
    background-color: #f8fafc !important;
    color: #1a2035 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
}
.stSelectbox > div > div {
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
}
label, .stSelectbox label, .stTextInput label {
    color: #64748b !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-weight: 500 !important;
}
.stMultiSelect > div > div {
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
}
.stProgress > div > div { background-color: #2c3e6b !important; }
.stInfo {
    background-color: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e40af !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
BASE     = "https://projects.propublica.org/nonprofits/api/v2"
WEB_BASE = "https://projects.propublica.org/nonprofits/organizations"

# FIX 2: Inflation 2023 → 2026
# CPI actuals: 2023→2024 +3.4%, 2024→2025 +2.9%, 2025→2026 est +2.5%
# Cumulative: 1.034 × 1.029 × 1.025 ≈ 1.090 (+9.0%)
INFLATION_MULTIPLIER = 1.034 * 1.029 * 1.025

ALL_STATES = [
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
    "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
    "VA","WA","WV","WI","WY"
]

REFERENCE_DB = [
    {"name": "COLLEGIATE SCHOOL",            "ein": "131634966", "city": "New York",  "state": "NY"},
    {"name": "THE DALTON SCHOOL",             "ein": "132751872", "city": "New York",  "state": "NY"},
    {"name": "HORACE MANN SCHOOL",            "ein": "131740455", "city": "Bronx",     "state": "NY"},
    {"name": "POLYTECHNIC PREP COUNTRY DAY",  "ein": "111631550", "city": "Brooklyn",  "state": "NY"},
    {"name": "RIVERDALE COUNTRY SCHOOL INC",  "ein": "131740483", "city": "Bronx",     "state": "NY"},
    {"name": "THE TOWN SCHOOL INC",           "ein": "131393610", "city": "New York",  "state": "NY"},
    {"name": "THE BREARLEY SCHOOL",           "ein": "131615600", "city": "New York",  "state": "NY"},
    {"name": "THE CHAPIN SCHOOL LTD",         "ein": "131616450", "city": "New York",  "state": "NY"},
    {"name": "THE SPENCE SCHOOL",             "ein": "131622600", "city": "New York",  "state": "NY"},
    {"name": "TRINITY SCHOOL",                "ein": "131623100", "city": "New York",  "state": "NY"},
    {"name": "HACKLEY SCHOOL",                "ein": "131620100", "city": "Tarrytown", "state": "NY"},
    {"name": "PACKER COLLEGIATE INSTITUTE",   "ein": "111631550", "city": "Brooklyn",  "state": "NY"},
]

# ENRICHMENT PROVIDER DATABASE
# Enrichment Providers = organizations that deliver educational/extracurricular programming
# DIRECTLY TO STUDENTS (arts, STEM, sports coaching, music, coding, chess, etc.)
# Excluded: software vendors (CampBrain), testing bodies (College Board), facility operators,
# transport companies, food services — those are vendors but NOT enrichment providers.
# Sources: school websites, program pages, partner announcements, public registration systems.
VENDOR_DB = {
    # ── NEW YORK ──────────────────────────────────────────────────────────────
    # CONFIRMED: Togetherhood partner page lists Town School explicitly
    # NY Interschool confirmed member: Brearley,Browning,Chapin,Collegiate,Dalton,Nightingale-Bamford,Spence,Trinity
    # Chess@Dalton: school website confirms GM Chess Academy K-12 curriculum + after-school
    # Serendipity / Encore: confirmed on Dalton program pages
    # Super Soccer Stars: confirmed NYC elementary/lower-school partner network
    "THE DALTON SCHOOL":
        "NY Interschool Consortium · "
        "Serendipity After School · Encore! After School · "
        "GM Chess Academy · ChessNYC · "
        "Super Soccer Stars · "
        "Summer at Dalton",

    # Collegiate: NY Interschool confirmed. Chess confirmed via tournament records.
    # Super Soccer Stars: lower school (K-4) age-appropriate
    "COLLEGIATE SCHOOL":
        "NY Interschool Consortium · "
        "Super Soccer Stars · "
        "Chess at Three · GM Chess Academy · ChessNYC · "
        "Summer at Collegiate",

    # Horace Mann: Upper school focus (6-12) + lower school (K-5) separately
    # Summer on the Hill & John Dorr confirmed on HM website
    # Super Soccer Stars: relevant for Lower Division (K-5) only
    # Togetherhood: NOT confirmed — removed
    "HORACE MANN SCHOOL":
        "Summer on the Hill · "
        "John Dorr Nature Lab · "
        "Super Soccer Stars · "
        "HM Summer Institute",

    # Brearley: NY Interschool confirmed. Shares after-school program with Chapin (Wikipedia).
    # YMCA Frost Valley confirmed (Interschool + Brearley FAQ pages)
    # Togetherhood: NOT confirmed — removed
    "THE BREARLEY SCHOOL":
        "NY Interschool Consortium · "
        "Chapin-Brearley Shared After-School Program · "
        "YMCA Frost Valley · "
        "Super Soccer Stars · "
        "Chess at Three · ChessNYC",

    # Chapin: NY Interschool confirmed. Shares after-school with Brearley (Wikipedia).
    # YMCA Frost Valley confirmed. Speech & Debate confirmed on Chapin website.
    # Togetherhood: NOT confirmed — removed
    "THE CHAPIN SCHOOL LTD":
        "NY Interschool Consortium · "
        "Chapin-Brearley Shared After-School Program · "
        "YMCA Frost Valley · "
        "Super Soccer Stars · "
        "Chess at Three · ChessNYC",

    # Spence: NY Interschool confirmed. YMCA Frost Valley confirmed.
    # Togetherhood: NOT confirmed — removed
    "THE SPENCE SCHOOL":
        "NY Interschool Consortium · "
        "YMCA Frost Valley · "
        "Super Soccer Stars · "
        "Chess at Three · ChessNYC · "
        "Spence Summer Programs",

    # Trinity: NY Interschool confirmed. Chess via tournament records confirmed.
    # Togetherhood: NOT confirmed — removed
    "TRINITY SCHOOL":
        "NY Interschool Consortium · "
        "Super Soccer Stars · "
        "GM Chess Academy · Tri-State Chess · ChessNYC · "
        "Trinity Summer Programs",

    # Riverdale: Hilltop Schools Partnership confirmed on HM website.
    # Van Cortlandt Park Alliance confirmed on HM website.
    # Togetherhood: NOT confirmed — removed
    "RIVERDALE COUNTRY SCHOOL INC":
        "Hilltop Schools Partnership · "
        "Van Cortlandt Park Alliance · "
        "Super Soccer Stars · "
        "Riverdale Summer Day Camp",

    # Town School: CONFIRMED Togetherhood partner (togetherhood.us/partners-old/the-town-school)
    "THE TOWN SCHOOL INC":
        "Togetherhood · "
        "Super Soccer Stars · "
        "Chess at Three · ChessNYC · "
        "Town School Summer Programs",

    # Hackley: Westchester campus — Super Soccer Stars does not operate in Tarrytown
    # Teatown Lake Reservation: confirmed Westchester environmental education partner
    # Togetherhood: NOT confirmed, NOT in their market area — removed
    "HACKLEY SCHOOL":
        "Teatown Lake Reservation · "
        "Hackley Summer Programs · "
        "Arts & Theater Teaching Artists",

    # Poly Prep: Brooklyn campus. Mindful Sports confirmed Brooklyn-based.
    # Togetherhood: NOT confirmed — removed. Super Soccer Stars: confirmed Brooklyn area.
    "POLYTECHNIC PREP COUNTRY DAY":
        "Super Soccer Stars · "
        "Mindful Sports · "
        "ChessNYC · "
        "Brooklyn Robot Foundry · "
        "Poly Prep Summer Day Camp",

    # Packer: Brooklyn. Mindful Sports confirmed Park Slope/Brooklyn.
    # Brooklyn Arts Exchange: confirmed Packer-area arts partner.
    # Togetherhood: NOT confirmed — removed
    "PACKER COLLEGIATE INSTITUTE":
        "Brooklyn Arts Exchange · "
        "Super Soccer Stars · "
        "Mindful Sports · "
        "Chess at Three · ChessNYC · "
        "Packer Summer Programs",

    # ── WASHINGTON DC ─────────────────────────────────────────────────────────
    # Togetherhood operates DC market but NO specific school partnerships confirmed — removed from all DC schools
    # Sources: school websites only
    "SIDWELL FRIENDS SCHOOL":
        "Sidwell Summer Programs · "
        "Washington Performing Arts · "
        "Quaker Ridge Camp",

    "GEORGETOWN DAY SCHOOL":
        "GDS Summer Programs · "
        "Imagination Stage · "
        "Washington Tennis & Education Foundation",

    "ST ALBANS SCHOOL":
        "National Cathedral Summer · "
        "Washington Performing Arts · "
        "Episcopal Service Corps",

    "NATIONAL CATHEDRAL SCHOOL":
        "National Cathedral Summer Programs · "
        "Imagination Stage · "
        "Washington Performing Arts",

    "MARET SCHOOL":
        "Maret Summer Programs · "
        "Levine Music · "
        "Washington Tennis & Education Foundation",

    # ── PHILADELPHIA ──────────────────────────────────────────────────────────
    # Togetherhood Philadelphia confirmed operating; Newtown Friends + Princeton Friends on partner page
    # For the specific elite schools below: NOT individually confirmed — removed
    # Settlement Music School: confirmed Philadelphia arts enrichment institution
    "WILLIAM PENN CHARTER SCHOOL":
        "Penn Charter Summer Day Camp · "
        "Penn Charter Aquatics Club · "
        "Settlement Music School",

    "GERMANTOWN FRIENDS SCHOOL":
        "GFS Summer Programs · "
        "Settlement Music School · "
        "Philadelphia Chess Club",

    "EPISCOPAL ACADEMY":
        "EA Summer Programs · "
        "Philadelphia Museum of Art · "
        "Settlement Music School",

    "THE HAVERFORD SCHOOL":
        "Haverford Summer Programs · "
        "Settlement Music School",

    "SPRINGSIDE CHESTNUT HILL ACADEMY":
        "SCH Academy Summer Programs · "
        "Philadelphia Young Playwrights · "
        "Settlement Music School",

    # ── BOSTON ────────────────────────────────────────────────────────────────
    # Togetherhood: NOT confirmed in Boston — removed from all Boston schools
    # Sources: school websites only
    "NOBLE AND GREENOUGH SCHOOL":
        "Nobles Summer Programs · "
        "New England Aquarium · "
        "Boston Symphony Orchestra",

    "MILTON ACADEMY":
        "Milton Summer · "
        "Mass Audubon · "
        "Boston Symphony Orchestra",

    "GROTON SCHOOL":
        "Groton Summer Language Institute · "
        "Mass Audubon",

    "ROXBURY LATIN SCHOOL":
        "RL Summer Programs · "
        "Boston Debate League",

    "BOSTON LATIN SCHOOL":
        "Boston Debate League · "
        "826 Boston · "
        "Boston Symphony Orchestra",
}
def get_vendors(school_name):
    name = school_name.upper().strip()
    if name in VENDOR_DB:
        return VENDOR_DB[name]
    for key, vendors in VENDOR_DB.items():
        key_words = [w for w in key.split() if len(w) > 4]
        if sum(1 for w in key_words if w in name) >= 2:
            return vendors
    return "—"

# ── UTILITIES ─────────────────────────────────────────────────────────────────
def to_m(v):
    try: return round(float(v) / 1_000_000, 2)
    except: return 0.0

def fmt(v):
    return f"${v:.2f}M" if v != 0 else "$0.00M"

def clean_money(text):
    if not text: return 0.0
    try: return float(re.sub(r'[$,\s]', '', str(text)))
    except: return 0.0

# ── SEARCH ────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def discover_schools(city, state):
    found = {}
    search_cities = [city]
    if city.lower() in ["new york", "nyc", "manhattan"]:
        search_cities += ["Brooklyn", "Bronx", "Queens", "Staten Island"]

    for s in REFERENCE_DB:
        city_match  = not city.strip() or any(c.lower() in s["city"].lower() for c in search_cities)
        state_match = s.get("state", "NY") == state
        if city_match and state_match:
            found[s["ein"]] = {"name": s["name"], "ein": s["ein"], "city": s["city"]}

    keywords = ["School", "Country Day", "Preparatory"]
    for scity in search_cities:
        for kw in keywords:
            try:
                r = requests.get(f"{BASE}/search.json?q={requests.utils.quote(scity + ' ' + kw)}", timeout=5)
                for org in r.json().get("organizations", []):
                    ein  = str(org["ein"])
                    name = org["name"].upper()
                    if any(x in name for x in ["SCHOOL","ACADEMY","PREP"]):
                        if "UNIVERSITY" not in name and "COLLEGE" not in name:
                            found[ein] = {"name": name, "ein": ein, "city": org.get("city","")}
            except: continue

    return sorted(found.values(), key=lambda x: x["name"])

# ── XML EXTRACTION ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_from_xml(ein, name=""):
    try:
        r = requests.get(f"{BASE}/organizations/{ein}.json", timeout=10)
        if r.status_code != 200: return None

        org_data  = r.json().get("organization", {})
        object_id = org_data.get("latest_object_id")

        if not object_id and name:
            try:
                sr = requests.get(f"{BASE}/search.json?q={requests.utils.quote(name)}", timeout=8)
                for o in sr.json().get("organizations", []):
                    words = [w for w in name.upper().split() if len(w) > 3 and w not in {"THE","SCHOOL","INC","LTD"}]
                    if all(w in o["name"].upper() for w in words[:2]):
                        r2 = requests.get(f"{BASE}/organizations/{o['ein']}.json", timeout=10)
                        if r2.status_code == 200:
                            org_data  = r2.json().get("organization", {})
                            object_id = org_data.get("latest_object_id")
                            if object_id: break
            except: pass

        if not object_id: return None

        xr = requests.get(
            f"https://projects.propublica.org/nonprofits/download-xml?object_id={object_id}",
            timeout=15
        )
        if xr.status_code != 200: return None

        xml_text = xr.content.decode('utf-8-sig').strip()
        if xml_text.startswith('ï»¿'): xml_text = xml_text[3:]
        if not xml_text.strip().startswith('<?xml'): return None

        root = ET.fromstring(xml_text)

        def fv(patterns):
            for p in patterns:
                e = root.find(p)
                if e is not None and e.text:
                    try: return float(e.text)
                    except: return e.text
            return None

        yr   = fv(['.//{*}TaxYr','.//{*}TaxYear','.//{*}TaxPeriodEndDt'])
        year = str(int(float(str(yr).replace(',','')))) if yr else None
        if year and '-' in year: year = year[:4]

        rev  = fv(['.//{*}CYTotalRevenueAmt','.//{*}TotalRevenueAmt','.//{*}TotalRevenueCurrentYear','.//{*}TotalRevenueColumnAmt']) or 0.0
        exp  = fv(['.//{*}CYTotalExpensesAmt','.//{*}TotalExpensesAmt','.//{*}TotalExpensesCurrentYear','.//{*}TotalExpensesColumnAmt']) or 0.0
        tuit = fv(['.//{*}CYProgramServiceRevenueAmt','.//{*}TotalProgramServiceRevenueAmt','.//{*}ProgramServiceRevenueAmt']) or 0.0
        spec = fv(['.//{*}CYOtherRevenueAmt','.//{*}OtherRevenueAmt','.//{*}OtherRevenueTotalAmt','.//{*}CYInvestmentIncomeAmt']) or 0.0

        students = 0
        desc_text = org_data.get("description", "") or org_data.get("activity", "") or ""
        if desc_text:
            m = re.search(r'(\d[\d,]+)\s*student', desc_text, re.IGNORECASE)
            if m: students = int(m.group(1).replace(',', ''))
        if not students:
            for elem in root.iter():
                tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                if tag in ('Desc','ActivityOrMissionDesc','MissionDesc','ProgramServiceRevenueGrpDesc'):
                    if elem.text:
                        m = re.search(r'(\d[\d,]+)\s*student', elem.text, re.IGNORECASE)
                        if m:
                            students = int(m.group(1).replace(',', ''))
                            break

        return {
            "year": year, "rev": float(rev), "exp": float(exp),
            "tuition": float(tuit), "special": float(spec), "students": students
        }
    except: return None

# ── HTML FALLBACK ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_from_html(ein):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        org_page = requests.get(f"{WEB_BASE}/{ein}", headers=headers, timeout=10)
        if org_page.status_code != 200: return None

        soup = BeautifulSoup(org_page.text, 'html.parser')
        data = {"year": None, "rev": 0.0, "exp": 0.0, "tuition": 0.0, "special": 0.0, "students": 0}

        filing_href = next(
            (a['href'] for a in soup.find_all('a', href=True)
             if f'/organizations/{ein}/' in a['href'] and '/full' in a['href']), None
        )
        if not filing_href: return None

        fp = requests.get(f"https://projects.propublica.org{filing_href}", headers=headers, timeout=10)
        if fp.status_code != 200: return None

        fsoup = BeautifulSoup(fp.text, 'html.parser')
        for el in fsoup.find_all(['h1','h2','h3','td','span']):
            m = re.search(r'\b(20\d{2})\b', el.get_text())
            if m: data["year"] = m.group(1); break

        for table in fsoup.find_all('table'):
            for row in table.find_all('tr'):
                cells = row.find_all(['td','th'])
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True).lower()
                    val   = clean_money(cells[-1].get_text(strip=True))
                    if val > 1000:
                        if 'total revenue'   in label and data["rev"]     == 0.0: data["rev"]     = val
                        elif 'total expense' in label and data["exp"]     == 0.0: data["exp"]     = val
                        elif 'program serv'  in label and data["tuition"] == 0.0: data["tuition"] = val
                        elif 'other revenue' in label and data["special"] == 0.0: data["special"] = val

        return data if (data["rev"] > 0 or data["exp"] > 0) else None
    except: return None

# ── HYBRID FETCH ───────────────────────────────────────────────────────────────
def fetch_audit(ein, name=""):
    d = fetch_from_xml(ein, name)
    if d and (d["rev"] > 0 or d["exp"] > 0): return d
    d = fetch_from_html(ein)
    if d and (d["rev"] > 0 or d["exp"] > 0): return d
    return None

# ── TABLE STYLING ──────────────────────────────────────────────────────────────
def style_table(df, raw_rows):
    style = pd.DataFrame('', index=df.index, columns=df.columns)
    for i, row in enumerate(raw_rows):
        rev_val  = row.get("_rev", 0)
        gap_val  = row.get("_gap", 0)
        spec_val = row.get("_special", 0)
        if gap_val < 0:
            style.at[i, 'Operating Gap'] = 'background-color:#fff0f0;color:#c53030;font-weight:600'
        if rev_val > 0 and spec_val < 0.10 * rev_val:
            style.at[i, 'Auxiliary Revenue (2b)'] = 'background-color:#fff0f0;color:#c53030;font-weight:600'
    return style

# ── PAGE ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="th-header">
    <div class="th-logo">School Intelligence Platform</div>
    <div class="th-tagline">Helps You Target The Right Independent School With Max Potential!</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="search-panel">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([2, 1, 1])
with c1: city_in  = st.text_input("City", "New York", placeholder="Enter city name...")
with c2: state_in = st.selectbox("State", ALL_STATES, index=ALL_STATES.index("NY"))
with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("Search Schools", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown(
    '<div style="background:#f0f6ff;border-left:3px solid #3b82f6;border-radius:6px;'
    'padding:8px 14px;font-size:0.78rem;color:#1e40af;margin-bottom:0.5rem">'
    '⚠️ Lists <strong>Private/ Independent schools (501c3 Non-Profits) only</strong>. '
    '</div>',
    unsafe_allow_html=True
)

if search_btn:
    st.cache_data.clear()
    with st.spinner("Scanning school database..."):
        results = discover_schools(city_in, state_in)
        st.session_state["results"] = results

if "results" in st.session_state:
    schools = st.session_state["results"]
    st.markdown(f'<div style="color:#64748b;font-size:0.83rem;margin-bottom:0.8rem">⬡ {len(schools)} institutions identified in {city_in or state_in}</div>', unsafe_allow_html=True)

    options  = {f"{s['name']}  ·  {s['city']}": s for s in schools}
    selected = st.multiselect(
        "Select schools to audit (maximum 6)",
        list(options.keys()),
        max_selections=6
    )

    if st.button("Run Financial Audit", use_container_width=False):
        if not selected:
            st.warning("Select at least one school to audit.")
        else:
            rows     = []
            raw_rows = []
            prog     = st.progress(0)

            for i, label in enumerate(selected):
                school = options[label]
                d = fetch_audit(school["ein"], school["name"])

                if d and (d["rev"] > 0 or d["exp"] > 0):
                    gap           = d["rev"] - d["exp"]
                    spec          = d["special"]
                    tuit          = d["tuition"]
                    rev_2026      = d["rev"] * INFLATION_MULTIPLIER   # Est 2026 Operating Revenue
                    aux_potential = rev_2026 * 0.10                   # 10% of est 2026 rev (tile only)
                    students      = d.get("students", 0)
                    vendors       = get_vendors(school["name"])
                    rows.append({
                        "School":                       school["name"],
                        "City":                         school["city"],
                        "Year":                         d["year"] or "N/A",
                        "Students":                     students if students else "—",
                        "Operating Revenue":            fmt(to_m(d["rev"])),
                        "Operating Expenses":           fmt(to_m(d["exp"])),
                        "Operating Gap":                fmt(to_m(gap)),
                        "Tuition & Fees (2a)":          fmt(to_m(tuit)),
                        "Auxiliary Revenue (2b)":       fmt(to_m(spec)),
                        "Est 2026 Operating Revenue":   fmt(to_m(rev_2026)),
                        "Enrichment Providers":    vendors,
                    })
                    raw_rows.append({
                        "_rev":           d["rev"],
                        "_gap":           gap,
                        "_special":       spec,
                        "_tuition":       tuit,
                        "_rev_2026":      rev_2026,
                        "_aux_potential": aux_potential,
                    })
                else:
                    rows.append({
                        "School":                       school["name"],
                        "City":                         school["city"],
                        "Year":                         "N/A",
                        "Students":                     "—",
                        "Operating Revenue":            "Unavailable",
                        "Operating Expenses":           "Unavailable",
                        "Operating Gap":                "Unavailable",
                        "Tuition & Fees (2a)":          "Unavailable",
                        "Auxiliary Revenue (2b)":       "Unavailable",
                        "Est 2026 Operating Revenue":   "Unavailable",
                        "Enrichment Providers":    "—",
                    })
                    raw_rows.append({
                        "_rev": 0, "_gap": 0, "_special": 0, "_tuition": 0,
                        "_rev_2026": 0, "_aux_potential": 0,
                    })

                prog.progress((i + 1) / len(selected))
                time.sleep(0.5)

            prog.empty()

            valid          = [r for r in raw_rows if r["_rev"] > 0]
            n_neg          = sum(1 for r in raw_rows if r["_gap"] < 0)
            n_low          = sum(1 for r in raw_rows if r["_rev"] > 0 and r["_special"] < 0.10 * r["_rev"])
            # Tile: sum of 10% of each school's inflation-adjusted 2026 operating revenue
            total_aux_potential = sum(r["_aux_potential"] for r in raw_rows) / 1e6

            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card">
                    <div class="metric-value">{len(selected)}</div>
                    <div class="metric-label">Schools Audited</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len(valid)}</div>
                    <div class="metric-label">Data Retrieved</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#e53e3e">{n_neg}</div>
                    <div class="metric-label">Negative Gap</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#e53e3e">{n_low}</div>
                    <div class="metric-label">Low Aux Revenue</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${total_aux_potential:.1f}M</div>
                    <div class="metric-label">2026 Aux Potential</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="target-alert">
                <strong>⬡ Targeting Signal</strong> — Cells highlighted in Red indicate
                either a <strong>Negative Operating Gap</strong> OR
                <strong>Auxiliary Revenue Below 10% of Tuition &amp; Fees</strong>.
                These schools may represent strategic partnership opportunities.
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-label">Financial Audit Results</div>', unsafe_allow_html=True)

            if rows:
                cols = [
                    "School","City","Year","Students",
                    "Operating Revenue","Operating Expenses","Operating Gap",
                    "Tuition & Fees (2a)","Auxiliary Revenue (2b)",
                    "Est 2026 Operating Revenue","Enrichment Providers",
                ]
                header_html = "".join(f"<th>{c}</th>" for c in cols)
                rows_html = ""
                for idx, row in enumerate(rows):
                    rr = raw_rows[idx]
                    cells_html = ""
                    for c in cols:
                        val = row.get(c, "")
                        classes = []
                        # Red highlight rules
                        if c == "Operating Gap" and rr["_gap"] < 0 and val not in ("Unavailable","N/A"):
                            classes.append("cell-red")
                        elif c == "Auxiliary Revenue (2b)" and rr["_tuition"] > 0 and rr["_special"] < 0.10 * rr["_tuition"]:
                            classes.append("cell-red")
                        # Unavailable styling
                        if val == "Unavailable":
                            classes.append("cell-na")
                        # Wide column for Enrichment Providers
                        if c == "Enrichment Providers":
                            classes.append("ep")
                        css = (f' class="{" ".join(classes)}"') if classes else ""
                        cells_html += f"<td{css}>{val}</td>"
                    rows_html += f"<tr>{cells_html}</tr>"

                table_html = f"""
                <div class="audit-table-wrap">
                  <table class="audit-table">
                    <thead><tr>{header_html}</tr></thead>
                    <tbody>{rows_html}</tbody>
                  </table>
                </div>
                """
                st.markdown(table_html, unsafe_allow_html=True)

                ok = sum(1 for r in rows if r["Year"] != "N/A")
                st.markdown(
                    f'<div style="color:#2f855a;font-size:0.8rem;margin-top:0.8rem">'
                    f'✓ Data retrieved for {ok} of {len(selected)} institutions · '
                    f'Source: IRS Form 990 via ProPublica</div>',
                    unsafe_allow_html=True
                )

            st.markdown("""
            <div class="inflation-note" style="margin-top:1.2rem">
                <strong>📊 2026 Estimation</strong> — Est 2026 Operating Revenue is obtained by          
                adjusting 2023 Values for Inflation (Cumulative 9%)and 2026 Aux Potential is 
                assumed at 10% of Est 2026 Operating Revenue.
            </div>
            """, unsafe_allow_html=True)
