from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('form.views',
	url(r'^$', 'bridge'),
)
