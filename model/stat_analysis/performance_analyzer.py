import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
from model.constants import TOTAL_PAYOFF, COOPERATE_COUNT, DEFECT_COUNT, MATCHES_PLAYED

class PerformanceAnalyzer:
    def __init__(self, tournament_stats: List[Dict], aggregate_stats: Dict):
        self.tournament_stats = tournament_stats
        self.aggregate_stats = aggregate_stats
        self.output_dir = "analysis_output"  # Directory for saving plots
        
        # Create output directory if it doesn't exist
        import os
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def analyze_all(self):
        """Run all analyses and save plots"""
        # Create a single figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # Create the bar chart in first subplot
        plt.sca(ax1)  # Set current axes to first subplot
        self.analyze_qlearning_vs_strategies()
        
        # Create the cooperation rates chart in second subplot
        plt.sca(ax2)  # Set current axes to second subplot
        self.analyze_cooperation_rates()
        
        # Save the combined figure
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/analysis_results.png')
        plt.show()
        plt.close()

    def analyze_qlearning_vs_strategies(self):
        """
        Creates a bar chart comparing QLearningAgent's average payoff against different strategies.
        """
        print("\nAnalyzing QLearningAgent vs Strategies:")
        
        qlearning_payoffs = {}  # Dictionary to store payoffs against each opponent
        
        # Go through all matches to find QLearningAgent's payoffs against each opponent
        for match in self.tournament_stats:
            for bot_name, stats in match.items():
                if bot_name == "QLearningAgent":
                    # Find the opponent in this match
                    opponent = [name for name in match.keys() if name != "QLearningAgent"][0]
                    payoff = stats[TOTAL_PAYOFF] / stats[MATCHES_PLAYED]  # Calculate average payoff per match
                    
                    # Initialize list for this opponent if not exists
                    if opponent not in qlearning_payoffs:
                        qlearning_payoffs[opponent] = []
                    
                    # Add average payoff to list
                    qlearning_payoffs[opponent].append(payoff)
        
        # Calculate average payoff against each opponent
        avg_payoffs = {
            opponent: np.mean(payoffs) 
            for opponent, payoffs in qlearning_payoffs.items()
        }
        
        # Create bar chart
        opponents = list(avg_payoffs.keys())
        payoffs = list(avg_payoffs.values())
        
        bars = plt.bar(opponents, payoffs)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
        
        plt.title('QLearningAgent Average Payoff per Match vs Different Strategies')
        plt.xlabel('Opponent Strategy')
        plt.ylabel('Average Payoff per Match')
        plt.ylim(0, 5.5)  # Set y-axis limits based on payoff matrix
        plt.xticks(rotation=45)

    def analyze_cooperation_rates(self):
        """
        Creates a bar chart comparing cooperation rates between bots.
        """
        bot_names = list(self.aggregate_stats.keys())
        coop_rates = []
        
        for bot_name in bot_names:
            stats = self.aggregate_stats[bot_name]
            total_actions = stats[COOPERATE_COUNT] + stats[DEFECT_COUNT]
            coop_rate = (stats[COOPERATE_COUNT] / total_actions * 100 
                        if total_actions > 0 else 0)
            coop_rates.append(coop_rate)
        
        bars = plt.bar(bot_names, coop_rates)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom')
        
        plt.title('Cooperation Rates by Bot')
        plt.xlabel('Bot')
        plt.ylabel('Cooperation Rate (%)')
        plt.xticks(rotation=45)
