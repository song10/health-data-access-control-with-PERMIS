from django.contrib import admin
from his1.models import Record, Document

class DocumentInline (admin.StackedInline):
	model = Document
	extra = 1

class RecordAdmin (admin.ModelAdmin):
	fieldsets = [
		('Patient',		  {'fields': ['owner']}),
		('Date information', {'fields': ['create_date'], 'classes': ['collapse']}),
	]
	inlines = [DocumentInline]

admin.site.register(Record, RecordAdmin)
admin.site.register(Document)
