from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm

from form.models import *

def show_form (request):
	d = dict(form=AuthorForm ())
	d.update(csrf(request))
	return render_to_response('form/form.html', d)

def post_form (request):
	return HttpResponse("form.views.post_form")
