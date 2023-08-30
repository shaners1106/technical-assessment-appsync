from constructs import Construct
from aws_cdk import (
    Stack,
    aws_appsync as appsync,
    aws_lambda as _lambda
)


class TechAssessmentApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # AppSync API
        api = appsync.GraphqlApi(self,
                                 'tech-assessment-api',
                                 name='InfoMathicaAPI',
                                 schema=appsync.SchemaFile.from_asset('schema.graphql'),
                                 log_config=appsync.LogConfig(field_log_level=appsync.FieldLogLevel.ALL, exclude_verbose_content=False)
                                 )
        # Resolver 1: Mean
        lambda_mean = _lambda.Function(self,
                                       'calculate_mean',
                                       runtime=_lambda.Runtime.PYTHON_3_9,
                                       handler='mean.handler',
                                       code=_lambda.Code.from_asset('lambda')
                                       )
        # Resolver 2: Median
        lambda_median = _lambda.Function(self,
                                         'calculate_median',
                                         runtime=_lambda.Runtime.PYTHON_3_9,
                                         handler='median.handler',
                                         code=_lambda.Code.from_asset('lambda')
                                         )
        # Resolver 3: Mode
        lambda_mode = _lambda.Function(self,
                                       'calculate_mode',
                                       runtime=_lambda.Runtime.PYTHON_3_9,
                                       handler='mode.handler',
                                       code=_lambda.Code.from_asset('lambda')
                                       )
        # TODO: fix this/figure out how to attach lambdas as pipeline functions
        # # Define a pipeline resolver
        # pipeline_resolver = appsync.CfnResolver(self,
        #                                         'CalculateResolver',
        #                                         api_id=api.api_id,
        #                                         type_name='Query',
        #                                         field_name='calculate'
        #                                         )
        # # Attach lambdas as pipeline functions
        # pipeline_resolver.add_property_override(
        #     'pipeline_config', [
        #         {
        #             'functionId': lambda_mean.function_arn,
        #             'category': 'FUNCTION',
        #         },
        #         {
        #             'functionId': lambda_median.function_arn,
        #             'category': 'FUNCTION',
        #         },
        #         {
        #             'functionId': lambda_mode.function_arn,
        #             'category': 'FUNCTION',
        #         }
        #     ]
        # )
