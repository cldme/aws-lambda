# aws-lambda
This project implements a set of microservices that coordinate in order to guarantee data consistency using AWS Lambda and the AWS serverless application model (SAM).

# Resources
For this project we will use AWS Lambdas to implement several microservices that will run code in response to HTTP requests (using the Amazon API Gateway) and will coordinate in order to achieve data consistency. Below we provide some useful links with more information about the AWS systems being used for this project.

- [What is AWS Lambda?](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [What is Amazon API Gateway?](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [What is AWS Serverless Application Model?](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)

# Tools
For developing microservices using lambdas AWS offers a set of command line interface tools and editor plugins that make development and deployment easier.

- [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [Installing the AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-windows.html)
- [Installing the AWS VS Code Toolkit](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/setup-toolkit.html)

# Setup
The setup process for configuring an AWS account with all the required prerequisits in order to start developing with AWS Lambdas can be found [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).

This is a blank project for Python development with CDK. The `cdk.json` file tells the CDK Toolkit how to execute your app. This project is set up like a standard Python project. The initialization process also creates a virtualenv within this project, stored under the .env directory. To create the virtualenv it assumes that there is a `python3` (or `python` for Windows) executable in your path with access to the `venv` package. If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:
```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following step to activate your virtualenv.
```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:
```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.
```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add them to your `setup.py` file and rerun the `pip install -r requirements.txt` command.

  

## Useful commands

*  `cdk ls` list all stacks in the app
*  `cdk synth` emits the synthesized CloudFormation template
*  `cdk deploy` deploy this stack to your default AWS account/region
*  `cdk diff` compare deployed stack with current state
*  `cdk docs` open CDK documentation