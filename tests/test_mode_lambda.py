import unittest
from unittest.mock import MagicMock
from lambdas import mode


class TestCalculateModeLambda(unittest.TestCase):
    """
    A class to validate the Mode Lambda function
    """

    def test_calculate_mode(self):
        """
        A test to confirm that the lambda accurately calculates the Mode value of the input set
        """

        # Mock event data and context
        event = {
            "values": [10.5, 20.2, 15.7, 8.9, 8.9, 4.4, 13.6],
            "calculation": {
                "mean": 11.743,
                "median": 13.6,
            }
        }
        context = MagicMock()

        # Invoke Mode Lambda
        result = mode.handler(event, context)

        # Verify results
        self.assertEqual(len(result), 3)  # As the final pipeline function, it contains 3 objects corresponding with the final API calculation
        expected_mode_value = 8.9
        self.assertEqual(result["mode"], expected_mode_value)  # Confirm accurate calculation
        expected_final_calculation = {
            "mean": 11.743,
            "median": 13.6,
            "mode": 8.9
        }
        self.assertDictEqual(result, expected_final_calculation)    # Validate the final calculation


if __name__ == '__main__':
    unittest.main()
