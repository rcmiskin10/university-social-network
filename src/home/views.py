from django.contrib.auth import authenticate, login, logout
from itertools import tee, islice, chain, izip
from django import forms
from django.contrib.sites.models import Site
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render_to_response, RequestContext, Http404, HttpResponseRedirect, render, HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
import hashlib, datetime, random
from django.utils import timezone
from docx2html import convert
from dateutil.parser import parse
from django.db.models import Q
import json

import collections
from accounts.forms import RegistrationForm
from accounts.models import MyUser, UserProfile
from clubs.models import Club, ClubMember
from clubs.forms import ClubForm, AddClubForm
from frats.models import Frat, Member
from frats.forms import FratForm, AddFratForm
from teams.models import Team, TeamMember
from teams.forms import TeamForm, AddTeamForm
from profiles.models import ProfileInfo, UserPicture
from course.models import Course, Syllabus, Assignment, StudentCourse
from comments.models import MyPost
from comments.forms import MyPostForm, LinkMyPostForm, ImageMyPostForm, EventForm
from .forms import LoginForm
from schedule.models import Schedule
from schedule.forms import ScheduleForm
from team_schedule.models import TeamSchedule
from team_schedule.forms import TeamScheduleForm
from frat_schedule.models import FratSchedule
from frat_schedule.forms import FratScheduleForm
from main_schedule.models import MainSchedule
from main_schedule.forms import MainScheduleForm


def terms(request):

    return render_to_response('terms.html', locals(), context_instance=RequestContext(request))

def privacy(request):

    return render_to_response('privacy.html', locals(), context_instance=RequestContext(request))

def home(request):
    if not request.user.is_authenticated():
        login_form = LoginForm(request.POST or None)
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            site = request.META['HTTP_HOST']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password2']
            
            new_user = MyUser()
            new_user.email = email
            new_user.username = username
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.set_password(password)
            new_user.save()
            
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
            #Get user by username
            user=MyUser.objects.get(email=email)
        
            # Create and save user profile                                                                                                                                  
            new_profile = UserProfile(user=user, activation_key=activation_key, 
                key_expires=key_expires)
            new_profile.save()
            email = form.cleaned_data['email']
            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://%s/accounts/confirm/%s" % (email, site, activation_key)

            send_mail(email_subject, email_body, 'studentgroundsinc@gmail.com',
                [email], fail_silently=False)
            
            return HttpResponseRedirect('/registration_complete/')
            
        
        return render_to_response('home.html', locals(), context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/home/')


def registration_complete(request):
    
    return render_to_response('register_complete.html', locals(), context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/home/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('user_profile/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    login_form = LoginForm(request.POST or None)
    return render_to_response('user_profile/confirm.html', locals(), context_instance=RequestContext(request))
    

def main(request):
    if request.user.is_authenticated():
        schedule_form = MainScheduleForm(request.POST or None, prefix='schedule')
        event_form = EventForm(request.POST or None, prefix='imagemypost')
        image_mypost_form = ImageMyPostForm(request.POST or None , request.FILES or None, prefix='imagemypost')
        link_mypost_form = LinkMyPostForm(request.POST or None , prefix='linkmypost')
        path=request.get_full_path()       
        posts = MyPost.objects.filter(main='main').filter(parent=None) 
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
                    main = 'main',
                    text=mypost_text,
                    parent=parent_mypost,
                    
                    )
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

        courses = Course.objects.all()
        club_form = ClubForm(request.POST or None, request.FILES or None)
        add_frat_form = AddFratForm(request.POST or None, request.FILES or None)
        add_team_form = AddTeamForm(request.POST or None, request.FILES or None)
        add_club_form = AddClubForm(request.POST or None, request.FILES or None)
        schedule = Schedule.objects.filter(user=request.user)
        studentcourses = StudentCourse.objects.filter(user=request.user)
        my_clubs = ClubMember.objects.filter(user=request.user)
        my_teams = TeamMember.objects.filter(user=request.user)
        my_frats = Member.objects.filter(user=request.user)
        courses = Course.objects.all()
        clubs = Club.objects.all()
        teams = Team.objects.all()
        frats = Frat.objects.all()
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
               
        return render_to_response('main.html', locals(), context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

 
def main_link(request):
    
    
    path = '/home/'

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
            new_comment.main = 'main'
            new_comment.parent = parent_mypost
            new_comment.save()

            
            
             
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

def main_image(request):

   
    
    path = '/home/'
        
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
            new_comment.main = 'main'
            new_comment.text = image_mypost_text
            new_comment.image = image_mypost_image
            new_comment.parent = parent_mypost
            new_comment.save()

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

def main_event(request):

    
        
    event_form = EventForm(request.POST or None, prefix='imagemypost')
    if request.method == 'POST':
        if event_form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent_mypost = None
            if parent_id is not None:
                try:
                    parent_mypost = MyPost.objects.get(id=parent_id)
                except:
                    parent_mypost = None
            mypost_text = event_form.cleaned_data['mypost']
            event = event_form.cleaned_data['event']
            start_time = event_form.cleaned_data['start_time']
            end_time = event_form.cleaned_data['end_time']
            date = event_form.cleaned_data['date']

            new_comment = MyPost()
            new_comment.user = request.user
            new_comment.main = 'main'
            new_comment.text = mypost_text
            new_comment.event = event
            new_comment.start_time = start_time
            new_comment.end_time = end_time
            new_comment.date = date
            new_comment.parent = parent_mypost
            new_comment.save()

           
                
            

             
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
            response_data['event'] = new_comment.event
            response_data['start_time'] = new_comment.start_time
            response_data['end_time'] = new_comment.end_time
            response_data['date'] = new_comment.date.strftime('%b. %d, %Y')

            response_data['response'] = True
            new_data = json.dumps(response_data)
                
            return HttpResponse(new_data, content_type='application/json')

        else:
            data = {}
            data['response'] = False
            new_data = json.dumps(data)
            return HttpResponse(new_data, content_type='application/json')




def connect(request):
    if request.user.is_authenticated():
        schedule_form = MainScheduleForm(request.POST or None, prefix='schedule')
        add_frat_form = AddFratForm(request.POST or None, request.FILES or None)
        add_team_form = AddTeamForm(request.POST or None, request.FILES or None)
        add_club_form = AddClubForm(request.POST or None, request.FILES or None)
        schedule = Schedule.objects.filter(user=request.user)
        studentcourses = StudentCourse.objects.filter(user=request.user)
        my_clubs = ClubMember.objects.filter(user=request.user)
        my_teams = TeamMember.objects.filter(user=request.user)
        my_frats = Member.objects.filter(user=request.user)
        courses_all = Course.objects.all().order_by("course_name")
        paginator = Paginator(courses_all, 25) # Show 25 contacts per page


        page = request.GET.get('course')
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            courses = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            courses = paginator.page(paginator.num_pages)
        clubs = Club.objects.all().order_by("club_name")
        teams = Team.objects.all().order_by("name")
        frats = Frat.objects.all().order_by("name")
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
        
        
            
        return render_to_response('home/connect.html', locals(), context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')
def club_connect(request):
    club_id = request.POST.get('club_id')
    club = Club.objects.get(id=club_id)
    club_form = ClubForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        
        if not ClubMember.objects.filter(club_id=club).filter(user=request.user).exists():
            if club_form.is_valid():
                new_form = club_form.save(commit=False)
                new_form.user = request.user
                new_form.club_id = club
                new_form.save()
        
                      
                response_data = {}

                response_data['id'] = new_form.club_id.id


                new_data = json.dumps(response_data)

                return HttpResponse(new_data, content_type='application/json')


def team_connect(request):
    team_id = request.POST.get('team_id')
    team = Team.objects.get(id=team_id)
    team_form = TeamForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        
        if not TeamMember.objects.filter(team_id=team).filter(user=request.user).exists():
            if team_form.is_valid():
                new_form = team_form.save(commit=False)
                new_form.user = request.user
                new_form.team_id = team
                new_form.save()
        
                      
                response_data = {}

                response_data['id'] = new_form.team_id.id


                new_data = json.dumps(response_data)

                return HttpResponse(new_data, content_type='application/json')

def frat_connect(request):
    frat_id = request.POST.get('frat_id')
    frat = Frat.objects.get(id=frat_id)
    frat_form = FratForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        
        if not Member.objects.filter(frat_id=frat).filter(user=request.user).exists():
            if frat_form.is_valid():
                new_form = frat_form.save(commit=False)
                new_form.user = request.user
                new_form.frat_id = frat
                new_form.save()
        
                      
                response_data = {}

                response_data['id'] = new_form.frat_id.id


                new_data = json.dumps(response_data)

                return HttpResponse(new_data, content_type='application/json')



def connect_search(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            search_text = request.POST['search_text']
        
        courses = Course.objects.filter(course_name__icontains=search_text).distinct()
        clubs = Club.objects.filter(club_name__icontains=search_text).distinct()
        teams = Team.objects.filter(name__icontains=search_text).distinct()
        frats = Frat.objects.filter(name__icontains=search_text).distinct()

        return render_to_response('home/ajax_connect_search.html', locals(), context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')
def delete(request):
    assignment=Assignment.objects.filter(user=request.user).order_by('due_date')
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


def auth_login(request):
    login_form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                user = request.user
                if ProfileInfo.objects.filter(user=user).exists():
                    return HttpResponseRedirect('/home/')
                else:
                    return HttpResponseRedirect('/profile_info/')
        else:
            messages.error(request, 'Login email or password was incorrect. Please try again.', extra_tags='login_failed')
            return HttpResponseRedirect('/login/')

def error_login(request):          
    
    return render_to_response('login.html', locals(), context_instance=RequestContext(request))

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def add_club(request):
    users = MyUser.objects.filter(is_active=True)
    clubs = Club.objects.all()
    add_club_form = AddClubForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        
        if add_club_form.is_valid():
            form3 = add_club_form.save(commit=False)
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

def add_team(request):
    users = MyUser.objects.filter(is_active=True)
    teams = Team.objects.all()
    add_team_form = AddTeamForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        
        if add_team_form.is_valid():
            form3 = add_team_form.save(commit=False)
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

def add_frat(request):
    users = MyUser.objects.filter(is_active=True)
    frats = Frat.objects.all()
    add_frat_form = AddFratForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        
        if add_frat_form.is_valid():
            form3 = add_frat_form.save(commit=False)
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

def search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        clubs = Club.objects.filter(club_name__icontains = q )[:20]
        teams = Team.objects.filter(name__icontains = q )[:20]
        frats = Frat.objects.filter(name__icontains = q )[:20]
        courses = Course.objects.filter(course_name__icontains = q )[:20]
        
        results = []
        for club in clubs:
            club_json = {}
            club_json['label'] = club.club_name
            club_json['url'] = club.get_absolute_url()
            
            results.append(club_json)
        for team in teams:
            team_json = {}
            team_json['label'] = team.name
            team_json['url'] = team.get_absolute_url()
            
            results.append(team_json)
        for frat in frats:
            frat_json = {}
            frat_json['label'] = frat.name
            frat_json['url'] = frat.get_absolute_url()
            
            results.append(frat_json)
        for course in courses:
            course_json = {}
            course_json['label'] = course.course_name
            course_json['url'] = course.get_absolute_url()
            results.append(course_json)
        


        data = json.dumps(results)

    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def delete_post(request):
    if request.method =='POST':
        user =request.user
        post_id = request.POST['post_id']
        obj = MyPost.objects.get(id=post_id)
    response_data = {}
    response_data['id'] = obj.id



    new_data = json.dumps(response_data)
    obj.delete()
    return HttpResponse(new_data, content_type='application/json')


def main_search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        for term in q.split(' '):
                users = MyUser.objects.filter(is_active=True).filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))[:20]
        results = []
        for user in users:
                user_json = {}
                user_json['label'] = user.first_name + " " + user.last_name
                user_json['url'] = user.get_absolute_url()
                results.append(user_json)

        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


