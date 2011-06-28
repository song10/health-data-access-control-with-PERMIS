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

def view_rules (request):
	rules = [
		{'name':'Rule1', 'value':'A patient can read her own documents'},
		{'name':'Rule2', 'value':'A patient can authorize her own record read to doctors'},
		{'name':'Rule3', 'value':'A doctor can read her own composed or patient authorized documents'},
		{'name':'Rule4', 'value':'A hospital can write her own domain documents'},
		{'name':'Rule5', 'value':'A sensor can write its own domain test documents to authorized records'},
	]
	context = {'rules':rules}
	return render_to_response('form/form_rules.html', context)

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

	# valid
	doc = Document.objects.get(id=int(p.get('document')))
	req = Request ()
	req.add_subject(value=p.get('role'), name=Permis.permisRole, type=Xacml.string, issuer=My.issuer)
	req.add_action(value='read', name=Xacml.action_id, type=Xacml.string)
	req.add_resource(value='http://localhost/center/document/%s/'%p.get('document'), name=Xacml.resource_id, type=Xacml.string)
	req.add_environment(name='subject', value=p.get('subject'), type='String')
	req.add_environment(name='owner', value=doc.owner, type='String')
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	return render_to_response('form/form_rule1.html', {'post':p, 'result':dec, 'rule':'Rule1', 'title':'A patient can read her own documents', 'request':req})

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
	req.add_subject(value=p.get('role'), name=Permis.permisRole, type=Xacml.string, issuer=My.issuer)
	req.add_action(value='authorize', name=Xacml.action_id, type=Xacml.string)
	req.add_resource(value='http://localhost/center/record/%s/'%p.get('record'), name=Xacml.resource_id, type=Xacml.string)
	req.add_environment(name='subject', value=p.get('subject'), type='String')
	req.add_environment(name='owner', value=rec.owner, type='String')
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	context.update({'post':p, 'result':dec, 'request':req})
	return render_to_response('form/form_rule2.html', context)

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
	req.add_subject(value=p.get('role'), name=Permis.permisRole, type=Xacml.string, issuer=My.issuer)
	req.add_action(value='read', name=Xacml.action_id, type=Xacml.string)
	req.add_resource(value='http://localhost/center/document/%s/'%p.get('document'), name=Xacml.resource_id, type=Xacml.string)
	req.add_environment(name='subject', value=p.get('subject'), type='String')
	req.add_environment(name='author', value=doc.author, type='String')
	req.add_environment(name='authorized', value=p.get('authorized'), type='String')
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	context.update({'post':p, 'result':dec, 'request':req})
	return render_to_response('form/form_rule3.html', context)

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
	req.add_subject(value=p.get('role'), name=Permis.permisRole, type=Xacml.string, issuer=My.issuer)
	req.add_action(value='write', name=Xacml.action_id, type=Xacml.string)
	req.add_resource(value='http://localhost/center/document/%s/'%p.get('document'), name=Xacml.resource_id, type=Xacml.string)
	req.add_environment(name='subject', value=p.get('subject'), type='String')
	req.add_environment(name='hospital', value=doc.hospital, type='String')
#	req.add_environment(name='authorized', value=p.get('authorized'), type='String')
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	context.update({'post':p, 'result':dec, 'request':req})
	return render_to_response('form/form_rule4.html', context)

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
	req.add_subject(value=p.get('role'), name=Permis.permisRole, type=Xacml.string, issuer=My.issuer)
	req.add_action(value='write', name=Xacml.action_id, type=Xacml.string)
	req.add_resource(value='http://localhost/center/document/%s/'%p.get('document'), name=Xacml.resource_id, type=Xacml.string)
	req.add_environment(name='subject'   , value=p.get('subject')   , type='String')
	req.add_environment(name='author'    , value=doc.author         , type='String')
	req.add_environment(name='type'      , value=doc.type           , type='String')
	req.add_environment(name='authorized', value=p.get('authorized'), type='String')
	res = query(req.say(quiet=True))
	dec = Response (res).say(quiet=True)
	context.update({'post':p, 'result':dec, 'request':req})
	return render_to_response('form/form_rule5.html', context)
