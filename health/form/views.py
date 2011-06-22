from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm

from form.models import *
from center.models import *

def show_form (request):
	d = dict(form=AuthorForm ())
	d.update(csrf(request))
	return render_to_response('form/form.html', d)

def post_form (request):
	return HttpResponse("form.views.post_form")

def view_read (request):
#	return HttpResponse("form.views.view_read")
#	documents = Document.objects.all().order_by('create_date')
#	d = dict(form=ReadForm (),documents=documents)	
	d = dict(form=ReadForm ())
	d.update(csrf(request))
	return render_to_response('form/read_form.html', d)

def view_read_post (request):
#	return HttpResponse("form.views.view_read_post")
	p = request.POST
	s = request.session or {}
	return render_to_response('form/dump.html', {'post':p})
#	return render_to_response('form/dump.html', {'post':p, 'session':s})

def view_write (request):
#	return HttpResponse("form.views.view_write")
	d = dict(form=WriteForm ())
	d.update(csrf(request))
	return render_to_response('form/write_form.html', d)

def view_write_post (request):
	p = request.POST
	s = request.session or {}
	return render_to_response('form/dump.html', {'post':p})
#	return render_to_response('form/dump.html', {'post':p, 'session':s})

def view_authorize (request):
#	return HttpResponse("form.views.view_authorize")
	d = dict(form=AuthorizeForm ())
	d.update(csrf(request))
	return render_to_response('form/authorize_form.html', d)

def view_authorize_post (request):
	p = request.POST
	s = request.session or {}
	return render_to_response('form/dump.html', {'post':p})
#	return render_to_response('form/dump.html', {'post':p, 'session':s})
