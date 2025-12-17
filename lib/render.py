# lib/render.py
from __future__ import annotations
from html import escape
from typing import Dict, List, Tuple

def _team_chip(team, extra_cls=""):
    # Team is a Team dataclass
    name = escape(team.name)
    seed = escape(str(team.seed))
    return f"""
      <div class="team {extra_cls}">
        <div class="seed">{seed}</div>
        <div class="name" title="{name}">{name}</div>
      </div>
    """

def _matchup_block(a, b, winner=None):
    # Winner highlighting (optional)
    a_cls = "win" if (winner is not None and winner.name == a.name) else ""
    b_cls = "win" if (winner is not None and winner.name == b.name) else ""
    return f"""
      <div class="match">
        {_team_chip(a, a_cls)}
        {_team_chip(b, b_cls)}
      </div>
    """

def _region_column(region_name: str, region_data: dict, side: str) -> str:
    """
    side: 'left' or 'right' affects connector direction styling
    region_data: {R64: [(a,b)x8], R32:[8], S16:[4], E8:[2], REG_CHAMP:[1]}
    """
    title = escape(region_name)
    r64: List[Tuple] = region_data["R64"]
    r32: List = region_data["R32"]
    s16: List = region_data["S16"]
    e8:  List = region_data["E8"]
    reg_champ = region_data["REG_CHAMP"]

    # Round winners:
    # - R32 winners are r32 list; to highlight R64 matchups we need R32 winner per matchup
    # - For R32 matchups highlight S16 winners, etc.
    # Helper to build matchups from sequential list
    def pair(seq):
        return list(zip(seq[0::2], seq[1::2]))

    r32_matchups = pair(r32)   # 4 matchups
    s16_matchups = pair(s16)   # 2 matchups
    e8_matchups  = pair(e8)    # 1 matchup

    html = f"""
    <div class="region region-{side}">
      <div class="region-title">{title}</div>

      <div class="rounds rounds-{side}">
        <!-- R64 -->
        <div class="round">
          <div class="round-title">R64</div>
          <div class="stack">
            {''.join(_matchup_block(a,b,winner=r32[i]) for i,(a,b) in enumerate(r64))}
          </div>
        </div>

        <!-- R32 -->
        <div class="round">
          <div class="round-title">R32</div>
          <div class="stack tight">
            {''.join(_matchup_block(a,b,winner=s16[i]) for i,(a,b) in enumerate(r32_matchups))}
          </div>
        </div>

        <!-- S16 -->
        <div class="round">
          <div class="round-title">S16</div>
          <div class="stack tighter">
            {''.join(_matchup_block(a,b,winner=e8[i]) for i,(a,b) in enumerate(s16_matchups))}
          </div>
        </div>

        <!-- E8 -->
        <div class="round">
          <div class="round-title">E8</div>
          <div class="stack tightest">
            {_matchup_block(e8_matchups[0][0], e8_matchups[0][1], winner=reg_champ)}
          </div>
        </div>

        <!-- Regional Champ -->
        <div class="round champ">
          <div class="round-title">Champ</div>
          <div class="stack one">
            {_team_chip(reg_champ, "win")}
          </div>
        </div>
      </div>
    </div>
    """
    return html

def bracket_html(rounds: dict) -> str:
    by_region: Dict[str, dict] = rounds.get("by_region", {})
    if not by_region:
        return "<div style='font-family:system-ui'>No bracket to render.</div>"

    regions = sorted(by_region.keys())
    # Expect 4. If more/less, still render best-effort.
    left_regs  = regions[:2]
    right_regs = regions[2:4]

    f4 = rounds.get("F4", [])
    f2 = rounds.get("F2", [])
    champ = rounds.get("CHAMP")

    def team_box(team, cls=""):
        if team is None:
            return "<div class='center-team empty'>—</div>"
        return f"<div class='center-team {cls}'><div class='center-seed'>{escape(str(team.seed))}</div><div class='center-name' title='{escape(team.name)}'>{escape(team.name)}</div></div>"

    # Final Four matchups: (0 vs 1), (2 vs 3)
    # Championship: winners f2[0], f2[1], champ
    f4_pairs = list(zip(f4[0::2], f4[1::2])) if len(f4) >= 4 else []
    title = "March Madness Bracket"

    css = """
    <style>
      .wrap{font-family: ui-sans-serif, system-ui; padding: 10px 12px;}
      .title{font-weight:800; font-size:18px; margin: 0 0 10px 0;}
      .board{display:grid; grid-template-columns: 1fr 360px 1fr; gap:14px; align-items:start;}
      .region{border:1px solid #e5e5e5; border-radius:16px; padding:10px; box-shadow: 0 1px 10px rgba(0,0,0,.06); background:#fff;}
      .region-title{font-weight:800; font-size:14px; margin-bottom:8px;}
      .rounds{display:flex; gap:10px; overflow-x:auto; padding-bottom:6px;}
      .round{min-width: 150px;}
      .round-title{font-size:11px; font-weight:700; opacity:.7; margin: 2px 0 6px;}
      .stack{display:flex; flex-direction:column; gap:10px;}
      .stack.tight{gap:18px; margin-top: 18px;}
      .stack.tighter{gap:40px; margin-top: 44px;}
      .stack.tightest{gap:0; margin-top: 96px;}
      .stack.one{margin-top: 104px;}

      .match{border:1px solid #efefef; border-radius:14px; padding:6px; background:#fafafa;}
      .team{display:flex; align-items:center; gap:8px; padding:6px 8px; border-radius:10px; background:#fff; border:1px solid #f0f0f0;}
      .team + .team{margin-top:6px;}
      .seed{width:22px; font-weight:800; opacity:.7; font-size:12px;}
      .name{flex:1; font-weight:650; font-size:12px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
      .win{border-color:#d9d9d9; box-shadow: 0 1px 10px rgba(0,0,0,.08);}

      .center{border:1px solid #e5e5e5; border-radius:18px; padding:12px; background:#fff; box-shadow: 0 1px 10px rgba(0,0,0,.06);}
      .center h3{margin:0 0 10px 0; font-size:14px;}
      .center-grid{display:grid; grid-template-columns: 1fr; gap:10px;}
      .center-block{border:1px solid #efefef; border-radius:16px; padding:10px; background:#fafafa;}
      .center-row{display:flex; gap:10px; justify-content:space-between; align-items:center; flex-wrap:wrap;}
      .center-team{display:flex; gap:10px; align-items:center; border:1px solid #f0f0f0; background:#fff; border-radius:14px; padding:8px 10px; min-width: 300px;}
      .center-team.empty{justify-content:center; opacity:.5;}
      .center-seed{font-weight:900; opacity:.7;}
      .center-name{font-weight:800; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
      .champion{border-color:#d9d9d9; box-shadow: 0 1px 14px rgba(0,0,0,.10);}
      .small{font-size:11px; opacity:.7; margin-top:6px;}

      @media (max-width: 1100px){
        .board{grid-template-columns: 1fr; }
        .center-team{min-width: unset; width: 100%;}
      }
    </style>
    """

    left_html  = "".join(_region_column(r, by_region[r], "left") for r in left_regs)
    right_html = "".join(_region_column(r, by_region[r], "right") for r in right_regs)

    # Center: Final Four + Title game
    ff1 = f4_pairs[0] if len(f4_pairs) >= 1 else (None, None)
    ff2 = f4_pairs[1] if len(f4_pairs) >= 2 else (None, None)
    f2_a = f2[0] if len(f2) >= 1 else None
    f2_b = f2[1] if len(f2) >= 2 else None

    center_html = f"""
      <div class="center">
        <h3>Final Four & Championship</h3>

        <div class="center-grid">

          <div class="center-block">
            <div style="font-weight:800; font-size:12px; margin-bottom:8px;">Final Four</div>
            <div class="center-row">
              {team_box(ff1[0])}
              {team_box(ff1[1])}
            </div>
            <div class="center-row" style="margin-top:10px;">
              {team_box(ff2[0])}
              {team_box(ff2[1])}
            </div>
          </div>

          <div class="center-block">
            <div style="font-weight:800; font-size:12px; margin-bottom:8px;">Championship</div>
            <div class="center-row">
              {team_box(f2_a)}
              {team_box(f2_b)}
            </div>
            <div class="small">Winner</div>
            {team_box(champ, "champion")}
          </div>

        </div>
      </div>
    """

    return css + f"""
    <div class="wrap">
      <div class="title">{escape(title)}</div>
      <div class="board">
        <div>{left_html}</div>
        {center_html}
        <div>{right_html}</div>
      </div>
    </div>
    """
