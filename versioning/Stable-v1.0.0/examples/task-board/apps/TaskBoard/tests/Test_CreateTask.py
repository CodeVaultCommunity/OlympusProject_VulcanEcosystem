"""Generated from Minerva module TST-TASK-CREATE.

Source refs: UC-TASK-CREATE, AC-TASK-CREATE-AUTH, AC-TASK-CREATE-SUCCESS, AC-TASK-CREATE-INVALID, AC-TASK-CREATE-DUPLICATE, AC-TASK-CREATE-UNKNOWN
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "TST-TASK-CREATE"
SOURCE_REFS = ('UC-TASK-CREATE', 'AC-TASK-CREATE-AUTH', 'AC-TASK-CREATE-SUCCESS', 'AC-TASK-CREATE-INVALID', 'AC-TASK-CREATE-DUPLICATE', 'AC-TASK-CREATE-UNKNOWN')

import unittest

class Test_CreateTask(unittest.TestCase):
    """Generated behavioral-test binding; executable contracts live beside it."""
    tests_use_case = 'UC-TASK-CREATE'
    scenarios = [{'id': 'SCN-AC-TASK-CREATE-AUTH', 'source_ref': 'AC-TASK-CREATE-AUTH', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'Try absent context, an unresolved identity, an expired context, and a member lacking this permission. Every attempt is denied before tool invocation, with no task state or existence disclosed.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}, {'id': 'SCN-AC-TASK-CREATE-SUCCESS', 'source_ref': 'AC-TASK-CREATE-SUCCESS', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'With trusted create permission and unused TASK001 / Review Atlas, receive the exact open Task at revision zero; a later successful list includes it once.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}, {'id': 'SCN-AC-TASK-CREATE-INVALID', 'source_ref': 'AC-TASK-CREATE-INVALID', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'An empty title or whitespace-only identifier is refused before OP-TASK-CREATE is invoked.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}, {'id': 'SCN-AC-TASK-CREATE-DUPLICATE', 'source_ref': 'AC-TASK-CREATE-DUPLICATE', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'Creating TASK001 twice retains the first Task unchanged and returns duplicate-identifier refusal on the second attempt.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}, {'id': 'SCN-AC-TASK-CREATE-UNKNOWN', 'source_ref': 'AC-TASK-CREATE-UNKNOWN', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'Inject a write with lost confirmation. The case reports unknown; it does not claim no write, report success, or initiate a retry.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}]

    def test_scenarios_declare_observation_points(self) -> None:
        self.assertTrue(self.scenarios)
        for scenario in self.scenarios:
            self.assertIn("observation_points", scenario)
            self.assertNotIn("boundary", scenario)
