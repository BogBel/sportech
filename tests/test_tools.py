import unittest

from core.tools import merge_results


class TestMergeResults(unittest.TestCase):

    def test_empty_data(self):
        self.assertEqual(
            {'keys': [], 'data': []},
            merge_results(dict())
        )

    def test_one_company_exists(self):
        input_data = {
            'SkyBet': {
                'country1': 'odd1',
                'country2': 'odd2',
                'country3': 'odd3',
            }
        }
        self.assertEqual(
            {
                'keys': ['SkyBet'],
                'data': [
                    ('country1', ['odd1']),
                    ('country2', ['odd2']),
                    ('country3', ['odd3']),
                ]
            },
            merge_results(input_data)
        )

    def test_few_companies_exists(self):
        input_data = {
            'SkyBet': {
                'country1': 'odd1.1',
                'country2': 'odd1.2',
                'country3': 'odd1.3',
            },
            'Bet365': {
                'country1': 'odd2.1',
                'country2': 'odd2.2',
                'country3': 'odd2.3',
            },
            'Paddy': {
                'country1': 'odd3.1',
                'country2': 'odd3.2',
            }
        }
        self.assertEqual(
            {
                'keys': ['Bet365', 'Paddy', 'SkyBet'],
                'data': [
                    ('country1', ['odd2.1', 'odd3.1', 'odd1.1']),
                    ('country2', ['odd2.2', 'odd3.2', 'odd1.2']),
                    ('country3', ['odd2.3', 'odd1.3']),
                ]
            },
            merge_results(input_data)
        )
