CITIES = [
    "Paris",
    "Budapest",
    "Skopje",
    "Rotterdam",
    "Valencia",
    "Vancouver",
    "Amsterdam",
    "Vienna",
    "Sydney",
    "New York City",
    "London",
    "Bangkok",
    "Hong Kong",
    "Dubai",
    "Rome",
    "Istanbul",
]


def search_cities(search_text):
    if search_text == "*":
        return CITIES.copy()

    if len(search_text) < 2:
        return []

    normalized_search = search_text.lower()
    return [city for city in CITIES if normalized_search in city.lower()]
