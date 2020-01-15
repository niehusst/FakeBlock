#!/bin/python
import os
import pandas as pd
import urllib.request
#TODO ack data in README
#data cleaning script
url_base = 'https://raw.githubusercontent.com/KaiDMML/FakeNewsNet/master/dataset/'
url_combined_data = 'https://raw.githubusercontent.com/lutzhamel/fake-news/master/data/fake_or_real_news.csv'
gc_fake_fname = 'gc_fake.csv'
gc_real_fname = 'gc_real.csv'
pf_fake_fname = 'pf_fake.csv'
pf_real_fname = 'pf_real.csv'
real_fake_fname = 'real_fake.csv'
non_news_fname = 'data/non_news.csv'
fake_news_fname = 'data/fake.csv'

data_set_path = 'data/fake_news_dataset.csv'

#download datasets from github
print("[INFO] Downloading datasets from github...", end="", flush=True)
urllib.request.urlretrieve(url_base + 'gossipcop_fake.csv', gc_fake_fname)
urllib.request.urlretrieve(url_base + 'gossipcop_real.csv', gc_real_fname)
urllib.request.urlretrieve(url_base + 'politifact_fake.csv', pf_fake_fname)
urllib.request.urlretrieve(url_base + 'politifact_real.csv', pf_real_fname)
urllib.request.urlretrieve(url_combined_data, real_fake_fname)
print("[DONE]")

#get files as dataframes
print("[INFO] Reading CSV data into data frames")
gc_fake = pd.read_csv(gc_fake_fname)
gc_real = pd.read_csv(gc_real_fname)
pf_fake = pd.read_csv(pf_fake_fname)
pf_real = pd.read_csv(pf_real_fname)
real_fake_df = pd.read_csv(real_fake_fname)
non_news = pd.read_csv(non_news_fname, engine='python') #from https://www.kaggle.com/c/twitter-sentiment-analysis2/data
fake_news = pd.read_csv(fake_news_fname) #from https://www.kaggle.com/mrisdal/fake-news


print("[INFO] Cleaning data frames and merging")
#clean up fake news dataset; delete unneeded cols and repeat/non-english rows
fake_news.drop(fake_news[fake_news.language != 'english'].index, inplace=True)
fake_news['title'] = fake_news['thread_title']
fake_news = fake_news[['title']]
fake_news.drop_duplicates(inplace=True)

#strip white-space off non-news twitter post strings
non_news.applymap(lambda x: x.strip() if isinstance(x, str) else x)
#cut non-news dataset size to reduce its representation in the data
non_news.drop(non_news.sample(n=(len(non_news)-((len(gc_real)+len(pf_real))//2))).index, inplace=True)

#create truth columns. Fake news has 1 (True) in it's `fake` column
gc_fake['fake'] = 1
gc_real['fake'] = 0
pf_fake['fake'] = 1
pf_real['fake'] = 0
fake_news['fake'] = 1
non_news['fake'] = 0
real_fake_df['fake'] = list(map(int, real_fake_df['label']=='FAKE'))

#get all text to analyze under the same column name
non_news['title'] = non_news['SentimentText']

#merge dataframes
news_df = pd.concat([gc_real, gc_fake, pf_fake, pf_real, real_fake_df, non_news, fake_news])
#fix concatted index columns
news_df.index = list(range(len(news_df)))


#delete unused cols
news_df = news_df[['title', 'fake']]
#make sure no nulls
if news_df.isnull().values.any():
	nan_rows = news_df[news_df['title'].isnull()]
	news_df.drop(nan_rows.index, inplace=True)

#balance data set to have equal sample sizes between binary classes
num_fake = sum(news_df.fake)
num_real = len(news_df.fake) - num_fake
remove_instances = abs(num_real - num_fake)
#remove randomly from the class that has more occurances in the dataset
news_df = news_df.drop(news_df[news_df.fake==int(num_fake>num_real)].sample(n=remove_instances).index)

#basic metrics
n_fake = sum(news_df.fake)
n_real = len(news_df.fake) - n_fake
print("[INFO] {} data points collected. {} Real, {} Fake".format(len(news_df), n_real, n_fake))

#save as new single csv file
print("[INFO] Saving data set to " + data_set_path)
news_df.to_csv(data_set_path)

#remove old files
print("[INFO] Clean up")
os.remove(gc_real_fname)
os.remove(gc_fake_fname)
os.remove(pf_real_fname)
os.remove(pf_fake_fname)
os.remove(real_fake_fname)
