from model.bots.DefectBot import DefectBot
from model.bots.CooperateBot import CooperateBot
from model.bots.QLearningBot import QLearningBot
from model.bots.TFTBot import TFTBot
from model.bots.GrimBot import GrimBot
from model.bots.TFT90Bot import TFT90Bot
from model.tournament.tournament import Tournament
from model.tournament.MatchSimulator import MatchSimulator
from model.tournament.ResultManager import ResultManager
from model.constants import *
from ui.csv_export import export_tournament_stats

def main():
    num_tournaments = NUM_TOURNAMENTS
    aggregate_stats = {}
    tournament_stats = []  # List to store stats for each tournament

    for tournament_num in range(num_tournaments):
        print(f"\nTournament {tournament_num + 1}/{num_tournaments}")
        
        # Create fresh bots for each tournament
        qbot1 = QLearningBot()
        qbot1.name = "QLearningBot1"
        qbot2 = QLearningBot()
        qbot2.name = "QLearningBot2"
        
        bots = [
            qbot1,
            #qbot2,
            #GrimBot(),
            TFTBot(),
            #TFT90Bot(),
            #DefectBot(),
            #CooperateBot()
        ]
        
        # Create tournament components
        match_simulator = MatchSimulator()
        result_manager = ResultManager()

        # Create and run tournament
        tournament = Tournament(
            participants=bots,
            rounds=ROUNDS,
            match_simulator=match_simulator,
            result_manager=result_manager
        )

        # Run the tournament
        tournament.run_tournament()

        # Store this tournament's results
        tournament_results = result_manager.get_aggregate_results()
        tournament_stats.append(tournament_results)
        
        # Accumulate statistics for overall average
        for bot_name, stats in tournament_results.items():
            if bot_name not in aggregate_stats:
                aggregate_stats[bot_name] = {
                    TOTAL_PAYOFF: 0,
                    MATCHES_PLAYED: 0,
                    COOPERATE_COUNT: 0,
                    DEFECT_COUNT: 0
                }
            for key in [TOTAL_PAYOFF, MATCHES_PLAYED, COOPERATE_COUNT, DEFECT_COUNT]:
                aggregate_stats[bot_name][key] += stats[key]

    # Export both summary stats and detailed interactions
    export_tournament_stats(aggregate_stats, tournament_stats, num_tournaments)
    print("\nSummary statistics have been exported to tournament_stats.csv")
    
    qbot1.logger.export_to_csv('qlearning_detailed_log.csv')
    print("Detailed Q-learning interactions have been exported to qlearning_detailed_log.csv")


if __name__ == "__main__":
    main()