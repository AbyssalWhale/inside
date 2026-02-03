BASE_URL = "https://www.n11.com"
SEARCH_PATH = "/arama"

SEARCH_TERMS_BY_CATEGORY = {
    "electronics": [
        "laptop",
        "telefon",
        "kulaklik",
        "tablet",
        "akilli saat",
    ],
    "clothing": [
        "elbise",
        "ayakkabi",
        "canta",
        "gomlek",
        "mont",
    ],
    "home_appliances": [
        "supurge",
        "camasir makinesi",
        "bulasik makinesi",
        "mikser",
        "utu",
    ],
}

ALL_SEARCH_TERMS = [
    term
    for terms in SEARCH_TERMS_BY_CATEGORY.values()
    for term in terms
]

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
}
