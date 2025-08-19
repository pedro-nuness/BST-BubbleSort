# simulation.py

import random
from game_structures import Player, MatchStats

def create_random_players(n):
    players = []
    for i in range(n):
        nickname = f"Player{i+1}"
        points = random.randint(0, 99)   
        level = random.randint(1, 10)    
        players.append(Player(nickname, points, level))
    return players

def simulate_random_match(players):
    stats_map = {player: MatchStats(player) for player in players}
    for _ in range(random.randint(50, 200)):
        action = random.choice(["kill", "assist", "death", "damage"])
        player = random.choice(players)
        
        opponents = [p for p in players if p != player]
        if not opponents: continue

        match action:
            case "kill":
                target = random.choice(opponents)
                stats_map[player].increment_kills(target)
            case "assist":
                target = random.choice(opponents)
                stats_map[player].increment_assists(target)
            case "death":
                killer = random.choice(opponents)
                stats_map[player].increment_deaths(killer)
            case "damage":
                dmg = random.randint(10, 300)
                stats_map[player].increment_damage(dmg)
    return stats_map