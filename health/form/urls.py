from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('form.views',
	url(r'^$', 'show_form'),
	url(r'^post/$', 'post_form'),
)
