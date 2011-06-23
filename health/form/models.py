from django.db import models
from django.forms import ModelForm
from center.models import *

#ACCOUNT_CHOICES = (
#	('cn=Alice,o=Citizen,c=Taiwan', 'Alice'),
#	('cn=Bruce,o=Citizen,c=Taiwan', 'Bruce'),
#	('cn=Clark,o=Citizen,c=Taiwan', 'Clark'),
#)

PRINCIPAL_CHOICES = (
	# patient
	('cn=Alice,o=Citizen,c=Taiwan', 'Alice'),
	('cn=Bruce,o=Citizen,c=Taiwan', 'Bruce'),
	('cn=Clark,o=Citizen,c=Taiwan', 'Clark'),
	# doctor
	('cn=Talon,ou=Taipei,o=Hospital,c=Taiwan'    , 'Talon'),
	('cn=Stella,ou=Taipei,o=Hospital,c=Taiwan'   , 'Stella'),
	('cn=Nicholas,ou=Taipei,o=Hospital,c=Taiwan' , 'Nicholas'),
	('cn=Max,ou=Taichung,o=Hospital,c=Taiwan'    , 'Max'),
	('cn=Russell,ou=Taichung,o=Hospital,c=Taiwan', 'Russell'),
	('cn=Lana,ou=Taichung,o=Hospital,c=Taiwan'   , 'Lana'),
	('cn=Ruby,ou=Tainan,o=Hospital,c=Taiwan'     , 'Ruby'),
	('cn=Julia,ou=Tainan,o=Hospital,c=Taiwan'    , 'Julia'),
	('cn=Joe,ou=Tainan,o=Hospital,c=Taiwan'      , 'Joe'),
	# hospital
	('cn=Taipei,o=Hospital,c=Taiwan'  , 'Taipei'),
	('cn=Taichung,o=Hospital,c=Taiwan', 'Taichung'),
	('cn=Tainan,o=Hospital,c=Taiwan'  , 'Tainan'),
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

class Read (models.Model):
#	account = models.CharField(max_length=256, choices=PRINCIPAL_CHOICES)
	role = models.CharField(max_length=256, choices=ROLE_CHOICES)
	principal = models.CharField(max_length=256, choices=PRINCIPAL_CHOICES)
	document = models.CharField(max_length=256, choices=[(x.id, x) for x in Document.objects.all().order_by('create_date')])
#	environment = models.TextField()

	def __unicode__ (self):
		return self.name
	
class ReadForm (ModelForm):
	class Meta:
		model = Read

class Write (models.Model):
	account = models.CharField(max_length=256, choices=PRINCIPAL_CHOICES)
	hospital = models.CharField(max_length=256, choices=PRINCIPAL_CHOICES)
	department = models.CharField(max_length=256, choices=DEPARTMENT_CHOICES)
	doctor = models.CharField(max_length=256, choices=PRINCIPAL_CHOICES)
	patient = models.ForeignKey(Record)
	type = models.CharField(max_length=256, choices=TYPE_CHOICES)
	create_date = models.DateTimeField()
	publish_date = models.DateTimeField()
	prescription = models.TextField()
	environment = models.TextField()

	def __unicode__ (self):
		return self.account
	
class WriteForm (ModelForm):
	class Meta:
		model = Write
#		exclude = ('owner', 'author', 'hospital', 'type', 'department')

class Authorize (models.Model):
	account = models.CharField(max_length=256, choices=PRINCIPAL_CHOICES)
	hospital = models.CharField(max_length=256, choices=PRINCIPAL_CHOICES)
	doctor = models.CharField(max_length=256, choices=PRINCIPAL_CHOICES)
	type = models.CharField(max_length=256, choices=TYPE_CHOICES)
	environment = models.TextField()

	def __unicode__(self):
		return self.account
	
class AuthorizeForm (ModelForm):
	class Meta:
		model = Authorize
#		exclude = ('owner', 'author', 'hospital', 'type', 'department')
