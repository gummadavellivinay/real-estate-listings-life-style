"""CSV-backed search with deterministic, explicitly synthetic proximity data."""
import csv
import hashlib
import re
from pathlib import Path

LIFESTYLES = {
    "Tennis courts": r"tennis|racquet",
    "Pickleball": r"pickleball",
    "Trails & cycling": r"trail|hiking|cycling|biking|running",
    "Gym & fitness": r"gym|fitness|workout",
    "Coffee shops": r"coffee|cafe",
    "Parks": r"\bpark|green space",
    "Grocery stores": r"grocery|groceries|supermarket",
    "Whole Foods": r"whole\s*foods",
    "Hospitals": r"hospital|medical",
    "Highway access": r"highway|freeway",
    "Dog parks": r"dog|pet",
    "Restaurants": r"restaurant|dining|foodie",
    "Arts & culture": r"museum|culture|\barts?\b",
    "Libraries": r"library|libraries",
    "Golf courses": r"golf",
    "Swimming": r"swim",
}

def load_homes(path=None):
    path = path or Path(__file__).with_name("synthetic_real_estate_data.csv")
    with open(path, newline="", encoding="utf-8-sig") as source:
        homes = []
        for row in csv.DictReader(source):
            id_ = int(row["Id"])
            homes.append({
                **row, "id": id_, "price": int(row["SalePrice"]),
                "beds": int(row["BedroomAbvGr"]),
                "baths": float(row["FullBath"]) + .5 * float(row["HalfBath"]),
                "sqft": int(row["GrLivArea"]), "year": int(row["YearBuilt"]),
                "times": {name: 2 + int.from_bytes(hashlib.sha256(f"{id_}:{name}".encode()).digest()[:4], "big") % 24
                          for name in LIFESTYLES},
                "latitude": 42.0 + (id_ * 37 % 100) / 2000,
                "longitude": -93.68 + (id_ * 53 % 100) / 2000,
            })
    return homes

def parse_query(text):
    price = re.search(r"(?:under|below|max(?:imum)?|up to)\s*\$?([\d,.]+)\s*(million|k|m)?", text, re.I)
    beds = re.search(r"(\d+)\s*\+?\s*(?:bedroom|bed)", text, re.I)
    baths = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*bath", text, re.I)
    minutes = re.search(r"(?:within|under)\s*(\d+)\s*(?:min|minute)", text, re.I)
    return {
        "lifestyles": [name for name, pattern in LIFESTYLES.items() if re.search(pattern, text, re.I)],
        "max_price": int(float(price[1].replace(",", "")) * {"k": 1000, "m": 1000000, "million": 1000000}.get((price[2] or "").lower(), 1)) if price else None,
        "beds": int(beds[1]) if beds else None,
        "baths": float(baths[1]) if baths else None,
        "minutes": int(minutes[1]) if minutes else None,
        "unsupported": bool(re.search(r"school|quiet|hvac|verified|disclosure|commute", text, re.I)),
    }

def search_homes(homes, *, lifestyles=(), minutes=10, strict=False, min_price=0,
                 max_price=10000000, beds=0, baths=0, sqft=0, year=1800,
                 neighborhoods=(), garage=False, air=False, sort="Best lifestyle match"):
    results = []
    for home in homes:
        if not (min_price <= home["price"] <= max_price and home["beds"] >= beds
                and home["baths"] >= baths and home["sqft"] >= sqft and home["year"] >= year):
            continue
        if neighborhoods and home["Neighborhood"] not in neighborhoods:
            continue
        if garage and float(home["GarageCars"]) <= 0:
            continue
        if air and home["CentralAir"] != "Y":
            continue
        matches = [name for name in lifestyles if home["times"][name] <= minutes]
        if strict and len(matches) != len(lifestyles):
            continue
        score = round(100 * sum(max(0, 1 - home["times"][name] / (minutes * 2)) for name in lifestyles) / len(lifestyles)) if lifestyles else None
        results.append({**home, "matches": matches, "score": score})
    keys = {"Price: low to high": lambda h: h["price"],
            "Price: high to low": lambda h: -h["price"],
            "Newest built": lambda h: -h["year"],
            "Best lifestyle match": lambda h: (-(h["score"] or 0), h["price"])}
    return sorted(results, key=keys[sort])
