from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^health/', include('health.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
	(r'^center/', include('health.center.urls')),
	(r'^form/', include('health.form.urls')),
	(r'^permis/', include('health.permis.urls')),
	(r'^his1/', include('health.his1.urls')),
)
