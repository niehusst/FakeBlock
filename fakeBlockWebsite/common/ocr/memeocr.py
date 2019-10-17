"""
Copyright (c) 2013, averangeall and johnlinp
All rights reserved. 

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met: 

 * Redistributions of source code must retain the above copyright notice, 
   this list of conditions and the following disclaimer. 
 * Redistributions in binary form must reproduce the above copyright 
   notice, this list of conditions and the following disclaimer in the 
   documentation and/or other materials provided with the distribution. 
 * Neither the name of  nor the names of its contributors may be used to 
   endorse or promote products derived from this software without specific 
   prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
"""
import sys
import os
import re
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cld2
import pytesseract

#TODO: make sure the TESSDATA_PREFIX environment variable is set so meme language can be found
class MemeOCR:
    def __init__(self):
        self._white_thresh = 240
        self._tmp_image = None

    def recognize(self, url):
        txt = None
        self._get_image_from_url(url)
        self._thresh_words(self._tmp_image)
        txt = self._exec_tesseract()
        print("txt is:  {}".format(txt))
        self._delete_tmp_files()
        return self._filter_response(txt)

    def _get_image_from_url(self, url):    #TODO: THIS CANT OPEN JPGs FOR SOME REASON????
        """
        Load the data from url into a cv Mat image and save it into
        temporary PIL Image so it can be OCRed.

        @param url - string, a valid url pointing to an image address
        @return meme_fname - the temporary file name the image was saved to
        """
        response = requests.get(url)
        byteio = BytesIO(response.content)
        self._tmp_image = Image.open(byteio)
        #convert to rgb to eliminate possible alpha channel
        self._tmp_image = self._tmp_image.convert('RGB')

    def _thresh_words(self, img):
        if not img:
            return
        img = np.array(img)

        # threshold all pixels above _white_thresh to white, others to black
        # to more easily isolate/read the text
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if all([elem >= self._white_thresh for elem in img[i][j]]):
                    img[i][j] = [255]*3
                else:
                    img[i][j] = [0]*3

        self._tmp_image.close() #cleanup before overwriting with new data
        self._tmp_image = Image.fromarray(img)

    def _exec_tesseract(self):
        # use the meme tessdata language file
        config = r'-l meme'
        return pytesseract.image_to_string(self._tmp_image, config=config)

    def _filter_response(self, txt):
        """
        Filter out illegible text responses.

        @param txt - list, each element representing a line of OCRed text
        @return legible_lines - list, contains only the english legible
                            elements of `txt`
        """
        legible_lines = []
        if txt:
            blocks = re.split(r'\n\n', txt)
            lines = [re.sub(r'\s+', ' ', block) for block in blocks if block.strip()]
            print("in memeocer, raw:  {}".format(lines)) #TODO debug
            for line in lines:
                reliable, numBytes, details = cld2.detect(line)
                lang = details[0][0]
                if lang == "UNKNOWN" or not reliable:
                    continue
                legible_lines.append(line)

        return legible_lines

    def _delete_tmp_files(self):
        if self._tmp_image:
            self._tmp_image.close()

