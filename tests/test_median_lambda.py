import unittest
from unittest.mock import MagicMock
from lambdas import median


class TestCalculateMedianLambda(unittest.TestCase):
    """
    A class to validate the Median Lambda function
    """

    def test_calculate_median(self):
        """
        A test to confirm that the lambda accurately calculates the Median value of the input set
        """

        # Mock event data and context
        event = {
            "values": [10.5, 20.2, 15.7, 8.9, 8.9, 4.4, 13.6],
            "calculation": {
                "mean": 11.743
            }
        }
        context = MagicMock()

        # Invoke Median Lambda
        result = median.handler(event, context)

        # Verify results
        self.assertEqual(len(result), 2)  # Contains 2 objects - 1 for input values and 1 for calculation
        self.assertIn("values", result)
        self.assertGreater(len(result["values"]), 0)
        for value in result["values"]:
            self.assertTrue(isinstance(value, (int, float)))
        self.assertIn("calculation", result)
        self.assertEqual(len(result["calculation"]), 2)  # Concatenated calculation should now contain 2 objects
        expected_median_value = 10.5
        self.assertEqual(result["calculation"]["median"], expected_median_value)  # Confirm accurate calculation


if __name__ == '__main__':
    unittest.main()
