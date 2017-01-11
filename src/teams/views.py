from django.shortcuts import render_to_response, RequestContext, Http404, render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notifications.signals import notify
import datetime
import json
from django.utils import timezone
from teams.models import Team, TeamMember
from teams.forms import TeamForm
from clubs.models import Club, ClubMember
from clubs.forms import ClubForm
from comments.models import MyPost
from comments.forms import MyPostForm, ReplyForm, ImageMyPostForm, LinkMyPostForm
from schedule.models import Schedule
from schedule.forms import ScheduleForm
from team_schedule.forms import TeamScheduleForm
from team_schedule.models import TeamSchedule

def team_page(request, id):
	if request.user.is_authenticated():
		team = Team.objects.get(id=id)
		print team.id
		path = request.get_full_path()
		print path
		today = datetime.datetime.now().date()
		schedule_all = TeamSchedule.objects.filter(team=team, user=request.user, duedate__gte=today ).order_by('duedate')
		paginator = Paginator(schedule_all, 5) # Show 25 contacts per page

		page = request.GET.get('page')
		try:
		    schedule = paginator.page(page)
		except PageNotAnInteger:
		    # If page is not an integer, deliver first page.
		    schedule = paginator.page(1)
		except EmptyPage:
		    # If page is out of range (e.g. 9999), deliver last page of results.
		    schedule = paginator.page(paginator.num_pages)
		team_schedule_form = TeamScheduleForm(request.POST or None, prefix='team_schedule')
		image_mypost_form = ImageMyPostForm(request.POST or None , request.FILES or None, prefix='imagemypost')
		link_mypost_form = LinkMyPostForm(request.POST or None , prefix='linkmypost')

		path=request.get_full_path()       
		posts = MyPost.objects.filter(team=team).filter(parent=None) 
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
				    team=team,
				    text=mypost_text,
				    parent=parent_mypost,
				    
				    )
				affected_users = new_comment.team.team_members.all()
			
				
				
				notify.send(target=team, sender=new_comment.user, recipient=None, action='commented on', affected_users=affected_users)
				print new_comment.parent
			


				response_data = {}
				response_data['result'] = 'Create post successful!'
				response_data['text'] = new_comment.text
				response_data['first_name'] = new_comment.user.first_name
				response_data['last_name'] = new_comment.user.last_name


				response_data['created'] = timezone.localtime(new_comment.timestamp).strftime('%b. %d, %Y, %-I:%M %-P')
				if new_comment.parent is not None:
					response_data['parent_id'] = new_comment.parent.id
				
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
				response_data['id'] = new_comment.id
				response_data['response'] = True
				new_data = json.dumps(response_data)
				    
				return HttpResponse(new_data, content_type='application/json')
			else:
				data = {}
				data['response'] = False
				new_data = json.dumps(data)
				return HttpResponse(new_data, content_type='application/json')
		return render_to_response("teams/team_page.html", locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def team_link(request, id):
	
	team = Team.objects.get(id=id)
	path = team.get_absolute_url()

	link_mypost_form = LinkMyPostForm(request.POST or None , prefix='linkmypost')
	if request.method == 'POST':

		if link_mypost_form.is_valid():
		    
			parent_id = request.POST.get('parent_id')
			parent_mypost = None
			if parent_id is not None:
				try:
					parent_mypost = MyPost.objects.get(id=parent_id)
				except:
					parent_mypost = None
			link_mypost_text = link_mypost_form.cleaned_data['mypost']
			link_mypost_link = link_mypost_form.cleaned_data['link']

			new_comment = MyPost()
			new_comment.text = link_mypost_text
			new_comment.links = str(link_mypost_link).replace("watch?v=", "v/")
			new_comment.user = request.user
			new_comment.team = team
			new_comment.parent = parent_mypost
			new_comment.save()
			affected_users = new_comment.team.team_members.all()
			
				
				
			notify.send(target=team, sender=new_comment.user, recipient=None, action='commented on', affected_users=affected_users)

		    
		    

			response_data = {}
			response_data['result'] = 'Create post successful!'
			response_data['text'] = new_comment.text
			response_data['first_name'] = new_comment.user.first_name
			response_data['last_name'] = new_comment.user.last_name
			response_data['link'] = new_comment.links
			response_data['input_link'] = link_mypost_form.cleaned_data['link']

			response_data['created'] = timezone.localtime(new_comment.timestamp).strftime('%b. %d, %Y, %-I:%M %-P')
			if new_comment.parent is not None:
				response_data['parent_id'] = new_comment.parent.id
		    
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
			response_data['id'] = new_comment.id
			response_data['response'] = True
			new_data = json.dumps(response_data)
			    
			return HttpResponse(new_data, content_type='application/json')
		else:
			data = {}
			data['response'] = False
			new_data = json.dumps(data)
			return HttpResponse(new_data, content_type='application/json')

def team_image(request, id):

	team = Team.objects.get(id=id)
	path = reverse("team_page", kwargs={"id":team.id })
     
        
	image_mypost_form = ImageMyPostForm(request.POST or None , request.FILES or None, prefix='imagemypost')
	if request.method == 'POST':
		if image_mypost_form.is_valid():
			parent_id = request.POST.get('parent_id')
			parent_mypost = None
			if parent_id is not None:
				try:
					parent_mypost = MyPost.objects.get(id=parent_id)
				except:
					parent_mypost = None
			image_mypost_text = image_mypost_form.cleaned_data['mypost']
			image_mypost_image = image_mypost_form.cleaned_data['image']

			new_comment = MyPost()
			new_comment.user = request.user
			new_comment.team = team
			new_comment.text = image_mypost_text
			new_comment.image = image_mypost_image
			new_comment.parent = parent_mypost
			new_comment.save()
			affected_users = new_comment.team.team_members.all()
			
				
				
			notify.send(target=team, sender=new_comment.user, recipient=None, action='commented on', affected_users=affected_users)
			image_post = new_comment.image.url
			    

			 
			response_data = {}
			response_data['result'] = 'Create post successful!'
			response_data['text'] = new_comment.text
			response_data['first_name'] = new_comment.user.first_name
			response_data['last_name'] = new_comment.user.last_name

			response_data['created'] = timezone.localtime(new_comment.timestamp).strftime('%b. %d, %Y, %-I:%M %-P')
			if new_comment.parent is not None:
				response_data['parent_id'] = new_comment.parent.id

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

			response_data['id'] = new_comment.id
			response_data['image_post'] = image_post
			response_data['response'] = True
			new_data = json.dumps(response_data)
			    
			return HttpResponse(new_data, content_type='application/json')
		else:
			data = {}
			data['response'] = False
			new_data = json.dumps(data)
			return HttpResponse(new_data, content_type='application/json')
def team_member(request, id):
	team = Team.objects.get(id=id)
	team_form = TeamForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            
            if not TeamMember.objects.filter(team_id=team).filter(user=request.user).exists():
                if team_form.is_valid():
                    new_form = team_form.save(commit=False)
                    new_form.user = request.user
                    new_form.team_id = team
                    new_form.save()
                    
		response_data = {}




		new_data = json.dumps(response_data)

		return HttpResponse(new_data, content_type='application/json')

def team_schedule(request, id):
	team = Team.objects.get(id=id)
	path = reverse("team_page", kwargs={"id":team.id})
	team_schedule_form = TeamScheduleForm(request.POST or None, prefix='schedule')

	if request.method == 'POST':
		if team_schedule_form.is_valid():
		    schedule_text = team_schedule_form.cleaned_data['text']
		    schedule_duedate = team_schedule_form.cleaned_data['duedate']
		    
		    new_form = TeamSchedule()
		    new_form.user = request.user
		    new_form.team = team
		    new_form.text = schedule_text
		    new_form.duedate = schedule_duedate
		    new_form.save()
		    

		    response_data = {}
		    					

		    response_data['response'] = True

		    new_data = json.dumps(response_data)
		    
		    return HttpResponse(new_data, content_type='application/json')
		else:
		    data = {}
		    data['response'] = False
		    new_data = json.dumps(data)
		    return HttpResponse(new_data, content_type='application/json')
def delete_team_sched(request):
	
		
		
	if request.method =='POST':
		user =request.user
        sched_id = request.POST.get('sched_id')
	    
	
		
	
	obj = TeamSchedule.objects.get(id=sched_id)
	print obj.id


	response_data = {}
	response_data['id'] = obj.id
	


	new_data = json.dumps(response_data)
	obj.delete()
	return HttpResponse(new_data, content_type='application/json')

def delete_team(request):
    if request.method =='POST':
        user =request.user
        team_id = request.POST['team_id']
        obj = TeamMember.objects.get(id=team_id)
	response_data = {}
	response_data['id'] = obj.id



	new_data = json.dumps(response_data)
	obj.delete()
	return HttpResponse(new_data, content_type='application/json')