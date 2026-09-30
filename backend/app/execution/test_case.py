from dataclasses import dataclass


@dataclass
class JudgeTestCase:
    input_data: str
    expected_output: str
    is_hidden: bool = False
