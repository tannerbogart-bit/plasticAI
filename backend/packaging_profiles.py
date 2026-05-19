# Plastic packaging type profiles — used to adjust risk score based on
# how a product is packaged, not just its ingredients.

PACKAGING_PROFILES = {
    "pet": {
        "name": "PET Plastic (Type 1)",
        "plastic_pct_contribution": 8,
        "leaches": ["acetaldehyde", "antimony", "phthalates"],
        "note": "Common in water/soda bottles. Leaching increases with heat and reuse.",
    },
    "hdpe": {
        "name": "HDPE Plastic (Type 2)",
        "plastic_pct_contribution": 3,
        "leaches": ["nonylphenol"],
        "note": "Relatively stable. Milk jugs, detergent bottles.",
    },
    "pvc": {
        "name": "PVC Plastic (Type 3)",
        "plastic_pct_contribution": 18,
        "leaches": ["phthalates", "lead", "cadmium", "bpa"],
        "note": "High risk. Cling wrap, some food containers. Avoid for food contact.",
    },
    "ldpe": {
        "name": "LDPE Plastic (Type 4)",
        "plastic_pct_contribution": 4,
        "leaches": ["nonylphenol"],
        "note": "Squeeze bottles, bread bags. Relatively low risk.",
    },
    "pp": {
        "name": "Polypropylene (Type 5)",
        "plastic_pct_contribution": 3,
        "leaches": ["polypropylene oligomers"],
        "note": "Yogurt containers, bottle caps. Generally safer.",
    },
    "ps": {
        "name": "Polystyrene (Type 6)",
        "plastic_pct_contribution": 15,
        "leaches": ["styrene", "benzene"],
        "note": "Coffee cups, takeout containers. Styrene is a possible carcinogen.",
    },
    "eps": {
        "name": "Expanded Polystyrene (Styrofoam)",
        "plastic_pct_contribution": 20,
        "leaches": ["styrene", "ethylbenzene"],
        "note": "Foam cups and boxes. Leaching is significant with hot food/drinks.",
    },
    "pc": {
        "name": "Polycarbonate (Type 7)",
        "plastic_pct_contribution": 22,
        "leaches": ["bpa", "bisphenol-s"],
        "note": "Baby bottles, reusable bottles. High BPA concern.",
    },
    "bopp": {
        "name": "BOPP Film (snack bags)",
        "plastic_pct_contribution": 6,
        "leaches": ["plastic additives", "slip agents"],
        "note": "Chip bags, candy wrappers. Microplastic shedding from crinkle.",
    },
    "tetra_pak": {
        "name": "Tetra Pak / Multi-layer",
        "plastic_pct_contribution": 10,
        "leaches": ["polyethylene layer migrants"],
        "note": "Inner PE layer contacts liquid. More risk with acidic contents.",
    },
    "epoxy_lining": {
        "name": "Epoxy Can Lining",
        "plastic_pct_contribution": 14,
        "leaches": ["bpa", "bisphenol-a diglycidyl ether"],
        "note": "Most canned food linings. BPA leaching is well-documented.",
    },
    "pfas_coating": {
        "name": "PFAS Non-stick / Grease-proof Coating",
        "plastic_pct_contribution": 25,
        "leaches": ["pfas", "pfoa", "pfos"],
        "note": "Fast-food wrappers, microwave popcorn bags, some baking papers.",
    },
}

# Map Open Food Facts packaging tags → profile keys
OFF_PACKAGING_MAP = {
    "en:pet-plastic": "pet",
    "en:hdpe-plastic": "hdpe",
    "en:pvc-plastic": "pvc",
    "en:ldpe-plastic": "ldpe",
    "en:polypropylene": "pp",
    "en:polystyrene": "ps",
    "en:expanded-polystyrene": "eps",
    "en:polycarbonate": "pc",
    "en:tetra-pak": "tetra_pak",
    "en:can": "epoxy_lining",
    "en:tin": "epoxy_lining",
    "en:metal-can": "epoxy_lining",
}

# Map product category tags → likely packaging when tags are missing
CATEGORY_PACKAGING_DEFAULTS = {
    "en:beverages": "pet",
    "en:sodas": "pet",
    "en:waters": "pet",
    "en:canned-foods": "epoxy_lining",
    "en:canned-vegetables": "epoxy_lining",
    "en:snacks": "bopp",
    "en:chips-and-crisps": "bopp",
    "en:microwave-popcorn": "pfas_coating",
    "en:fast-foods": "pfas_coating",
}


def get_packaging_profile(packaging_tags, category_tags):
    """Return the highest-risk matching packaging profile."""
    for tag in (packaging_tags or []):
        key = OFF_PACKAGING_MAP.get(tag)
        if key:
            return key, PACKAGING_PROFILES[key]

    for tag in (category_tags or []):
        key = CATEGORY_PACKAGING_DEFAULTS.get(tag)
        if key:
            return key, PACKAGING_PROFILES[key]

    return None, None


def get_packaging_block(packaging_tags, category_tags):
    """Returns a text block for Claude's prompt describing packaging risk."""
    key, profile = get_packaging_profile(packaging_tags, category_tags)
    if not profile:
        return ""
    return (
        f"PACKAGING: {profile['name']} (+{profile['plastic_pct_contribution']}% plastic risk)\n"
        f"  Leaches: {', '.join(profile['leaches'])}\n"
        f"  Note: {profile['note']}"
    )
