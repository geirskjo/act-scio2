from act.scio.plugin import BasePlugin, Result
import addict
from typing import Text, List, Dict, Set
import ipaddress
import re


class Plugin(BasePlugin):
    name = "indicators"
    info = "Extracting Atomic indicators like ip/fqdn/hash from body of text"
    version = "0.1"
    dependencies: List[Text] = []

    md5 = re.compile("\\b[0-9a-fA-F]{32}\\b")
    sha1 = re.compile("\\b[.0-9a-fA-F]{40}\\b")
    sha256 = re.compile("\\b[0-9a-fA-F]{64}\\b")
    ipv4 = re.compile("\\b([0-2]?[0-9]?[0-9])\\.([0-2]?[0-9]?[0-9])\\.([0-2]?[0-9]?[0-9])" +
                      "\\.([0-2]?[0-9]?[0-9])\\b")
    email = re.compile("\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}\\b")
    fqdn = re.compile("\\b([a-zA-Z0-9\\.\\-]+\\.[a-zA-Z0-9\\.\\-]+)\\b")

    allposipv6 = re.compile("\\b[a-f0-9:.]+:[a-f0-9:.]+:[a-f0-9:.]+\\b")

    async def analyze(self, nlpdata: addict.Dict) -> Result:

        text = nlpdata.content

        res = addict.Dict()

        res.md5 = self.md5.findall(text)
        res.sha1 = self.sha1.findall(text)
        res.sha256 = self.sha256.findall(text)
        res.email = self.email.findall(text)
        res.fqdn = [dn for dn in self.fqdn.findall(text)
                    if dn.split(".")[-1] in TLDS]
        res.ipv4 = ['.'.join(ip) for ip in self.ipv4.findall(text)]

        pos_ipv6 = []
        for candidate in self.allposipv6.findall(text):
            try:
                addr = ipaddress.ip_address(candidate)
                if addr.version != 6:
                    pos_ipv6.append(candidate)
            except ValueError:
                pass

        res.ipv6 = pos_ipv6

        return Result(name=self.name, version=self.version, result=res)


TLDS: Set[Text] = {
    "abb",
    "abbott",
    "abogado",
    "ac",
    "academy",
    "accountant",
    "accountants",
    "active",
    "actor",
    "ad",
    "ads",
    "adult",
    "ae",
    "aero",
    "af",
    "afl",
    "ag",
    "agency",
    "ai",
    "airforce",
    "al",
    "allfinanz",
    "alsace",
    "am",
    "amsterdam",
    "an",
    "android",
    "ao",
    "apartments",
    "aq",
    "aquarelle",
    "ar",
    "archi",
    "army",
    "arpa",
    "as",
    "asia",
    "associates",
    "at",
    "attorney",
    "au",
    "auction",
    "audio",
    "autos",
    "aw",
    "ax",
    "axa",
    "az",
    "ba",
    "band",
    "bank",
    "bar",
    "barclaycard",
    "barclays",
    "bargains",
    "bauhaus",
    "bayern",
    "bb",
    "bbc",
    "bd",
    "be",
    "beer",
    "berlin",
    "best",
    "bf",
    "bg",
    "bh",
    "bi",
    "bid",
    "bike",
    "bingo",
    "bio",
    "biz",
    "bj",
    "bl",
    "black",
    "blackfriday",
    "bloomberg",
    "blue",
    "bm",
    "bmw",
    "bn",
    "bnpparibas",
    "bo",
    "boats",
    "bond",
    "boo",
    "boutique",
    "bq",
    "br",
    "brussels",
    "bs",
    "bt",
    "budapest",
    "build",
    "builders",
    "business",
    "buzz",
    "bv",
    "bw",
    "by",
    "bz",
    "bzh",
    "ca",
    "cab",
    "cafe",
    "cal",
    "camera",
    "camp",
    "cancerresearch",
    "canon",
    "capetown",
    "capital",
    "caravan",
    "cards",
    "care",
    "career",
    "careers",
    "cartier",
    "casa",
    "cash",
    "casino",
    "cat",
    "catering",
    "cbn",
    "cc",
    "cd",
    "center",
    "ceo",
    "cern",
    "cf",
    "cfd",
    "cg",
    "ch",
    "channel",
    "chat",
    "cheap",
    "chloe",
    "christmas",
    "chrome",
    "church",
    "ci",
    "citic",
    "city",
    "ck",
    "cl",
    "claims",
    "cleaning",
    "click",
    "clinic",
    "clothing",
    "club",
    "cm",
    "cn",
    "co",
    "coach",
    "codes",
    "coffee",
    "college",
    "cologne",
    "com",
    "community",
    "company",
    "computer",
    "condos",
    "construction",
    "consulting",
    "contractors",
    "cooking",
    "cool",
    "coop",
    "country",
    "courses",
    "cr",
    "credit",
    "creditcard",
    "cricket",
    "crs",
    "cruises",
    "cu",
    "cuisinella",
    "cv",
    "cw",
    "cx",
    "cy",
    "cymru",
    "cyou",
    "cz",
    "dabur",
    "dad",
    "dance",
    "date",
    "dating",
    "datsun",
    "day",
    "dclk",
    "de",
    "deals",
    "degree",
    "delivery",
    "democrat",
    "dental",
    "dentist",
    "desi",
    "design",
    "dev",
    "diamonds",
    "diet",
    "digital",
    "direct",
    "directory",
    "discount",
    "dj",
    "dk",
    "dm",
    "dnp",
    "do",
    "docs",
    "doha",
    "domains",
    "doosan",
    "download",
    "durban",
    "dvag",
    "dz",
    "eat",
    "ec",
    "edu",
    "education",
    "ee",
    "eg",
    "eh",
    "email",
    "emerck",
    "energy",
    "engineer",
    "engineering",
    "enterprises",
    "epson",
    "equipment",
    "er",
    "erni",
    "es",
    "esq",
    "estate",
    "et",
    "eu",
    "eurovision",
    "eus",
    "events",
    "everbank",
    "exchange",
    "expert",
    "exposed",
    "express",
    "fail",
    "faith",
    "fan",
    "fans",
    "farm",
    "fashion",
    "feedback",
    "fi",
    "film",
    "finance",
    "financial",
    "firmdale",
    "fish",
    "fishing",
    "fit",
    "fitness",
    "fj",
    "fk",
    "flights",
    "florist",
    "flowers",
    "flsmidth",
    "fly",
    "fm",
    "fo",
    "foo",
    "football",
    "forex",
    "forsale",
    "foundation",
    "fr",
    "frl",
    "frogans",
    "fund",
    "furniture",
    "futbol",
    "ga",
    "gal",
    "gallery",
    "garden",
    "gb",
    "gbiz",
    "gd",
    "gdn",
    "ge",
    "gent",
    "gf",
    "gg",
    "ggee",
    "gh",
    "gi",
    "gift",
    "gifts",
    "gives",
    "gl",
    "glass",
    "gle",
    "global",
    "globo",
    "gm",
    "gmail",
    "gmo",
    "gmx",
    "gn",
    "gold",
    "goldpoint",
    "golf",
    "goo",
    "goog",
    "google",
    "gop",
    "gov",
    "gp",
    "gq",
    "gr",
    "graphics",
    "gratis",
    "green",
    "gripe",
    "gs",
    "gt",
    "gu",
    "guge",
    "guide",
    "guitars",
    "guru",
    "gw",
    "gy",
    "hamburg",
    "hangout",
    "haus",
    "healthcare",
    "help",
    "here",
    "hermes",
    "hiphop",
    "hiv",
    "hk",
    "hm",
    "hn",
    "holdings",
    "holiday",
    "homes",
    "horse",
    "host",
    "hosting",
    "house",
    "how",
    "hr",
    "ht",
    "hu",
    "ibm",
    "id",
    "ie",
    "ifm",
    "il",
    "im",
    "immo",
    "immobilien",
    "in",
    "industries",
    "infiniti",
    "info",
    "ing",
    "ink",
    "institute",
    "insure",
    "int",
    "international",
    "investments",
    "io",
    "iq",
    "ir",
    "irish",
    "is",
    "it",
    "iwc",
    "java",
    "jcb",
    "je",
    "jetzt",
    "jewelry",
    "jm",
    "jo",
    "jobs",
    "joburg",
    "jp",
    "juegos",
    "kaufen",
    "kddi",
    "ke",
    "kg",
    "kh",
    "ki",
    "kim",
    "kitchen",
    "kiwi",
    "km",
    "kn",
    "koeln",
    "komatsu",
    "kp",
    "kr",
    "krd",
    "kred",
    "kw",
    "ky",
    "kyoto",
    "kz",
    "la",
    "lacaixa",
    "land",
    "lat",
    "latrobe",
    "lawyer",
    "lb",
    "lc",
    "lds",
    "lease",
    "leclerc",
    "legal",
    "lgbt",
    "li",
    "lidl",
    "life",
    "lighting",
    "limited",
    "limo",
    "link",
    "lk",
    "loan",
    "loans",
    "london",
    "lotte",
    "lotto",
    "love",
    "lr",
    "ls",
    "lt",
    "ltda",
    "lu",
    "luxe",
    "luxury",
    "lv",
    "ly",
    "ma",
    "madrid",
    "maif",
    "maison",
    "management",
    "mango",
    "market",
    "marketing",
    "markets",
    "marriott",
    "mc",
    "md",
    "me",
    "media",
    "meet",
    "melbourne",
    "meme",
    "memorial",
    "menu",
    "mf",
    "mg",
    "mh",
    "miami",
    "mil",
    "mini",
    "mk",
    "ml",
    "mm",
    "mma",
    "mn",
    "mo",
    "mobi",
    "moda",
    "moe",
    "monash",
    "money",
    "mormon",
    "mortgage",
    "moscow",
    "motorcycles",
    "mov",
    "movie",
    "mp",
    "mq",
    "mr",
    "ms",
    "mt",
    "mtn",
    "mtpc",
    "mu",
    "museum",
    "mv",
    "mw",
    "mx",
    "my",
    "mz",
    "na",
    "nagoya",
    "name",
    "navy",
    "nc",
    "ne",
    "net",
    "network",
    "neustar",
    "new",
    "news",
    "nexus",
    "nf",
    "ng",
    "ngo",
    "nhk",
    "ni",
    "nico",
    "ninja",
    "nissan",
    "nl",
    "no",
    "np",
    "nr",
    "nra",
    "nrw",
    "ntt",
    "nu",
    "nyc",
    "nz",
    "okinawa",
    "om",
    "one",
    "ong",
    "onl",
    "online",
    "ooo",
    "org",
    "organic",
    "osaka",
    "otsuka",
    "ovh",
    "pa",
    "page",
    "panerai",
    "paris",
    "partners",
    "parts",
    "party",
    "pe",
    "pf",
    "pg",
    "ph",
    "pharmacy",
    "photo",
    "photography",
    "photos",
    "physio",
    "piaget",
    "pics",
    "pictet",
    "pictures",
    "pink",
    "pizza",
    "pk",
    "pl",
    "place",
    "plumbing",
    "plus",
    "pm",
    "pn",
    "pohl",
    "poker",
    "porn",
    "post",
    "pr",
    "praxi",
    "press",
    "pro",
    "prod",
    "productions",
    "prof",
    "properties",
    "property",
    "ps",
    "pt",
    "pub",
    "pw",
    "py",
    "qa",
    "qpon",
    "quebec",
    "racing",
    "re",
    "realtor",
    "recipes",
    "red",
    "redstone",
    "rehab",
    "reise",
    "reisen",
    "reit",
    "ren",
    "rentals",
    "repair",
    "report",
    "republican",
    "rest",
    "restaurant",
    "review",
    "reviews",
    "rich",
    "rio",
    "rip",
    "ro",
    "rocks",
    "rodeo",
    "rs",
    "rsvp",
    "ru",
    "ruhr",
    "rw",
    "ryukyu",
    "sa",
    "saarland",
    "sale",
    "samsung",
    "sap",
    "sarl",
    "saxo",
    "sb",
    "sc",
    "sca",
    "scb",
    "schmidt",
    "scholarships",
    "school",
    "schule",
    "schwarz",
    "science",
    "scot",
    "sd",
    "se",
    "seat",
    "services",
    "sew",
    "sex",
    "sexy",
    "sg",
    "sh",
    "shiksha",
    "shoes",
    "show",
    "shriram",
    "si",
    "singles",
    "site",
    "sj",
    "sk",
    "sky",
    "sl",
    "sm",
    "sn",
    "so",
    "social",
    "software",
    "sohu",
    "solar",
    "solutions",
    "sony",
    "soy",
    "space",
    "spiegel",
    "spreadbetting",
    "sr",
    "ss",
    "st",
    "study",
    "style",
    "su",
    "sucks",
    "supplies",
    "supply",
    "support",
    "surf",
    "surgery",
    "suzuki",
    "sv",
    "sx",
    "sy",
    "sydney",
    "systems",
    "sz",
    "taipei",
    "tatar",
    "tattoo",
    "tax",
    "tc",
    "td",
    "team",
    "tech",
    "technology",
    "tel",
    "temasek",
    "tennis",
    "tf",
    "tg",
    "th",
    "tickets",
    "tienda",
    "tips",
    "tires",
    "tirol",
    "tj",
    "tk",
    "tl",
    "tm",
    "tn",
    "to",
    "today",
    "tokyo",
    "tools",
    "top",
    "toshiba",
    "tours",
    "town",
    "toys",
    "tp",
    "tr",
    "trade",
    "trading",
    "training",
    "travel",
    "trust",
    "tt",
    "tui",
    "tv",
    "tw",
    "tz",
    "ua",
    "ug",
    "uk",
    "um",
    "university",
    "uno",
    "uol",
    "us",
    "uy",
    "uz",
    "va",
    "vacations",
    "vc",
    "ve",
    "vegas",
    "ventures",
    "versicherung",
    "vet",
    "vg",
    "vi",
    "viajes",
    "video",
    "villas",
    "vision",
    "vlaanderen",
    "vn",
    "vodka",
    "vote",
    "voting",
    "voto",
    "voyage",
    "vu",
    "wales",
    "wang",
    "watch",
    "webcam",
    "website",
    "wed",
    "wedding",
    "weir",
    "wf",
    "whoswho",
    "wien",
    "wiki",
    "williamhill",
    "win",
    "wme",
    "work",
    "works",
    "world",
    "ws",
    "wtc",
    "wtf",
    "xerox",
    "xin",
    "测试",
    "परीक्षा",
    "佛山",
    "慈善",
    "集团",
    "在线",
    "한국",
    "ভারত",
    "八卦",
    "موقع",
    "বাংলা",
    "公益",
    "公司",
    "移动",
    "我爱你",
    "москва",
    "испытание",
    "қаз",
    "онлайн",
    "сайт",
    "срб",
    "бел",
    "时尚",
    "테스트",
    "淡马锡",
    "орг",
    "삼성",
    "சிங்கப்பூர்",
    "商标",
    "商店",
    "商城",
    "дети",
    "мкд",
    "טעסט",
    "中文网",
    "中信",
    "中国",
    "中國",
    "谷歌",
    "భారత్",
    "ලංකා",
    "測試",
    "ભારત",
    "भारत",
    "آزمایشی",
    "பரிட்சை",
    "网店",
    "संगठन",
    "网络",
    "укр",
    "香港",
    "δοκιμή",
    "飞利浦",
    "إختبار",
    "台湾",
    "台灣",
    "手机",
    "мон",
    "الجزائر",
    "عمان",
    "ایران",
    "امارات",
    "بازار",
    "پاکستان",
    "الاردن",
    "بھارت",
    "المغرب",
    "السعودية",
    "سودان",
    "عراق",
    "مليسيا",
    "澳門",
    "政府",
    "شبكة",
    "გე",
    "机构",
    "组织机构",
    "健康",
    "ไทย",
    "سورية",
    "рус",
    "рф",
    "تونس",
    "みんな",
    "グーグル",
    "世界",
    "ਭਾਰਤ",
    "网址",
    "游戏",
    "vermögensberater",
    "vermögensberatung",
    "企业",
    "信息",
    "مصر",
    "قطر",
    "广东",
    "இலங்கை",
    "இந்தியா",
    "հայ",
    "新加坡",
    "فلسطين",
    "テスト",
    "政务",
    "xxx",
    "xyz",
    "yachts",
    "yandex",
    "ye",
    "yodobashi",
    "yoga",
    "yokohama",
    "youtube",
    "yt",
    "za",
    "zip",
    "zm",
    "zone",
    "zuerich",
    "zw",
}
