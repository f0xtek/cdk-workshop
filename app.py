#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_workshop.pipeline_stack import WorkshopPipelinStack

app = cdk.App()
WorkshopPipelinStack(app, "WorkshopPipelineStack")

app.synth()
