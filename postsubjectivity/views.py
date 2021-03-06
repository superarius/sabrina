# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import Alias, Habla, Beat, TextPost, ImagePost
from datetime import datetime
import random
from itertools import combinations_with_replacement
import pytz

tz = pytz.timezone('America/Santiago')


def index_ajax(request):
	last = request.GET.get("last_text", None);
	Posts = TextPost.objects.all()
	data = {"text":random.choice([post.t.upper() for post in Posts if post.t.upper()!=last])}
	return JsonResponse(data)

def index(request):
	Posts = TextPost.objects.all()
	images = [i.embedding for i in ImagePost.objects.all()]
	random.shuffle(images)
	context = {"new_text":random.choice([post.t.upper() for post in Posts]), "image_links":images}
	return render(request, "index.html", context)

def enter(request):
	return render(request, "enter.html")

def home(request):
	try:
		x = "%s" %request.POST["alias"]
		count = 0
		for char in x:
			if char == ' ':
				count +=1
			else:
				count +=100000
		if count==0:
			return render(request, "enter.html")
	except:
		return HttpResponse("hi")
	try:
		count = 0
		all_A = Alias.objects.all()
		for A in all_A:
			if A.name == x:
				A.logins+=1
				A.last_login=datetime.now(tz)
				A.save()
				current_A = A
				count +=1
		if count == 0:
			new_A = Alias()
			new_A.name = x
			new_A.date = datetime.now(tz)
			new_A.last_login = datetime.now(tz)
			new_A.logins = 1
			new_A.save()
			current_A = new_A
		latest_habla=Habla.objects.order_by('-id')[0:5]
		latest_habla=list(reversed(latest_habla))[0:5]
		show_habla=[(h.text, h.date) for h in latest_habla]
		context={"alias":current_A, "habla":show_habla}
	except:
		return HttpResponse("hi2")
	try:
		return render(request, "home.html", context)
	except:
		return HttpResponse("hi3")

def contribute(request, alias_id):
	try:
		current_A = Alias.objects.get(id=alias_id)
		current_A.logins += 1
		current_A.last_login = datetime.now(tz)
		current_A.save()
	except:
		return HttpResponse("if I don't know who you are I don't know who I am")
	try:
		input_text = request.POST["talk"]
		spaces = 0
		letters = 0
		for char in input_text:
			if char == ' ':
				spaces += 1
			else:
				letters += 1
		if spaces == 0:
			if letters > 50:
				return HttpResponse("sorry you have temporarily lost access to sabrinas conciousness (most text is allowed so maybe just add some spaces to your text? or if it is a url make a tinyurl...")
		else:
			check = float(letters)/float(spaces)
			if check > 24:
				return HttpResponse("sorry you have temporarily lost access to sabrinas conciousness")
		new_H = Habla()
		new_H.text = input_text
		new_H.date = datetime.now(tz)
		new_H.alias = current_A
		new_H.save()
		latest_habla=Habla.objects.order_by('-id')[0:5]
		latest_habla=list(reversed(latest_habla))[0:5]
		show_habla=[(h.text, h.date) for h in latest_habla]
		context={"alias":current_A, "habla":show_habla}
		return render(request, "home.html", context)
	except:
		latest_habla=Habla.objects.order_by('-id')[0:5]
		latest_habla=list(reversed(latest_habla))[0:5]
		show_habla=[(h.text, h.date) for h in latest_habla]
		context={"alias":current_A, "habla":show_habla}
		return render(request, "home.html", context)

def incarnations(request, alias_id):
	aliases=Alias.objects.order_by("-last_login")[:]
	current_A = Alias.objects.get(id=alias_id)
	current_A.logins += 1
	current_A.last_login = datetime.now(tz)
	current_A.save()
	context={"aliases":aliases, "user":current_A}
	return render(request, "incarnations.html", context)

def heartbeats(request, alias_id):
	current_A = Alias.objects.get(id=alias_id)
	current_A.logins += 1
	current_A.last_login = datetime.now(tz)
	current_A.save()
	new_H = Beat()
	new_H.tag = datetime.now(tz)
	new_H.alias = current_A
	new_H.save()
	heartbeats = Beat.objects.order_by("-tag")[:]
	context={"alias":current_A, "beats":heartbeats, "new":new_H}
	return render(request, "heartbeats.html", context)

def official(request, alias_id):
	return HttpResponse("ok")

def thoughts(request, alias_id):
	current_A = Alias.objects.get(id=alias_id)
	current_A.logins += 1
	current_A.last_login = datetime.now(tz)
	current_A.save()
	latest_habla=Habla.objects.order_by('-id')[0:25]
	latest_habla=list(reversed(latest_habla))[0:25]
	show_habla=[(h.text, h.date) for h in latest_habla]
	context={"alias":current_A, "habla":show_habla}
	return render(request, "thoughts.html", context)

def questions(request, alias_id):
	return HttpResponse("ok")

def writing(request):
	Posts = TextPost.objects.all()
	p = [Posts[1], Posts[0]]
	p.extend(Posts[2:])
	context = {"Posts":p}
	return render(request, "writings.html", context)














