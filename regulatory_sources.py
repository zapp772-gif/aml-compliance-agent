"""
Regulatory sources configuration for AML/BSA compliance monitoring
"""

REGULATORY_SOURCES = {
    "FINRA": {
        "name": "Financial Industry Regulatory Authority",
        "rss_feeds": [
            "https://www.finra.org/rss/rule-filings",
            "https://www.finra.org/rss/notices"
        ],
        "urls": [
            "https://www.finra.org/rules-guidance/rulebooks/finra-rules",
            "https://www.finra.org/rules-guidance/notices"
        ],
        "type": "traditional"
    },
    "FATF": {
        "name": "Financial Action Task Force",
        "rss_feeds": [],
        "urls": [
            "https://www.fatf-gafi.org/en/publications.html",
            "https://www.fatf-gafi.org/en/topics/virtual-assets.html"
        ],
        "type": "both"
    },
    "Wolfsberg": {
        "name": "Wolfsberg Group",
        "rss_feeds": [],
        "urls": [
            "https://www.wolfsberg-principles.com/articles"
        ],
        "type": "traditional"
    },
    "FinCEN": {
        "name": "Financial Crimes Enforcement Network",
        "rss_feeds": [
            "https://www.fincen.gov/news-room/rss.xml"
        ],
        "urls": [
            "https://www.fincen.gov/resources/advisories",
            "https://www.fincen.gov/resources/statutes-and-regulations"
        ],
        "type": "both"
    },
    "OFAC": {
        "name": "Office of Foreign Assets Control",
        "rss_feeds": [
            "https://ofac.treasury.gov/rss/ofac_rss.xml"
        ],
        "urls": [
            "https://ofac.treasury.gov/recent-actions",
            "https://ofac.treasury.gov/sanctions-programs-and-country-information"
        ],
        "type": "traditional"
    },
    "FRB": {
        "name": "Federal Reserve Board",
        "rss_feeds": [
            "https://www.federalreserve.gov/feeds/press_all.xml"
        ],
        "urls": [
            "https://www.federalreserve.gov/supervisionreg/topics/aml.htm"
        ],
        "type": "traditional"
    },
    "FDIC": {
        "name": "Federal Deposit Insurance Corporation",
        "rss_feeds": [
            "https://www.fdic.gov/news/press-releases/rss/index.xml"
        ],
        "urls": [
            "https://www.fdic.gov/regulations/laws/rules/"
        ],
        "type": "traditional"
    },
    "OCC": {
        "name": "Office of the Comptroller of the Currency",
        "rss_feeds": [
            "https://www.occ.gov/rss/news-issuances-rss.xml"
        ],
        "urls": [
            "https://www.occ.gov/topics/supervision-and-examination/bsa/index-bsa.html"
        ],
        "type": "traditional"
    },
    "SEC": {
        "name": "United States Securities and Exchange Commission",
        "rss_feeds": [
            "https://www.sec.gov/news/pressreleases.rss"
        ],
        "urls": [
            "https://www.sec.gov/rules/final.shtml",
            "https://www.sec.gov/litigation/litreleases.htm"
        ],
        "type": "both"
    },
    "FCA": {
        "name": "Financial Conduct Authority",
        "rss_feeds": [
            "https://www.fca.org.uk/news/rss.xml"
        ],
        "urls": [
            "https://www.fca.org.uk/publications/policy-statements"
        ],
        "type": "both"
    },
    "AMLA": {
        "name": "European Anti-Money Laundering Authority",
        "rss_feeds": [],
        "urls": [
            "https://www.amla.europa.eu/news"
        ],
        "type": "traditional"
    },
    "EBA": {
        "name": "European Banking Authority",
        "rss_feeds": [
            "https://www.eba.europa.eu/rss.xml"
        ],
        "urls": [
            "https://www.eba.europa.eu/regulation-and-policy/anti-money-laundering-and-countering-financing-terrorism"
        ],
        "type": "both"
    },
    "FFIEC": {
        "name": "Federal Financial Institutions Examination Council",
        "rss_feeds": [],
        "urls": [
            "https://www.ffiec.gov/press/press_releases.htm",
            "https://bsaaml.ffiec.gov/manual"
        ],
        "type": "traditional"
    }
}

REGULATION_CATEGORIES = {
    "BSA": "Bank Secrecy Act",
    "PATRIOT": "USA PATRIOT Act",
    "CDD": "Customer Due Diligence",
    "CIP": "Customer Identification Program",
    "SAR": "Suspicious Activity Reports",
    "CTR": "Currency Transaction Reports",
    "SANCTIONS": "OFAC Sanctions",
    "DIGITAL_ASSETS": "Cryptocurrency/Digital Assets"
}
