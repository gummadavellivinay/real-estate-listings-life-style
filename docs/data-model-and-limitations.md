# Data model and limitations

[Back to README](../README.md)

## CSV-backed records

`load_homes()` reads the local CSV using `csv.DictReader` with `utf-8-sig` encoding. The current file contains 2,500 records. Each returned dictionary retains every original CSV column as a string, then adds normalized fields and generated values.

| Normalized field | Source / calculation |
| --- | --- |
| `id` | Integer `Id` |
| `price` | Integer `SalePrice` |
| `beds` | Integer `BedroomAbvGr` |
| `baths` | Float `FullBath + 0.5 × HalfBath` |
| `sqft` | Integer `GrLivArea` |
| `year` | Integer `YearBuilt` |
| `times` | Generated driving minutes by lifestyle |
| `latitude`, `longitude` | Generated positions by ID |

The UI also reads raw `Neighborhood`, `GarageCars`, `CentralAir`, `HeatingQC`, and `YearRemodAdd` values. Basement bathrooms are excluded from displayed totals. Heating quality is a condition code; it does not establish HVAC age.

`search_homes()` returns copies of matching records with `matches` (amenities meeting the drive preference) and `score` (rounded lifestyle score or `None`). It does not write back to the CSV.

## Generated proximity

For each listing ID and lifestyle name:

```text
digest = SHA-256("listing_id:lifestyle_name")
drive_minutes = 2 + (integer from first 4 digest bytes, big-endian) % 24
walk_minutes = drive_minutes × 5
```

Driving values therefore range from 2 to 25 minutes; walking values range from 10 to 125 minutes. Walking time is calculated in `app.py`, not stored in the CSV. These values represent no verified destination, distance, road network, pedestrian route, or traffic measurement.

The sixteen lifestyle categories are tennis, pickleball, trails/cycling, gym/fitness, coffee, parks, groceries, Whole Foods, hospitals, highway access, dog parks, restaurants, arts/culture, libraries, golf, and swimming. Their exact keyword patterns are in `search.py`.

Coordinates use:

```text
latitude  = 42.0 + ((id × 37) % 100) / 2000
longitude = -93.68 + ((id × 53) % 100) / 2000
```

They illustrate a region around Ames, Iowa. They are not actual addresses or amenity locations; repeated positions are possible.

## Photos

`HOME_PHOTOS` is the sorted list of `assets/homes/*.jpg`. The current bundle contains seven sample Unsplash photos. `Random(home['id']).choice(HOME_PHOTOS)` assigns a repeatable image for each ID while that asset list remains unchanged. Images are reused across homes and do not depict the CSV properties. Changing the asset list can change assignments.

## Boundaries

- Records are synthetic sale/property data, not a live listing feed. Currency amounts are displayed with a dollar sign.
- Real addresses, property-specific photos, school ratings, quietness, HVAC age, appliance health, HOA fees, certification, truth scores, and seller disclosures are unavailable.
- There is no geocoding, real places lookup, routing service, location detection, customer/agent authentication, or actual showing scheduling.
- Search is regular-expression parsing. Unsupported intent can be ignored or misinterpreted; selected warning keywords do not cover all unsupported requests.
- There is no persistent database, user profile, saved-search service, outbound messaging, or application recording storage.
- Data loading assumes valid fields and conversion-ready values. There is no comprehensive schema validation or malformed-query recovery.
- Footer disclosures explain the synthetic/generated data. Details label missing evidence; cards label photos as samples; the map labels positions as illustrative.

The supplied Word reference is a repository artifact, not a runtime data source. Proposed integrations are listed in [Future improvements](future-improvements.md).
