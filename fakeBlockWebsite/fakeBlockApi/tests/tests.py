from django.test import TestCase
from common.ai.determinators import FakeDeterminator


# Test the truthyness evaluator (convert human readable text to boolean)
class FakeDeterminatorTestCase(TestCase):
	def setUp(self):
		self.determinator = FakeDeterminator()

	def test_truthy_eval(self):
		"""test that know responses are correctly converted to boolean"""
		false_inputs = [
			"False",
			"Mostly False",
			"Spins the Facts",
			"Pants on Fire",
			"3 Pinnochios",
			"Not True",
			"Misleading",
			"An element of truth, but exaggerated and misleading",
			"Cherry Picks",
			"Incorrect",
			"Decontextualized",
			"This is misleading.",
			"Fake",
			"This is exaggerated.",
			"Scam",
			"Miscaptioned",
			"Incorrect",
			"Unproven",
		]
		true_inputs = [
			"True",
			"Mostly True",
			"Accurate",
			"Correct Attribution",
			"Half True",
			"Maybe.",
			"Mixture",
			"Correct",
			"Mostly correct",
			"Reports heavily disputed",
		]

		for human_readable in false_inputs:
			self.assertEqual(bool(self.determinator._eval_truthyness(human_readable)), False)

		for human_readable in true_inputs:
			self.assertEqual(bool(self.determinator._eval_truthyness(human_readable)), True)

