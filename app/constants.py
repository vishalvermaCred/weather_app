from enum import Enum

UNIT = "metric"

class Units(Enum):
    TEMPERATURE = "°C"
    AIR_PRESSURE = "hPa"
    WINDSPEED = "m/s"
    HUMIDITY = "%"

class Tables(Enum):
    LOCATION = {
        "name": "locations",
        "get_columns": [
            "location_id::VARCHAR",
            "city",
            "latitude::VARCHAR",
            "longitude::VARCHAR",
            "state",
            "country",
        ],
        "insert_columns": [
            "location_id",
            "city",
            "latitude",
            "longitude",
            "state",
            "country",
            "created",
            "updated"
        ]
    }

    WEATHER = {
        "name": "weather",
        "get_columns": [
            "current_weather",
            "description",
            "temperature",
            "feels_like_temperature",
            "air_pressure",
            "humidity",
            "windspeed"
        ],
        "insert_columns": [
            "weather_id",
            "location_id",
            "current_weather",
            "description",
            "temperature",
            "feels_like_temperature",
            "air_pressure",
            "humidity",
            "windspeed",
            "created",
            "updated"
        ]
    }


COUNTRY_CODES = {"afghanistan": "AF", "\u00e5land islands": "AX", "albania": "AL", "algeria": "DZ", "american samoa": "AS", "andorra": "AD", "angola": "AO", "anguilla": "AI", "antarctica": "AQ", "antigua and barbuda": "AG", "argentina": "AR", "armenia": "AM", "aruba": "AW", "australia": "AU", "austria": "AT", "azerbaijan": "AZ", "bahamas": "BS", "bahrain": "BH", "bangladesh": "BD", "barbados": "BB", "belarus": "BY", "belgium": "BE", "belize": "BZ", "benin": "BJ", "bermuda": "BM", "bhutan": "BT", "bolivia (plurinational state of)": "BO", "bonaire, sint eustatius and saba": "BQ", "bosnia and herzegovina": "BA", "botswana": "BW", "bouvet island": "BV", "brazil": "BR", "british indian ocean territory": "IO", "brunei darussalam": "BN", "bulgaria": "BG", "burkina faso": "BF", "burundi": "BI", "cabo verde": "CV", "cambodia": "KH", "cameroon": "CM", "canada": "CA", "cayman islands": "KY", "central african republic": "CF", "chad": "TD", "chile": "CL", "china": "CN", "christmas island": "CX", "cocos (keeling) islands": "CC", "colombia": "CO", "comoros": "KM", "congo": "CG", "congo, democratic republic of the": "CD", "cook islands": "CK", "costa rica": "CR", "c\u00f4te d'ivoire": "CI", "croatia": "HR", "cuba": "CU", "cura\u00e7ao": "CW", "cyprus": "CY", "czechia": "CZ", "denmark": "DK", "djibouti": "DJ", "dominica": "DM", "dominican republic": "DO", "ecuador": "EC", "egypt": "EG", "el salvador": "SV", "equatorial guinea": "GQ", "eritrea": "ER", "estonia": "EE", "eswatini": "SZ", "ethiopia": "ET", "falkland islands (malvinas)": "FK", "faroe islands": "FO", "fiji": "FJ", "finland": "FI", "france": "FR", "french guiana": "GF", "french polynesia": "PF", "french southern territories": "TF", "gabon": "GA", "gambia": "GM", "georgia": "GE", "germany": "DE", "ghana": "GH", "gibraltar": "GI", "greece": "GR", "greenland": "GL", "grenada": "GD", "guadeloupe": "GP", "guam": "GU", "guatemala": "GT", "guernsey": "GG", "guinea": "GN", "guinea-bissau": "GW", "guyana": "GY", "haiti": "HT", "heard island and mcdonald islands": "HM", "holy see": "VA", "honduras": "HN", "hong kong": "HK", "hungary": "HU", "iceland": "IS", "india": "IN", "indonesia": "ID", "iran (islamic republic of)": "IR", "iraq": "IQ", "ireland": "IE", "isle of man": "IM", "israel": "IL", "italy": "IT", "jamaica": "JM", "japan": "JP", "jersey": "JE", "jordan": "JO", "kazakhstan": "KZ", "kenya": "KE", "kiribati": "KI", "korea (democratic)": "KP", "korea": "KR", "kuwait": "KW", "kyrgyzstan": "KG", "lao people's democratic republic": "LA", "latvia": "LV", "lebanon": "LB", "lesotho": "LS", "liberia": "LR", "libya": "LY", "liechtenstein": "LI", "lithuania": "LT", "luxembourg": "LU", "macao": "MO", "madagascar": "MG", "malawi": "MW", "malaysia": "MY", "maldives": "MV", "mali": "ML", "malta": "MT", "marshall islands": "MH", "martinique": "MQ", "mauritania": "MR", "mauritius": "MU", "mayotte": "YT", "mexico": "MX", "micronesia (federated states of)": "FM", "moldova, republic of": "MD", "monaco": "MC", "mongolia": "MN", "montenegro": "ME", "montserrat": "MS", "morocco": "MA", "mozambique": "MZ", "myanmar": "MM", "namibia": "NA", "nauru": "NR", "nepal": "NP", "netherlands": "NL", "new caledonia": "NC", "new zealand": "NZ", "nicaragua": "NI", "niger": "NE", "nigeria": "NG", "niue": "NU", "norfolk island": "NF", "north macedonia": "MK", "northern mariana islands": "MP", "norway": "NO", "oman": "OM", "pakistan": "PK", "palau": "PW", "palestine, state of": "PS", "panama": "PA", "papua new guinea": "PG", "paraguay": "PY", "peru": "PE", "philippines": "PH", "pitcairn": "PN", "poland": "PL", "portugal": "PT", "puerto rico": "PR", "qatar": "QA", "r\u00e9union": "RE", "romania": "RO", "russian federation": "RU", "rwanda": "RW", "saint barth\u00e9lemy": "BL", "saint helena, ascension and tristan da cunha": "SH", "saint kitts and nevis": "KN", "saint lucia": "LC", "saint martin (french part)": "MF", "saint pierre and miquelon": "PM", "saint vincent and the grenadines": "VC", "samoa": "WS", "san marino": "SM", "sao tome and principe": "ST", "saudi arabia": "SA", "senegal": "SN", "serbia": "RS", "seychelles": "SC", "sierra leone": "SL", "singapore": "SG", "sint maarten (dutch part)": "SX", "slovakia": "SK", "slovenia": "SI", "solomon islands": "SB", "somalia": "SO", "south africa": "ZA", "south georgia and the south sandwich islands": "GS", "south sudan": "SS", "spain": "ES", "sri lanka": "LK", "sudan": "SD", "suriname": "SR", "svalbard and jan mayen": "SJ", "sweden": "SE", "switzerland": "CH", "syrian arab republic": "SY", "taiwan, province of china": "TW", "tajikistan": "TJ", "tanzania, united republic of": "TZ", "thailand": "TH", "timor-leste": "TL", "togo": "TG", "tokelau": "TK", "tonga": "TO", "trinidad and tobago": "TT", "tunisia": "TN", "turkey": "TR", "turkmenistan": "TM", "turks and caicos islands": "TC", "tuvalu": "TV", "uganda": "UG", "ukraine": "UA", "united arab emirates": "AE", "united kingdom of great britain and northern ireland": "GB", "united states of america": "US", "united states minor outlying islands": "UM", "uruguay": "UY", "uzbekistan": "UZ", "vanuatu": "VU", "venezuela": "VE", "vietnam": "VN", "virgin islands (british)": "VG", "virgin islands (u.s.)": "VI", "wallis and futuna": "WF", "western sahara": "EH", "yemen": "YE", "zambia": "ZM", "zimbabwe": "ZW"}

COUNTRY_CODES_TO_NAMES = {"AF": "Afghanistan", "AX": "\u00c5land Islands", "AL": "Albania", "DZ": "Algeria", "AS": "American Samoa", "AD": "Andorra", "AO": "Angola", "AI": "Anguilla", "AQ": "Antarctica", "AG": "Antigua and Barbuda", "AR": "Argentina", "AM": "Armenia", "AW": "Aruba", "AU": "Australia", "AT": "Austria", "AZ": "Azerbaijan", "BS": "Bahamas", "BH": "Bahrain", "BD": "Bangladesh", "BB": "Barbados", "BY": "Belarus", "BE": "Belgium", "BZ": "Belize", "BJ": "Benin", "BM": "Bermuda", "BT": "Bhutan", "BO": "Bolivia (Plurinational State of)", "BQ": "Bonaire, Sint Eustatius and Saba", "BA": "Bosnia and Herzegovina", "BW": "Botswana", "BV": "Bouvet Island", "BR": "Brazil", "IO": "British Indian Ocean Territory", "BN": "Brunei Darussalam", "BG": "Bulgaria", "BF": "Burkina Faso", "BI": "Burundi", "CV": "Cabo Verde", "KH": "Cambodia", "CM": "Cameroon", "CA": "Canada", "KY": "Cayman Islands", "CF": "Central African Republic", "TD": "Chad", "CL": "Chile", "CN": "China", "CX": "Christmas Island", "CC": "Cocos (Keeling) Islands", "CO": "Colombia", "KM": "Comoros", "CG": "Congo", "CD": "Congo, Democratic Republic of the", "CK": "Cook Islands", "CR": "Costa Rica", "CI": "C\u00f4te d'Ivoire", "HR": "Croatia", "CU": "Cuba", "CW": "Cura\u00e7ao", "CY": "Cyprus", "CZ": "Czechia", "DK": "Denmark", "DJ": "Djibouti", "DM": "Dominica", "DO": "Dominican Republic", "EC": "Ecuador", "EG": "Egypt", "SV": "El Salvador", "GQ": "Equatorial Guinea", "ER": "Eritrea", "EE": "Estonia", "SZ": "Eswatini", "ET": "Ethiopia", "FK": "Falkland Islands (Malvinas)", "FO": "Faroe Islands", "FJ": "Fiji", "FI": "Finland", "FR": "France", "GF": "French Guiana", "PF": "French Polynesia", "TF": "French Southern Territories", "GA": "Gabon", "GM": "Gambia", "GE": "Georgia", "DE": "Germany", "GH": "Ghana", "GI": "Gibraltar", "GR": "Greece", "GL": "Greenland", "GD": "Grenada", "GP": "Guadeloupe", "GU": "Guam", "GT": "Guatemala", "GG": "Guernsey", "GN": "Guinea", "GW": "Guinea-Bissau", "GY": "Guyana", "HT": "Haiti", "HM": "Heard Island and McDonald Islands", "VA": "Holy See", "HN": "Honduras", "HK": "Hong Kong", "HU": "Hungary", "IS": "Iceland", "IN": "India", "ID": "Indonesia", "IR": "Iran (Islamic Republic of)", "IQ": "Iraq", "IE": "Ireland", "IM": "Isle of Man", "IL": "Israel", "IT": "Italy", "JM": "Jamaica", "JP": "Japan", "JE": "Jersey", "JO": "Jordan", "KZ": "Kazakhstan", "KE": "Kenya", "KI": "Kiribati", "KP": "Korea (Democratic People's Republic of)", "KR": "Korea, Republic of", "KW": "Kuwait", "KG": "Kyrgyzstan", "LA": "Lao People's Democratic Republic", "LV": "Latvia", "LB": "Lebanon", "LS": "Lesotho", "LR": "Liberia", "LY": "Libya", "LI": "Liechtenstein", "LT": "Lithuania", "LU": "Luxembourg", "MO": "Macao", "MG": "Madagascar", "MW": "Malawi", "MY": "Malaysia", "MV": "Maldives", "ML": "Mali", "MT": "Malta", "MH": "Marshall Islands", "MQ": "Martinique", "MR": "Mauritania", "MU": "Mauritius", "YT": "Mayotte", "MX": "Mexico", "FM": "Micronesia (Federated States of)", "MD": "Moldova, Republic of", "MC": "Monaco", "MN": "Mongolia", "ME": "Montenegro", "MS": "Montserrat", "MA": "Morocco", "MZ": "Mozambique", "MM": "Myanmar", "NaN": "Namibia", "NR": "Nauru", "NP": "Nepal", "NL": "Netherlands", "NC": "New Caledonia", "NZ": "New Zealand", "NI": "Nicaragua", "NE": "Niger", "NG": "Nigeria", "NU": "Niue", "NF": "Norfolk Island", "MK": "North Macedonia", "MP": "Northern Mariana Islands", "NO": "Norway", "OM": "Oman", "PK": "Pakistan", "PW": "Palau", "PS": "Palestine, State of", "PA": "Panama", "PG": "Papua New Guinea", "PY": "Paraguay", "PE": "Peru", "PH": "Philippines", "PN": "Pitcairn", "PL": "Poland", "PT": "Portugal", "PR": "Puerto Rico", "QA": "Qatar", "RE": "R\u00e9union", "RO": "Romania", "RU": "Russian Federation", "RW": "Rwanda", "BL": "Saint Barth\u00e9lemy", "SH": "Saint Helena, Ascension and Tristan da Cunha", "KN": "Saint Kitts and Nevis", "LC": "Saint Lucia", "MF": "Saint Martin (French part)", "PM": "Saint Pierre and Miquelon", "VC": "Saint Vincent and the Grenadines", "WS": "Samoa", "SM": "San Marino", "ST": "Sao Tome and Principe", "SA": "Saudi Arabia", "SN": "Senegal", "RS": "Serbia", "SC": "Seychelles", "SL": "Sierra Leone", "SG": "Singapore", "SX": "Sint Maarten (Dutch part)", "SK": "Slovakia", "SI": "Slovenia", "SB": "Solomon Islands", "SO": "Somalia", "ZA": "South Africa", "GS": "South Georgia and the South Sandwich Islands", "SS": "South Sudan", "ES": "Spain", "LK": "Sri Lanka", "SD": "Sudan", "SR": "Suriname", "SJ": "Svalbard and Jan Mayen", "SE": "Sweden", "CH": "Switzerland", "SY": "Syrian Arab Republic", "TW": "Taiwan, Province of China", "TJ": "Tajikistan", "TZ": "Tanzania, United Republic of", "TH": "Thailand", "TL": "Timor-Leste", "TG": "Togo", "TK": "Tokelau", "TO": "Tonga", "TT": "Trinidad and Tobago", "TN": "Tunisia", "TR": "Turkey", "TM": "Turkmenistan", "TC": "Turks and Caicos Islands", "TV": "Tuvalu", "UG": "Uganda", "UA": "Ukraine", "AE": "United Arab Emirates", "GB": "United Kingdom of Great Britain and Northern Ireland", "US": "United States of America", "UM": "United States Minor Outlying Islands", "UY": "Uruguay", "UZ": "Uzbekistan", "VU": "Vanuatu", "VE": "Venezuela (Bolivarian Republic of)", "VN": "Viet Nam", "VG": "Virgin Islands (British)", "VI": "Virgin Islands (U.S.)", "WF": "Wallis and Futuna", "EH": "Western Sahara", "YE": "Yemen", "ZM": "Zambia", "ZW": "Zimbabwe"}

STATE_NAME_TO_CODES = {"andaman and nicobar islands":"AN", "andhra pradesh":"AP","arunachal pradesh":"AR","assam":"AS","bihar":"BR","chandigarh":"CH","chhattisgarh":"CG","dadra and nagar haveli":"DH","daman and diu":"DD","delhi":"DL","goa":"GA","gujarat":"GJ","haryana":"HR","himachal pradesh":"HP","jammu and kashmir":"JK","jharkhand":"JH","karnataka":"KA","kerala":"KL","lakshadweep":"LD","madhya pradesh":"MP","maharashtra":"MH","manipur":"MN","meghalaya":"ML","mizoram":"MZ","nagaland":"NL","orissa":"OR","pondicherry":"PY","punjab":"PB","rajasthan":"RJ","sikkim":"SK","tamil nadu":"TN","tripura":"TR","uttar pradesh":"UP","uttarakhand":"UK","west bengal":"WB"}