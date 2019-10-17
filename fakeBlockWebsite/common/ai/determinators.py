


class FakeDeterminator(object):
    def __init__(self):
        #should hold singleton instance of loaded dnn model
        pass

    def evaluate_post(self, post_txt=None, image_txt=None):
        """
        Determine if a Facebook post (defined as post text and/or image)
        likely contains fake news or not.

        """
        txt_fake = image_fake = False

        if post_txt:
            txt_fake = self._determine(post_txt)
        if image_txt:
            image_fake = self._dtermine(image_txt)
        #TODO: return other info about probabilty and which determinator did it?
        return txt_fake or image_fake

    def _dertermine(self, text):
        #perform more reliable fact check first
        if self._fact_check_determinator(text):
            return True
        if self._predict_determinator(text):
            return True
        return False

    def _fact_check_determinator(self, text):
        pass

    def _predict_determinator(self, text):
        pass
