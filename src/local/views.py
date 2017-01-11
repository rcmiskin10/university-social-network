from django.shortcuts import render
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import geopy
from geopy.distance import vincenty
import datetime
import urllib2
import json

from django.utils import timezone
from django.core.context_processors import csrf
from .models import PlaceCategory, Place
from schedule.models import Schedule
from schedule.forms import ScheduleForm
from team_schedule.models import TeamSchedule
from team_schedule.forms import TeamScheduleForm
from frat_schedule.models import FratSchedule
from frat_schedule.forms import FratScheduleForm
from comments.models import MyPost
from comments.forms import MyPostForm
from accounts.models import MyUser, UserProfile
from clubs.models import Club, ClubMember
from clubs.forms import ClubForm, AddClubForm
from frats.models import Frat, Member
from frats.forms import FratForm
from teams.models import Team, TeamMember
from teams.forms import TeamForm
from profiles.models import ProfileInfo
from course.models import Course, Syllabus, Assignment, StudentCourse
from main_schedule.models import MainSchedule
from main_schedule.forms import MainScheduleForm



def local(request):
	
	if request.user.is_authenticated():	
		places_all = Place.objects.all().order_by("-rating")
		
		delivery = Place.objects.filter(delivery=True)

		paginator = Paginator(places_all, 10) # Show 25 contacts per page


		page = request.GET.get('schedule')
		try:
			places = paginator.page(page)
		except PageNotAnInteger:
	        # If page is not an integer, deliver first page.
			places = paginator.page(1)
		except EmptyPage:
	        # If page is out of range (e.g. 9999), deliver last page of results.
			places = paginator.page(paginator.num_pages)

		club_form = ClubForm(request.POST or None, request.FILES or None)
		add_club_form = AddClubForm(request.POST or None, request.FILES or None)
		schedule = Schedule.objects.filter(user=request.user)
		studentcourses = StudentCourse.objects.filter(user=request.user)
		my_clubs = ClubMember.objects.filter(user=request.user)
		my_teams = TeamMember.objects.filter(user=request.user)
		my_frats = Member.objects.filter(user=request.user)

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

		
		
		


		return render_to_response('local/local.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def local_search(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			search_text = request.POST['search_text']
		
		
		category = PlaceCategory.objects.filter(name__icontains=search_text)
		category_places = Place.objects.filter(category__icontains=category).distinct()
		places = Place.objects.filter(name__icontains=search_text).distinct()

		return render_to_response('local/ajax_local_search.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def local_page(request, id):
	if request.user.is_authenticated():
		place = Place.objects.get(id=id)
		path=request.get_full_path()
		      
		posts = MyPost.objects.filter(place=place).filter(parent=None) 
		mypost_form = MyPostForm(request.POST or None , prefix='mypost')

		if request.method == 'POST':
			if mypost_form.is_valid():
				created = mypost_form.cleaned_data.get('timestamp')
				parent_id = request.POST.get('parent_id')

				parent_mypost = None
				if parent_id is not None:
					try:
						parent_mypost = MyPost.objects.get(id=parent_id)
					except:
						parent_mypost = None
				mypost_text = mypost_form.cleaned_data['mypost']
				new_comment = MyPost.objects.create_mypost(
					user=request.user,
					path=request.get_full_path(),
					place=place,
					text=mypost_text,
					parent=parent_mypost,

				    )
				


				response_data = {}
				response_data['result'] = 'Create post successful!'
				response_data['text'] = new_comment.text
				response_data['first_name'] = new_comment.user.first_name
				response_data['last_name'] = new_comment.user.last_name

				for item in new_comment.user.userpicture_set.all():
					if item.image:
						response_data['image'] = 'Yes'
						response_data['image_url'] = item.image.url


				if not new_comment.user.userpicture_set.all():
					response_data['image'] = 'None'

				for item in request.user.userpicture_set.all():
					if item.image:
						response_data['request_image'] = 'Yes'
						response_data['request_image_url'] = item.image.url


				if not request.user.userpicture_set.all():
					response_data['request_image'] = 'None'

				response_data['created'] = timezone.localtime(new_comment.timestamp).strftime('%b. %d, %Y, %-I:%M %-P')
				if new_comment.parent is not None:
					response_data['parent_id'] = new_comment.parent.id
				response_data['response'] = True
				
				response_data['id'] = new_comment.id
				
				new_data = json.dumps(response_data)
				    
				return HttpResponse(new_data, content_type='application/json')
			else:
				data = {}
				data['response'] = False
				new_data = json.dumps(data)
				return HttpResponse(new_data, content_type='application/json')

		place = Place.objects.get(id=id)
		brandeis = (42.366284,-71.258734)
		end = ( place.latitude, place.longitude )
		distance = vincenty(brandeis, end).miles
		miles = round(distance, 2)
		add_club_form = AddClubForm(request.POST or None, request.FILES or None)
		schedule = Schedule.objects.filter(user=request.user)
		studentcourses = StudentCourse.objects.filter(user=request.user)
		my_clubs = ClubMember.objects.filter(user=request.user)
		my_teams = TeamMember.objects.filter(user=request.user)
		my_frats = Member.objects.filter(user=request.user)

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


		
		return render_to_response('local/local_page.html', locals(), context_instance=RequestContext(request))

	else:
		return HttpResponseRedirect('/login/')