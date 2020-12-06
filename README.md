Chalice CI/CD App
=================
## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
    - [AWS CDK](#aws-cdk)
    - [Chalice](#chalice)
- [Development Flow](#development-flow)
    - [Deploying the application](#deploying-the-chalice-application)

## Overview
chalice-cicd-app is a template repo for a serverless application using the [AWS Chalice serverless framework](https://aws.github.io/chalice/index.html#). This repo includes both a hello-world Chalice app, as well as a CI/CD pipeline for deploying the code written using the [AWS Cloud Development Kit](https://aws.amazon.com/cdk/). It is **highly** recommended that developers have a working understanding of the CDK, Chalice framework, and the underlying serverless AWS resources being manipulated during serverless development.

## Installation

### AWS CDK
To install the AWS CDK, please follow the [AWS CDK installation instructions](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_install).

### Chalice
To install Chalice (only necessary for local development without the CI/CD pipeline), please follow the [Chalice installation instructions](https://aws.github.io/chalice/quickstart.html).

## Development Flow
The development flow for this repo can be split into two streams. Work on the CI/CD pipeline to deploy the application is found under the [pipeline](https://github.com/folksgl/chalice-cicd-app/pipeline) while the application code can be done in the [helloworld](https://github.com/folksgl/chalice-cicd-app/helloworld).

### Deploying the Chalice application
All deployments require having the correct AWS CLI credentials in place. If you haven't already, install the AWS CLI and set up credentials to your account.
#### With the CI/CD pipeline
Before deploying with the CI/CD pipeline, you must create a CodeStar Connection to the GitHub account your repo is located in. Once that connection is created,
store the ARN of the connection in a SecretsManager Secret, with the JSON key of 'arn'. In JSON, the secret should look like the following:
```json
{ "arn": "<my-connection-arn>" }
```
To deploy the application with the CI/CD pipeline:
```sh
cd pipeline
cdk deploy --parameters ConnectionSecretId=<secret-id>
```
#### Without the pipeline
Deployments without the pipeline must change directories into the hello world directory. Chalice deployments can make direct usage of the `chalice` CLI tool
using `chalice local` or `chalice deploy` commands. Please use `chalice --help` and see the [Chalice documentation](https://aws.github.io/chalice/index.html).
