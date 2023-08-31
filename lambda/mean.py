import json
import logging

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)


def handler(event, context):
    try:

        _logger.info(f"Mean function received event:  {json.dumps(event)}")
        _logger.info("********************************************************************")

        # Grab the previous resolver result
        # prev_result = event.get("prevResult", {})

        # Calculate the mean
        mean = sum(event) / len(event)

        _logger.info(f"Mean calculated:  {mean}")

        # Concatenate APIResult
        # new_calculation = {
        #     **prev_result,
        #     'mean': round(mean, 3),
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

        return response

    except Exception as e:
        _logger.exception(e)
        # Handle errors and return an error response
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        return response
