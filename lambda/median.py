import json
import statistics


def handler(event, context):
    try:

        # Calculate the median
        median = statistics.median(event)

        # Return the result as a JSON response
        response = {
            'statusCode': 200,
            'body': json.dumps({'mean': round(median, 3)})
        }

        return response

    except Exception as e:
        # Handle errors and return an error response
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        return response
