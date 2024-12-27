import unittest
from model.tournament.ResultManager import ResultManager
from model.constants import COOPERATE, DEFECT


class TestResultManager(unittest.TestCase):
    def setUp(self):
        self.result_manager = ResultManager()
        self.sample_result = {
            "rounds_played": 3,
            "TFTBot_actions": [COOPERATE, COOPERATE, DEFECT],
            "GrimBot_actions": [COOPERATE, DEFECT, DEFECT],
            "TFTBot_total_payoff": 10,
            "GrimBot_total_payoff": 12
        }

    def test_record_and_get_results(self):
        """Test recording a result and retrieving all results"""
        self.result_manager.record_result(self.sample_result)
        results = self.result_manager.get_all_results()
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.sample_result)

    def test_get_aggregate_results(self):
        """Test aggregating results across multiple matches"""
        # Record multiple results
        self.result_manager.record_result(self.sample_result)
        second_result = {
            "rounds_played": 3,
            "TFTBot_actions": [COOPERATE, DEFECT, DEFECT],
            "RandomBot_actions": [DEFECT, DEFECT, COOPERATE],
            "TFTBot_total_payoff": 8,
            "RandomBot_total_payoff": 11
        }
        self.result_manager.record_result(second_result)

        aggregate_results = self.result_manager.get_aggregate_results()
        
        # Check TFTBot's aggregate statistics
        self.assertIn("TFTBot", aggregate_results)
        tft_stats = aggregate_results["TFTBot"]
        self.assertEqual(tft_stats["total_payoff"], 18)  # 10 + 8
        self.assertEqual(tft_stats["matches_played"], 2)
        
        # Check other bots' statistics
        self.assertIn("GrimBot", aggregate_results)
        self.assertIn("RandomBot", aggregate_results)
        self.assertEqual(aggregate_results["GrimBot"]["matches_played"], 1)
        self.assertEqual(aggregate_results["RandomBot"]["matches_played"], 1)

    def test_get_bot_statistics(self):
        """Test retrieving statistics for a specific bot"""
        self.result_manager.record_result(self.sample_result)
        
        tft_stats = self.result_manager.get_bot_statistics("TFTBot")
        
        self.assertEqual(tft_stats["total_payoff"], 10)
        self.assertEqual(tft_stats["matches_played"], 1)
        self.assertEqual(tft_stats["cooperate_count"], 2)
        self.assertEqual(tft_stats["defect_count"], 1)
        self.assertEqual(tft_stats["cooperation_rate"], 2/3)

    def test_clear_results(self):
        """Test clearing all results"""
        self.result_manager.record_result(self.sample_result)
        self.result_manager.clear_results()
        
        self.assertEqual(len(self.result_manager.get_all_results()), 0)
        self.assertEqual(len(self.result_manager.get_aggregate_results()), 0)

    def test_get_bot_statistics_nonexistent_bot(self):
        """Test getting statistics for a bot that hasn't played"""
        with self.assertRaises(KeyError):
            self.result_manager.get_bot_statistics("NonexistentBot")

    def test_record_invalid_result(self):
        """Test recording an invalid result format"""
        invalid_result = {"invalid": "format"}
        with self.assertRaises(KeyError):
            self.result_manager.record_result(invalid_result)


if __name__ == '__main__':
    unittest.main()