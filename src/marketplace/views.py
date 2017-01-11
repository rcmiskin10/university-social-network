from django.shortcuts import get_object_or_404, render_to_response, RequestContext, Http404, HttpResponseRedirect, render, HttpResponse
import hashlib, datetime, random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from schedule.models import Schedule
from schedule.forms import ScheduleForm
from team_schedule.models import TeamSchedule
from team_schedule.forms import TeamScheduleForm
from frat_schedule.models import FratSchedule
from frat_schedule.forms import FratScheduleForm
from course.models import Course, Syllabus, Assignment, StudentCourse
from main_schedule.models import MainSchedule
from main_schedule.forms import MainScheduleForm
from .models import Product, Category
from .forms import ProductForm
from accounts.models import MyUser


import json


def marketplace(request):
	if request.user.is_authenticated():
		newest = Product.objects.filter(sold=False).order_by('-timestamp')

		schedule_form = MainScheduleForm(request.POST or None, prefix='schedule')

		product_form = ProductForm(request.POST or None, request.FILES or None, prefix='product')
		electronic = Category.objects.get(name='Electronics')
		electronics = Product.objects.filter(category=electronic).filter(sold=False)
		house = Category.objects.get(name='Sublet')
		housing = Product.objects.filter(category=house).filter(sold=False)
		room = Category.objects.get(name='Furniture')
		rooms = Product.objects.filter(category=room).filter(sold=False)
		tutor = Category.objects.get(name='Tutors')
		tutors = Product.objects.filter(category=tutor).filter(sold=False)
		textbook = Category.objects.get(name='Textbooks')
		textbooks = Product.objects.filter(category=textbook).filter(sold=False)
		other = Category.objects.get(name='Other')
		others = Product.objects.filter(category=other).filter(sold=False)
		apparel = Category.objects.get(name='Apparel')
		apparels = Product.objects.filter(category=apparel).filter(sold=False)

		print electronics
		main_schedule = MainSchedule.objects.filter(user=request.user)
		syllabus = Syllabus.objects.filter(user=request.user)
		schedule = Schedule.objects.filter(user=request.user)
		assignment=Assignment.objects.filter(user=request.user)
		team_schedule=TeamSchedule.objects.filter(user=request.user)
		frat_schedule=FratSchedule.objects.filter(user=request.user)
		today = datetime.datetime.now().date()
		date_list = []
		name_list = []
		id_list = []
		course_list = []
		group_list = []
		main_list = []
		choice_list = []
		for item in main_schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append("General")
		        choice_list.append("main")
		for item in assignment:
		    if not datetime.datetime.strptime(item.due_date, '%Y-%m-%d').date() < today:
		        date_list.append(datetime.datetime.strptime(item.due_date, '%Y-%m-%d').date())
		        name_list.append(item.name)
		        id_list.append(item.id)
		        group_list.append(item.course.course_num)
		        choice_list.append("course")
		for item in schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append(item.club.club_name)
		        choice_list.append("club")
		for item in team_schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append(item.team.name)
		        choice_list.append("team")
		for item in frat_schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append(item.frat.name)
		        choice_list.append("frat")

		g = zip(id_list, date_list, name_list, group_list, choice_list )
		f_all = sorted(g, key=lambda x: x[1])
		paginator = Paginator(f_all, 5) # Show 25 contacts per page


		page = request.GET.get('page')
		try:
		    f = paginator.page(page)
		except PageNotAnInteger:
		    # If page is not an integer, deliver first page.
		    f = paginator.page(1)
		except EmptyPage:
		    # If page is out of range (e.g. 9999), deliver last page of results.
		    f = paginator.page(paginator.num_pages) 
		return render_to_response('marketplace/marketplace.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def product_search(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		products = Product.objects.filter(title__icontains = q )[:20]
        
        
		results = []
		for product in products:
			product_json = {}
			product_json['label'] = product.title
            
            
			results.append(product_json)
      


		data = json.dumps(results)

	else:
		data = 'fail'
	mimetype = 'application/json'


	return HttpResponse(data, mimetype)

def add_product(request):
    users = MyUser.objects.filter(is_active=True)
    products = Product.objects.all()
    product_form = ProductForm(request.POST or None, request.FILES or None, prefix='product')
    if request.method == 'POST':
        
        if product_form.is_valid():
            form3 = product_form.save(commit=False)
            form3.owner = request.user
            
            form3.save()
            
            response_data = {}

            
            response_data['response'] = True

            new_data = json.dumps(response_data)

            return HttpResponse(new_data, content_type='application/json')

        else:
            data = {}
            data['response'] = False
            new_data = json.dumps(data)
            return HttpResponse(new_data, content_type='application/json')

def sold(request):
    
	if request.method =='POST':
		user = request.user
		product_id = request.POST.get('product_id')
            
        
		obj = Product.objects.get(id=product_id)
		


		response_data = {}
		response_data['id'] = obj.id

		obj.sold = True
		obj.save()

		new_data = json.dumps(response_data)
		
		return HttpResponse(new_data, content_type='application/json')



def account_history_sold(request):
	if request.user.is_authenticated():
		products = Product.objects.filter(owner=request.user).filter(sold=True)

		schedule_form = MainScheduleForm(request.POST or None, prefix='schedule')
		main_schedule = MainSchedule.objects.filter(user=request.user)
		syllabus = Syllabus.objects.filter(user=request.user)
		schedule = Schedule.objects.filter(user=request.user)
		assignment=Assignment.objects.filter(user=request.user)
		team_schedule=TeamSchedule.objects.filter(user=request.user)
		frat_schedule=FratSchedule.objects.filter(user=request.user)
		today = datetime.datetime.now().date()
		date_list = []
		name_list = []
		id_list = []
		course_list = []
		group_list = []
		main_list = []
		choice_list = []
		for item in main_schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append("General")
		        choice_list.append("main")
		for item in assignment:
		    if not datetime.datetime.strptime(item.due_date, '%Y-%m-%d').date() < today:
		        date_list.append(datetime.datetime.strptime(item.due_date, '%Y-%m-%d').date())
		        name_list.append(item.name)
		        id_list.append(item.id)
		        group_list.append(item.course.course_num)
		        choice_list.append("course")
		for item in schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append(item.club.club_name)
		        choice_list.append("club")
		for item in team_schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append(item.team.name)
		        choice_list.append("team")
		for item in frat_schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append(item.frat.name)
		        choice_list.append("frat")

		g = zip(id_list, date_list, name_list, group_list, choice_list )
		f_all = sorted(g, key=lambda x: x[1])
		paginator = Paginator(f_all, 5) # Show 25 contacts per page


		page = request.GET.get('page')
		try:
		    f = paginator.page(page)
		except PageNotAnInteger:
		    # If page is not an integer, deliver first page.
		    f = paginator.page(1)
		except EmptyPage:
		    # If page is out of range (e.g. 9999), deliver last page of results.
		    f = paginator.page(paginator.num_pages)  
		return render_to_response('marketplace/account_history_sold.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def account_history_selling(request):
	if request.user.is_authenticated():
		products = Product.objects.filter(owner=request.user).filter(sold=False)
		schedule_form = MainScheduleForm(request.POST or None, prefix='schedule')
		main_schedule = MainSchedule.objects.filter(user=request.user)
		syllabus = Syllabus.objects.filter(user=request.user)
		schedule = Schedule.objects.filter(user=request.user)
		assignment=Assignment.objects.filter(user=request.user)
		team_schedule=TeamSchedule.objects.filter(user=request.user)
		frat_schedule=FratSchedule.objects.filter(user=request.user)
		today = datetime.datetime.now().date()
		date_list = []
		name_list = []
		id_list = []
		course_list = []
		group_list = []
		main_list = []
		choice_list = []
		for item in main_schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append("General")
		        choice_list.append("main")
		for item in assignment:
		    if not datetime.datetime.strptime(item.due_date, '%Y-%m-%d').date() < today:
		        date_list.append(datetime.datetime.strptime(item.due_date, '%Y-%m-%d').date())
		        name_list.append(item.name)
		        id_list.append(item.id)
		        group_list.append(item.course.course_num)
		        choice_list.append("course")
		for item in schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append(item.club.club_name)
		        choice_list.append("club")
		for item in team_schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append(item.team.name)
		        choice_list.append("team")
		for item in frat_schedule:
		    if not item.duedate < today:
		        date_list.append(item.duedate)
		        name_list.append(item.text)
		        id_list.append(item.id)
		        group_list.append(item.frat.name)
		        choice_list.append("frat")

		g = zip(id_list, date_list, name_list, group_list, choice_list )
		f_all = sorted(g, key=lambda x: x[1])
		paginator = Paginator(f_all, 5) # Show 25 contacts per page


		page = request.GET.get('page')
		try:
		    f = paginator.page(page)
		except PageNotAnInteger:
		    # If page is not an integer, deliver first page.
		    f = paginator.page(1)
		except EmptyPage:
		    # If page is out of range (e.g. 9999), deliver last page of results.
		    f = paginator.page(paginator.num_pages) 
		return render_to_response('marketplace/account_history_selling.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def product_search(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			search_text = request.POST['search_text']
		
		
		category = Category.objects.filter(name__icontains=search_text)
		category_products = Product.objects.filter(category__icontains=category, sold=False).distinct()
		products = Product.objects.filter(title__icontains=search_text, sold=False).distinct()

		return render_to_response('marketplace/ajax_product_search.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')