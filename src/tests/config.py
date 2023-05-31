import toml
import os
import boto3

sfn = boto3.client("stepfunctions")
cloudformation = boto3.resource("cloudformation")


class Config:
    spmid: int
    stage: str
    email: str
    stack_name: str
    _api_gateway_url: str

    step_function_arn: str
    step_function_orchestration_arn: str

    def __init__(self) -> None:
        if os.path.exists("samconfig.toml"):
            with open("samconfig.toml", mode="r") as f:
                config = toml.load(f)
                self.stack_name = config["default"]["global"]["parameters"][
                    "stack_name"
                ]
                parameter_overrides = config["default"]["deploy"]["parameters"][
                    "parameter_overrides"
                ]

        else:
            self.stack_name = os.environ["STACK_NAME"]
            parameter_overrides = os.environ["PARAMETER_OVERRIDES"]

        for entry in parameter_overrides.split(" "):
            key, value = entry.split("=")
            if key == "PartnerIdParameter":
                self.spmid = value.replace('"', "")
            elif key == "StageParameter":
                self.stage = value.replace('"', "")
            elif key == "WorkflowNotificationEmail":
                self.email = value.replace('"', "")
            

        for step_function in sfn.list_state_machines()["stateMachines"]:
            if step_function["name"] == f"AIF-Partner-to-AWS-Orchestrate-{self.stage}":
                self.step_function_orchestration_arn = step_function["stateMachineArn"]
            if step_function["name"] == f"AIF-Partner-to-AWS-{self.stage}]":
                self.step_function_arn = step_function["stateMachineArn"]
        self._api_gateway_url = None

    @property
    def bucket_name(self) -> str:
        return f"ace-partner-integration-{self.spmid}-{self.stage}-us-west-2"

    @property
    def api_gateway_url(self) -> str:
        if not self._api_gateway_url:
            stack = cloudformation.Stack(self.stack_name)
            outputs = stack.outputs
            self._api_gateway_url = [
                output["OutputValue"]
                for output in outputs
                if output["OutputKey"] == "ApiGatewayURL"
            ][0]
        return self._api_gateway_url
