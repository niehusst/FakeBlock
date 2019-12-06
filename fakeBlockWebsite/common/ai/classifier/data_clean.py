#!/bin/python
import os
import pandas as pd
import urllib.request

#data cleaning script
url_base = 'https://raw.githubusercontent.com/KaiDMML/FakeNewsNet/master/dataset/'
gc_fake_fname = 'gc_fake.csv'
gc_real_fname = 'gc_real.csv'
pf_fake_fname = 'pf_fake.csv'
pf_real_fname = 'pf_real.csv'
data_set_path = 'data/fake_news_dataset.csv'

#download datasets from FakeNewsNet github
print("[INFO] Downloading datasets from github...", end="", flush=True)
urllib.request.urlretrieve(url_base + 'gossipcop_fake.csv', gc_fake_fname)
urllib.request.urlretrieve(url_base + 'gossipcop_real.csv', gc_real_fname)
urllib.request.urlretrieve(url_base + 'politifact_fake.csv', pf_fake_fname)
urllib.request.urlretrieve(url_base + 'politifact_real.csv', pf_real_fname)
print("[DONE]")

#get files as dataframes
print("[INFO] Reading CSV data into data frames")
gc_fake = pd.read_csv(gc_fake_fname)
gc_real = pd.read_csv(gc_real_fname)
pf_fake = pd.read_csv(pf_fake_fname)
pf_real = pd.read_csv(pf_real_fname)

print("[INFO] data has {} gossipcop headlines and {} politifact headlines".format(len(gc_fake)+len(gc_real), len(pf_real)+len(pf_fake)))


#create truth columns
print("[INFO] Cleaning data frames and merging")
gc_fake['fake'] = 1
gc_real['fake'] = 0
pf_fake['fake'] = 1
pf_real['fake'] = 0
#TODO: use one hot for real/fake? then get probability for sure

#merge dataframes
news_df = pd.concat([gc_real, gc_fake, pf_fake, pf_real])
#fix concatted index columns
news_df.index = list(range(len(news_df)))

#delete unused cols
cols_to_delete = ['id', 'news_url', 'tweet_ids']
news_df = news_df.drop(labels=cols_to_delete, axis='columns')

#balance data set to have equal sample sizes between binary classes
n_true = sum(news_df.fake)
n_false = len(news_df.fake) - n_true
remove_instances = abs(n_false - n_true)
news_df = news_df.drop(news_df[news_df.fake==0].sample(n=remove_instances).index)

#basic metrics
n_true = sum(news_df.fake)
n_false = len(news_df.fake) - n_true
print("[INFO] data has {} fake news instances and {} real news instances".format(n_true, n_false))

#save as new single csv file
print("[INFO] Saving data set to " + data_set_path)
news_df.to_csv(data_set_path)

#remove old files
print("[INFO] Clean up")
os.remove(gc_real_fname)
os.remove(gc_fake_fname)
os.remove(pf_real_fname)
os.remove(pf_fake_fname)
