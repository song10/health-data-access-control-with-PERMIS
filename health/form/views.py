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
	role = Attribute (name=Permis.permisRole, type=Xacml.string, value=p.get('role'), issuer=My.issuer)
	reso = Attribute (name=Xacml.resource_id, type=Xacml.string, value='http://localhost/center/document/%s/'%p.get('document'))
	acti = Attribute (name=Xacml.action_id, type=Xacml.string, value='read')
	env0 = Attribute (name='subject', type='String', value=p.get('subject'))
	env1 = Attribute (name='owner', type='String', value=doc.owner)
#	env2 = Attribute (name='author', type='String', value=doc.author)
#	env3 = Attribute (name='authorized', type='String', value='false')
	req.subject.Attributes.user = role
	req.resource.Attributes.res = reso
	req.action.Attributes.act = acti
	req.environment.add_attribute(env0)
	req.environment.add_attribute(env1)
#	req.environment.add_attribute(env2)
#	req.environment.add_attribute(env3)
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	return render_to_response('form/form_rule1.html', {'post':p, 'result':dec, 'rule':'Rule1', 'title':'A patient can read her own documents', 'request':req})
#	return HttpResponse(dec)

def view_rule2 (request):
	context = {'rule':'Rule2', 'title':'A patient can authorize her own record read to doctors'}
	
	if request.method == 'GET':
		context.update({'form':FormRule2 ()})
		context.update(csrf(request))
		return render_to_response('form/form_rule2.html', context)
	elif not request.method == 'POST':
		return HttpResponse("form.views.view_rule2 not(GET|POST)")

	# POST
	p = request.POST

	form = FormRule2 (request.POST)
	if not form.is_valid():
		return render_to_response('form/dump.html', context.update({'post':p}))

	# valid
	rec = Record.objects.get(id=int(p.get('record')))
	req = Request ()
	role = Attribute (name=Permis.permisRole, type=Xacml.string, value=p.get('role'), issuer=My.issuer)
	reso = Attribute (name=Xacml.resource_id, type=Xacml.string, value='http://localhost/center/record/%s/'%p.get('record'))
	acti = Attribute (name=Xacml.action_id, type=Xacml.string, value='authorize')
	env0 = Attribute (name='subject', type='String', value=p.get('subject'))
	env1 = Attribute (name='owner', type='String', value=rec.owner)
#	env2 = Attribute (name='author', type='String', value=doc.author)
#	env3 = Attribute (name='authorized', type='String', value='false')
	req.subject.Attributes.user = role
	req.resource.Attributes.res = reso
	req.action.Attributes.act = acti
	req.environment.add_attribute(env0)
	req.environment.add_attribute(env1)
#	req.environment.add_attribute(env2)
#	req.environment.add_attribute(env3)
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	context.update({'post':p, 'result':dec, 'request':req})
	return render_to_response('form/form_rule2.html', context)
#	return HttpResponse(dec)

def view_rule3 (request):
	context = {'rule':'Rule3', 'title':'A doctor can read her own composed or patient authorized documents'}
	
	if request.method == 'GET':
		context.update({'form':FormRule3 ()})
		context.update(csrf(request))
		return render_to_response('form/form_rule3.html', context)
	elif not request.method == 'POST':
		return HttpResponse("form.views.view_rule3 not(GET|POST)")

	# POST
	p = request.POST

	form = FormRule3 (request.POST)
	if not form.is_valid():
		context.update({'post':p})
		return render_to_response('form/dump.html', context)

	# valid
	doc = Document.objects.get(id=int(p.get('document')))
	req = Request ()
	role = Attribute (name=Permis.permisRole, type=Xacml.string, value=p.get('role'), issuer=My.issuer)
	reso = Attribute (name=Xacml.resource_id, type=Xacml.string, value='http://localhost/center/document/%s/'%p.get('document'))
	acti = Attribute (name=Xacml.action_id, type=Xacml.string, value='read')
	env0 = Attribute (name='subject', type='String', value=p.get('subject'))
#	env1 = Attribute (name='owner', type='String', value=doc.owner)
	env2 = Attribute (name='author', type='String', value=doc.author)
	env3 = Attribute (name='authorized', type='String', value=p.get('authorized'))
	req.subject.Attributes.user = role
	req.resource.Attributes.res = reso
	req.action.Attributes.act = acti
	req.environment.add_attribute(env0)
#	req.environment.add_attribute(env1)
	req.environment.add_attribute(env2)
	req.environment.add_attribute(env3)
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	context.update({'post':p, 'result':dec, 'request':req})
	return render_to_response('form/form_rule3.html', context)
#	return HttpResponse(dec)

def view_rule4 (request):
	context = {'rule':'Rule4', 'title':'A hospital can write her own domain documents'}
	
	if request.method == 'GET':
		context.update({'form':FormRule4 ()})
		context.update(csrf(request))
		return render_to_response('form/form_rule4.html', context)
	elif not request.method == 'POST':
		return HttpResponse("form.views.view_rule4 not(GET|POST)")

	# POST
	p = request.POST

	form = FormRule4 (request.POST)
	if not form.is_valid():
		context.update({'post':p})
		return render_to_response('form/dump.html', context)

	# valid
	doc = Document.objects.get(id=int(p.get('document')))
	req = Request ()
	role = Attribute (name=Permis.permisRole, type=Xacml.string, value=p.get('role'), issuer=My.issuer)
	reso = Attribute (name=Xacml.resource_id, type=Xacml.string, value='http://localhost/center/document/%s/'%p.get('document'))
	acti = Attribute (name=Xacml.action_id, type=Xacml.string, value='write')
	env0 = Attribute (name='subject', type='String', value=p.get('subject'))
	env1 = Attribute (name='hospital', type='String', value=doc.hospital)
	req.subject.Attributes.user = role
	req.resource.Attributes.res = reso
	req.action.Attributes.act = acti
	req.environment.add_attribute(env0)
	req.environment.add_attribute(env1)
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	context.update({'post':p, 'result':dec, 'request':req})
	return render_to_response('form/form_rule4.html', context)
#	return HttpResponse(dec)

def view_rule5 (request):
	context = {'rule':'Rule5', 'title':'A sensor can write own domain test documents'}
	
	if request.method == 'GET':
		context.update({'form':FormRule5 ()})
		context.update(csrf(request))
		return render_to_response('form/form_rule5.html', context)
	elif not request.method == 'POST':
		return HttpResponse("form.views.view_rule5 not(GET|POST)")

	# POST
	p = request.POST

	form = FormRule5 (request.POST)
	if not form.is_valid():
		context.update({'post':p})
		return render_to_response('form/dump.html', context)

	# valid
	doc = Document.objects.get(id=int(p.get('document')))
	req = Request ()
	role = Attribute (name=Permis.permisRole, type=Xacml.string, value=p.get('role'), issuer=My.issuer)
	reso = Attribute (name=Xacml.resource_id, type=Xacml.string, value='http://localhost/center/document/%s/'%p.get('document'))
	acti = Attribute (name=Xacml.action_id, type=Xacml.string, value='write')
	env0 = Attribute (name='subject', type='String', value=p.get('subject'))
	env1 = Attribute (name='author', type='String', value=doc.author)
	env2 = Attribute (name='type', type='String', value=doc.type)
	env3 = Attribute (name='authorized', type='String', value=p.get('authorized'))
	req.subject.Attributes.user = role
	req.resource.Attributes.res = reso
	req.action.Attributes.act = acti
	req.environment.add_attribute(env0)
	req.environment.add_attribute(env1)
	req.environment.add_attribute(env2)
	req.environment.add_attribute(env3)
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	context.update({'post':p, 'result':dec, 'request':req})
	return render_to_response('form/form_rule5.html', context)
#	return HttpResponse(dec)
