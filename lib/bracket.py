# lib/bracket.py
from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class Team:
    name: str
    region: str
    seed: int

def win_prob(power_a: float, power_b: float) -> float:
    denom = power_a + power_b
    if denom <= 0:
        return 0.5
    return power_a / denom

def pick_winner(team_a: Team, team_b: Team, power: Dict[str, float], rng: random.Random) -> Team:
    pA = float(power.get(team_a.name, 0.0))
    pB = float(power.get(team_b.name, 0.0))
    r = rng.random()
    return team_a if r < win_prob(pA, pB) else team_b

def r64_matchups(teams: List[Team]) -> List[Tuple[Team, Team]]:
    by_key = {(t.region, t.seed): t for t in teams}
    pairings = [(1,16),(8,9),(5,12),(4,13),(6,11),(3,14),(7,10),(2,15)]
    regions = sorted({t.region for t in teams})
    out = []
    for region in regions:
        for a,b in pairings:
            out.append((by_key[(region,a)], by_key[(region,b)]))
    return out

def pair_sequential(winners: List[Team]) -> List[Tuple[Team, Team]]:
    return list(zip(winners[0::2], winners[1::2]))

def advance_round(matchups: List[Tuple[Team, Team]], power: Dict[str, float], rng: random.Random) -> List[Team]:
    return [pick_winner(a, b, power, rng) for a, b in matchups]

def _split_r64_by_region(r64: List[Tuple[Team, Team]]) -> Dict[str, List[Tuple[Team, Team]]]:
    by_region: Dict[str, List[Tuple[Team, Team]]] = {}
    for a, b in r64:
        by_region.setdefault(a.region, []).append((a, b))
    return by_region

def _winners_to_round_matchups(r64: List[Tuple[Team, Team]], winners: List[Team]) -> List[Tuple[Team, Team]]:
    # winners are in the same order as r64 matchups; next round pairs adjacent winners
    return pair_sequential(winners)

def generate_bracket(teams: List[Team], power: Dict[str, float], seed: int | None = None) -> dict:
    rng = random.Random(seed)

    r64 = r64_matchups(teams)
    r32_w = advance_round(r64, power, rng)
    s16_w = advance_round(pair_sequential(r32_w), power, rng)
    e8_w  = advance_round(pair_sequential(s16_w), power, rng)
    f4_w  = advance_round(pair_sequential(e8_w), power, rng)
    f2_w  = advance_round(pair_sequential(f4_w), power, rng)
    champ = advance_round(pair_sequential(f2_w), power, rng)[0]

    # Region grouping for rendering (assumes r64 is ordered by regions)
    r64_by_region = _split_r64_by_region(r64)

    # Also group winners by region based on ordering: 8 matchups per region
    regions = sorted(r64_by_region.keys())
    by_region = {}
    idx = 0
    for region in regions:
        # 8 r64 matchups per region → 8 winners
        r32_w_reg = r32_w[idx:idx+8]
        # then 4, then 2, then 1
        s16_reg = s16_w[(idx//2):(idx//2)+4]
        e8_reg  = e8_w[(idx//4):(idx//4)+2]
        champ_reg = f4_w[(idx//8):(idx//8)+1][0]  # regional champion (final four team)

        by_region[region] = {
            "R64": r64_by_region[region],  # 8 matchups
            "R32": r32_w_reg,              # 8 teams
            "S16": s16_reg,                # 4 teams
            "E8":  e8_reg,                 # 2 teams
            "REG_CHAMP": champ_reg,        # 1 team
        }
        idx += 8

    return {
        "R64": r64,
        "R32": r32_w,
        "S16": s16_w,
        "E8":  e8_w,
        "F4":  f4_w,
        "F2":  f2_w,
        "CHAMP": champ,
        "by_region": by_region
    }
