from django.test import TestCase
from common.ai.determinators import FakeDeterminator

#TODO use coverage?? actually seriously test this proj?
#run with:
#python manage.py test fakeBlockApi/tests/

# Unit test functional behaviors of FakeDeterminator 
class FakeDeterminatorTestCase(TestCase):
	def setUp(self):
		self.determinator = FakeDeterminator()

	def test_find_story(self):
		"""Test that POS tagging method of matching stories works"""
		pass

	def test_truthy_eval(self):
		"""Test human readable ratings are correctly converted to boolean"""
		false_inputs = [
			"False",
			"Mostly False",
			"Spins the Facts",
			"Pants on Fire",
			"3 Pinocchios",
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
			#"DNC didn't direct",
			#"They're not strangers",
			"No evidence she is",
			"No, not highest ever",
			#"Not fact witness' job",
			"No Evidence",
			"Not the Whole Story",
			#"Misleads in several ways",
			"Four Pinocchios",
			"This contradicts earlier statements.",
			"Inaccurate",
			"The UK has exceeded its own targets in cutting emissions compared to 1990 levels, and has made bigger cuts than other G7 countries. But this isn’t expected to be enough to meet future targets.",
			#"Flawed_Reasoning",
			#"The litter was actually left following an event in Hyde Park promoting cannabis use.",
			#"Lacks Context",
			#"This claim is unproven",
			"Distorts the Facts",
			"Fake News",
			"Unsupported",
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
			#"Mostly True - Mostly accurate but there is more than one error or problem.",
			"In some cases",
			"True.",
			"Correct. Climate change is also part of the science curriculum in England, which all children are taught up to the age of 16. Some students have recently said they’re not learning enough about climate change on the current curriculum.",
			"Mostly_Correct",
			"Factual but not relevant",
			"True with a big caveat",
		]

		for human_readable in false_inputs:
			self.assertFalse(bool(self.determinator._eval_truthyness(human_readable)))

		for human_readable in true_inputs:
			self.assertTrue(bool(self.determinator._eval_truthyness(human_readable)))

