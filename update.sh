#!/usr/bin/env bash

set -e

echo 'Prepare ChangeSet...'

stackName='serverlessrepo-aws-partner-custom-crm-connector'

json=$(aws cloudformation describe-stacks --stack-name "$stackName" --query 'Stacks[*].Parameters')
json="${json//ParameterKey/Name}"
json="${json//ParameterValue/Value}"
json="${json//\[ \[/\[}"
json="${json//\] \]/\]}"
json=$(echo $json | tr -d "[]")
json=[$json]

changeARN=$(aws serverlessrepo create-cloud-formation-change-set \
--application-id arn:aws:serverlessrepo:us-west-2:815116410066:applications/aws-partner-custom-crm-connector \
--stack-name "aws-partner-custom-crm-connector" \
--capabilities CAPABILITY_RESOURCE_POLICY CAPABILITY_NAMED_IAM \
--parameter-overrides "$json" \
--query "ChangeSetId")
changeARN=$(sed -e 's/^"//' -e 's/"$//' <<< "$changeARN")

echo 'Wait 30 seconds...'
sleep 30
echo 'Deploy...'

aws cloudformation execute-change-set --change-set-name "$changeARN"
aws cloudformation describe-stacks --stack-name "$stackName" --query 'Stacks[*].Tags'

echo 'Done!'
echo 'Check AWS CloudFormation console for progress and/or any errors!'
