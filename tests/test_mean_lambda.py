import unittest
from unittest.mock import MagicMock
from lambdas import mean


class TestCalculateMeanLambda(unittest.TestCase):
    """
    A class to validate the Mean Lambda function
    """

    def test_empty_input(self):
        """
        A test to confirm that an empty input returns a 400 Bad Request response
        """

        # Mock event data and context
        event = {"values": []}
        context = MagicMock()

        # Invoke Mean Lambda
        result = mean.handler(event, context)

        # Verify the result
        self.assertEqual(result["status_code"], 400)

    def test_calculate_mean(self):
        """
        A test to confirm that the lambda accurately calculates the Mean value of the input set
        """

        # Mock event data and context
        event = {"values": [10.5, 20.2, 15.7, 8.9, 8.9, 4.4, 13.6]}
        context = MagicMock()

        # Invoke Mean Lambda
        result = mean.handler(event, context)

        # Verify results
        self.assertEqual(len(result), 2)    # Contains 2 objects - 1 for input values and 1 for calculation
        self.assertIn("values", result)
        self.assertGreater(len(result["values"]), 0)
        for value in result["values"]:
            self.assertTrue(isinstance(value, (int, float)))
        self.assertIn("calculation", result)
        expected_mean_value = 11.743
        self.assertEqual(result["calculation"]["mean"], expected_mean_value)    # Confirm accurate calculation


if __name__ == '__main__':
    unittest.main()
