#!/usr/bin/env python2

import sys
from memeocr import MemeOCR
from PIL import Image
import requests
from io import BytesIO
import cld2

def getImageFromUrl(url):
  response = requests.get(url)
  byteio = BytesIO(response.content)
  img = Image.open(byteio)

  meme_fname = 'temp.jpg'
  meme_f = open(meme_fname, 'w')

  img.save(meme_f)
  meme_f.close()
  return meme_fname

def main(argv):
  if len(argv) != 2:
      print('usage:')
      print ('    ./main.py meme-file-name')
      return

  meme_fname= argv[1] #getImageFromUrl(argv[1])

  ocr = MemeOCR()
  txt = ocr.recognize(meme_fname)

  for line in txt:
    reliable, numBytes, details = cld2.detect(line)
    lang = details[0][0]
    if lang == "UNKNOWN" or not reliable:
      continue
    print(line)

if __name__ == '__main__':
  main(sys.argv)

