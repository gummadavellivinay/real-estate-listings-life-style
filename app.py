from pathlib import Path
from random import Random
import pandas as pd
import streamlit as st
from search import LIFESTYLES, load_homes, parse_query, search_homes
from voice_search import search_box, SUGGESTIONS

HOME_PHOTOS = sorted((Path(__file__).parent / "assets" / "homes").glob("*.jpg"))

def home_photo(home):
    return str(Random(home["id"]).choice(HOME_PHOTOS))

st.set_page_config(page_title="True Home | Lifestyle search", page_icon="🏡", layout="wide")
st.markdown("""<style>
.stApp{background:radial-gradient(ellipse at 50% 0%,#e9f0e5 0%,#f8f7f2 55%)}
.block-container{max-width:1440px;padding-top:1.5rem}
[data-testid="stSidebar"]{background:#eff2e9}
[data-testid="stImage"] img{border-radius:12px}
[data-testid="stButton"] button{border-radius:10px}
[data-testid="stTabs"] [role="tablist"]{gap:24px}h1,h2,h3{color:#163c32}div[data-testid='stMetricValue']{color:#23654d}
div[data-testid='stVerticalBlockBorderWrapper']{background:white;border-radius:14px}
.hero{text-align:center;padding:8px 0 4px}.eyebrow{color:#587364;letter-spacing:3px;font-size:12px}.hero h1{font-size:clamp(18px,3.8vw,46px);line-height:1.15;letter-spacing:-1px;white-space:nowrap}.hero p{color:#69756c;font-size:16px;margin-top:10px}.hero .eyebrow{display:inline-block;padding:8px 14px;background:#e4ecde;border-radius:999px;letter-spacing:2px}
</style>""", unsafe_allow_html=True)

@st.cache_data
def data(modified):
    return load_homes()

homes = data(Path(__file__).with_name("synthetic_real_estate_data.csv").stat().st_mtime)
defaults = dict(lifestyles=[], minutes=10, strict=False, min_price=0, max_price=1000000,
                beds=0, baths=0.0, sqft=0, year=1800, neighborhoods=[], garage=False, air=False)
for key, value in defaults.items():
    st.session_state.setdefault(key, value)
st.session_state.setdefault("compare", [])
st.session_state.setdefault("page_size", 12)
st.session_state.setdefault("query", "")
st.session_state.setdefault("has_searched", False)

def apply_query():
    st.session_state.has_searched = True
    parsed = parse_query(st.session_state.query)
    st.session_state.lifestyles = parsed["lifestyles"]
    for source, target in [("max_price", "max_price"), ("beds", "beds"), ("baths", "baths"), ("minutes", "minutes")]:
        if parsed[source] is not None:
            value = parsed[source]
            if source == "minutes":
                value = max(1, min(30, value))
            st.session_state[target] = value
    st.session_state.query_warning = parsed["unsupported"]
    st.session_state.page_size = 12

def accept_search():
    query = st.session_state.home_search.get("search")
    if query is not None:
        st.session_state.query = query.strip()
        if st.session_state.query:
            apply_query()
        else:
            reset()

def reset():
    for key, value in defaults.items():
        st.session_state[key] = value
    st.session_state.has_searched = False
    st.session_state.query = ""
    st.session_state.query_warning = False
    st.session_state.page_size = 12

st.markdown('<div class="hero"><div class="eyebrow">TRUE HOME · FIND YOUR EVERYDAY</div><h1>Find a home. Keep your lifestyle.</h1><p>Morning coffee. Evening tennis. A trail around the corner.</p></div>', unsafe_allow_html=True)
search_box(
    data={"query": st.session_state.query, "suggestions": SUGGESTIONS},
    key="home_search", on_search_change=accept_search,
)

with st.sidebar:
    st.header("Your everyday")
    st.button("Reset filters", on_click=reset)
    st.multiselect("Lifestyle choices", list(LIFESTYLES), key="lifestyles")
    st.slider("Maximum drive time (minutes)", 1, 30, key="minutes")
    st.checkbox("Require every lifestyle match", key="strict", help="When off, homes are ranked by proximity, even if some choices exceed your time limit.")
    st.header("Home essentials")
    st.number_input("Minimum price ($)", min_value=0, step=25000, key="min_price")
    st.number_input("Maximum price ($)", min_value=0, step=25000, key="max_price")
    st.number_input("Minimum bedrooms", min_value=0, step=1, key="beds")
    st.number_input("Minimum bathrooms (above ground)", min_value=0.0, step=0.5, key="baths")
    st.number_input("Minimum living area (sq ft)", min_value=0, step=250, key="sqft")
    st.number_input("Built in or after", min_value=1800, max_value=2026, key="year")
    st.multiselect("Neighborhood codes", sorted({h["Neighborhood"] for h in homes}), key="neighborhoods")
    st.checkbox("Garage", key="garage")
    st.checkbox("Central air", key="air")
    st.caption("Search uses selected filters and supported text patterns, without an LLM. Applying a text search updates the recognized filters; other filters stay as selected.")

def footer():
    st.divider()
    if st.session_state.get("query_warning"):
        st.warning("School ratings, quietness, HVAC age, verification, disclosures and real commute times are not available in this dataset.")
    st.caption("Prices and property specs come from the synthetic CSV. Photos are illustrative samples. Walking and driving times and map coordinates are generated values. Walking times are modeled as five times driving times, not actual route estimates. Homes have no real addresses and are not verified listings.")
    st.caption("Lifestyle scores and time filters use driving times. Scores do not measure property quality or verification. Bathroom totals exclude basement bathrooms.")
    st.caption("TRUE HOME · 2,500 synthetic listings for learning and exploration")

if not st.session_state.has_searched:
    footer()
    st.stop()

count_col, sort_col = st.columns([3, 2], vertical_alignment="center")
with sort_col:
    sort_label, sort_control = st.columns([1, 3], vertical_alignment="center")
    with sort_label:
        st.markdown("**Sort homes**")
    with sort_control:
        sort = st.selectbox("Sort homes", ["Best lifestyle match", "Price: low to high", "Price: high to low", "Newest built"], label_visibility="collapsed", key="sort")
filters = {key: st.session_state[key] for key in defaults}
results = search_homes(homes, **filters, sort=sort)
with count_col:
    st.subheader(f"{len(results):,} homes for your next chapter")

if filters["min_price"] > filters["max_price"]:
    st.error("Minimum price must be less than or equal to maximum price.")
if not results:
    st.warning("No matching homes. Increase your budget or drive time, or turn off requiring every lifestyle match.")

def walk_time(home, lifestyle):
    # Illustrative walking time only; there are no real routes in this dataset.
    return home["times"][lifestyle] * 5

def proximity_table(home):
    return pd.DataFrame([{"Lifestyle": name, "Walk time (min)": walk_time(home, name),
                          "Drive time (min)": home["times"][name],
                          "Within drive preference": "Yes" if home["times"][name] <= filters["minutes"] else "No"}
                         for name in (filters["lifestyles"] or LIFESTYLES)])

@st.dialog("Home details", width="large")
def detail(home):
    st.header(f"${home['price']:,} · Home #{home['id']}")
    st.image(home_photo(home), caption="Sample home photo · not this property", width="stretch")
    st.write(f"Neighborhood {home['Neighborhood']} · Synthetic listing; address unavailable")
    st.write(f"{home['beds']} bedrooms · {home['baths']:g} baths · {home['sqft']:,} sq ft · Built {home['year']}")
    st.write(f"Garage: {home['GarageCars']} cars · Central air: {home['CentralAir']} · Heating quality: {home['HeatingQC']} · Remodel year: {home['YearRemodAdd']}")
    st.dataframe(proximity_table(home), hide_index=True, width="stretch")
    st.subheader("Evidence & disclosures")
    st.write("Truth score, image authenticity, appliance health, certification, school ratings, seller disclosures and HOA fees: unknown. Heating quality does not establish HVAC age.")
    st.subheader("Showing request draft")
    date = st.date_input("Preferred date")
    notes = st.text_area("Notes for a future agent")
    st.download_button("Download request draft", f"DEMO REQUEST — NOT SENT\nHome #{home['id']}\nPreferred date: {date}\nNotes: {notes}\n", file_name=f"showing-home-{home['id']}.txt")
    st.caption("No request is sent or appointment booked.")

list_tab, map_tab, compare_tab = st.tabs(["Home cards", "Illustrative map", "Compare homes"])
with list_tab:
    for offset in range(0, min(len(results), st.session_state.page_size), 3):
        for col, home in zip(st.columns(3), results[offset:offset + 3]):
            with col, st.container(border=True):
                st.image(home_photo(home), caption="Sample photo · not this property", width="stretch")
                st.caption(f"HOME #{home['id']} · {home['Neighborhood']}")
                st.subheader(f"${home['price']:,}")
                st.write(f"**{home['beds']}** beds · **{home['baths']:g}** baths · **{home['sqft']:,}** sq ft")
                st.caption(f"Built {home['year']} · ${home['price']/home['sqft']:,.0f}/sq ft" if home['sqft'] else f"Built {home['year']}")
                if home['score'] is not None:
                    st.progress(home['score']/100, text=f"{home['score']}% lifestyle proximity score")
                    for name in filters['lifestyles']:
                        st.caption(f"{'✓' if name in home['matches'] else '○'} {name}: Walk {walk_time(home, name)} min · Drive {home['times'][name]} min")
                else:
                    st.caption("Select lifestyles to see a match score")
                if st.button("View details", key=f"detail-{home['id']}", width="stretch"):
                    detail(home)
                selected = home['id'] in st.session_state.compare
                if st.button("Remove from compare" if selected else "Add to compare", key=f"compare-{home['id']}", width="stretch"):
                    if selected:
                        st.session_state.compare.remove(home['id'])
                    elif len(st.session_state.compare) < 4:
                        st.session_state.compare.append(home['id'])
                    else:
                        st.warning("Compare up to four homes. Remove one first.")
                    st.rerun()
    if len(results) > st.session_state.page_size and st.button("Show 12 more homes"):
        st.session_state.page_size += 12
        st.rerun()
with map_tab:
    st.warning("Illustrative positions around Ames, Iowa, generated by listing ID. These are not actual property or amenity locations.")
    if results:
        st.map(pd.DataFrame(results[:100])[["latitude", "longitude"]])
        st.caption("Showing up to the first 100 matches. Use the table to identify listings; map markers are illustrative.")
        st.dataframe(pd.DataFrame(results[:100])[["id", "Neighborhood", "price", "beds", "baths", "sqft", "score"]], hide_index=True)
with compare_tab:
    chosen = [h for h in homes if h['id'] in st.session_state.compare]
    st.write(f"{len(chosen)}/4 homes selected · selections remain when filters change")
    if chosen:
        columns = {}
        for home in chosen:
            columns[f"Home #{home['id']}"] = {"Price": f"${home['price']:,}", "Price / sq ft": f"${home['price']/home['sqft']:,.0f}" if home['sqft'] else "Unknown",
                "Bedrooms": home['beds'], "Bathrooms": home['baths'], "Sq ft": home['sqft'], "Year": home['year'], "Garage spaces": home['GarageCars'], "HOA": "Unknown", "Truth score": "Unknown",
                **{f"{name} · {mode} (min)": value
                   for name in (filters['lifestyles'] or LIFESTYLES)
                   for mode, value in [("Walk", walk_time(home, name)), ("Drive", home['times'][name])]}}
        st.dataframe(pd.DataFrame(columns).astype(str), width="stretch")
        for home in chosen:
            with st.expander(f"Tradeoffs · Home #{home['id']}"):
                matched = [n for n in filters['lifestyles'] if home['times'][n] <= filters['minutes']]
                missed = [n for n in filters['lifestyles'] if n not in matched]
                st.write("Within preferred drive time: " + (", ".join(matched) or "None selected or matched"))
                st.write("Outside preferred drive time: " + (", ".join(missed) or "None"))
                st.caption("Rule-based observations, not model-generated claims.")
        if st.button("Clear comparison"):
            st.session_state.compare = []
            st.rerun()
    else:
        st.info("Add up to four homes from the cards to compare property specs and lifestyle proximity.")
footer()
