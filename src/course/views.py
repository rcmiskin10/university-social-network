from django.shortcuts import render_to_response, RequestContext, Http404, render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.contrib import messages
from notifications.signals import notify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Course, StudentCourse, Syllabus, Assignment, CourseNote
from .forms import CourseForm, SyllabusForm, AssignmentForm, CourseNoteForm
from comments.forms import MyPostForm, ImageMyPostForm, LinkMyPostForm
from comments.models import MyPost
import datetime
from boto.s3.connection import S3Connection
from django.core.files import temp as tempfile 
import os
from django.utils import timezone
from django.conf import settings
import json
from docx2html import convert
from bs4 import BeautifulSoup
import re
import collections
from dateutil.parser import parse


def course_page(request, slug):
	if request.user.is_authenticated():
		course = Course.objects.get(slug=slug)
		print course.slug
		test = reverse("course_page", kwargs={"slug":course.slug })
		print test
		course_form = CourseForm(request.POST or None, request.FILES or None)
		add_note_form = CourseNoteForm(request.POST or None, request.FILES or None)
		image_mypost_form = ImageMyPostForm(request.POST or None , request.FILES or None, prefix='imagemypost')
		link_mypost_form = LinkMyPostForm(request.POST or None , prefix='linkmypost')

		path=request.get_full_path()       
		posts = MyPost.objects.filter(course=course).filter(parent=None) 
		notes = CourseNote.objects.filter(course=course).order_by("-timestamp")
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
				    text=mypost_text,
				    course=course,
				    parent=parent_mypost,
				    
				    )
				affected_users = new_comment.course.students.all()
			
				notify.send(target=course, sender=new_comment.user, recipient=None, action='commented on', affected_users=affected_users)
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

		

			
				
		
	 
		


				
		
		
		
		course = Course.objects.get(slug=slug)
		syllabus = Syllabus.objects.filter(course=course,user=request.user)
		
		assignment=Assignment.objects.filter(course=course, user=request.user).order_by('due_date')
		if assignment:
			today = datetime.datetime.now().date()
			date_list = []
			name_list = []
			id_list = []
			for item in assignment:
				if not datetime.datetime.strptime(item.due_date, '%Y-%m-%d').date() < today:
					date_list.append(datetime.datetime.strptime(item.due_date, '%Y-%m-%d').strftime('%b. %d, %Y'))
					name_list.append(item.name)
					id_list.append(item.id)
					g_all = zip(id_list, date_list, name_list )

				
					paginator = Paginator(g_all, 5) # Show 25 contacts per page


					page = request.GET.get('page')
					try:
					    g = paginator.page(page)
					except PageNotAnInteger:
					    # If page is not an integer, deliver first page.
					    g = paginator.page(1)
					except EmptyPage:
					    # If page is out of range (e.g. 9999), deliver last page of results.
					    g = paginator.page(paginator.num_pages)

		
		syllabus = Syllabus.objects.filter(course=course,user=request.user)
		SyllabusFormset = modelformset_factory(Syllabus, form=SyllabusForm, extra=1, max_num=1)
		formset_syl = SyllabusFormset(request.POST or None, request.FILES or None, queryset=syllabus)

		if Syllabus.objects.filter(course=course,user=request.user).exists():
			syllabus = Syllabus.objects.get(course=course,user=request.user)
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																										 
			
			assignment_form = AssignmentForm(request.POST or None)
			


		    																																																																										
		    


		

		return render_to_response("courses/course_page.html", locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def course_syllabus(request, slug):
	course = Course.objects.get(slug=slug)
	syllabus = Syllabus.objects.filter(course=course,user=request.user)
	SyllabusFormset = modelformset_factory(Syllabus, form=SyllabusForm, extra=1, max_num=1)
	formset_syl = SyllabusFormset(request.POST or None, request.FILES or None, queryset=syllabus)
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	
	print tempfile.gettempdir()
	if request.method == 'POST':
		if formset_syl.is_valid():
			for form in formset_syl:
				form1 = form.save(commit=False)

				form1.user = request.user
				form1.path = request.get_full_path()
				form1.course = course
				if '.docx' in str(form1.syllabus):
					form1.save()
				else:
					data = {}
					data['response'] = False
					new_data = json.dumps(data)
					return HttpResponse(new_data, content_type='application/json')
				AWS_KEY = #key
				AWS_SECRET = #secret
				aws_connection = S3Connection(AWS_KEY, AWS_SECRET)
				obj = Syllabus.objects.get(course=course,user=request.user)
				bucket_name = #bucket
				key = aws_connection.get_bucket(bucket_name).get_key('media/' + str(obj.syllabus))
				res = key.get_contents_to_filename(BASE_DIR +'/'+key.name)
				
				html = convert(BASE_DIR +'/'+key.name)
				obj.html = html
				obj.save()

				response_data = {}
			    
				response_data['response'] = True
				new_data = json.dumps(response_data)
			        
				return HttpResponse(new_data, content_type='application/json')
def student_course(request, slug):
	course = Course.objects.get(slug=slug)
	course_form = CourseForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            
            if not StudentCourse.objects.filter(course_id=course).filter(user=request.user).exists():
                if course_form.is_valid():
                    new_form = course_form.save(commit=False)
                    new_form.user = request.user
                    new_form.course_id = course
                    new_form.save()
                    
		response_data = {}

			


		new_data = json.dumps(response_data)

		return HttpResponse(new_data, content_type='application/json')

def profile_course_connect(request, slug):
	course = Course.objects.get(slug=slug)
	course_form = CourseForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
            
		if not StudentCourse.objects.filter(course_id=course).filter(user=request.user).exists():
			if course_form.is_valid():
				new_form = course_form.save(commit=False)
				new_form.user = request.user
				new_form.course_id = course
				new_form.save()
				messages.success(request,'You succesfully connected to a course, add another!', extra_tags='course')
				return HttpResponseRedirect('/profile_info/courses/')
		else:
			messages.error(request,'You are already connected, add another!', extra_tags='error')	
			return HttpResponseRedirect('/profile_info/courses/')
def course_link(request, slug):
	
	course = Course.objects.get(slug=slug)
	path = course.get_absolute_url()

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
			new_comment.course = course
			new_comment.parent = parent_mypost
			new_comment.save()
			affected_users = new_comment.course.students.all()
			
			notify.send(target=course, sender=new_comment.user, recipient=None, action='commented on', affected_users=affected_users)
		    
		        
		        
		    
		    
		     
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

def course_image(request, slug):

	course = Course.objects.get(slug=slug)
	path = reverse("course_page", kwargs={"slug":course.slug })
     
        
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
			new_comment.course = course
			new_comment.text = image_mypost_text
			new_comment.image = image_mypost_image
			new_comment.parent = parent_mypost
			new_comment.save()
			affected_users = new_comment.course.students.all()
			
			notify.send(target=course, sender=new_comment.user, recipient=None, action='commented on', affected_users=affected_users)
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

def course_assign(request, slug):
	course = Course.objects.get(slug=slug)
	
	syllabus = Syllabus.objects.get(course=course,user=request.user)
	assignment_form = AssignmentForm(request.POST or None)
	if request.method == 'POST':
		if assignment_form.is_valid():
			due_date = assignment_form.cleaned_data['due_date']
			test = parse(due_date + " 16").date()
			name = assignment_form.cleaned_data['name']

			new_assign = Assignment()
			new_assign.due_date = test.strftime('%Y-%m-%d')
			new_assign.name = name
			new_assign.user = request.user
			new_assign.course = course

			new_assign.save()

			response_data = {}
			response_data['result'] = 'Create post successful!'
			response_data['name'] = new_assign.name
			response_data['due_date'] = test.strftime('%b. %d, %Y')
			

			new_data = json.dumps(response_data)
			    
			return HttpResponse(new_data, content_type='application/json')

def delete_assign(request):
	
	
	assignment=Assignment.objects.filter(user=request.user)
	date_list = []
	name_list = []
	id_list = []
	for item in assignment:
		date_list.append(datetime.datetime.strptime(item.due_date, '%Y-%m-%d').strftime('%b. %d, %Y'))
		name_list.append(item.name)
		id_list.append(item.id)
		g = zip(id_list, date_list, name_list )
		
		if request.method =='POST':
			user =request.user
	        assign_id = request.POST.get('assign_id')
		    
		
		for n in g:
			if n[0] == int(request.POST.get('assign_id')):
				obj = Assignment.objects.get(id=n[0])
				print obj.id

		
				response_data = {}
				response_data['id'] = obj.id
				


				new_data = json.dumps(response_data)
				obj.delete()
				return HttpResponse(new_data, content_type='application/json')

def delete_course(request):
    if request.method =='POST':
        user =request.user
        course_id = request.POST['course_id']
        obj = StudentCourse.objects.get(id=course_id)
	response_data = {}
	response_data['id'] = obj.id



	new_data = json.dumps(response_data)
	obj.delete()
	return HttpResponse(new_data, content_type='application/json')

def add_note(request, slug):
    if request.method == 'POST':
		course = Course.objects.get(slug=slug)
		path = course.get_absolute_url()
		add_note_form = CourseNoteForm(request.POST or None, request.FILES or None)
        
		if add_note_form.is_valid():
            
			form1 = add_note_form.save(commit=False)
			form1.user = request.user
			form1.course = course
			form1.save()

			
		    
		     
			response_data = {}
			response_data['result'] = 'Create post successful!'
			response_data['text'] = form1.text
			response_data['first_name'] = form1.user.first_name
			response_data['last_name'] = form1.user.last_name


			response_data['created'] = timezone.localtime(form1.timestamp).strftime('%b. %d, %Y, %-I:%M %-P')


			for item in form1.user.userpicture_set.all():
				if item.image:
					response_data['image'] = 'Yes'
					response_data['image_url'] = item.image.url


			if not form1.user.userpicture_set.all():
				response_data['image'] = 'None'
                
			for item in request.user.userpicture_set.all():
				if item.image:
					response_data['request_image'] = 'Yes'
					response_data['request_image_url'] = item.image.url
			if not request.user.userpicture_set.all():
				response_data['request_image'] = 'None'
			response_data['id'] = form1.id
			response_data['response'] = True
			new_data = json.dumps(response_data)
			    
			return HttpResponse(new_data, content_type='application/json')
		else:
			data = {}
			data['response'] = False
			new_data = json.dumps(data)
			return HttpResponse(new_data, content_type='application/json')