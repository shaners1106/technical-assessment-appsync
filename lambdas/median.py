import json
import statistics
import logging

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)


def handler(event, context):
    try:

        # Calculate the median
        median = round(statistics.median(event["values"]), 3)

        # Concatenate APIResult and build response context
        new_calculation = {
            **event["calculation"],
            'median': round(median, 3),
        }

        response_context = {
            "values": event["values"],
            "calculation": new_calculation,
        }
        _logger.info(f"Sending the following response context through the pipeline to the mode function: {response_context}")

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
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        return response
