import pandas as pd

# === CONFIGURATION ===
EXCEL_FILE = "data/locations_cleaned.xlsx"
DISPLAY_COLUMNS = ["city", "address", "location", "phone"]

# 🔁 Common alias mapping (deduplicated keys)
aliases = {
    "khi": "karachi",
    "kar": "karachi",
    "lhr": "lahore",
    "lah": "lahore",
    "ryk": "rahim yar khan",
    "rahimyar": "rahim yar khan",
    "dgk": "dera ghazi khan",
    "dgkhan": "dera ghazi khan",
    "dik": "dera ismail khan",
    "dikhan": "dera ismail khan",
    "isb": "islamabad",
    "isl": "islamabad",
    "rwp": "rawalpindi",
    "fsd": "faisalabad",
    "faisal": "faisalabad",
    "mtn": "multan",
    "qta": "quetta",
    "psh": "peshawar",
    "hyd": "hyderabad",
    "skt": "sukkur",
    "gwr": "gujranwala",
    "grt": "gujrat",
    "bwp": "bahawalpur",
    "bwn": "bahawalnagar",
    "sgr": "sargodha",
    "swl": "swat",
    "mwl": "mianwali",
    "nsh": "nowshera",
    "swb": "swabi",
    "khn": "khushab",
    "khnw": "khanewal",
    "kpr": "khanpur",
    "lrk": "larkana",
    "mzd": "muzaffarabad",
    "mzg": "muzaffargarh",
    "ok": "okara",
    "tt": "toba tek singh",
    "veh": "vehari",
    "zbt": "zhob",
    "gwd": "gwadar",
    "tbt": "turbat",
    "skd": "skardu",
    "glt": "gilgit",
    "mir": "mirpur",
    "kot": "kotli",
    "rkt": "rawalakot",
    "bgh": "bagh",
    "bnn": "bannu",
    "kht": "kohat",
    "ddu": "dadu",
    "jcd": "jacobabad",
    "shk": "shikarpur",
    "ngr": "nagar",
    "hbl": "haripur",
    "att": "attock",
    "jhl": "jhelum",
    "jng": "jhang",
    "mdk": "mandi bahauddin",
    "skp": "sheikhupura",
    "bwr": "burewala",
    "smd": "samundri",
    "sng": "sanghar",
    "suk": "sukkur",
    "swt": "swat",
    "tnd": "tando adam",
    "tndj": "tando jam",
    "tndu": "tando allahyar",
    "tndm": "tando muhammad khan",
    "tndb": "tando bagho",
    "tndg": "tando ghulam ali",
    "tndh": "tando haider",
    "tndk": "tando khan",
    "tndn": "tando nizam",
    "tndp": "tando pur",
    "tndr": "tando rahim",
    "tnds": "tando soomro",
    "tndt": "tando thoro",
    "tndw": "tando wah",
    "tndz": "tando zubair",
}

# === LOAD FILE ===
df = pd.read_excel(EXCEL_FILE)
df.columns = [col.lower().strip() for col in df.columns]  # Normalize column names

# Determine which columns to display based on what's available
available_display_cols = [col for col in DISPLAY_COLUMNS if col in df.columns]

# === SEARCH FUNCTION ===
def search_city(keyword):
    original_keyword = keyword
    keyword = keyword.lower().strip()
    keyword = aliases.get(keyword, keyword)  # Expand alias if exists

    # Search across all columns (case-insensitive match)
    mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(keyword).any(), axis=1)
    results = df[mask]

    if results.empty:
        print(f"🔍 No results found for: {original_keyword}")
    else:
        for idx, (_, row) in enumerate(results.iterrows(), start=1):
            print(f"Location {idx}:")
            # Address
            if "address" in available_display_cols:
                print(f"Address: {row['address']}")
            # Location / Name
            if "location" in available_display_cols:
                print(f"Name: {row['location']}")
            # Phone
            if "phone" in available_display_cols:
                print(f"Phone: {row['phone']}")
            print("")  # Blank line after each location

# === MAIN LOOP ===
if __name__ == "__main__":
    import sys

    if sys.stdin.isatty():  # Interactive shell
        while True:
            query = input("\nEnter a location keyword (or type 'exit'): ")
            if query.lower() == "exit":
                break
            search_city(query)
    else:
        # Subprocess mode: read query from stdin, output result
        query = sys.stdin.read().strip()
        from io import StringIO
        import contextlib

        with contextlib.redirect_stdout(StringIO()) as buf:
            search_city(query)
        output = buf.getvalue()
        print(output)
