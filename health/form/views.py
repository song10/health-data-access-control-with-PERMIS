# -*- 
#coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm

from form.request import *
from form.models import *
from center.models import *

def view_rule1 (request):
	context = {'rule':'Rule1', 'title':'A patient can read her own documents'}
	
	if request.method == 'GET':
		d = dict(form=FormRule1 ())
		d.update(context)
		d.update(csrf(request))
		return render_to_response('form/form_rule1.html', d)
	elif not request.method == 'POST':
		return HttpResponse("form.views.view_rule1 not(GET|POST)")

	# POST
	p = request.POST

	form = FormRule1 (request.POST)
	if not form.is_valid():
		return render_to_response('form/dump.html', context.update({'post':p}))
#		s = request.session or {}
#		return render_to_response('form/dump.html', {'post':p, 'session':s})

	# valid
	doc = Document.objects.get(id=int(p.get('document')))
	req = Request ()
	subj = Attribute (name=Permis.permisRole, type=Xacml.string, value=p.get('role'), issuer=My.issuer)
	reso = Attribute (name=Xacml.resource_id, type=Xacml.string, value='http://localhost/center/document/%s/'%p.get('document'))
	acti = Attribute (name=Xacml.action_id, type=Xacml.string, value='read')
	env0 = Attribute (name='subject', type='String', value=p.get('subject'))
	env1 = Attribute (name='owner', type='String', value=doc.owner)
	env2 = Attribute (name='author', type='String', value=doc.author)
#	env3 = Attribute (name='authorized', type='String', value='false')
	req.subject.Attributes.user = subj
	req.resource.Attributes.res = reso
	req.action.Attributes.act = acti
#	req.action.add_attribute(arg0)
#	req.action.add_attribute(arg1)
	req.environment.add_attribute(env0)
	req.environment.add_attribute(env1)
	req.environment.add_attribute(env2)
#	req.say()
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	return render_to_response('form/form_rule1.html', {'post':p, 'result':dec, 'rule':'Rule1', 'title':'A patient can read her own documents', 'request':req})
#	return HttpResponse(dec)

def view_read (request):
#	return HttpResponse("form.views.view_read")
#	documents = Document.objects.all().order_by('create_date')
#	d = dict(form=ReadForm (),documents=documents)	
	d = dict(form=ReadForm ())
	d.update(csrf(request))
	return render_to_response('form/read_form.html', d)

def view_read_post (request):
	if request.method == 'POST': # If the form has been submitted
		form = ReadForm(request.POST) # A form bound to the POST data
		if not form.is_valid(): # All validation rules pass
			p = request.POST
			s = request.session or {}
#			return render_to_response('form/dump.html', {'post':p})
		#	return render_to_response('form/dump.html', {'post':p, 'session':s})
	else:
		return HttpResponse("form.views.view_read_post")
		
#	p = request.POST
	doc = Document.objects.get(id=int(p.get('document')))
	req = Request ()
	subj = Attribute (name=Permis.permisRole, type=Xacml.string, value=p.get('role'), issuer=My.issuer)
	reso = Attribute (name=Xacml.resource_id, type=Xacml.string, value='http://localhost/center/document/%s/'%p.get('document'))
	acti = Attribute (name=Xacml.action_id, type=Xacml.string, value='read')
	env0 = Attribute (name='principal', type='String', value=p.get('principal'))
	env1 = Attribute (name='owner', type='String', value=doc.owner)
	env2 = Attribute (name='author', type='String', value=doc.author)
#	env3 = Attribute (name='authorized', type='String', value='false')
	req.subject.Attributes.user = subj
	req.resource.Attributes.res = reso
	req.action.Attributes.act = acti
#	req.action.add_attribute(arg0)
#	req.action.add_attribute(arg1)
	req.environment.add_attribute(env0)
	req.environment.add_attribute(env1)
	req.environment.add_attribute(env2)
#	req.say()
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	return render_to_response('form/dump.html', {'post':p, 'session':s, 'error_message':dec})
#	return HttpResponse(dec)


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
