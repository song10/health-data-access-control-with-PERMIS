from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm

from suds.client import Client

from form.request import *
from form.models import *
from center.models import *

def bridge (request):
	url = "http://localhost:1104/axis2/services/AuthzService?wsdl" 
	client = Client(url)
	client.service.XACMLAuthzRequest(__inject={'msg':message.encode()})
	recvdata = client.last_received() 
	pass
