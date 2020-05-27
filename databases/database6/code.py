import json
import csv
import os


# Opening JSON file and loading the data
# into the variable data


path = '/Users/tanis_vt1gg0x/Desktop/clickbait'
base_link = "https://www.instagram.com/p/"
files = []
# r=root, d=directories, f = files

for f in os.listdir(path):
    files.append(f)
for file in files :

    try:
		with open(path+"/"+file) as json_file:
            data = json.load(json_file)
		isclickbait=1
		print (file)

		typename = data['__typename']
		comments_disabled = data['comments_disabled']
		height = data['dimensions']['height']
		width = data['dimensions']['width']
		displey_url = data['display_url']
		like = data['edge_liked_by']['count']
		link = base_link + data['shortcode']
		text = data['edge_media_to_caption']['edges'][0]['node']['text']
		comment_count = data['edge_media_to_comment']['count']
		post_id = data['id']
		is_video = data['is_video']
		user_id = data['owner']['id']
		shortcode = data['shortcode']
		timestamp = data['taken_at_timestamp']
		thumbnail_src = data['thumbnail_src']
		with open('data.csv', 'a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow([isclickbait,link,typename,comments_disabled ,height ,width,displey_url,like,text,comment_count,post_id,is_video,user_id,timestamp,thumbnail_src])
    except Exception as e:
        print(e)
