# E-number additives reference — flags additives that are plastic-derived
# or linked to plastic contamination from processing.

PLASTIC_ADDITIVES = {
    # Petroleum-derived preservatives
    "e320": {"name": "BHA (Butylated Hydroxyanisole)", "pct": 4, "reason": "Petroleum-derived antioxidant"},
    "e321": {"name": "BHT (Butylated Hydroxytoluene)", "pct": 4, "reason": "Petroleum-derived antioxidant"},
    "e310": {"name": "Propyl Gallate", "pct": 2, "reason": "Synthetic antioxidant, petroleum-derived"},
    "e311": {"name": "Octyl Gallate", "pct": 2, "reason": "Synthetic antioxidant, petroleum-derived"},
    "e312": {"name": "Dodecyl Gallate", "pct": 2, "reason": "Synthetic antioxidant, petroleum-derived"},

    # Synthetic dyes (petroleum-derived)
    "e102": {"name": "Tartrazine (Yellow 5)", "pct": 3, "reason": "Petroleum-derived azo dye"},
    "e104": {"name": "Quinoline Yellow", "pct": 3, "reason": "Petroleum-derived synthetic dye"},
    "e110": {"name": "Sunset Yellow (Yellow 6)", "pct": 3, "reason": "Petroleum-derived azo dye"},
    "e122": {"name": "Carmoisine (Red 3)", "pct": 3, "reason": "Petroleum-derived azo dye"},
    "e124": {"name": "Ponceau 4R", "pct": 3, "reason": "Petroleum-derived azo dye"},
    "e129": {"name": "Allura Red (Red 40)", "pct": 3, "reason": "Petroleum-derived azo dye"},
    "e133": {"name": "Brilliant Blue (Blue 1)", "pct": 3, "reason": "Petroleum-derived synthetic dye"},

    # Plastic waxes / coatings
    "e901": {"name": "Beeswax", "pct": 0, "reason": "Natural — no plastic concern"},
    "e914": {"name": "Oxidised Polyethylene Wax", "pct": 12, "reason": "Direct polyethylene plastic wax coating"},
    "e905": {"name": "Mineral Hydrocarbons (Microcrystalline Wax)", "pct": 6, "reason": "Petroleum-derived wax used on fruit"},

    # Synthetic emulsifiers
    "e471": {"name": "Mono/Diglycerides", "pct": 1, "reason": "Can be petroleum-derived"},
    "e472": {"name": "Acetic/Lactic Acid Esters of Mono/Diglycerides", "pct": 2, "reason": "Synthetic emulsifier"},
    "e433": {"name": "Polysorbate 80", "pct": 3, "reason": "Synthetic emulsifier, gut barrier concerns"},
    "e435": {"name": "Polysorbate 60", "pct": 3, "reason": "Synthetic emulsifier"},
    "e436": {"name": "Polysorbate 65", "pct": 3, "reason": "Synthetic emulsifier"},

    # Others
    "e171": {"name": "Titanium Dioxide", "pct": 5, "reason": "Nanoparticle often coated with plastic polymer"},
    "e174": {"name": "Silver", "pct": 0, "reason": "Metal — no plastic concern"},
    "e900": {"name": "Dimethyl Silicone (Simethicone)", "pct": 4, "reason": "Silicone polymer — synthetic plastic family"},
    "e322": {"name": "Lecithin", "pct": 0, "reason": "Natural emulsifier — no plastic concern"},
}


def match_additives(additives_tags):
    """
    Match OFT additives_tags against our reference.
    Returns list of matched additive dicts.
    """
    matched = []
    for tag in (additives_tags or []):
        key = tag.lower().replace("en:", "")
        if key in PLASTIC_ADDITIVES:
            entry = PLASTIC_ADDITIVES[key].copy()
            entry["e_number"] = key.upper()
            if entry["pct"] > 0:
                matched.append(entry)
    return matched


def get_additives_block(additives_tags):
    """Returns a text block for Claude's prompt listing plastic-linked additives found."""
    matched = match_additives(additives_tags)
    if not matched:
        return ""
    lines = ["ADDITIVES FLAGGED:"]
    for a in matched:
        lines.append(f"  - {a['e_number']} {a['name']}: +{a['pct']}% — {a['reason']}")
    return "\n".join(lines)
