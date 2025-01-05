import csv
from typing import Dict, List
from model.constants import *

def export_tournament_stats(aggregate_stats: Dict, tournament_stats: List[Dict], num_tournaments: int, filename: str = "tournament_stats.csv"):
    """
    Exports the tournament statistics to a CSV file.
    
    Args:
        aggregate_stats (Dict): Dictionary containing the aggregated statistics across all tournaments
        tournament_stats (List[Dict]): List of dictionaries containing stats for each match
        num_tournaments (int): Number of tournaments run
        filename (str): Name of the output CSV file
    """
    
    # Prepare the data rows
    rows = []
    
    # Add header row
    headers = ['Match', 'Bot Name', 'Total Payoff', 'Matches Played', 'Cooperation Rate']
    rows.append(headers)
    
    # Add data for each match
    for match_num, match_result in enumerate(tournament_stats):
        for bot_name, stats in match_result.items():
            total_actions = stats[COOPERATE_COUNT] + stats[DEFECT_COUNT]
            coop_rate = stats[COOPERATE_COUNT] / total_actions if total_actions > 0 else 0
            
            row = [
                f"Match {match_num + 1}",
                bot_name,
                f"{stats[TOTAL_PAYOFF]:.2f}",
                f"{stats[MATCHES_PLAYED]}",
                f"{coop_rate:.2%}"
            ]
            rows.append(row)
    
    # Add a separator row
    rows.append([''] * len(headers))
    
    # Add tournament averages
    rows.append(['TOURNAMENT AVERAGES', '', '', '', ''])
    for bot_name, stats in aggregate_stats.items():
        total_actions = stats[COOPERATE_COUNT] + stats[DEFECT_COUNT]
        avg_coop_rate = stats[COOPERATE_COUNT] / total_actions if total_actions > 0 else 0
        
        row = [
            'Average',
            bot_name,
            f"{stats[TOTAL_PAYOFF]:.2f}",
            f"{stats[MATCHES_PLAYED]}",
            f"{avg_coop_rate:.2%}"
        ]
        rows.append(row)
    
    # Write to CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
