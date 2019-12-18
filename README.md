# FakeBlock
A chrome plugin to prevent Facebook users from becoming misinformed by 
their news feeds by obscuring posts determined to be fake news.
Utilizing a mixture of AI and the Google FactCheck API, FakeBlock
meticulously examines each post to determine its legitimacy before
allowing it to be shown to the user.

TODO specifically target englush (political?) fake new
TODO ack data sets
{
	https://www.kaggle.com/shashank1558/preprocessed-twitter-tweets/data
	https://github.com/KaiDMML/FakeNewsNet
	https://github.com/lutzhamel/fake-news

	https://www.kaggle.com/mrisdal/fake-news
}
TODO add download link

### Usage
Download the extension from the Google store [here](), and navigate to
`https://www.facebook.com/?sk=nf` where you will need an account in order
to see your news feed. You should see that the FakeBlock icon in the top
right has lit up, and is no longer gray. Clicking on the icon will open a 
small popup that contains the setting to activate/deactivate the fake news
blocker; make sure the switch is on if you want FakeBlock to block fake news
for you! And you can always switch it off if you want to stop blocking 
posts for a while.

FakeBlock does not store any data long-term other than the activation setting; 
any and all information it scrapes from your Facebook news feed is sent to the 
Google FactCheck API, passed through the FakeBlock machine learning algorithm,
and then immediatly released. 

### Getting Started with Development
If you want to make your own adjustments to this project, the first step is 
installing the dependencies with `pip install -r DEPS`. If you want to use the 
OCR module that I decided not to include, you will also have to download Tesseract,
following the instructions on [their github](https://github.com/tesseract-ocr/tesseract/wiki).
This will set you up with the necessary tools to work with the Django API and TensorFlow
neural network. I developed this project using Python 3.6.5.

To gain access to the Google FactCheck Claim Search API client library, you will need to set up an API
key through a Google account to authorize your access to their API. That can be done for free
(since the FactCheck API isn't super popular/powerful) following the instructions on [their 
website](https://developers.google.com/fact-check/tools/api/).

To develop on the Chrome extension aspect of the project, you will also need a Google account 
and Google Chrome to enable developer mode in the Chrome browser settings and upload your custom extension
package to. The directory to upload as the extension is `chrome_extension`. There are more
details on how to get started with Chrome extensions on Google's [developer website](https://developer.chrome.com/extensions/getstarted).

In order to make the local API visible to the extension, you will need to change the 
value of the `apiUrl` parameter in the **events.js** file to `'http://127.0.0.1:8000/api/fake'`
for the extension to find your localy hosted API. Lastly to start the API server,
just call `python manage.py runserver` to start the Django server.

Once everything is setup, you will need a Facebook account in order to test
it on `https://www.facebook.com/?sk=nf` (the only URL the extension is set to run on).
You should see the icon for the browser page extension light up on this page, and
the extension will immediately start running in the background as soon as the DOM loads.

Troubleshooting can be done with both the Chrome debugging tools and the output from the
local Django server.

## Author
* **Liam Niehus-Staab** - [niehusst](https://github.com/niehusst)

## Acknowledgements
* Custom logo and images were adjusted from stock images under Creative Commons and from [Pixabay](https://pixabay.com/users/clker-free-vector-images-3736/)
* [Imgur](https://imgur.com/) for free online image hosting for my logos
* [Google FactCheck API](https://developers.google.com/fact-check/tools/api/)
* (Unused) Tesseract OCR modified from work by [johnlinp](https://github.com/johnlinp/meme-ocr)
* [Heroku](https://www.heroku.com/) for hosting the API and website
