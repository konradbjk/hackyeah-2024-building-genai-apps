from langflow.custom import Component
from langflow.io import BoolInput, DropdownInput, MessageInput, MessageTextInput, Output
from langflow.schema.message import Message


class ConditionalRouterComponent(Component):
    display_name = "Conditional Router"
    description = "Routes an input message to a corresponding output based on text comparison."
    icon = "equal"
    name = "ConditionalRouter"

    inputs = [
        MessageTextInput(
            name="score",
            display_name="LLM-as-Judge Score",
            info="The primary text input for the operation.",
        ),
        MessageTextInput(
            name="full_fedback",
            display_name="Full Feedback",
            info="The primary text input for the operation.",
        ),
        MessageTextInput(
            name="match_text",
            display_name="Match Text",
            info="The text input to compare against.",
        ),
        DropdownInput(
            name="operator",
            display_name="Operator",
            options=["equals", "not equals", "contains", "starts with", "ends with"],
            info="The operator to apply for comparing the texts.",
            value="equals",
            advanced=True,
        ),
        BoolInput(
            name="case_sensitive",
            display_name="Case Sensitive",
            info="If true, the comparison will be case sensitive.",
            value=False,
            advanced=True,
        ),
        MessageInput(
            name="message",
            display_name="Message",
            info="The message to pass through either route.",
        ),
    ]

    outputs = [
        Output(display_name="True Route", name="true_result", method="true_response"),
        Output(display_name="False Route", name="false_result", method="false_response"),
    ]

    def evaluate_condition(self, input_text: str, match_text: str, operator: str, case_sensitive: bool) -> bool:
        score = float(input_text)
        threshold = float(match_text)
        
        return score <=threshold

    def true_response(self) -> Message:
        result = self.evaluate_condition(self.score, self.match_text, self.operator, self.case_sensitive)
        if result:
            self.status = self.message
            return self.message
        else:
            self.stop("true_result")
            return None  # type: ignore

    def false_response(self) -> Message:
        result = self.evaluate_condition(self.score, self.match_text, self.operator, self.case_sensitive)
        if not result:
            self.status = self.full_fedback
            return self.full_fedback
        else:
            self.stop("false_result")
            return None  # type: ignore
