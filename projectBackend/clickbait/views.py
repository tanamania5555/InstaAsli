from django.shortcuts import render
from .models import Post, User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json,csv
from .code import classify_post as clp
from .code import classify_user3 as clu

@csrf_exempt
def post(request):
    if request.method == "POST":
        print("Request received for checking link!")
        data_1 = request.body.decode('utf-8')
        data = json.loads(data_1)
        l = data['link']
        d = dict()
        d['status'] = 'Post link posted successfully!'
        try:
            clp_res = clp(l)*100
            d['classifier_result'] = clp_res
            pLink = Post(link=l, clickbait=clp_res)
            pLink.save()
        except Exception as e:
            print(str(e))
            d['classifier_result'] = -1
    
        return HttpResponse(json.dumps(d),status=200)
   
    if request.method == "GET":
        data = Post.objects.all()
        f = open('clickbaits.csv','w')
        w = csv.writer(f)
        result = dict()
        for i in data:
            result[i.link]=i.clickbait
            w.writerow([i.link, i.clickbait])
        return HttpResponse(json.dumps(result),status=200)
    else:
        return HttpResponse("Bad request!",status=400)



@csrf_exempt
def user(request):
    if request.method == "POST":
        print("Request received for checking user!")
        data_1 = request.body.decode('utf-8')
        data = json.loads(data_1)
        u = data['link']
        d = dict()
        d['status'] = 'User link posted successfully!'
        try:
            clu_res = clu(u)*100
            d['classifier_result'] = clu_res
            uLink = User(handle=u, clickbait=clu_res)
            uLink.save()
        except Exception as e:
            print(str(e))
            d['classifier_result'] = -1

        return HttpResponse(json.dumps(d),status=200)
    if request.method == "GET":
        data = User.objects.all()
        f = open('Usersclickbaits.csv','w')
        w = csv.writer(f)
        result = dict()
        for i in data:
            result[i.handle]=i.clickbait
            w.writerow([i.handle, i.clickbait])
        return HttpResponse(json.dumps(result),status=200)
    else:
        return HttpResponse("Bad request!",status=400)