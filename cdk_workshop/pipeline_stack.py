from aws_cdk import Stack
from aws_cdk import aws_codecommit as codecommit
from constructs import Construct


class WorkshopPipelinStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repo = codecommit.Repository(
            self, 'WorkshopRepo',
            repository_name='WorkshopRepo',
        )
