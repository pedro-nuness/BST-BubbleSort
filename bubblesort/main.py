from simulation import create_random_players, simulate_random_match
from game_structures import Match
from visualizer import SortVisualizer

NUM_PLAYERS = 15 

def main():
    players = create_random_players(NUM_PLAYERS)
    
    stats = simulate_random_match(players)
    match = Match(players, stats)
    match.startMatch()
    result_map = match.finishMatch()

    if result_map:
        visualizer = SortVisualizer(result_map)
        visualizer.run()
    else:
        print("No match results to visualize.")

if __name__ == "__main__":
    main()