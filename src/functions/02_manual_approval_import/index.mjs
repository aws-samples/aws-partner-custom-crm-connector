console.log('Loading function');

import { SNSClient, PublishCommand } from "@aws-sdk/client-sns";
import { XRayClient, BatchGetTracesCommand } from "@aws-sdk/client-xray";

export const handler = async (event, context, callback) => {

    console.log('event= ' + JSON.stringify(event));
    console.log('context= ' + JSON.stringify(context));

    const executionContext = event.ExecutionContext;
    console.log('executionContext= ' + executionContext);

    const executionName = executionContext.Execution.Name;
    console.log('executionName= ' + executionName);

    const statemachineName = executionContext.StateMachine.Name;
    console.log('statemachineName= ' + statemachineName);

    const taskToken = executionContext.Task.Token;
    console.log('taskToken= ' + taskToken);

    const apigwEndpint = process.env.ApiGatewayURL;
    console.log('apigwEndpint = ' + apigwEndpint)

    const approveEndpoint = apigwEndpint + "/approve?taskToken=" + encodeURIComponent(taskToken);
    console.log('approveEndpoint= ' + approveEndpoint);

    const rejectEndpoint = apigwEndpint + "/reject?taskToken=" + encodeURIComponent(taskToken);
    console.log('rejectEndpoint= ' + rejectEndpoint);

    const emailSnsTopic = process.env.TopicArn;
    console.log('emailSnsTopic= ' + emailSnsTopic);

    var emailMessage = 'Welcome! \n\n';
    emailMessage += 'For security reasons, we require your consent before importing any data into AWS APN (ACE). \n\n'
    emailMessage += 'Please click "Approve" link if you want to start the import job. \n\n'
    emailMessage += 'Job Name -> ' + executionName + '\n\n'
    emailMessage += 'Approve ' + approveEndpoint + '\n\n'
    emailMessage += 'Reject ' + rejectEndpoint + '\n\n'
    emailMessage += 'Thanks for using the AWS ACE Integration!'

    const snsClient = new SNSClient();
    var params = {
        Message: emailMessage,
        Subject: "Required approval from AWS ACE Integration",
        TopicArn: emailSnsTopic
    };

    try {
        const data = await snsClient.send(new PublishCommand(params));
        console.log("Success.", data);
        return data; // For unit tests.
    } catch (err) {
        console.log("Error", err.stack);
    }

    /*const response = {
        statusCode: 200,
        body: JSON.stringify('All good!'),
    };
    return response;*/
};