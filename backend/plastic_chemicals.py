# Curated reference list of plastic-linked chemicals and ingredients.
# Each entry: ingredient keyword (lowercase) → {risk, reason}
# This is fed into the Claude prompt to ground scoring in real data.

PLASTIC_CHEMICALS = {
    # Direct microplastics
    "microplastic": {"risk": "very high", "reason": "Direct microplastic particle"},
    "polyethylene": {"risk": "very high", "reason": "Plastic polymer (PE)"},
    "polypropylene": {"risk": "very high", "reason": "Plastic polymer (PP)"},
    "polystyrene": {"risk": "very high", "reason": "Plastic polymer (PS), leaches styrene"},
    "polyvinyl chloride": {"risk": "very high", "reason": "PVC, releases vinyl chloride"},
    "pvc": {"risk": "very high", "reason": "PVC, releases vinyl chloride"},
    "nylon": {"risk": "high", "reason": "Synthetic plastic polymer"},
    "teflon": {"risk": "high", "reason": "PTFE — PFAS-related coating"},
    "ptfe": {"risk": "high", "reason": "PFAS-related plastic coating"},

    # Plasticisers
    "bpa": {"risk": "very high", "reason": "Bisphenol A — endocrine disruptor, leaches from plastic"},
    "bisphenol": {"risk": "very high", "reason": "Bisphenol compound — endocrine disruptor"},
    "phthalate": {"risk": "very high", "reason": "Plasticiser, endocrine disruptor"},
    "dibutyl phthalate": {"risk": "very high", "reason": "Plasticiser, endocrine disruptor"},
    "dehp": {"risk": "very high", "reason": "Di(2-ethylhexyl) phthalate — plasticiser"},
    "dep": {"risk": "high", "reason": "Diethyl phthalate — plasticiser"},

    # PFAS / forever chemicals
    "pfas": {"risk": "very high", "reason": "Per/polyfluoroalkyl 'forever chemicals'"},
    "pfoa": {"risk": "very high", "reason": "Perfluorooctanoic acid — PFAS compound"},
    "pfos": {"risk": "very high", "reason": "Perfluorooctane sulfonate — PFAS compound"},
    "fluoropolymer": {"risk": "high", "reason": "PFAS-related polymer family"},

    # Synthetic antioxidants / preservatives often plastic-packaged or derived
    "bht": {"risk": "moderate", "reason": "Butylated hydroxytoluene — petroleum-derived preservative"},
    "bha": {"risk": "moderate", "reason": "Butylated hydroxyanisole — petroleum-derived preservative"},
    "tbhq": {"risk": "moderate", "reason": "Tertiary butylhydroquinone — petroleum-derived"},

    # Synthetic dyes with plastic carriers
    "red 40": {"risk": "moderate", "reason": "Petroleum-derived dye, often in plastic-lined packaging"},
    "yellow 5": {"risk": "moderate", "reason": "Petroleum-derived dye (tartrazine)"},
    "yellow 6": {"risk": "moderate", "reason": "Petroleum-derived dye"},
    "blue 1": {"risk": "moderate", "reason": "Petroleum-derived synthetic dye"},

    # Synthetic emulsifiers / coatings
    "carboxymethylcellulose": {"risk": "low", "reason": "Synthetic cellulose derivative, processing concerns"},
    "polysorbate 80": {"risk": "low", "reason": "Synthetic emulsifier, gut barrier concerns"},
    "polysorbate 60": {"risk": "low", "reason": "Synthetic emulsifier"},
    "carrageenan": {"risk": "low", "reason": "Can carry plastic contamination from processing equipment"},

    # Packaging migrants
    "styrene": {"risk": "high", "reason": "Monomer that leaches from polystyrene packaging"},
    "acetaldehyde": {"risk": "moderate", "reason": "Leaches from PET plastic bottles"},
    "antimony": {"risk": "moderate", "reason": "Catalyst residue from PET production"},
}


def get_reference_block():
    """Returns a compact string of known plastic chemicals for Claude prompt injection."""
    lines = []
    for name, info in PLASTIC_CHEMICALS.items():
        lines.append(f"  - {name}: {info['risk']} risk — {info['reason']}")
    return "\n".join(lines)
