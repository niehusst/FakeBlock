# FakeBlock
A chrome plugin to prevent Facebook users from becoming misinformed by 
their news feeds by obscuring posts determined to be fake news.
Utilizing a mixture of AI and the Google FactCheck API, FakeBlock
meticulously examines each post to determine its legitimacy before
allowing it to be shown to the user.

This tool only has support for English-language, political news checking;
any and all other languages will be ignored without further examination.


TODO add chrome store download link

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
installing the dependencies with `pip install -r DEPS`. This will set you up with 
the necessary tools to work with the Django API and TensorFlow neural network. If 
you want to use the OCR module that I decided not to include, you will also have 
to download Tesseract, following the instructions on [their github](https://github.com/tesseract-ocr/tesseract/wiki). 
I developed this project using Python 3.6.5. The Chrome extension aspect needs
no installations (other than an up-to-date Chrome browser).

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
just call `python manage.py runserver` to start the Django server to host the API locally.

Lastly, you may have noticed that a `secrets.py` file is missing from the `fakeBlockWebsite/fakeBlockWebsite/`
directory (for obvious security reasons), so you will have to create your own. It should contain:
```
SECRET_KEY='your django secret key here'
GOOGLE_FACT_API_KEY='your google api key here'
```

Once everything is setup, you will need a Facebook account in order to test
it on `https://www.facebook.com/?sk=nf` (the only URL the extension is set to run on).
Once you are logged in and reach the page, you should see the icon for the browser page 
extension light up on this page, and the extension will immediately start running in the 
background as soon as the DOM loads.

Troubleshooting can be done with both the Chrome debugging tools and the output from the
local Django server.

## Author
* **Liam Niehus-Staab** - [niehusst](https://github.com/niehusst)

## Acknowledgements
* Custom logo and images were adjusted from stock images under Creative Commons and from [Pixabay](https://pixabay.com/users/clker-free-vector-images-3736/)
* [Imgur](https://imgur.com/) for free online image hosting for my logos
* [Google FactCheck API](https://developers.google.com/fact-check/tools/api/)
* (Unused) Tesseract OCR modified from work by [johnlinp](https://github.com/johnlinp/meme-ocr)
* [Heroku](https://www.heroku.com/) for hosting the API and demo website
* [Bootstrap](https://getbootstrap.com/) for helping make my demo website pretty
* Training data for the neural network was compiled from datasets provided by 
[Megan Risdal](https://www.kaggle.com/mrisdal/fake-news) under CC0 licensing, 
[lutzhamel](https://github.com/lutzhamel/fake-news) under GNU 3.0 licensing, 
(anonymous) [Kaggle Twitter data](https://www.kaggle.com/c/twitter-sentiment-analysis2/data) provided freely without license,
and [KaiDMML](https://github.com/KaiDMML/FakeNewsNet) data was provided given the citation of the following papers: 

```
@article{shu2018fakenewsnet,
  title={FakeNewsNet: A Data Repository with News Content, Social Context and Dynamic Information for Studying Fake News on Social Media},
  author={Shu, Kai and  Mahudeswaran, Deepak and Wang, Suhang and Lee, Dongwon and Liu, Huan},
  journal={arXiv preprint arXiv:1809.01286},
  year={2018}
}

@article{shu2017fake,
  title={Fake News Detection on Social Media: A Data Mining Perspective},
  author={Shu, Kai and Sliva, Amy and Wang, Suhang and Tang, Jiliang and Liu, Huan},
  journal={ACM SIGKDD Explorations Newsletter},
  volume={19},
  number={1},
  pages={22--36},
  year={2017},
  publisher={ACM}
}

@article{shu2017exploiting,
  title={Exploiting Tri-Relationship for Fake News Detection},
  author={Shu, Kai and Wang, Suhang and Liu, Huan},
  journal={arXiv preprint arXiv:1712.07709},
  year={2017}
}
```
