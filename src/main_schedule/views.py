from django.shortcuts import render_to_response, RequestContext, Http404, render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import MainScheduleForm
from .models import MainSchedule
import json

def main_schedule(request):
	
	schedule_form = MainScheduleForm(request.POST or None, prefix='schedule')

	if request.method == 'POST':
		if schedule_form.is_valid():
			schedule_text = schedule_form.cleaned_data['text']
			schedule_duedate = schedule_form.cleaned_data['duedate']

			new_form = MainSchedule()
			new_form.user = request.user
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

def delete_main_sched(request):
	
		
		
	if request.method =='POST':
		user =request.user
        sched_id = request.POST.get('sched_id')
	    
	
		
	
	obj = MainSchedule.objects.get(id=sched_id)
	print obj.id


	response_data = {}
	response_data['id'] = obj.id
	


	new_data = json.dumps(response_data)
	obj.delete()
	return HttpResponse(new_data, content_type='application/json')