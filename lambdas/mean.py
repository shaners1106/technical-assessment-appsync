import json
import logging
import statistics

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)


def handler(event, context):
    try:

        # Calculate the mean
        mean = round(statistics.mean(event["values"]), 3)

        # Couple the input value set with the calculation for a response context
        response_context = {
            "values": event["values"],
            "calculation": {"mean": mean},
        }
        _logger.info(f"Sending the following response context through the pipeline to the median function: {response_context}")

        return response_context

    except statistics.StatisticsError as e:
        # An empty values array or errant input values will throw a StatisticsError
        _logger.exception(e)
        response = {
            'status_code': 400,
            'body': json.dumps({'error': str(e)})
        }
        return response
    except Exception as e:
        # Handle errors and return an error response
        _logger.exception(e)
        response = {
            'status_code': 500,
            'body': json.dumps({'error': str(e)})
        }
        return response
