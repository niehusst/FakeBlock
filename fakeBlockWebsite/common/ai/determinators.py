import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googleapiclient.discovery import build

from common.common import get_logger, Singleton
from fakeBlockWebsite.secrets import GOOGLE_FACT_API_KEY 

err_logger = get_logger(__name__)

class FakeDeterminator(object, metaclass=Singleton):
    """
    An object with methods for determining if text is likely to contain fake
    news or not. Requires instantiation for setup of various helpers.
    """

    def __init__(self):
        #TODO hold singleton instance of loaded dnn model
        #download resources for sentiment analysis
        nltk.download('vader_lexicon') 
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        self.sentiment_analyze = SentimentIntensityAnalyzer()
        print("creating singleton")

    def evaluate_post(self, post_txt=None, image_txt=None):
        """
        Determine if a Facebook post (defined as post text and/or image)
        likely contains fake news or not.

        @param post_txt - String, text to examine the legitimacy of
        @return - Boolean
        """
        txt_fake = image_fake = False
        if post_txt:
            txt_fake = self._determine(post_txt)
        if image_txt:
            image_fake = self._dtermine(image_txt) #TODO chop out image stuff
        
        return txt_fake or image_fake

    def _determine(self, text):#TODO: return other info about probabilty and which determinator did it?
        """
        Determines (using Google Fact Check API and a custom neural net) if
        the input text is likely to be fake news.

        @param text - String, the text to evaluate the truthfulness of
        @return - Boolean, indicating if text is likely to be fake (True) or 
                  legit (False)
        """
        #perform more(?) reliable fact check first
        api_check = self._fact_check_determinator(text)
        #TODO return more info here???
        if api_check == 1:
            return True
        elif api_check == 0:
            return False
        else:
            # -1 indicates no matching API response for text
            if self._predict_determinator(text):
                return True 
            else:
                return False

    def _fact_check_determinator(self, text):
        """
        maybe we try to do some NLP or response matching with the API results (of a more generalized search?)
        #TODO: determine if this tool ultimately hurts or helps performance stats at end (same with OCR? still 2 slow. Unless Heroku server is super fast)

        @param text - String, the query text to search for in the Google
                    Fact Check API
        @return - Integer, -1 for No match found, 0 for False, 1 for True
        """
        try:
            factCheckService = build("factchecktools", "v1alpha1", developerKey=GOOGLE_FACT_API_KEY)
            request = factCheckService.claims().search(query=text, pageSize=30, offset=0)
            response = request.execute()
        except HttpError as err:
            # cant access API right now! return no match
            err_logger.error("Error accessing Google Fact API:  {}".format(err))
            return -1

        if response:
            # NLP POS tagging. Parse all nouns, verbs, and adjectives out of text
            tokens = nltk.word_tokenize(text)
            desired_pos = set(['NN','NNS','NNP','NNPS','JJ','JJR','JJS','VB','VBG','VBN','VBP','VBZ'])
            crit_words = [word[0] for word in nltk.pos_tag(tokens) if word[1] in desired_pos]
            # pick response from claims array that represents input (if there is one)
            for possible_match in response['claims']:
                if self._matches(crit_words, possible_match['text'], 0.7):
                    print('foudn a matach!')#TODO debgu
                    #evaluate from textualRating the truthyness of the claim
                    return self._eval_truthyness(possible_match['claimReview'][0]['textualRating'])
        return -1

    def _matches(self, base_set, candidate, threshold):
        """
        Determines if threshold% or more of base_set matches the candidate.
        Base set is a list of words that are 'important'. 
        (Important words only in order to reduce false buffer percent that 
        simple articles etc. would provide)

        @param base_set - List of Strings, the text we want to find the 
                            matching percentage of.
        @param candidate - String, the text that we are testing for a match
                            against base_text.
        @param threshold - Float, number between 0 and 1.0 [inclusive] that
                            is the percentage of words in base_set
                            that must be present in candidate in order to 
                            return True.
        @return - Boolean, True if threshold is met, else False
        """
        #TODO: this method does not deal with negated sentences (e.g. "world is flat" will 100% match "world is not flat":True, returning wrong result)
        threshold = min(max(0.0, threshold), 1.0)
        candidate_set = set(nltk.word_tokenize(candidate))
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
        ss = FakeDeterminator.__instance.sentiment_analyze.polarity_scores(fact_rating) 
        # if compound is positive, it is likely to be true
        if ss['compound'] > 0:
            return 1
        elif ss['compound'] < 0:
            return 0
        else:
            #TODO special parsing???
            pass
        # compound is often 0 for negative fact_rating (e.g. False -> 0 compound score)
        return 1

    def _predict_determinator(self, text):
        """
        Use a neural net to make a prediction
        """
        #TODO use NLTK for neural net? dense net?? look online what others do
        pass


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