"""Seed German cities with state/county hierarchy."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.database import SessionLocal
from app.models.location import City, County, Country, State

# (state_name, state_code, county_name, county_code, city_name, postal_code)
DATA = [
    # Bayern
    ("Bayern", "BY", "Stadt München", "MUC", "München", "80331"),
    ("Bayern", "BY", "Stadt München", "MUC", "München", "80333"),
    ("Bayern", "BY", "Stadt München", "MUC", "München", "80335"),
    ("Bayern", "BY", "Stadt Nürnberg", "NUE", "Nürnberg", "90402"),
    ("Bayern", "BY", "Stadt Nürnberg", "NUE", "Nürnberg", "90403"),
    ("Bayern", "BY", "Stadt Augsburg", "AUG", "Augsburg", "86150"),
    ("Bayern", "BY", "Stadt Augsburg", "AUG", "Augsburg", "86152"),
    ("Bayern", "BY", "Landkreis München", "LKM", "Unterschleißheim", "85716"),
    ("Bayern", "BY", "Landkreis München", "LKM", "Garching", "85748"),
    ("Bayern", "BY", "Stadt Regensburg", "REG", "Regensburg", "93047"),
    ("Bayern", "BY", "Stadt Ingolstadt", "IN", "Ingolstadt", "85049"),
    ("Bayern", "BY", "Stadt Würzburg", "WUE", "Würzburg", "97070"),
    ("Bayern", "BY", "Stadt Fürth", "FUE", "Fürth", "90762"),
    ("Bayern", "BY", "Stadt Erlangen", "ER", "Erlangen", "91052"),
    # Berlin
    ("Berlin", "BE", "Berlin", "B", "Berlin", "10115"),
    ("Berlin", "BE", "Berlin", "B", "Berlin", "10117"),
    ("Berlin", "BE", "Berlin", "B", "Berlin", "10119"),
    ("Berlin", "BE", "Berlin", "B", "Berlin", "10178"),
    ("Berlin", "BE", "Berlin", "B", "Berlin-Mitte", "10115"),
    ("Berlin", "BE", "Berlin", "B", "Berlin-Prenzlauer Berg", "10405"),
    ("Berlin", "BE", "Berlin", "B", "Berlin-Kreuzberg", "10961"),
    ("Berlin", "BE", "Berlin", "B", "Berlin-Charlottenburg", "10623"),
    ("Berlin", "BE", "Berlin", "B", "Berlin-Schöneberg", "10777"),
    ("Berlin", "BE", "Berlin", "B", "Berlin-Neukölln", "12043"),
    # Brandenburg
    ("Brandenburg", "BB", "Stadt Potsdam", "P", "Potsdam", "14467"),
    ("Brandenburg", "BB", "Stadt Potsdam", "P", "Potsdam", "14469"),
    ("Brandenburg", "BB", "Landkreis Oder-Spree", "LOS", "Frankfurt (Oder)", "15230"),
    # Bremen
    ("Bremen", "HB", "Stadt Bremen", "HB", "Bremen", "28195"),
    ("Bremen", "HB", "Stadt Bremen", "HB", "Bremen", "28197"),
    ("Bremen", "HB", "Stadt Bremen", "HB", "Bremen", "28199"),
    ("Bremen", "HB", "Stadt Bremerhaven", "BHV", "Bremerhaven", "27568"),
    # Hamburg
    ("Hamburg", "HH", "Hamburg", "HH", "Hamburg", "20095"),
    ("Hamburg", "HH", "Hamburg", "HH", "Hamburg", "20097"),
    ("Hamburg", "HH", "Hamburg", "HH", "Hamburg", "20099"),
    ("Hamburg", "HH", "Hamburg", "HH", "Hamburg-Altona", "22765"),
    ("Hamburg", "HH", "Hamburg", "HH", "Hamburg-Eimsbüttel", "20259"),
    ("Hamburg", "HH", "Hamburg", "HH", "Hamburg-Barmbek", "22303"),
    # Hessen
    ("Hessen", "HE", "Stadt Frankfurt am Main", "F", "Frankfurt am Main", "60306"),
    ("Hessen", "HE", "Stadt Frankfurt am Main", "F", "Frankfurt am Main", "60308"),
    ("Hessen", "HE", "Stadt Frankfurt am Main", "F", "Frankfurt am Main", "60310"),
    ("Hessen", "HE", "Stadt Wiesbaden", "WI", "Wiesbaden", "65183"),
    ("Hessen", "HE", "Stadt Wiesbaden", "WI", "Wiesbaden", "65185"),
    ("Hessen", "HE", "Stadt Kassel", "KS", "Kassel", "34117"),
    ("Hessen", "HE", "Stadt Darmstadt", "DA", "Darmstadt", "64283"),
    ("Hessen", "HE", "Landkreis Offenbach", "OF", "Offenbach am Main", "63065"),
    # Mecklenburg-Vorpommern
    ("Mecklenburg-Vorpommern", "MV", "Landkreis Rostock", "LRO", "Rostock", "18055"),
    ("Mecklenburg-Vorpommern", "MV", "Stadt Schwerin", "SN", "Schwerin", "19053"),
    # Niedersachsen
    ("Niedersachsen", "NI", "Stadt Hannover", "H", "Hannover", "30159"),
    ("Niedersachsen", "NI", "Stadt Hannover", "H", "Hannover", "30161"),
    ("Niedersachsen", "NI", "Stadt Hannover", "H", "Hannover", "30163"),
    ("Niedersachsen", "NI", "Stadt Braunschweig", "BS", "Braunschweig", "38100"),
    ("Niedersachsen", "NI", "Stadt Osnabrück", "OS", "Osnabrück", "49074"),
    ("Niedersachsen", "NI", "Stadt Oldenburg", "OL", "Oldenburg", "26122"),
    ("Niedersachsen", "NI", "Stadt Wolfsburg", "WOB", "Wolfsburg", "38440"),
    # Nordrhein-Westfalen
    ("Nordrhein-Westfalen", "NW", "Stadt Köln", "K", "Köln", "50667"),
    ("Nordrhein-Westfalen", "NW", "Stadt Köln", "K", "Köln", "50668"),
    ("Nordrhein-Westfalen", "NW", "Stadt Köln", "K", "Köln", "50670"),
    ("Nordrhein-Westfalen", "NW", "Stadt Düsseldorf", "D", "Düsseldorf", "40210"),
    ("Nordrhein-Westfalen", "NW", "Stadt Düsseldorf", "D", "Düsseldorf", "40212"),
    ("Nordrhein-Westfalen", "NW", "Stadt Dortmund", "DO", "Dortmund", "44135"),
    ("Nordrhein-Westfalen", "NW", "Stadt Essen", "E", "Essen", "45127"),
    ("Nordrhein-Westfalen", "NW", "Stadt Duisburg", "DU", "Duisburg", "47051"),
    ("Nordrhein-Westfalen", "NW", "Stadt Bochum", "BO", "Bochum", "44787"),
    ("Nordrhein-Westfalen", "NW", "Stadt Wuppertal", "W", "Wuppertal", "42103"),
    ("Nordrhein-Westfalen", "NW", "Stadt Bonn", "BN", "Bonn", "53111"),
    ("Nordrhein-Westfalen", "NW", "Stadt Münster", "MS", "Münster", "48143"),
    ("Nordrhein-Westfalen", "NW", "Stadt Bielefeld", "BI", "Bielefeld", "33602"),
    ("Nordrhein-Westfalen", "NW", "Stadt Aachen", "AC", "Aachen", "52062"),
    ("Nordrhein-Westfalen", "NW", "Stadt Gelsenkirchen", "GE", "Gelsenkirchen", "45879"),
    # Rheinland-Pfalz
    ("Rheinland-Pfalz", "RP", "Stadt Mainz", "MZ", "Mainz", "55116"),
    ("Rheinland-Pfalz", "RP", "Stadt Mainz", "MZ", "Mainz", "55118"),
    ("Rheinland-Pfalz", "RP", "Stadt Ludwigshafen", "LU", "Ludwigshafen am Rhein", "67059"),
    ("Rheinland-Pfalz", "RP", "Stadt Koblenz", "KO", "Koblenz", "56068"),
    ("Rheinland-Pfalz", "RP", "Stadt Trier", "TR", "Trier", "54290"),
    # Saarland
    ("Saarland", "SL", "Regionalverband Saarbrücken", "SB", "Saarbrücken", "66111"),
    ("Saarland", "SL", "Regionalverband Saarbrücken", "SB", "Saarbrücken", "66113"),
    # Sachsen
    ("Sachsen", "SN", "Stadt Dresden", "DD", "Dresden", "01067"),
    ("Sachsen", "SN", "Stadt Dresden", "DD", "Dresden", "01069"),
    ("Sachsen", "SN", "Stadt Leipzig", "L", "Leipzig", "04103"),
    ("Sachsen", "SN", "Stadt Leipzig", "L", "Leipzig", "04105"),
    ("Sachsen", "SN", "Stadt Chemnitz", "C", "Chemnitz", "09111"),
    # Sachsen-Anhalt
    ("Sachsen-Anhalt", "ST", "Stadt Magdeburg", "MD", "Magdeburg", "39104"),
    ("Sachsen-Anhalt", "ST", "Stadt Halle (Saale)", "HAL", "Halle (Saale)", "06108"),
    # Schleswig-Holstein
    ("Schleswig-Holstein", "SH", "Stadt Kiel", "KI", "Kiel", "24103"),
    ("Schleswig-Holstein", "SH", "Stadt Kiel", "KI", "Kiel", "24105"),
    ("Schleswig-Holstein", "SH", "Stadt Lübeck", "HL", "Lübeck", "23552"),
    ("Schleswig-Holstein", "SH", "Stadt Flensburg", "FL", "Flensburg", "24937"),
    # Thüringen
    ("Thüringen", "TH", "Stadt Erfurt", "EF", "Erfurt", "99084"),
    ("Thüringen", "TH", "Stadt Erfurt", "EF", "Erfurt", "99086"),
    ("Thüringen", "TH", "Stadt Jena", "J", "Jena", "07743"),
    ("Thüringen", "TH", "Stadt Gera", "G", "Gera", "07545"),
    # Baden-Württemberg
    ("Baden-Württemberg", "BW", "Stuttgart", "S", "Stuttgart", "70173"),
    ("Baden-Württemberg", "BW", "Stuttgart", "S", "Stuttgart", "70174"),
    ("Baden-Württemberg", "BW", "Stuttgart", "S", "Stuttgart", "70176"),
    ("Baden-Württemberg", "BW", "Stadt Mannheim", "MA", "Mannheim", "68159"),
    ("Baden-Württemberg", "BW", "Stadt Karlsruhe", "KA", "Karlsruhe", "76131"),
    ("Baden-Württemberg", "BW", "Stadt Freiburg im Breisgau", "FR", "Freiburg im Breisgau", "79098"),
    ("Baden-Württemberg", "BW", "Stadt Heidelberg", "HD", "Heidelberg", "69115"),
    ("Baden-Württemberg", "BW", "Stadt Heilbronn", "HN", "Heilbronn", "74072"),
    ("Baden-Württemberg", "BW", "Stadt Ulm", "UL", "Ulm", "89073"),
    ("Baden-Württemberg", "BW", "Landkreis Böblingen", "BB", "Böblingen", "71032"),
    ("Baden-Württemberg", "BW", "Landkreis Esslingen", "ES", "Esslingen am Neckar", "73728"),
]


def run():
    db = SessionLocal()
    try:
        expected = len(DATA)
        actual = db.query(City).count()
        if actual == expected:
            print(f"Locations already seeded ({actual} cities). Skipping.")
            return
        if actual > 0:
            print(f"Locations incomplete ({actual}/{expected}) — reseeding...")
            from app.models.location import County, State, Country
            db.query(City).delete()
            db.query(County).delete()
            db.query(State).delete()
            db.query(Country).delete()
            db.commit()

        print("Seeding locations...")

        germany = Country(name="Deutschland", code="DE")
        db.add(germany)
        db.flush()

        state_cache: dict[str, State] = {}
        county_cache: dict[str, County] = {}

        for state_name, state_code, county_name, county_code, city_name, postal_code in DATA:
            state_key = state_code
            if state_key not in state_cache:
                s = State(country_id=germany.id, name=state_name, code=state_code)
                db.add(s)
                db.flush()
                state_cache[state_key] = s

            county_key = f"{state_code}:{county_code}"
            if county_key not in county_cache:
                c = County(state_id=state_cache[state_key].id, name=county_name, code=county_code)
                db.add(c)
                db.flush()
                county_cache[county_key] = c

            db.add(City(
                county_id=county_cache[county_key].id,
                name=city_name,
                postal_code=postal_code,
            ))

        db.commit()
        print(f"Done: 1 country, {len(state_cache)} states, {len(county_cache)} counties, {db.query(City).count()} cities.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()
