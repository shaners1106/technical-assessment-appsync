import json
import statistics
import logging

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)


def handler(event, context):
    try:

        _logger.info(f"Median function received event:  {json.dumps(event)}")
        _logger.info(f"Hello from Median land!")

        # Grab the previous resolver result
        # prev_result = event.get("prevResult", {})

        # Calculate the median
        median = statistics.median(event)

        _logger.info(f"Median calculated:  {median}")

        # Concatenate APIResult
        # new_calculation = {
        #     **prev_result,
        #     'mean': round(median, 3),
        # }

        # Return the result as a JSON response
        # response = {
        #     'statusCode': 200,
        #     'body': json.dumps(new_calculation)
        # }

        response = {
            'statusCode': 200,
            'body': json.dumps(context.prev.result)
        }

        # _logger.info(f"Median function response body:  {json.dumps({'mean': 3.4, 'median': 4.5, 'mode': 5.6})}")

        return response

    except Exception as e:
        # Handle errors and return an error response
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        return response
