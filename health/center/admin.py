from django.contrib import admin
from center.models import Record, Document, Session

class DocumentInline (admin.StackedInline):
	model = Document
	extra = 1

class RecordAdmin (admin.ModelAdmin):
	fieldsets = [
		('Patient',		  {'fields': ['owner']}),
		('Date information', {'fields': ['create_date'], 'classes': ['collapse']}),
	]
	inlines = [DocumentInline]

class SessionAdmin (admin.ModelAdmin):
	display_fields = ["loginname", "environment",]

admin.site.register(Session, SessionAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Document)
