import json


def handler(event, context):
    try:

        # Calculate the mean
        mean = sum(event) / len(event)

        # Return the result as a JSON response
        response = {
            'statusCode': 200,
            'body': json.dumps({'mean': round(mean, 3)})
        }

        return response

    except Exception as e:
        # Handle errors and return an error response
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        return response
