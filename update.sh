#!/bin/bash

set -e

echo 'Prepare ChangeSet...'

json=$(aws cloudformation describe-stacks --stack-name serverlessrepo-aws-partner-custom-crm-connector --query 'Stacks[*].Parameters')
json=$(sed 's/ParameterKey/Name/g' <<< $json)
json=$(sed 's/ParameterValue/Value/g' <<< $json)
json=$(sed 's/\[ \[/\[/g' <<< $json)
json=$(sed 's/\] \]/\]/g' <<< $json)
changeARN=$(aws serverlessrepo create-cloud-formation-change-set \
--application-id arn:aws:serverlessrepo:us-west-2:815116410066:applications/aws-partner-custom-crm-connector \
--stack-name aws-partner-custom-crm-connector \
--capabilities CAPABILITY_RESOURCE_POLICY CAPABILITY_NAMED_IAM \
--parameter-overrides "$json" \
--query "ChangeSetId")
changeARN=$(sed -e 's/^"//' -e 's/"$//' <<<"$changeARN")

echo 'Wait 30 seconds...'
sleep 30
echo 'Deploy...'
aws cloudformation execute-change-set --change-set-name $changeARN
aws cloudformation describe-stacks --stack-name serverlessrepo-aws-partner-custom-crm-connector --query 'Stacks[*].Tags'
echo 'All done! Check AWS CloudFormation console for any errors!'
