from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse

from .models import *
from main import settings

import string
import random
import numpy as np
import requests
from datetime import datetime, timedelta, date

# Create your views here.
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)
###########################################

def index(request):    
    return render(request, 'index.html')

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - timedelta(days=1)

def visit_table_data(request):
	start_at = request.GET["start_at"]
	end_at = request.GET["end_at"]

	if start_at == "":
		start_at = date.today().replace(day=1).strftime("%Y-%m-%d")
	if end_at == "":
		end_at = last_day_of_month(date.today()).strftime("%Y-%m-%d")

	visit_data_list = {}

	#calc first and last date of the week
	start_at_obj = datetime.strptime(start_at, "%Y-%m-%d").date()
	end_at_obj = datetime.strptime(end_at, "%Y-%m-%d").date()

	index = 0
	for d in daterange(start_at_obj, end_at_obj):		
		sql = "SELECT id, COUNT(id) as cc FROM boarding_visit WHERE start_at<='{}' AND end_at>'{}'".format(d, d)
		a = Visit.objects.raw(sql)
		cc = a[0].cc

		day = d.day
		title = str(day)
		if day == 1 :
			title = d.strftime("%b ") + str(day)

		if index == 0:
			title = d.strftime("%b ") + str(day)			

		_d = d.strftime("%Y-%m-%d")
		visit_data_list[_d] = {"title": title, "cc": cc, "date": _d}
		index = index + 1

	start_weekday = start_at_obj.weekday()
	start_timedelta = start_weekday + 1
	if start_weekday == 6:
		start_timedelta = 0

	end_weekday = end_at_obj.weekday()
	end_timedelta = 5 - end_weekday
	if end_weekday == 6:
		end_timedelta = 6


	table_start_at = (start_at_obj - timedelta(days=start_timedelta))
	table_end_at = (end_at_obj + timedelta(days=end_timedelta))

	result_arr = [[], [], [], [], [], [], []]

	index = 0
	for d in daterange(table_start_at, table_end_at):
		_d = d.strftime("%Y-%m-%d")
		if _d in visit_data_list:
			result_arr[index].append(visit_data_list[_d])
		else:
			result_arr[index].append({"title": "", "cc": "", "date": _d})

		index = index + 1
		if index == 7: index = 0	

	response = {
        "message": "success",
        "data": result_arr,        
    }
	return JsonResponse(response, safe=False, status=200)
	

def generate_data(request):
	random.seed(datetime.now())
	date_in_years = Dateinyear.objects.all()
	
	date_weight_arr = []

	index = 0
	for d in date_in_years:
		for i in range(d.weight):
			date_weight_arr.append(index)

		index = index + 1

	date_in_years_cc = len(date_in_years)
	date_weight_arr_cc = len(date_weight_arr)
		
	dogs = Dog.objects.all()

	for dog in dogs:
		visit_list = []

		visit_weight_year = random.randint(50, 500)

		x = np.zeros(date_in_years_cc, int)

		for i in range(visit_weight_year):
			val = random.randint(0, date_weight_arr_cc-1)
			val = date_weight_arr[val]
			
			x[val] = 1

		start_index = 0
		end_index = 0
		
		for i in range(date_in_years_cc):
			if x[i] == 1:
				if x[start_index] == 0:
					start_index = i
					end_index = i
				else:
					end_index = i
			else:
				if x[end_index] == 1:
					visit_list.append((date_in_years[start_index].date, date_in_years[end_index].date))
					start_index = i
					end_index = i
					
		if x[i] == 1:
			if x[start_index] == 0:
				start_index = i

			visit_list.append((date_in_years[start_index].date, date_in_years[end_index].date))

		instances = [
			Visit(dog=dog, start_at=i[0], end_at=i[1])
			for i in visit_list
		]
		
		Visit.objects.bulk_create(instances)
			
	response = {
        "message": "success",
        "data": "",        
    }
	return JsonResponse(response, safe=False, status=200)

def check_visit_date(request):
	date = request.GET["date"]

	res_arr = []

	v_arr = Visit.objects.filter(start_at__lte=date).filter(end_at__gt=date)

	for v in v_arr:
		res = {"dog": v.dog.first_name + " " + v.dog.last_name, "start_at": v.start_at, "end_at": v.end_at}
		res_arr.append(res)

	response = {
        "message": "success",
        "data": res_arr,        
    }
	return JsonResponse(response, safe=False, status=200)