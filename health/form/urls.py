from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('form.views',
	url(r'^$'      , 'view_rules'),
	url(r'^rule1/$', 'view_rule1'),
	url(r'^rule2/$', 'view_rule2'),
	url(r'^rule3/$', 'view_rule3'),
	url(r'^rule4/$', 'view_rule4'),
	url(r'^rule5/$', 'view_rule5'),
)
