#!/usr/bin/env python3

import aws_cdk as cdk

from gaggle.gaggle_stack import GaggleStack


app = cdk.App()
GaggleStack(app, "gaggle")

app.synth()
