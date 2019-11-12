import requests

from fakeBlockWebsite.secrets import GOOGLE_FACT_API_KEY #TODO does this import work???

class FakeDeterminator(object):
    def __init__(self):
        #TODO hold singleton instance of loaded dnn model
        #TODO only instantiate this object 1 time
        self.google_api_get_fact_check = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    def evaluate_post(self, post_txt=None, image_txt=None):
        """
        Determine if a Facebook post (defined as post text and/or image)
        likely contains fake news or not.

        """
        txt_fake = image_fake = False

        if post_txt:
            txt_fake = self._determine(post_txt)
        if image_txt:
            image_fake = self._dtermine(image_txt) #TODO chop our image stuff
        
        return txt_fake or image_fake

    def _dertermine(self, text):#TODO: return other info about probabilty and which determinator did it?
        """
        Determines (using Google Fact Check API and a custom neural net) if
        the input text is likely to be fake news.

        @param text - String, the text to evaluate the truthfulness of
        @return - Boolean, indicating if text is likely to be fake (True) or 
                  legit (False)
        """
        #perform more reliable fact check first
        if self._fact_check_determinator(text):
            return True
        if self._predict_determinator(text):
            return True
        return False

    def _fact_check_determinator(self, text):
        """
        maybe we try to do some NLP or response matching with the API results (of a more generalized search?)

        #TODO: determine if this tool ultimately hurts or helps performance stats at end (same with OCR? still 2 slow. Unless Heroku server is super fast)

        @return - Integer, -1 for No match found, 0 for False, 1 for True
        """
        qparams = {
            'query': text,
            'pageSize': 30,
            'offset': 0,
            'key': GOOGLE_FACT_API_KEY, #TODO is this where this should be?
        }
        resp = requests.get(self.google_api_get_fact_check, params=qparams)

        #pick response from claims array that represents input (if there is one)
        for possible_match in resp['claims']:
            if self._matches(text, possible_match['text'], 0.7):
                #evaluate from textualRating the truthyness of the claim
                return self._eval_truthyness(possible_match['claimReview'][0]['textualRating'])
        return -1

    def _matches(self, base_text, candidate, threshold):
        """
        Determines if threshold% or more of base_text matches the candidate.

        @param base_text - String, the text we want to maximize the 
                            matching percentage of.
        @param candidate - String, the text that we are testing for a match
                            against base_text.
        @param threshold - Float, number between 0 and 1.0 [inclusive] that
                            is the percentage of [important] words in base_text
                            that must be present in candidate in order to 
                            return True.
                            (Important words only in order to reduce false 
                            buffer percent that simple articles would provide)
        @return - Boolean, True if threshold is met, else False
        """
        threshold = min(max(0.0, threshold), 1.0)

        #TODO NLP POS tagging
        base_set = nlp.important_words(base_text) #use Part Of Speech tagging to get nouns+verbs+adjectives
        candidate_set = set(candidate.split(" "))

        count = 0
        for word in base_set:
            if word in candidate_set:
                count += 1

        return (count/len(base_set)) >= threshold

    def _eval_truthyness(self, fact_rating):
        """
        Decide if fact_rating is indicating a positive (True) or negative
        (False) rating.

        @param fact_rating - String, indicates a level truthyness, but may be
                            represented in non-standard ways.
        @return - Integer, 0 if fact_rating indicates a negative rating, 1
                    if rating appears to be positive (or shows uncertainty)
        """
        #TODO use NLP sentiment analysis?? do some special case testing (i.e. when it's a 1/5 number rating)
        #False
        #Mostly False
        #Spins the Facts
        #Pants on Fire
        #3 pinnochios
        #Not True
        return 1
"""
{
  "claims": [
    {
      "text": "Flat earth 'theory' says Tunisia’s Jugurtha Tableland is the stump of an ancient giant tree",
      "claimant": "YouTube channel",
      "claimDate": "2016-08-01T00:00:00Z",
      "claimReview": [
        {
          "publisher": {
            "name": "Africa Check",
            "site": "africacheck.org"
          },
          "url": "https://africacheck.org/fbcheck/no-flat-earth-conspiracy-theorists-cant-claim-tunisias-jugurtha-tableland-as-the-stump-of-an-ancient-giant-tree/",
          "title": "No, flat earth conspiracy theorists can't claim Tunisia's Jugurtha Tableland as the stump of an ancient giant tree",
          "reviewDate": "2019-01-24T00:00:00Z",
          "textualRating": "False",
          "languageCode": "en"
        }
      ]
    }
  ]
}

"""

    def _predict_determinator(self, text):
        """
        Use a neural net to make a prediction
        """
        #TODO use NLTK?
        pass
