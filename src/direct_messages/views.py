from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect, get_object_or_404
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import DirectMessage
from accounts.models import MyUser
from .forms import ComposeForm, ProductComposeForm, ReplyForm
from course.models import Syllabus, Assignment
from schedule.models import Schedule
from team_schedule.models import TeamSchedule
from frat_schedule.models import FratSchedule
from marketplace.models import Product
from main_schedule.models import MainSchedule
from main_schedule.forms import MainScheduleForm

def view_direct_message(request, dm_id):
	if request.user.is_authenticated():
    
		message = get_object_or_404(DirectMessage, id=dm_id)
	    
		
	    
		if not message.read:
			message.read = True
			message.read_at = datetime.datetime.now()
			message.save()
		else:
			message = get_object_or_404(DirectMessage, id=dm_id)
	        
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
	        
		return render_to_response('directmessages/view.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/') 
        
    
def view_sent_message(request, dm_id):
	if request.user.is_authenticated():
		message = get_object_or_404(DirectMessage, id=dm_id)
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
		

		  
	          
	        
		return render_to_response('directmessages/view_sent.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')
def product_compose(request,id):
	if request.user.is_authenticated():
		product = Product.objects.get(id=id)
		form = ProductComposeForm(request.POST or None)
	    
		if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			send_message.receiver = product.owner
			send_message.sent = datetime.datetime.now()
			send_message.save()
			messages.success(request, "Message sent!", extra_tags='product')
			return HttpResponseRedirect(reverse('inbox'))
			
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
	          
	        
		return render_to_response('directmessages/product_compose.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')  
def user_compose(request,id):
	if request.user.is_authenticated():
		user = MyUser.objects.get(id=id)
		user_form = ComposeForm(request.POST or None)

		if user_form.is_valid():
			send_message = user_form.save(commit=False)
			send_message.sender = request.user
			send_message.receiver = user
			send_message.sent = datetime.datetime.now()
			send_message.save()
			messages.success(request, "Message sent!", extra_tags='user')
			return HttpResponseRedirect(reverse('inbox'))
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
	        
		return render_to_response('directmessages/user_compose.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')	    
def reply(request,dm_id):
	if request.user.is_authenticated():
		parent_id=dm_id
	    
		parent = get_object_or_404(DirectMessage, id=parent_id)
	    
		form = ReplyForm(request.POST or None)
	    
		if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			send_message.receiver = parent.sender
			send_message.subject = "Re: " + parent.subject
			send_message.sent = datetime.datetime.now()
			send_message.parent = parent
			send_message.save()
			parent.replied = True
			parent.save()
			messages.success(request, "Reply sent!", extra_tags='reply')
			return HttpResponseRedirect('/messages/inbox/')
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
	        
	        
		return render_to_response('directmessages/reply.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')    

def inbox(request):
	if request.user.is_authenticated():
		user = request.user
		messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
		direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
		request.session['num_of_messages'] = direct_messages
		
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
	        
	        
	        
		return render_to_response('directmessages/inbox.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')    
def sent(request):
	if request.user.is_authenticated():
		messages_sent = DirectMessage.objects.filter(sender=request.user)

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
	        
	        
		return render_to_response('directmessages/sent.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')