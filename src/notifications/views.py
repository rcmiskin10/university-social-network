from django.shortcuts import get_object_or_404, render_to_response, RequestContext, Http404, HttpResponseRedirect, render, HttpResponse
import json
from .models import Notification
from clubs.models import ClubMember


def notifications_all(request):

	if request.user.is_authenticated():
		notifications = Notification.objects.filter(recipient=request.user)
		return render_to_response('notifications/all.html', locals(), context_instance=RequestContext(request))

	else:
		return HttpResponseRedirect('/login/')

def notifications_count(request):
	notes = Notification.objects.filter(read=False)
		

		
	results = []
	for item in notes:
		if item.target_object_id is not None:
			if item.recipient == request.user:
				if str(item.target_content_type) == 'club':

					if request.user in item.target_object.club_members.all():
						
						note_json = {}
						note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
						note_json['action'] = item.action
						note_json['club'] = item.target_object.club_name
						note_json['target'] = str(item.target_content_type)
						note_json['id'] = item.target_object_id
						note_json['note_id'] = item.id


						results.append(note_json)
				if str(item.target_content_type) == 'frat':
					if request.user in item.target_object.members.all():
						
						note_json = {}
						note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
						note_json['action'] = item.action
						note_json['frat'] = item.target_object.name
						note_json['target'] = str(item.target_content_type)
						note_json['id'] = item.target_object_id
						note_json['note_id'] = item.id

						results.append(note_json)

				if str(item.target_content_type) == 'team':
					if request.user in item.target_object.team_members.all():
						
						note_json = {}
						note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
						note_json['action'] = item.action
						note_json['team'] = item.target_object.name
						note_json['target'] = str(item.target_content_type)
						note_json['id'] = item.target_object_id
						note_json['note_id'] = item.id

						results.append(note_json)

				if str(item.target_content_type) == 'course':
					if request.user in item.target_object.students.all():
						
						note_json = {}
						note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
						note_json['action'] = item.action
						note_json['course'] = item.target_object.course_num
						note_json['target'] = str(item.target_content_type)
						note_json['id'] = item.target_object.slug

						note_json['note_id'] = item.id

						results.append(note_json)


		if item.target_object_id is None:
			if item.recipient == request.user:
				
				note_json = {}
				note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
				note_json['action'] = item.action
				note_json['id'] = request.user.id
				note_json['note_id'] = item.id
				note_json['target'] = str(item.target_content_type)
				note_json['obj_id'] = str(item.target_object_id)

				results.append(note_json)

	count = len(results)

	
	
	note_json = {}
	note_json['count'] = count
	
	data = json.dumps(note_json)
		

	return HttpResponse(data, content_type='application/json')

def get_notifications_ajax(request):
	if request.is_ajax() and request.method == "POST":
		prof_notes = Notification.objects.filter(recipient=request.user).filter(read=False)
		notes = Notification.objects.filter(read=False)
		

		
		results = []
		for item in notes:
			if item.target_object_id is not None:
				if item.recipient == request.user:
					if str(item.target_content_type) == 'club':
						if request.user in item.target_object.club_members.all():
							
							note_json = {}
							note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
							note_json['action'] = item.action
							note_json['club'] = item.target_object.club_name
							note_json['target'] = str(item.target_content_type)
							note_json['id'] = item.target_object_id
							note_json['note_id'] = item.id


							results.append(note_json)
					if str(item.target_content_type) == 'frat':
						if request.user in item.target_object.members.all():
							
							note_json = {}
							note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
							note_json['action'] = item.action
							note_json['frat'] = item.target_object.name
							note_json['target'] = str(item.target_content_type)
							note_json['id'] = item.target_object_id
							note_json['note_id'] = item.id

							results.append(note_json)

					if str(item.target_content_type) == 'team':
						if request.user in item.target_object.team_members.all():
							
							note_json = {}
							note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
							note_json['action'] = item.action
							note_json['team'] = item.target_object.name
							note_json['target'] = str(item.target_content_type)
							note_json['id'] = item.target_object_id
							note_json['note_id'] = item.id

							results.append(note_json)

					if str(item.target_content_type) == 'course':
						if request.user in item.target_object.students.all():
							
							note_json = {}
							note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
							note_json['action'] = item.action
							note_json['course'] = item.target_object.course_num
							note_json['target'] = str(item.target_content_type)
							note_json['id'] = item.target_object.slug

							note_json['note_id'] = item.id

							results.append(note_json)


			if item.target_object_id is None:

				if item.recipient == request.user:
					
					note_json = {}
					note_json['sender'] = item.sender.first_name + " " + item.sender.last_name
					note_json['action'] = item.action
					note_json['id'] = request.user.id
					note_json['note_id'] = item.id
					note_json['target'] = str(item.target_content_type)
					note_json['obj_id'] = str(item.target_object_id)

					results.append(note_json)



		data = json.dumps(results)
		

		return HttpResponse(data, content_type='application/json')

	else:
		raise Http404

def read(request, id):
	next = request.GET.get('next', None)
	notification = Notification.objects.get(id=id)
	if notification.recipient == request.user:
		notification.read = True
		notification.save()
		if next is not None:
			return HttpResponseRedirect(next)