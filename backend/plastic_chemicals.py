# Curated reference of plastic-linked chemicals.
# Used to pre-screen ingredients before Claude runs, and injected into the prompt.

PLASTIC_CHEMICALS = {
    # ── Direct microplastics / polymers ──────────────────────────────────────
    "microplastic":       {"risk": "very high", "pct": 20, "reason": "Direct microplastic particle"},
    "nanoplastic":        {"risk": "very high", "pct": 20, "reason": "Sub-micron plastic particle"},
    "polyethylene":       {"risk": "very high", "pct": 15, "reason": "Plastic polymer (PE)"},
    "polypropylene":      {"risk": "very high", "pct": 15, "reason": "Plastic polymer (PP)"},
    "polystyrene":        {"risk": "very high", "pct": 15, "reason": "Plastic polymer (PS), leaches styrene"},
    "polyvinyl chloride": {"risk": "very high", "pct": 18, "reason": "PVC, releases vinyl chloride and phthalates"},
    "pvc":                {"risk": "very high", "pct": 18, "reason": "PVC, releases vinyl chloride and phthalates"},
    "polycarbonate":      {"risk": "very high", "pct": 16, "reason": "Releases BPA"},
    "nylon":              {"risk": "high",      "pct": 10, "reason": "Synthetic plastic polymer"},
    "polyurethane":       {"risk": "high",      "pct": 10, "reason": "Synthetic polymer, MDI/TDI concerns"},
    "teflon":             {"risk": "high",      "pct": 12, "reason": "PTFE — PFAS-related coating"},
    "ptfe":               {"risk": "high",      "pct": 12, "reason": "PFAS-related plastic coating"},
    "acrylic":            {"risk": "moderate",  "pct": 6,  "reason": "Synthetic polymer, methyl methacrylate residues"},

    # ── Bisphenols ───────────────────────────────────────────────────────────
    "bpa":                {"risk": "very high", "pct": 18, "reason": "Bisphenol A — endocrine disruptor"},
    "bisphenol a":        {"risk": "very high", "pct": 18, "reason": "BPA — endocrine disruptor"},
    "bisphenol s":        {"risk": "very high", "pct": 16, "reason": "BPS — BPA replacement, similar toxicity"},
    "bisphenol f":        {"risk": "very high", "pct": 16, "reason": "BPF — BPA replacement, endocrine disruptor"},
    "bisphenol":          {"risk": "very high", "pct": 15, "reason": "Bisphenol compound — endocrine disruptor"},

    # ── Phthalates ───────────────────────────────────────────────────────────
    "phthalate":          {"risk": "very high", "pct": 15, "reason": "Plasticiser class, endocrine disruptors"},
    "dehp":               {"risk": "very high", "pct": 16, "reason": "Di(2-ethylhexyl) phthalate — plasticiser"},
    "dbp":                {"risk": "very high", "pct": 14, "reason": "Dibutyl phthalate — plasticiser"},
    "dep":                {"risk": "high",      "pct": 10, "reason": "Diethyl phthalate — plasticiser"},
    "dmp":                {"risk": "high",      "pct": 10, "reason": "Dimethyl phthalate — plasticiser"},
    "dinp":               {"risk": "high",      "pct": 12, "reason": "Diisononyl phthalate — plasticiser"},
    "didp":               {"risk": "high",      "pct": 12, "reason": "Diisodecyl phthalate — plasticiser"},
    "bbp":                {"risk": "very high", "pct": 15, "reason": "Benzyl butyl phthalate — plasticiser"},

    # ── PFAS / forever chemicals ─────────────────────────────────────────────
    "pfas":               {"risk": "very high", "pct": 20, "reason": "Per/polyfluoroalkyl 'forever chemicals'"},
    "pfoa":               {"risk": "very high", "pct": 20, "reason": "Perfluorooctanoic acid — PFAS"},
    "pfos":               {"risk": "very high", "pct": 20, "reason": "Perfluorooctane sulfonate — PFAS"},
    "pfna":               {"risk": "very high", "pct": 18, "reason": "Perfluorononanoic acid — PFAS"},
    "pfhxa":              {"risk": "high",      "pct": 14, "reason": "Perfluorohexanoic acid — PFAS"},
    "pfhxs":              {"risk": "high",      "pct": 14, "reason": "Perfluorohexane sulfonate — PFAS"},
    "fluoropolymer":      {"risk": "high",      "pct": 12, "reason": "PFAS-related polymer family"},
    "fluorosurfactant":   {"risk": "high",      "pct": 12, "reason": "PFAS-class surfactant"},

    # ── Petroleum-derived preservatives ──────────────────────────────────────
    "bht":                {"risk": "moderate", "pct": 4, "reason": "Butylated hydroxytoluene — petroleum-derived"},
    "bha":                {"risk": "moderate", "pct": 4, "reason": "Butylated hydroxyanisole — petroleum-derived"},
    "tbhq":               {"risk": "moderate", "pct": 4, "reason": "Tertiary butylhydroquinone — petroleum-derived"},
    "propyl gallate":     {"risk": "low",      "pct": 2, "reason": "Synthetic antioxidant"},

    # ── Flame retardants ─────────────────────────────────────────────────────
    "pbde":               {"risk": "very high", "pct": 14, "reason": "Polybrominated diphenyl ether flame retardant"},
    "tris":               {"risk": "high",      "pct": 10, "reason": "TRIS flame retardant — possible carcinogen"},
    "tcep":               {"risk": "high",      "pct": 12, "reason": "Chlorinated phosphate flame retardant"},
    "hbcd":               {"risk": "very high", "pct": 14, "reason": "Hexabromocyclododecane — persistent pollutant"},

    # ── Synthetic dyes with plastic carriers ─────────────────────────────────
    "red 40":             {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived azo dye"},
    "allura red":         {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived azo dye (Red 40)"},
    "yellow 5":           {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived dye (Tartrazine)"},
    "tartrazine":         {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived azo dye (Yellow 5)"},
    "yellow 6":           {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived dye"},
    "sunset yellow":      {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived azo dye (Yellow 6)"},
    "blue 1":             {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived synthetic dye"},
    "brilliant blue":     {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived dye (Blue 1)"},
    "red 3":              {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived dye, banned in cosmetics"},
    "erythrosine":        {"risk": "moderate", "pct": 3, "reason": "Petroleum-derived dye (Red 3)"},

    # ── Synthetic emulsifiers ─────────────────────────────────────────────────
    "polysorbate 80":     {"risk": "low", "pct": 3, "reason": "Synthetic emulsifier, gut barrier concerns"},
    "polysorbate 60":     {"risk": "low", "pct": 3, "reason": "Synthetic emulsifier"},
    "polysorbate 20":     {"risk": "low", "pct": 2, "reason": "Synthetic emulsifier"},
    "carboxymethylcellulose": {"risk": "low", "pct": 2, "reason": "Synthetic cellulose derivative"},
    "methylcellulose":    {"risk": "low", "pct": 1, "reason": "Synthetic cellulose derivative"},

    # ── Packaging migrants ───────────────────────────────────────────────────
    "styrene":            {"risk": "high",     "pct": 12, "reason": "Monomer leaching from polystyrene packaging"},
    "acetaldehyde":       {"risk": "moderate", "pct": 6,  "reason": "Leaches from PET plastic bottles"},
    "antimony":           {"risk": "moderate", "pct": 6,  "reason": "Catalyst residue from PET production"},
    "vinyl chloride":     {"risk": "very high","pct": 18, "reason": "PVC monomer — known carcinogen"},
    "epichlorohydrin":    {"risk": "high",     "pct": 10, "reason": "Epoxy resin precursor, genotoxic"},
    "formaldehyde":       {"risk": "high",     "pct": 8,  "reason": "Resin cross-linker, leaches from melamine plastics"},
    "melamine":           {"risk": "high",     "pct": 10, "reason": "Plastic resin — leaches into hot food"},

    # ── Silicones ────────────────────────────────────────────────────────────
    "dimethicone":        {"risk": "low",      "pct": 3, "reason": "Silicone polymer — synthetic plastic family"},
    "simethicone":        {"risk": "low",      "pct": 3, "reason": "Silicone polymer"},
    "silicone":           {"risk": "low",      "pct": 3, "reason": "Synthetic polymer family"},

    # ── Plasticised coatings / waxes ─────────────────────────────────────────
    "polyethylene wax":   {"risk": "high",     "pct": 12, "reason": "Direct polyethylene plastic coating"},
    "mineral oil":        {"risk": "moderate", "pct": 5,  "reason": "Petroleum-derived, MOSH/MOAH contamination"},
    "paraffin wax":       {"risk": "moderate", "pct": 5,  "reason": "Petroleum-derived wax"},
    "microcrystalline wax": {"risk": "moderate","pct": 5, "reason": "Petroleum-derived wax used on produce"},
}


def match_ingredients(ingredients_text):
    """
    Pre-screen ingredient text against known plastic chemicals.
    Returns list of matched {name, risk, pct, reason} dicts.
    Faster than relying solely on Claude for well-known chemicals.
    """
    if not ingredients_text:
        return []
    text_lower = ingredients_text.lower()
    matched = []
    seen = set()
    for keyword, info in PLASTIC_CHEMICALS.items():
        if keyword in text_lower and keyword not in seen:
            seen.add(keyword)
            matched.append({"name": keyword, **info})
    # Sort by pct descending
    return sorted(matched, key=lambda x: x["pct"], reverse=True)


def get_reference_block():
    """Compact string of known plastic chemicals for Claude prompt injection."""
    lines = []
    for name, info in PLASTIC_CHEMICALS.items():
        lines.append(f"  - {name}: {info['risk']} risk (+{info['pct']}%) — {info['reason']}")
    return "\n".join(lines)
