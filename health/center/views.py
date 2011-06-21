# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
#from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm

from center.models import Record, Document, Session

class SessionForm (ModelForm):
	class Meta:
		model = Session
#		exclude = ["post"]

#@login_required
@staff_member_required
def record (request):
	return HttpResponse("center: record view")

@staff_member_required
def documents (request):
	s = request.session
	s['test'] = '123'
	name = '%s'%s.loginname if hasattr(s, "loginname") else ''
	document_list = Document.objects.all().filter(owner=name).order_by('create_date')
	return render_to_response('center/documents.html', {'document_list': document_list, 'session':s})

def detail (request, document_id):
	d = get_object_or_404(Document, pk=document_id)
	return render_to_response('center/document.html', {'document': d}, context_instance=RequestContext(request))

def show_session (request):
#	return HttpResponse("center: session view")
	d = dict(form=SessionForm ())
	d.update(csrf(request))
	return render_to_response('center/session.html', d)

def setup_session (request):
	p = request.POST
	s = request.session
	
	if p.has_key("loginname") and p["loginname"]:
		s['loginname'] = p["loginname"]
	else:
		s['loginname'] = None
		
	if p.has_key("environment"):
		s["environment"] = p["environment"]
	else:
		s["environment"] = None
	
#	return HttpResponse("center.view.setup_session: post(name='%(loginname)s',environment='%(environment)s'"%s)
#	return render_to_response('center/session.html', context_instance=RequestContext(request))
	return HttpResponseRedirect(reverse("health.center.views.documents"))

#def set_session (request, pk):
#	"""Add a new comment."""
#	p = request.POST
#
#	if p.has_key("body") and p["body"]:
#		author = "Anonymous"
#		if p["author"]: author = p["author"]
#
#		comment = Comment(post=Post.objects.get(pk=pk))
#		cf = CommentForm(p, instance=comment)
#		cf.fields["author"].required = False
#
#		comment = cf.save(commit=False)
#		comment.author = author
#		comment.save()
#	return HttpResponseRedirect(reverse("dbe.blog.views.post", args=[pk]))
