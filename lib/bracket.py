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
    # Robust normalization for any positive scale
    denom = (power_a + power_b)
    if denom <= 0:
        return 0.5
    return power_a / denom

def pick_winner(team_a: Team, team_b: Team, power: Dict[str, float], rng: random.Random) -> Team:
    pA = float(power.get(team_a.name, 0.0))
    pB = float(power.get(team_b.name, 0.0))
    prob_a = win_prob(pA, pB)
    r = rng.random()
    return team_a if r < prob_a else team_b

def r64_matchups(teams: List[Team]) -> List[Tuple[Team, Team]]:
    # Assumes exactly one team per (region, seed)
    by_key = {(t.region, t.seed): t for t in teams}

    pairings = [(1,16),(8,9),(5,12),(4,13),(6,11),(3,14),(7,10),(2,15)]
    regions = sorted({t.region for t in teams})
    out = []
    for region in regions:
        for a,b in pairings:
            out.append((by_key[(region,a)], by_key[(region,b)]))
    return out

def advance_round(matchups: List[Tuple[Team, Team]], power: Dict[str, float], rng: random.Random) -> List[Team]:
    winners = []
    for a, b in matchups:
        winners.append(pick_winner(a, b, power, rng))
    return winners

def pair_sequential(winners: List[Team]) -> List[Tuple[Team, Team]]:
    return list(zip(winners[0::2], winners[1::2]))

def generate_bracket(teams: List[Team], power: Dict[str, float], seed: int | None = None) -> dict:
    rng = random.Random(seed)

    r64 = r64_matchups(teams)
    r32_w = advance_round(r64, power, rng)
    s16_w = advance_round(pair_sequential(r32_w), power, rng)
    e8_w  = advance_round(pair_sequential(s16_w), power, rng)
    f4_w  = advance_round(pair_sequential(e8_w), power, rng)
    f2_w  = advance_round(pair_sequential(f4_w), power, rng)
    champ = advance_round(pair_sequential(f2_w), power, rng)[0]

    return {
        "R64": r64,
        "R32": r32_w,
        "S16": s16_w,
        "E8":  e8_w,
        "F4":  f4_w,
        "F2":  f2_w,
        "CHAMP": champ
    }
