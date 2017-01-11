from django.shortcuts import get_object_or_404, render_to_response, RequestContext, Http404, HttpResponse, HttpResponseRedirect, render
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from django.forms.models import modelformset_factory
from django.contrib import messages
from .models import ProfileInfo, UserPicture
from .forms import ProfileInfoForm, UserPictureForm
from clubs.models import Club, ClubMember
from clubs.forms import ClubForm, AddClubForm
from frats.models import Frat, Member
from frats.forms import FratForm
from teams.models import Team, TeamMember
from teams.forms import TeamForm
from profiles.models import ProfileInfo, UserPicture
from course.models import Course, Syllabus, Assignment, StudentCourse
from course.forms import CourseForm
from comments.models import MyPost
from comments.forms import MyPostForm, LinkMyPostForm, ImageMyPostForm, EventForm
from notifications.signals import notify
from schedule.models import Schedule
from schedule.forms import ScheduleForm
from team_schedule.models import TeamSchedule
from team_schedule.forms import TeamScheduleForm
from frat_schedule.models import FratSchedule
from frat_schedule.forms import FratScheduleForm
from accounts.models import MyUser
from comments.models import MyPost
from comments.forms import MyPostForm, ReplyForm, ImageMyPostForm, LinkMyPostForm
from .models import Post, Bio, Work, Interest
from .forms import PostForm, BioForm, WorkForm, InterestForm
from main_schedule.models import MainSchedule
from main_schedule.forms import MainScheduleForm
import datetime

def first_login(request):
    user = request.user
    info = ProfileInfo.objects.filter(user=user)
    ProfileInfoFormset = modelformset_factory(ProfileInfo, form=ProfileInfoForm, extra=1, max_num=1)
    formset_info = ProfileInfoFormset(request.POST or None, request.FILES or None, queryset=info)
    
    return render_to_response('profiles/first_login.html', locals(), context_instance=RequestContext(request))

def profile_info(request):
    if request.method == 'POST':
        user = request.user
        info = ProfileInfo.objects.filter(user=user)
        ProfileInfoFormset = modelformset_factory(ProfileInfo, form=ProfileInfoForm, extra=1, max_num=1)
        formset_info = ProfileInfoFormset(request.POST or None, request.FILES or None, queryset=info)
        
        if formset_info.is_valid():
            for form in formset_info:
                form1 = form.save(commit=False)
                form1.user = request.user
                form1.save()
        else:
            messages.error(request, 'Profile did not save. Please try again.', extra_tags='profile_failed')
        return HttpResponseRedirect('/profile_info/courses/')

def profile_courses(request):
    course_form = CourseForm(request.POST or None, request.FILES or None)
    return render_to_response('profiles/update_courses.html', locals(), context_instance=RequestContext(request))
def course_search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        
        courses = Course.objects.filter(course_name__icontains = q )[:20]
        
        results = []
        
        for course in courses:
            course_json = {}
            course_json['label'] = course.course_name + "-" + str(course.course_num)
            course_json['url'] = course.get_absolute_url()
            course_json['id'] = course.course_code
            results.append(course_json)
        


        data = json.dumps(results)

    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def edit_profile_image(request):
    user = request.user
    picture = UserPicture.objects.filter(user=user)
    UserPictureFormset = modelformset_factory(UserPicture, form=UserPictureForm, extra=1, max_num=1)
    formset_pic = UserPictureFormset(request.POST or None, request.FILES or None, queryset=picture)
    if request.method == 'POST':
        
        
        if formset_pic.is_valid():
            for form in formset_pic:
                form3 = form.save(commit=False)
                form3.user = request.user
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
def profile_image(request):
    user = request.user
    picture = UserPicture.objects.filter(user=user)
    UserPictureFormset = modelformset_factory(UserPicture, form=UserPictureForm, extra=1, max_num=1)
    formset_pic = UserPictureFormset(request.POST or None, request.FILES or None, queryset=picture)
    if request.method == 'POST':
        
        
        if formset_pic.is_valid():
            for form in formset_pic:
                form3 = form.save(commit=False)
                form3.user = request.user
                form3.save()
        else:
            messages.error(request, 'Image did not save. Please try again.')
        return HttpResponseRedirect('/home/')
    
    return render_to_response('profiles/update_image.html', locals(), context_instance=RequestContext(request))

def edit_profile_info(request):
    if request.method == 'POST':
        user = request.user
        info = ProfileInfo.objects.filter(user=user)
        ProfileInfoFormset = modelformset_factory(ProfileInfo, form=ProfileInfoForm, extra=1, max_num=1)
        formset_info = ProfileInfoFormset(request.POST or None, request.FILES or None, queryset=info)
        
        if formset_info.is_valid():
            for form in formset_info:
                form1 = form.save(commit=False)
                form1.user = request.user
                form1.save()
                
                response_data = {}
                
                response_data['id'] = form1.id
                response_data['response'] = True
                new_data = json.dumps(response_data)
                    
                return HttpResponse(new_data, content_type='application/json')

        else:
            data = {}
            data['response'] = False
            new_data = json.dumps(data)
            return HttpResponse(new_data, content_type='application/json') 


def bio(request):
    if request.method == 'POST':
        user = request.user
        bio = Bio.objects.filter(user=user)
        BioFormset = modelformset_factory(Bio, form=BioForm, extra=1, max_num=1)
        formset_bio = BioFormset(request.POST or None, request.FILES or None, queryset=bio)
        
        if formset_bio.is_valid():
            for form in formset_bio:
                form1 = form.save(commit=False)
                form1.user = request.user
                form1.save()
                response_data = {}
                response_data['text'] = form1.bio
                response_data['response'] = True
                new_data = json.dumps(response_data)
                    
                return HttpResponse(new_data, content_type='application/json')

        else:
            data = {}
            data['response'] = False
            new_data = json.dumps(data)
            return HttpResponse(new_data, content_type='application/json') 

def work(request):
    if request.method == 'POST':
        user = request.user
        work = Work.objects.filter(user=user)
        WorkFormset = modelformset_factory(Work, form=WorkForm, extra=1, max_num=1)
        formset_work = WorkFormset(request.POST or None, request.FILES or None, queryset=work)
        
        if formset_work.is_valid():
            for form in formset_work:
                form1 = form.save(commit=False)
                form1.user = request.user
                form1.save()
                response_data = {}
                
                response_data['id'] = form1.id
                response_data['response'] = True
                new_data = json.dumps(response_data)
                    
                return HttpResponse(new_data, content_type='application/json')
        else:
            data = {}
            data['response'] = False
            new_data = json.dumps(data)
            return HttpResponse(new_data, content_type='application/json')

def add_work(request):
    if request.method == 'POST':
        
        add_work_form = WorkForm(request.POST or None, request.FILES or None)
        
        if add_work_form.is_valid():
            
            form1 = add_work_form.save(commit=False)
            form1.user = request.user
            form1.save()
            response_data = {}
            
            response_data['id'] = form1.id
            response_data['position'] = form1.position
            response_data['company'] = form1.company
            response_data['start_date'] = form1.start_date.strftime('%b. %d, %Y')
            response_data['end_date'] = form1.end_date.strftime('%b. %d, %Y')
            response_data['location'] = form1.location
            response_data['response'] = True
           
            new_data = json.dumps(response_data)
                
            return HttpResponse(new_data, content_type='application/json')
        else:
            data = {}
            data['response'] = False
            new_data = json.dumps(data)
            return HttpResponse(new_data, content_type='application/json')

def add_interest(request):

    if request.method == 'POST':
        
        add_interest_form = InterestForm(request.POST or None, request.FILES or None)
        
        if add_interest_form.is_valid():
            
            form1 = add_interest_form.save(commit=False)
            form1.user = request.user
            form1.save()
            response_data = {}
            
            response_data['id'] = form1.id
            response_data['interest'] = form1.interest
            
            response_data['response'] = True
           
            new_data = json.dumps(response_data)
                
            return HttpResponse(new_data, content_type='application/json')
        else:
            data = {}
            data['response'] = False
            new_data = json.dumps(data)
            return HttpResponse(new_data, content_type='application/json')

def delete_work(request):
    if request.method =='POST':
        user =request.user
        work_id = request.POST['work_id']
        obj = Work.objects.get(id=work_id)
    response_data = {}
    response_data['id'] = obj.id



    new_data = json.dumps(response_data)
    obj.delete()
    return HttpResponse(new_data, content_type='application/json')

def delete_interest(request):

    if request.method =='POST':
        user =request.user
        interest_id = request.POST['interest_id']
        obj = Interest.objects.get(id=interest_id)
    response_data = {}
    response_data['id'] = obj.id



    new_data = json.dumps(response_data)
    obj.delete()
    return HttpResponse(new_data, content_type='application/json')
    


def profile(request,id):
    if request.user.is_authenticated():
        try:
            user = MyUser.objects.get(id=id)
            if user.is_active:
                single_user = user
            
        except:
            raise Http404
        add_club_form = AddClubForm(request.POST or None, request.FILES or None)
        schedule = Schedule.objects.filter(user=request.user)
        studentcourses = StudentCourse.objects.filter(user=single_user)
        my_clubs = ClubMember.objects.filter(user=single_user)
        my_teams = TeamMember.objects.filter(user=single_user)
        my_frats = Member.objects.filter(user=single_user)
        courses = Course.objects.all()
        clubs = Club.objects.all()
        teams = Team.objects.all()
        frats = Frat.objects.all()
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

        bio_info = Bio.objects.filter(user=single_user)
        work_info = Work.objects.filter(user=single_user)
        interest_info = Interest.objects.filter(user=single_user)
        profile_info = ProfileInfo.objects.filter(user=single_user)
        user_pic = UserPicture.objects.filter(user=single_user)
        

        
        path = request.get_full_path()
        posts = MyPost.objects.filter(profile=single_user).filter(parent=None)    

        user = request.user
        picture = UserPicture.objects.filter(user=user)
        UserPictureFormset = modelformset_factory(UserPicture, form=UserPictureForm, extra=1, max_num=1)
        formset_pic = UserPictureFormset(request.POST or None, request.FILES or None, queryset=picture)

        info = ProfileInfo.objects.filter(user=single_user)
        ProfileInfoFormset = modelformset_factory(ProfileInfo, form=ProfileInfoForm, extra=1, max_num=1)
        formset_info = ProfileInfoFormset(request.POST or None, request.FILES or None, queryset=info)

        image_mypost_form = ImageMyPostForm(request.POST or None , request.FILES or None, prefix='imagemypost')
        link_mypost_form = LinkMyPostForm(request.POST or None , prefix='linkmypost')
        
        work = Work.objects.filter(user=single_user)
        WorkFormset = modelformset_factory(Work, form=WorkForm, extra=1, max_num=1)
        formset_work = WorkFormset(request.POST or None, request.FILES or None, queryset=work)

        add_work_form = WorkForm(request.POST or None, request.FILES or None)
        add_interest_form = InterestForm(request.POST or None, request.FILES or None)

        bio = Bio.objects.filter(user=single_user)
        BioFormset = modelformset_factory(Bio, form=BioForm, extra=1, max_num=1)
        formset_bio = BioFormset(request.POST or None, request.FILES or None, queryset=bio)

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
                    profile=single_user,
                    text=mypost_text,
                    parent=parent_mypost,
                    
                    )
                notify.send(target=None, sender=new_comment.user, recipient=single_user, action='commented on', affected_user=None)
                
                
                
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
                response_data['single_user'] = single_user.id
                
                response_data['id'] = new_comment.id
                response_data['response'] = True
                new_data = json.dumps(response_data)
                    
                return HttpResponse(new_data, content_type='application/json')
            else:
                data = {}
                data['response'] = False
                new_data = json.dumps(data)
                return HttpResponse(new_data, content_type='application/json')
            
        

        return render_to_response('profiles/profile.html', locals(), context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def link(request,id):
    try:
        user = MyUser.objects.get(id=id)
        if user.is_active:
            single_user = user
        
    except:
        raise Http404
    path = reverse("profile", kwargs={"id":single_user.id})
    
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
            new_comment.profile = single_user
            new_comment.parent = parent_mypost
            new_comment.save()
            notify.send(target=None, sender=new_comment.user, recipient=single_user, action='commented on', affected_user=None)
            
            
                
            
            
             
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

        
    

def image(request, id):

    try:
        user = MyUser.objects.get(id=id)
        if user.is_active:
            single_user = user
        
    except:
        raise Http404
    path = reverse("profile", kwargs={"id":single_user.id})
     
        
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
            new_comment.profile = single_user
            new_comment.text = image_mypost_text
            new_comment.image = image_mypost_image
            new_comment.parent = parent_mypost
            new_comment.save()
            notify.send(target=None, sender=new_comment.user, recipient=single_user, action='commented on', affected_users=None)
            image_post = new_comment.image.url
                
            
            
             
            response_data = {}
            response_data['result'] = 'Create post successful!'
            response_data['text'] = new_comment.text
            response_data['first_name'] = new_comment.user.first_name
            response_data['last_name'] = new_comment.user.last_name

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
            response_data['image_post'] = image_post

            new_data = json.dumps(response_data)
                
            return HttpResponse(new_data, content_type='application/json')
                
        else:
            data = {}
            data['response'] = False
            new_data = json.dumps(data)
            return HttpResponse(new_data, content_type='application/json')
    
    

def add_ajax(request):
    if request.is_ajax() and request.POST:
        mypost_form = MyPostForm(request.POST or None , prefix='mypost')
        if mypost_form.is_valid():
            mypost_user = mypost_form.cleaned_data['user']
            
            
            new_data = json.dumps(mypost_user)
                
            return HttpResponse(new_data, mimetype='application/json')
            
    else:
        raise Http404

