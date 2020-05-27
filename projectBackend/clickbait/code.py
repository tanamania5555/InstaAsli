from instalooter.looters import ProfileLooter, HashtagLooter, PostLooter
from InstagramAPI import InstagramAPI
import pytesseract
from nltk.corpus import stopwords
import string
import emoji

import re
import os
import sys
import math
import time
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, date
from pprint import pprint, PrettyPrinter

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB, GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

import imageio
# !pip install --user --upgrade imageio-ffmpeg # Run this line in cmd once

username="testtt_acccc"
InstagramAPI = InstagramAPI(username, "rerHgLEc5fKYzyx")
InstagramAPI.login()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
_baseurl = "https://www.instagram.com/p/"

_stopwords = set(stopwords.words('english'))
# from string.punctuation
punctuation = r"""!"#%&'()*+,-./:;<=>?@[\]^_`{|}~""" + "°" # except $

MAX_POST_COUNT = 10
EMPTY_PROFILE_PIC = "44884218_345707102882519_2446069589734326272_n.jpg"


def count_emoji(text):
	emoji_count = 0
	for i in text:
		if i in emoji.UNICODE_EMOJI:
			emoji_count += 1
	return emoji_count


def count_digits(string):
	count = 0
	for i in range(10):
		count += string.count(str(i))
	return count


def process_text(text):
	try:
		t = emoji.demojize(text, delimiters=("   ", "   ")).split("_")
		text = ""
		for i in t:
			text += i + " "
		text = text[:-1]
	except Exception as e:
		print(e)

	for i in range(len(text)-1, -1, -1):
		if text[i] == '\n':
			text = text[:i] + " " + text[i+1:]
		if text[i:i+2] == 'w/':
			text = text[:i] + " " + text[i+2:]
	text2 = text.split(" ")
	for i in range(len(text2)-1, -1, -1):
		text2[i] = text2[i].strip()
		if text2[i] == "":
			text2 = text2[:i] + text2[i+1:]

	for i in range(len(text2)-1, -1, -1):
		if text2[i] in _stopwords:
			text2 = text2[:i] + text2[i+1:]

	text = ""
	for i in text2:
		text += i + " "
	text = text[:-1]

	text = text.translate(text.maketrans("", "", punctuation))
	text = text.lower()
	return text


def scrape_post_from_link(given_link):  # scrape post from a given link
	looter = PostLooter(given_link)
	post_list = []
	for post_info in looter.medias():
		post_dict = {}
		comment_users = []
		comment_texts = []
		comment_users_verified = []
		comment_texts_processed = []
		for i in post_info['edge_media_to_parent_comment']['edges']:
			comment_users += [i['node']['owner']['username']]
			comment_texts += [i['node']['text']]
			comment_texts_processed += [process_text(i['node']['text'])]
			comment_users_verified += [i['node']['owner']['is_verified']]
		try:
			caption = post_info['edge_media_to_caption']['edges'][0]['node']['text']
		except Exception:
			caption = ""
		if caption:
			post_dict['hashtags_cap'] = re.findall(r"#(\w+)", caption)
			post_dict['mentions_cap'] = re.findall(r"@(\w+)", caption)
		else :
			post_dict['hashtags_cap'] = []
			post_dict['mentions_cap'] = []
		post_dict['shortcode'] = post_info['shortcode']
		post_dict['photo_url'] = post_info['display_url']
		post_dict['comment_users'] = comment_users
		post_dict['comment_texts'] = comment_texts
		post_dict['comment_users_verified'] = comment_users_verified
		post_dict['comment_texts_processed'] = comment_texts_processed
		post_dict['caption'] = caption
		post_dict['post_url'] = _baseurl + str(post_info['shortcode'])
		post_dict['post_id'] = post_info['id']
		post_dict['user_name'] = post_info['owner']['username']
		post_dict['user_id'] = post_info['owner']['id']
		post_dict['user_full_name'] = post_info['owner']['full_name']
		post_dict['user_verified'] = post_info['owner']['is_verified']
		post_dict['user_private'] = post_info['owner']['is_private']
		post_dict['user_profile_pic_url'] = post_info['owner']['profile_pic_url']
		post_dict['user_post_count'] = post_info['owner']['edge_owner_to_timeline_media']['count']
		post_dict['is_ad'] = post_info['is_ad']
		post_dict['is_video'] = post_info['is_video']
		post_dict['location'] = post_info['location']
		post_dict['timestamp'] = post_info['taken_at_timestamp']
		post_dict['datetime'] = datetime.fromtimestamp(post_info['taken_at_timestamp'])
		post_dict['comments_disabled'] = post_info['comments_disabled']
		post_dict['likes'] = post_info['edge_media_preview_like']['count']
		post_dict['comments'] = post_info['edge_media_to_parent_comment']['count']

		tagged_usernames = []
		tagged_user_full_name = []
		tagged_user_verified = []
		for i in post_info['edge_media_to_tagged_user']['edges']:
			tagged_usernames += [i['node']['user']['username']]
			tagged_user_full_name += [i['node']['user']['full_name']]
			tagged_user_verified += [i['node']['user']['is_verified']]
		post_dict['tagged_usernames'] = tagged_usernames
		post_dict['tagged_user_full_name'] = tagged_user_full_name
		post_dict['tagged_user_verified'] = tagged_user_verified

		try:
			ploot = PostLooter(post_dict['post_url'])
			ploot.download('instaLooter_images/temp/')
			img = cv2.imread('instaLooter_images/temp/' + post_info['id'] + ".jpg")
			text = pytesseract.image_to_string(img)
			post_dict['image_text'] = text
			post_dict['hashtags_img'] = re.findall(r"#(\w+)", text)
			post_dict['mentions_img'] = re.findall(r"@(\w+)", text)
			text = process_text(text)
			post_dict['image_text_processed'] = text
		except Exception as e:
			post_dict['image_text'] = ""
			post_dict['hashtags_img'] = ""
			post_dict['mentions_img'] = ""
			post_dict['image_text_processed'] = ""

		post_list += [post_dict]
	return post_list


def scrape_profile(username, scrape_posts=True):  # scrape profile from a given username (not link)
	if scrape_posts == False:
		MAX_POST_SCRAPE = 1
	else:
		MAX_POST_SCRAPE = MAX_POST_COUNT
	looter = ProfileLooter(username)
	user_dict = {}
	user_dict['username'] = username
	post_list = []
	post_count = 0
	for i in looter.medias():
		post_count += 1
		code = str(i['shortcode'])
		post_list += scrape_post_from_link(_baseurl+code)
		if post_count == MAX_POST_SCRAPE:
			break
	user_dict['z_posts'] = post_list

	user_dict['full_name'] = ""
	try:
		user_dict['full_name'] = post_list[0]['user_full_name']
	except KeyError as e:
		print(e)

	user_dict['is_verified'] = False
	try:
		user_dict['is_verified'] = post_list[0]['user_verified']
	except KeyError as e:
		print(e)

	user_dict['id'] = ''
	try:
		user_dict['id'] = post_list[0]['user_id']
	except KeyError as e:
		print(e)

	user_dict['profile_pic_url'] = ""
	user_dict['profile_pic'] = 1
	try:
		user_dict['profile_pic_url'] = post_list[0]['user_profile_pic_url']
		te = ""+user_dict['profile_pic_url']
		te = re.split("[\/?]+", te)
		if EMPTY_PROFILE_PIC in te:
			user_dict['profile_pic'] = 0
	except KeyError as e:
		print(e)

	try:
		user_dict['post_count'] = post_list[0]['user_post_count']
	except KeyError as e:
		print(e)

	user_dict['is_private'] = False
	try:
		user_dict['is_private'] = post_list[0]['user_private']
	except KeyError as e:
		print(e)

	user_dict['followers'] = 0
	user_dict['following'] = 0
	user_dict['description'] = ""
	user_dict['external_url_01'] = 0
	user_dict['external_url'] = ""
	user_dict['is_business'] = False
	try:
		InstagramAPI.searchUsername(username)
		if InstagramAPI.LastResponse.status_code == 200:
			js = InstagramAPI.LastJson
			user_dict['followers'] = js['user']['follower_count']
			user_dict['following'] = js['user']['following_count']
			user_dict['description'] = js['user']['biography']
			user_dict['is_business'] = js['user']['is_business']
			if len(js['user']['external_url']) > 0:
				user_dict['external_url_01'] = 1
				user_dict['external_url'] = js['user']['external_url']
	except Exception as e:
		print(e)
	return user_dict


def classify_post1(given_post_link):  # uses database 1 to classify a post
	post = scrape_post_from_link(given_post_link)[0]
	user = scrape_profile(post['user_name'], False)
	post_arr = []
	cols = ['Likes', 'Comments', 'Followings', 'Followers', 'MediaCounts', 'LocationExistence', 'Hashtags', 'Captions', 'LengthOfHashtags', 'LengthOfCaptions', 'URLInclusion', 'MentionInclusion', 'EmojiCount', 'EmojiExistence', 'EmojiPortion']

	hashtags = ""
	for i in list(post['hashtags_cap']):
		hashtags += "#" + i + " "
	for i in list(post['hashtags_img']):
		hashtags += "#" + i + " "
	hashtags = hashtags.strip()

	post_arr += [post['likes'],
				 post['comments'],
				 user['following'],
				 user['followers'],
				 post['user_post_count'],
				 1 - int(post['location'] == 'None'),
				 hashtags,
				 post['caption'],
				]
	lenhashs = 0
	for i in post['hashtags_cap']:
		lenhashs += len(i)
	for i in post['hashtags_img']:
		lenhashs += len(i)
	post_arr += [lenhashs,
				 len(post['caption']),
				 int(len(re.findall(r'(https?://\S+)', post['caption'])) > 0),
				 int(len(list(post['mentions_cap']) + list(post['mentions_img'])) > 0),
				 count_emoji(post['caption'] + post['image_text']),
				]
	if post_arr[-1] > 0:
		post_arr += [1]
	else:
		post_arr += [0]

	post_arr += [ post_arr[-2] / ( len(post['caption']) + len(post['image_text']) ) ]
	given_post_df = pd.DataFrame([post_arr], columns=cols)

	with open("clickbait/pickle_files/classifiers1", 'rb') as file:
		classifiers1 = pickle.load(file)
	with open('clickbait/pickle_files/vectorizer1_1', 'rb') as file:
		vectorizer1_1 = pickle.load(file)
	with open('clickbait/pickle_files/vectorizer1_2', 'rb') as file:
		vectorizer1_2 = pickle.load(file)

	len_arr = [29054, 44137]
	arr = [[]]

	arr2 = vectorizer1_1.transform(given_post_df['Hashtags']).toarray()
	for j in range(len(arr2)):
		arr[j] += arr2[j, :].tolist()
	# print(len(arr[0]))

	arr2 = vectorizer1_2.transform(given_post_df['Captions']).toarray()
	for j in range(len(arr2)):
		arr[j] += arr2[j, :].tolist()
	# print(len(arr[0]))
	given_post_test = pd.DataFrame(arr)

	for i in given_post_df.columns:
		if i != 'Hashtags' and i != 'Captions':
			given_post_test[i] = given_post_df[i]
	predictions = []
	for i in classifiers1:
		predictions += i.predict(given_post_test).tolist()
	# print(predictions)
	return sum(predictions)/len(predictions)


def classify_user3(given_user): # uses database 3 to classify a user
	user = scrape_profile(given_user)
	user_arr = []
	cols = ['profile pic', 'nums/length username', 'fullname words', 'nums/length fullname', 'name==username', 'description length', 'external URL', 'private', '#posts', '#followers', '#follows']
	user_arr += [user['profile_pic'],
				 count_digits(user['username']),
				 len(user['full_name'].strip().split()),
				 count_digits(user['full_name']),
				 int(str(user['username']) == str(user['full_name'])),
				 len(user['description']),
				 user['external_url_01'],
				 int(user['is_private']),
				 int(user['post_count']),
				 int(user['followers']),
				 int(user['following'])
				]
	given_user_df = pd.DataFrame([user_arr], columns=cols)

	with open("clickbait/pickle_files/classifiers3", 'rb') as file:
		classifiers3 = pickle.load(file)
	# print("classifiers3 loaded from pickle file.")

	predictions = []
	for i in classifiers3:
		predictions += i.predict(given_user_df).tolist()
	# print(predictions)
	return sum(predictions)/len(predictions)


def classify_post6(given_link): # uses the self collected database (database6) to classify a post
	try:
		post = scrape_post_from_link(given_link)
	except Exception as e:
		print(e)
		return
	given_df = [given_link]
	for j in post[0].values():
		given_df += [j]

	given_df = pd.DataFrame([given_df], columns=['Link']+list(post[0].keys()))

	mentions_cap = []
	hashtags_cap = []
	verified_user_commented = []
	username_full_name = []
	location_in_post = []
	verified_user_tagged = []
	dollar_in_caption = []

	mentions_cap += [len(given_df['mentions_cap'][0])]
	hashtags_cap += [len(given_df['hashtags_cap'][0])]
	if True in list(given_df['comment_users_verified'][0]):
		verified_user_commented += [1]
	else:
		verified_user_commented += [0]
	if str(given_df['user_name'][0]).strip().lower() == str(given_df['user_full_name'][0]).strip().lower():
		username_full_name += [1]
	else:
		username_full_name += [0]
	if given_df['location'][0] is None:
		location_in_post += [0]
	else:
		location_in_post += [1]
	if True in list(given_df['tagged_user_verified'][0]):
		verified_user_tagged += [1]
	else:
		verified_user_tagged += [0]
	if '$' in given_df['caption'][0]:
		dollar_in_caption += [1]
	else:
		dollar_in_caption += [0]

	given_df = given_df.drop(columns=['Link', 'hashtags_cap', 'mentions_cap', 'shortcode', 'photo_url',
									  'comment_users', 'comment_texts', 'comment_users_verified',
									  'comment_texts_processed', 'post_url', 'user_full_name',
									  'user_profile_pic_url', 'location', 'datetime', 'tagged_usernames',
									  'tagged_user_full_name', 'tagged_user_verified', 'hashtags_img',
									  'mentions_img', 'image_text', 'image_text_processed'])
	given_df['mentions_cap'] = mentions_cap
	given_df['hashtags_cap'] = hashtags_cap
	given_df['verified_user_commented'] = verified_user_commented
	given_df['username_fullname'] = username_full_name
	given_df['loc_in_post'] = location_in_post
	given_df['verified_user_tagged'] = verified_user_tagged
	given_df['dollar_in_caption'] = dollar_in_caption

	given_df['user_verified'] = given_df['user_verified'].astype(int)
	given_df['user_private'] = given_df['user_private'].astype(int)
	given_df['is_ad'] = given_df['is_ad'].astype(int)
	given_df['is_video'] = given_df['is_video'].astype(int)
	given_df['comments_disabled'] = given_df['comments_disabled'].astype(int)

	with open("clickbait/pickle_files/classifiers6", 'rb') as file:
		classifiers6 = pickle.load(file)
	with open('clickbait/pickle_files/vectorizer6_1', 'rb') as file:
		vectorizer6_1 = pickle.load(file)
	with open('clickbait/pickle_files/vectorizer6_2', 'rb') as file:
		vectorizer6_2 = pickle.load(file)

	arr = []
	arr2 = vectorizer6_1.transform(given_df['caption']).toarray()
	arr += arr2[0].tolist()

	arr2 = vectorizer6_2.transform(given_df['user_name']).toarray()
	arr += arr2[0].tolist()
	given_df_train = pd.DataFrame([arr])

	for i in given_df.columns:
		if i != 'user_name' and i != 'caption':
			given_df_train[i] = given_df[i]

	result = []
	for i in classifiers6:
		result += list(i.predict(given_df_train))
	# print(result)
	return sum(result)/len(result)


def classify_post(given_link):
	return (classify_post1(given_link) + classify_post6(given_link))/2



# print('i am here')
#print(classify_user3('who'))