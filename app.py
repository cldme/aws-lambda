#!/usr/bin/env python3

from aws_cdk import core

from aws_lambda.aws_lambda_stack import AwsLambdaStack


app = core.App()
AwsLambdaStack(app, "aws-lambda")

app.synth()
