from constructs import Construct
from aws_cdk import Stack, aws_appsync as appsync


class ApiStack(Stack):
    api = appsync.GraphqlApi(self,
                             'tech-assessment-api',
                             name='?????',  # Give your API a reasonable name
                             schema=appsync.SchemaFile.from_asset('<figure out full path to schema.graphql file>'),
                             log_config=appsync.LogConfig(field_log_level=appsync.FieldLogLevel.ALL, exclude_verbose_content=False)
                             )
