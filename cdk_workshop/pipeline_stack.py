from aws_cdk import Stack
from aws_cdk import aws_codecommit as codecommit
from aws_cdk import pipelines
from constructs import Construct


class WorkshopPipelinStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repo = codecommit.Repository(
            self, 'WorkshopRepo',
            repository_name='WorkshopRepo',
        )

        pipeline = pipelines.CodePipeline(
            self, 'Pipeline',
            synth=pipelines.ShellStep(
                "synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            ),
        )
