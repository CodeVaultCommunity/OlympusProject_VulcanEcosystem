"""Generated from Minerva module TST-BOOKING-CREATE.

Source refs: UC-BOOKING-CREATE, AC-BOOKING-CREATE-01, AC-BOOKING-CREATE-02, AC-BOOKING-CREATE-03, AC-BOOKING-CREATE-TITLE, AC-BOOKING-CREATE-AUTH, AC-BOOKING-CREATE-QUALITY
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "TST-BOOKING-CREATE"
SOURCE_REFS = ('UC-BOOKING-CREATE', 'AC-BOOKING-CREATE-01', 'AC-BOOKING-CREATE-02', 'AC-BOOKING-CREATE-03', 'AC-BOOKING-CREATE-TITLE', 'AC-BOOKING-CREATE-AUTH', 'AC-BOOKING-CREATE-QUALITY')

import unittest

class Test_CreateBooking(unittest.TestCase):
    """Generated behavioral-test binding; executable contracts live beside it."""
    tests_use_case = 'UC-BOOKING-CREATE'
    scenarios = [{'id': 'SCN-AC-BOOKING-CREATE-01', 'source_ref': 'AC-BOOKING-CREATE-01', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'A valid code creates an active booking and a later lookup returns it.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}, {'id': 'SCN-AC-BOOKING-CREATE-02', 'source_ref': 'AC-BOOKING-CREATE-02', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'An invalid code is refused with no retained booking.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}, {'id': 'SCN-AC-BOOKING-CREATE-03', 'source_ref': 'AC-BOOKING-CREATE-03', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'A version conflict is never presented as a created booking.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}, {'id': 'SCN-AC-BOOKING-CREATE-TITLE', 'source_ref': 'AC-BOOKING-CREATE-TITLE', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'A whitespace-only title is refused and OP-BOOKING-SAVE is not invoked.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}, {'id': 'SCN-AC-BOOKING-CREATE-AUTH', 'source_ref': 'AC-BOOKING-CREATE-AUTH', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'Missing, unresolved, expired or insufficient caller context produces denial with no validation, tool call, composed call or data disclosure.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}, {'id': 'SCN-AC-BOOKING-CREATE-QUALITY', 'source_ref': 'AC-BOOKING-CREATE-QUALITY', 'given': 'Arrange inputs, trusted actor context, concrete-tool doubles/resources, and initial state declared by the case.', 'when': 'Invoke execute through the use-case API or a declared Boundary interaction.', 'then': 'In the declared didactic configuration, demonstrate the canonical quality criterion and its stated verification procedure; preserve its status as a teaching assumption, not a measured production claim.', 'observation_points': ['returned_outcome', 'declared_effects', 'concrete_tool_calls']}]

    def test_scenarios_declare_observation_points(self) -> None:
        self.assertTrue(self.scenarios)
        for scenario in self.scenarios:
            self.assertIn("observation_points", scenario)
            self.assertNotIn("boundary", scenario)
