#!/usr/bin/env python3

import aws_cdk as cdk

from tech_assessment_api.api_stack import TechAssessmentApiStack


app = cdk.App()
TechAssessmentApiStack(app, "tech-assessment-api")

app.synth()
