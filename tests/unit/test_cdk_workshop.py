import pytest
from aws_cdk import Stack, assertions
from aws_cdk import aws_lambda as _lambda

from cdk_workshop.hitcounter import HitCounter


@pytest.fixture
def stack():
    return Stack()


@pytest.fixture
def hit_counter(stack):
    return HitCounter(
        stack, "HitCounter",
        downstream=_lambda.Function(
            stack, "TestFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='hello.handler',
            code=_lambda.Code.from_asset('lambda')
        ),
    )


@pytest.fixture
def template(stack):
    return assertions.Template.from_stack(stack)


def test_dynamodb_table_created(stack, hit_counter, template):
    template.resource_count_is('AWS::DynamoDB::Table', 1)


def test_lambda_has_env_vars(stack, hit_counter, template):
    envCapture = assertions.Capture()
    template.has_resource_properties('AWS::Lambda::Function', {
        'Handler': 'hitcount.handler',
        'Environment': envCapture,
    })
    assert envCapture.as_object() == {
        'Variables': {
            'DOWNSTREAM_FUNCTION_NAME': {'Ref': 'TestFunction22AD90FC'},
            'HITS_TABLE_NAME': {'Ref': 'HitCounterHits079767E5'},
        },
    }


def test_dynamodb_with_encryption(stack, hit_counter, template):
    template.has_resource_properties('AWS::DynamoDB::Table', {
        'SSESpecification': {
            'SSEEnabled': True,
        },
    })


def test_dynamodb_raises_value_error_for_invalid_read_capacity(stack):
    with pytest.raises(Exception):
        HitCounter(
            stack, 'HitCounter',
            downstream=_lambda.Function(
                stack, 'TestFunction',
                runtime=_lambda.Runtime.PYTHON_3_9,
                handler='hello.handler',
                code=_lambda.Code.from_asset('lambda'),
            ),
            read_capacity=1,
        )
