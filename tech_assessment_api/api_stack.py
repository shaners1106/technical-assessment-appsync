from constructs import Construct
from aws_cdk import (
    Stack,
    aws_appsync as appsync,
    aws_lambda as _lambda,
    aws_iam as iam
)
from aws_cdk.aws_appsync import (
    CfnGraphQLApi,
    CfnGraphQLSchema,
    CfnDataSource,
    CfnResolver,
    CfnFunctionConfiguration,
)


class TechAssessmentApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # AppSync API
        api = CfnGraphQLApi(self,
                            id="TechAssessmentApi",
                            name="InfoMathicaAPI",
                            authentication_type="API_KEY"
                            )
        api_schema = CfnGraphQLSchema(self,
                                      id="Schema",
                                      api_id=api.attr_api_id,
                                      definition=open("schema.graphql", "r").read()
                                      )
        # Generate an API key for the API
        api_auth_key = appsync.CfnApiKey(self,
                                         id="TechAssessmentAuthKey",
                                         api_id=api.attr_api_id
                                         )
        # Pipeline function 1: Mean
        lambda_mean = _lambda.Function(self,
                                       id='CalculateMean',
                                       runtime=_lambda.Runtime.PYTHON_3_9,
                                       handler='mean.handler',
                                       code=_lambda.Code.from_asset('lambda')
                                       )
        # Pipeline function 2: Median
        lambda_median = _lambda.Function(self,
                                         id='CalculateMedian',
                                         runtime=_lambda.Runtime.PYTHON_3_9,
                                         handler='median.handler',
                                         code=_lambda.Code.from_asset('lambda')
                                         )
        # Pipeline function 3: Mode
        lambda_mode = _lambda.Function(self,
                                       id='CalculateMode',
                                       runtime=_lambda.Runtime.PYTHON_3_9,
                                       handler='mode.handler',
                                       code=_lambda.Code.from_asset('lambda')
                                       )
        # Authenticate lambda data sources with IAM Role
        appsync_lambda_role = iam.Role(self,
                                       'AppSyncLambdaRole',
                                       assumed_by=iam.ServicePrincipal('appsync.amazonaws.com')
                                       )
        lambda_mean.grant_invoke(appsync_lambda_role)
        lambda_median.grant_invoke(appsync_lambda_role)
        lambda_mode.grant_invoke(appsync_lambda_role)

        # Define the Data Sources
        mean_lambda_ds = CfnDataSource(self,
                                       id="MeanLambdaDS",
                                       api_id=api.attr_api_id,
                                       name="MeanLambdaDS",
                                       type="AWS_LAMBDA",
                                       lambda_config=appsync.CfnDataSource.LambdaConfigProperty(lambda_function_arn=lambda_mean.function_arn),
                                       service_role_arn=appsync_lambda_role.role_arn
                                       )
        median_lambda_ds = CfnDataSource(self,
                                         id="MedianLambdaDS",
                                         api_id=api.attr_api_id,
                                         name="MedianLambdaDS",
                                         type="AWS_LAMBDA",
                                         lambda_config=appsync.CfnDataSource.LambdaConfigProperty(lambda_function_arn=lambda_median.function_arn),
                                         service_role_arn=appsync_lambda_role.role_arn
                                         )
        mode_lambda_ds = CfnDataSource(self,
                                       id="ModeLambdaDS",
                                       api_id=api.attr_api_id,
                                       name="ModeLambdaDS",
                                       type="AWS_LAMBDA",
                                       lambda_config=appsync.CfnDataSource.LambdaConfigProperty(lambda_function_arn=lambda_mode.function_arn),
                                       service_role_arn=appsync_lambda_role.role_arn
                                       )
        # Connect lambdas to AppSync
        mean_function = CfnFunctionConfiguration(self,
                                                 id="MeanFunction",
                                                 api_id=api.attr_api_id,
                                                 name="MeanFunction",
                                                 data_source_name=mean_lambda_ds.name,
                                                 function_version="2018-05-29",
                                                 request_mapping_template="""
                                                    {
                                                        "operation": "Invoke",
                                                        "payload": $util.toJson($ctx.arguments)
                                                    }
                                                 """,
                                                 response_mapping_template="$util.toJson($ctx.result)"
                                                 )
        median_function = CfnFunctionConfiguration(self,
                                                   id="MedianFunction",
                                                   api_id=api.attr_api_id,
                                                   name="MedianFunction",
                                                   data_source_name=median_lambda_ds.name,
                                                   function_version="2018-05-29",
                                                   request_mapping_template="""
                                                       {
                                                           "operation": "Invoke",
                                                           "payload": $util.toJson($ctx.prev.result)
                                                       }
                                                    """,
                                                   response_mapping_template="$util.toJson($ctx.result)"
                                                   )
        mode_function = CfnFunctionConfiguration(self,
                                                 id="ModeFunction",
                                                 api_id=api.attr_api_id,
                                                 name="ModeFunction",
                                                 data_source_name=mode_lambda_ds.name,
                                                 function_version="2018-05-29",
                                                 request_mapping_template="""
                                                    {
                                                        "operation": "Invoke",
                                                        "payload": $util.toJson($ctx.prev.result)
                                                    }
                                                 """,
                                                 response_mapping_template="$util.toJson($ctx.result)"
                                                 )
        # Instantiate the Pipeline Resolver
        pipeline_resolver = CfnResolver(self,
                                        id="TechAssessmentPipelineResolver",
                                        api_id=api.attr_api_id,
                                        field_name="calculate",
                                        type_name="Query",
                                        kind="PIPELINE",
                                        pipeline_config=CfnResolver.PipelineConfigProperty(
                                            functions=[
                                                mean_function.attr_function_id,
                                                median_function.attr_function_id,
                                                mode_function.attr_function_id
                                            ]
                                        ),
                                        request_mapping_template="""
                                            {
                                                "version": "2018-05-29",
                                                "operation": "Invoke",
                                                "payload": $util.toJson($context.arguments),
                                            }
                                        """,
                                        response_mapping_template="$util.toJson($ctx.prev.result)"
                                        )

        # Add dependencies to ensure proper resource creation order
        mean_function.add_dependency(mean_lambda_ds)
        median_function.add_dependency(median_lambda_ds)
        mode_function.add_dependency(mode_lambda_ds)
        pipeline_resolver.add_dependency(mean_function)
        pipeline_resolver.add_dependency(median_function)
        pipeline_resolver.add_dependency(mode_function)

        # Authenticate with a dynamically generated API Key
        pipeline_resolver.add_dependency(api_auth_key)
