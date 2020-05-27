import requests, csv,json

url = 'http://192.168.0.103:8080/post/'
count1=-5
with open('nonClickbait_2.csv') as f:
    data = csv.reader(f)
    for row in data:
        count1+=1
        if count1>0:
            try:
                myobj = {'link': row[0]}
                x = requests.post(url, json = myobj)
                print(str(row[0])+" "+str(count1)+" "+str(json.loads(x.text)['classifier_result']))
            except:
                print('error'+str(count1))