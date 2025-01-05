from typing import Dict, Optional
from datetime import datetime

class InteractionLogger:
    def __init__(self):
        self.interactions = []
        
    def log_interaction(self, 
                       tournament_num: int,
                       round_num: int,
                       turn_num: int,
                       agent_name: str,
                       opponent_name: str,
                       state: Optional[str],
                       action_taken: str,
                       reward: float,
                       q_values: Dict[str, float],
                       exploration_rate: float):
        
        self.interactions.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tournament_num': tournament_num,
            'round_num': round_num,
            'turn_num': turn_num,
            'agent_name': agent_name,
            'opponent_name': opponent_name,
            'state': state,
            'action_taken': action_taken,
            'reward': reward,
            'q_value_cooperate': q_values['COOPERATE'],
            'q_value_defect': q_values['DEFECT'],
            'exploration_rate': exploration_rate
        })
    
    def export_to_csv(self, filename: str = 'qlearning_interaction_log.csv'):
        if not self.interactions:
            return
            
        import pandas as pd
        df = pd.DataFrame(self.interactions)
        df.to_csv(filename, index=False)
    
    print("Test")