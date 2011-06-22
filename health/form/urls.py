from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('form.views',
	url(r'^$', 'show_form'),
	url(r'^post/$', 'post_form'),
	url(r'^read/$', 'view_read'),
	url(r'^write/$', 'view_write'),
	url(r'^authorize/$', 'view_authorize'),
	url(r'^read/post/$', 'view_read_post'),
	url(r'^write/post/$', 'view_write_post'),
)
