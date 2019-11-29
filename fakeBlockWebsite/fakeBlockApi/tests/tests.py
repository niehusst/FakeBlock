from django.test import TestCase
from common.ai.determinators import FakeDeterminator
import nltk

#TODO use coverage?? actually seriously test this proj?
#run with:
#python manage.py test fakeBlockApi/tests/

threshold = 0.6

def tag(text):
	tokens = nltk.word_tokenize(text)
	desired_pos = set(['NN','NNS','NNP','NNPS','JJ','JJR','JJS','VB','VBG','VBN','VBP','VBZ'])
	return [word[0] for word in nltk.pos_tag(tokens) if word[1] in desired_pos]

# Unit test functional behaviors of FakeDeterminator 
class FakeDeterminatorTestCase(TestCase):
	def setUp(self):
		self.determinator = FakeDeterminator()

	def test_matching_false(self):
		"""Test that matching post-like text to news articles does not match
			unrelated stories"""
		false_inputs = [
			("Climate change is fake! The earth's climate changes on its own!", 
				"Magnus Söderlund proposed or advocated eating human flesh as a solution to climate change in remarks he made on Sept. 3, 2019."),
			("The earth is flat and not round; Christopher Columbus just sailed around the disk.", 
				"Sailor and explorer Christopher Columbus proved the earth was round."),
			#("The earth is flat",
			#	"The earth is not flat"),
			("Obama was was born in Kenya", 
				"Former U.S. President Barack Obama is about to claim Kenyan citizenship to avoid being tried for treason by the U.S."),
			("Stanley Kubrick helped the US government stage the moon landings",
				"Chinese lunar rover finds no evidence of American moon landings."),
		]
		for search, news in false_inputs:
			tagged_search = tag(search)
			self.assertFalse(self.determinator._matches(tagged_search, news, threshold))


	def test_matching_true(self):
		"""Test that matching post-like text to news articles does match
			related stories"""
		true_inputs = [
			#("Global warming is natural and has happened throughout the history of the earth!", 
			#	"Today’s global warming is no different from previous warming periods in Earth’s past."),
			("Obama was was born in Kenya",
				"Says President Obama's \"grandmother in Kenya said he was born in Kenya and she was there and witnessed the birth.\""),
			#("Stanley Kubrick helped the US government stage the moon landings",
			#	"A photograph showing a group of astronauts without their helmets on indicates that the moon landing was staged by Stanley Kubrick."),
			("Angela Merkel met Hitler",
				"A photograph shows a very young Angela Merkel with Adolf Hitler."),
			("Representative Elise Stefanik flipped off Republicans after impeachment hearing",
				"A image shows Rep. Elise Stefanik giving the middle finger at the end of a public impeachment inquiry hearing."),
		]
		for search, news in true_inputs:
			tagged_search = tag(search)
			self.assertTrue(self.determinator._matches(tagged_search, news, threshold))

	def test_truthy_eval_false(self):
		"""Test human readable ratings are correctly converted to boolean
			for inputs that should map to False."""
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
			"Flawed_Reasoning",
			#"The litter was actually left following an event in Hyde Park promoting cannabis use.",
			"Lacks Context",
			#"This claim is unproven",
			"Distorts the Facts",
			"Fake News",
			"Unsupported",
		]
		for human_readable in false_inputs:
			self.assertFalse(bool(self.determinator._eval_truthyness(human_readable)))


	def test_truthy_eval_true(self):
		"""Test human readable ratings are correctly converted to boolean
			for inputs that should map to True."""
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
		for human_readable in true_inputs:
			self.assertTrue(bool(self.determinator._eval_truthyness(human_readable)))

