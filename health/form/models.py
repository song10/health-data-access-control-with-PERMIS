from django.db import models
from django.forms import ModelForm
from center.models import *

#ACCOUNT_CHOICES = (
#	('cn=Alice,o=citizen,c=tw', 'Alice'),
#	('cn=Bruce,o=citizen,c=tw', 'Bruce'),
#	('cn=Clark,o=citizen,c=tw', 'Clark'),
#)

SUBJECT_CHOICES = (
	# patient
	('cn=Alice,o=citizen,c=tw', 'Alice'),
	('cn=Bruce,o=citizen,c=tw', 'Bruce'),
	('cn=Clark,o=citizen,c=tw', 'Clark'),
	# doctor
	('cn=Talon,ou=Taipei,o=hospital,c=tw'    , 'Talon'),
	('cn=Stella,ou=Taipei,o=hospital,c=tw'   , 'Stella'),
	('cn=Nicholas,ou=Taipei,o=hospital,c=tw' , 'Nicholas'),
	('cn=Max,ou=Taichung,o=hospital,c=tw'    , 'Max'),
	('cn=Russell,ou=Taichung,o=hospital,c=tw', 'Russell'),
	('cn=Lana,ou=Taichung,o=hospital,c=tw'   , 'Lana'),
	('cn=Ruby,ou=Tainan,o=hospital,c=tw'     , 'Ruby'),
	('cn=Julia,ou=Tainan,o=hospital,c=tw'    , 'Julia'),
	('cn=Joe,ou=Tainan,o=hospital,c=tw'      , 'Joe'),
	# hospital
	('cn=Taipei,o=hospital,c=tw'  , 'Taipei'),
	('cn=Taichung,o=hospital,c=tw', 'Taichung'),
	('cn=Tainan,o=hospital,c=tw'  , 'Tainan'),
	# sensor
	('cn=S100,o=sensor,c=tw', 'S100'),
	('cn=S301,o=sensor,c=tw', 'S301'),
	('cn=S703,o=sensor,c=tw', 'S703'),
)

TYPE_CHOICES = (
	('prescription', 'prescription'),
	('test', 'test'),
)

DEPARTMENT_CHOICES = (
	('medicine', 'medicine'),
	('surgery', 'surgery'),
	('ENT', 'ENT'),
)

ROLE_CHOICES = (
	('patient' , 'patient' ),
	('doctor'  , 'doctor'  ),
	('sensor'  , 'sensor'  ),
	('hospital', 'hospital'),
)

SETCLEAR_CHOICES = (
	('set'   , 'set'  ),
	('clear' , 'clear'),
)

class Rule1 (models.Model):
	subject = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	role = models.CharField(max_length=256, choices=ROLE_CHOICES)
	document = models.IntegerField(max_length=256, choices=[(x.id, x) for x in Document.objects.all().order_by('create_date')])
#	environment = models.TextField()

class FormRule1 (ModelForm):
	class Meta:
		model = Rule1

class Read (models.Model):
#	account = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	role = models.CharField(max_length=256, choices=ROLE_CHOICES)
	principal = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	document = models.CharField(max_length=256, choices=[(x.id, x) for x in Document.objects.all().order_by('create_date')])
#	environment = models.TextField()

	def __unicode__ (self):
		return self.name
	
class ReadForm (ModelForm):
	class Meta:
		model = Read

class Write (models.Model):
	account = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	hospital = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	department = models.CharField(max_length=256, choices=DEPARTMENT_CHOICES)
	doctor = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	patient = models.ForeignKey(Record)
	type = models.CharField(max_length=256, choices=TYPE_CHOICES)
	create_date = models.DateTimeField()
	publish_date = models.DateTimeField()
	prescription = models.TextField()
#	environment = models.TextField()

	def __unicode__ (self):
		return self.account
	
class WriteForm (ModelForm):
	class Meta:
		model = Write
#		exclude = ('owner', 'author', 'hospital', 'type', 'department')

class Authorize (models.Model):
	account = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	set = models.CharField(max_length=256, choices=SETCLEAR_CHOICES)
	doctor = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	hospital = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	type = models.CharField(max_length=256, choices=TYPE_CHOICES)
#	environment = models.TextField()

	def __unicode__(self):
		return self.account
	
class AuthorizeForm (ModelForm):
	class Meta:
		model = Authorize
#		exclude = ('owner', 'author', 'hospital', 'type', 'department')
