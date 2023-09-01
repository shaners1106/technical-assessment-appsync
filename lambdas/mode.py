import json
import statistics
import logging

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)


def handler(event, context):
    try:

        # Calculate the median
        mode = round(statistics.mode(event["values"]), 3)

        # Concatenate final APIResult
        final_calculation = {
            **event["calculation"],
            'mode': round(mode, 3),
        }
        _logger.info(f"Sending the final calculation through the pipeline to the After Mapping Template: {final_calculation}")

        return final_calculation

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
