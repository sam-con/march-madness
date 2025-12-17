from html import escape

def bracket_html(rounds: dict) -> str:
    # rounds["R64"] is list of (Team, Team)
    # rounds["R32"/"S16"/...] are list of Team
    # We'll render by region as 4 mini-brackets side-by-side.

    # NOTE: This is a starter renderer. It’ll look good, and we can iterate.
    css = """
    <style>
      .wrap{font-family: ui-sans-serif, system-ui; padding:12px;}
      .grid{display:grid; grid-template-columns: repeat(4, 1fr); gap:14px;}
      .card{border:1px solid #ddd; border-radius:14px; padding:10px; box-shadow:0 1px 8px rgba(0,0,0,.06);}
      .title{font-weight:700; font-size:14px; margin-bottom:8px;}
      .row{display:flex; justify-content:space-between; gap:8px; padding:6px 8px; border-radius:10px; margin:4px 0; background:#fafafa;}
      .seed{opacity:.7; width:22px;}
      .team{flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
      .champ{margin-top:14px; padding:10px; border-radius:14px; border:1px solid #ddd; font-weight:800;}
    </style>
    """

    # group round-of-64 matchups by region in order encountered
    r64 = rounds.get("R64", [])
    by_region = {}
    for a,b in r64:
        by_region.setdefault(a.region, []).append((a,b))

    regions = sorted(by_region.keys())
    blocks = []
    for region in regions:
        lines = [f'<div class="card"><div class="title">{escape(region)} Region</div>']
        for a,b in by_region[region]:
            lines.append(f'<div class="row"><div class="seed">{a.seed}</div><div class="team">{escape(a.name)}</div></div>')
            lines.append(f'<div class="row"><div class="seed">{b.seed}</div><div class="team">{escape(b.name)}</div></div>')
            lines.append("<div style='height:8px'></div>")
        lines.append("</div>")
        blocks.append("".join(lines))

    champ = rounds.get("CHAMP")
    champ_html = ""
    if champ is not None:
        champ_html = f'<div class="champ">Champion: {escape(champ.name)}</div>'

    return css + f'<div class="wrap"><div class="grid">{"".join(blocks)}</div>{champ_html}</div>'
