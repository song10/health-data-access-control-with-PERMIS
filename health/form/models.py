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
	('cn=guest,o=patient,c=tw', 'guest'), # test
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
#	('cn=guest,ou=Tainan,o=hospital,c=tw'    , 'guest'), # test
	# hospital
	('cn=Taipei,o=hospital,c=tw'  , 'Taipei'),
	('cn=Taichung,o=hospital,c=tw', 'Taichung'),
	('cn=Tainan,o=hospital,c=tw'  , 'Tainan'),
	# sensor
	('cn=S100,ou=Sensor,o=hospital,c=tw', 'S100'),
	('cn=S301,ou=Sensor,o=hospital,c=tw', 'S301'),
	('cn=S703,ou=Sensor,o=hospital,c=tw', 'S703'),
)

TYPE_CHOICES = (
	('prescription', 'prescription'),
	('test', 'test'),
	('all', 'all'),
	('unknown', 'unknown'),
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
	('guest'   , 'guest'),
)

ACTION_CHOICES = (
	('set'   , 'set'  ),
	('clear' , 'clear'),
)

BOOLING_CHOICES = (
	('true' , 'true' ),
	('false', 'false'),
)

class Rule1 (models.Model):
	'''
	A patient can read her own documents
	'''
	role = models.CharField(max_length=256, choices=ROLE_CHOICES)
	subject = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	document = models.IntegerField(max_length=256, choices=[(x.id, x) for x in Document.objects.all().order_by('create_date')])
#	environment = models.TextField()

class FormRule1 (ModelForm):
	class Meta:
		model = Rule1

class Rule2 (models.Model):
	'''
	A patient can authorize her own record read to doctors
	'''
	role    = models.CharField(max_length=256, choices=ROLE_CHOICES)
	subject = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	doctor  = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	record  = models.IntegerField(max_length=256, choices=[(x.id, x) for x in Record.objects.all()])
	type    = models.CharField(max_length=256, choices=TYPE_CHOICES)
	action  = models.CharField(max_length=256, choices=ACTION_CHOICES)
#	environment = models.TextField()

class FormRule2 (ModelForm):
	class Meta:
		model = Rule2

class Rule3 (models.Model):
	'''
	A doctor can read her own composed or patient authorized documents
	'''
	role = models.CharField(max_length=256, choices=ROLE_CHOICES)
	subject = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	document = models.IntegerField(max_length=256, choices=[(x.id, x) for x in Document.objects.all().order_by('create_date')])
	authorized = models.CharField(max_length=256, choices=BOOLING_CHOICES)
#	environment = models.TextField()

class FormRule3 (ModelForm):
	class Meta:
		model = Rule3

class Rule4 (models.Model):
	'''
	A hospital can write her own domain documents
	'''
	role = models.CharField(max_length=256, choices=ROLE_CHOICES)
	subject = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	document = models.IntegerField(max_length=256, choices=[(x.id, x) for x in Document.objects.all().order_by('create_date')])
#	environment = models.TextField()

class FormRule4 (ModelForm):
	class Meta:
		model = Rule4

class Rule5 (models.Model):
	'''
	A sensor can write own domain test documents
	'''
	role = models.CharField(max_length=256, choices=ROLE_CHOICES)
	subject = models.CharField(max_length=256, choices=SUBJECT_CHOICES)
	document = models.IntegerField(max_length=256, choices=[(x.id, x) for x in Document.objects.all().order_by('create_date')])
	authorized = models.CharField(max_length=256, choices=BOOLING_CHOICES)
#	environment = models.TextField()

class FormRule5 (ModelForm):
	class Meta:
		model = Rule5
