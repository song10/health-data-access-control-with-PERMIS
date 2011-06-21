from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from center.models import Record, Document

urlpatterns = patterns('health.center.views',
	(r'^documents/(?P<pk>\d+)/$', DetailView.as_view(model=Document, template_name='center/document.html')),
#	(r'^documents/(?P<document_id>\d+)/$', 'detail'),
#	url(r'^documents/$', ListView.as_view(queryset=Document.objects.order_by('create_date'), context_object_name='document_list', template_name='center/documents.html'), name='documents'),
	url(r'^documents/$', 'documents', name='documents'),
	(r'^record/$', 'record'),
	(r'^session/$', 'setup_session'),
	(r'^accounts/profile/$', 'viewProfile'),
	(r'^$', 'show_session'),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^accounts/login/$', 'login', {'template_name': 'center/login.html'}, name='login'),
	url(r'^accounts/logout/$', 'logout', {'template_name': 'center/logout.html'}, name='logout'),
)
