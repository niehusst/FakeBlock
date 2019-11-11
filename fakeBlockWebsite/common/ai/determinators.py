import requests

from fakeBlockWebsite.secrets import GOOGLE_FACT_API_KEY #TODO ???

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
        google fact check explorer hardly has any responses to what 
        I could send it, and the time it did have a response, it was unrelated to input....
        should this still be the most trusted response? or should I also force it to be in agreement with predictor?

        maybe we try to do some NLP or response matching with the API results (of a more generalized search?)
        """
        qparams = {
            'query': text,
            'pageSize': 30,
            'offset': 0,
            'key': GOOGLE_FACT_API_KEY, #TODO is this where this should be?
        }
        resp = requests.get(self.google_api_get_fact_check, params=qparams)

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
        pass
