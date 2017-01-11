from django.shortcuts import render_to_response, RequestContext, Http404, render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import json
from django.utils import timezone
from notifications.signals import notify
from frats.models import Frat, Member
from frats.forms import FratForm
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
from frat_schedule.forms import FratScheduleForm
from frat_schedule.models import FratSchedule

def frat_page(request, id):
	if request.user.is_authenticated():
		frat = Frat.objects.get(id=id)
		print frat.id
		path = request.get_full_path()
		print path
		today = datetime.datetime.now().date()
		schedule_all = FratSchedule.objects.filter(frat=frat, user=request.user, duedate__gte=today).order_by('duedate')

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

		frat_schedule_form = FratScheduleForm(request.POST or None, prefix='frat_schedule')
		image_mypost_form = ImageMyPostForm(request.POST or None , request.FILES or None, prefix='imagemypost')
		link_mypost_form = LinkMyPostForm(request.POST or None , prefix='linkmypost')

		path=request.get_full_path()       
		posts = MyPost.objects.filter(frat=frat).filter(parent=None) 
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
				    frat=frat,
				    text=mypost_text,
				    parent=parent_mypost,
				    
				    )
				affected_users = new_comment.frat.members.all()
			
				
				notify.send(target=frat, sender=new_comment.user, recipient=None, action='commented on', affected_users=affected_users)
				


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
		return render_to_response("frats/frat_page.html", locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def frat_link(request, id):
	
	frat = Frat.objects.get(id=id)
	path = frat.get_absolute_url()

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
			new_comment.frat = frat
			new_comment.parent = parent_mypost
			new_comment.save()
			affected_users = new_comment.frat.members.all()
			
				
			notify.send(target=frat, sender=new_comment.user, recipient=None, action='commented on', affected_users=affected_users)


		     
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
			response_data['response'] = True
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

			new_data = json.dumps(response_data)
			    
			return HttpResponse(new_data, content_type='application/json')
		else:
			data = {}
			data['response'] = False
			new_data = json.dumps(data)
			return HttpResponse(new_data, content_type='application/json')

def frat_image(request, id):

	frat = Frat.objects.get(id=id)
	path = reverse("frat_page", kwargs={"id":frat.id })
     
        
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
			new_comment.frat = frat
			new_comment.text = image_mypost_text
			new_comment.image = image_mypost_image
			new_comment.parent = parent_mypost
			new_comment.save()
			affected_users = new_comment.frat.members.all()
			
				
			notify.send(target=frat, sender=new_comment.user, recipient=None, action='commented on', affected_users=affected_users)
			image_post = new_comment.image.url
			    
			

			 
			response_data = {}
			response_data['result'] = 'Create post successful!'
			response_data['text'] = new_comment.text
			response_data['first_name'] = new_comment.user.first_name
			response_data['last_name'] = new_comment.user.last_name
			response_data['response'] = True
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

			new_data = json.dumps(response_data)
			    
			return HttpResponse(new_data, content_type='application/json')
		else:
			data = {}
			
			data['response'] = False
			new_data = json.dumps(data)
			return HttpResponse(new_data, content_type='application/json')
def frat_member(request, id):
	frat = Frat.objects.get(id=id)
	frat_form = FratForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            
            if not Member.objects.filter(frat_id=frat).filter(user=request.user).exists():
                if frat_form.is_valid():
                    new_form = frat_form.save(commit=False)
                    new_form.user = request.user
                    new_form.frat_id = frat
                    new_form.save()
                    
		response_data = {}




		new_data = json.dumps(response_data)

		return HttpResponse(new_data, content_type='application/json')

def frat_schedule(request, id):
	frat = Frat.objects.get(id=id)
	path = reverse("team_page", kwargs={"id":frat.id})
	frat_schedule_form = FratScheduleForm(request.POST or None, prefix='schedule')

	if request.method == 'POST':
		if frat_schedule_form.is_valid():
		    schedule_text = frat_schedule_form.cleaned_data['text']
		    schedule_duedate = frat_schedule_form.cleaned_data['duedate']
		    
		    new_form = FratSchedule()
		    new_form.user = request.user
		    new_form.frat = frat
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
def delete_frat_sched(request):
	
		
		
	if request.method =='POST':
		user =request.user
        sched_id = request.POST.get('sched_id')
	    
	
		
	
	obj = FratSchedule.objects.get(id=sched_id)
	print obj.id


	response_data = {}
	response_data['id'] = obj.id
	


	new_data = json.dumps(response_data)
	obj.delete()
	return HttpResponse(new_data, content_type='application/json')

def delete_frat(request):
    if request.method =='POST':
        user =request.user
        frat_id = request.POST['frat_id']
        obj = Member.objects.get(id=frat_id)
	response_data = {}
	response_data['id'] = obj.id



	new_data = json.dumps(response_data)
	obj.delete()
	return HttpResponse(new_data, content_type='application/json')
