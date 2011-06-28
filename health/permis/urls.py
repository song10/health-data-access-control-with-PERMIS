from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('permis.views',
	url(r'^$', 'bridge'),
)
