from django.db import models
import re

class Record (models.Model):
	create_date = models.DateTimeField('date created')
	owner = models.CharField(max_length=200)
	policy = models.CharField(max_length=4096, blank=True, null=True)

	def __unicode__(self):
		m = re.match(r'cn=(\w+)', self.owner)
		return m.group(1) or '?'

class Document (models.Model):
	create_date = models.DateTimeField('date created')
	record = models.ForeignKey(Record)
	owner = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	hospital = models.CharField(max_length=200)
	type = models.CharField(max_length=200)
	department = models.CharField(max_length=200)
	prescription = models.TextField()

	publish_date = models.DateTimeField('date published')

	def __unicode__(self):
		owner = re.match(r'cn=(\w+)', self.owner).group(1) or '?'
		author = re.match(r'cn=(\w+)', self.author).group(1) or '?'
		hospital = re.match(r'cn=(\w+)', self.hospital).group(1) or '?'
		type = self.type
		return "%s %s %s %s"%(owner, author, hospital, type)

class Session (models.Model):
	loginname = models.CharField(max_length=200)
	environment = models.TextField(max_length=4096, blank=True, null=True)

	def __unicode__(self):
		return self.loginname
