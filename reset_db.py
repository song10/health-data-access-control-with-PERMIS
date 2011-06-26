import datetime
import random
from center.models import Record, Document

hospital_departments = [
	'medicine',
	'surgery',
	'ENT',
]

hospital_names = [
	'Taipei',
	'Taichung',
	'Tainan',
]

hospital_domain = 'o=hospital,c=tw'

doctor_names = {
	'Taipei'  : [ 'Talon', 'Stella', 'Nicholas', ],
	'Taichung': [ 'Max', 'Russell', 'Lana', ],
	'Tainan'  : [ 'Ruby', 'Julia', 'Joe', ],
}

patient_names = [
	'Alice', 'Bruce', 'Clark',
]

patient_domain = 'o=citizen,c=tw'

document_types = [ 'prescription', 'test', ]

class Thing (object):
	def __iter__ (self):
		return self.__dict__.__iter__()
	
	def __len__ (self):
		return len(self.__dict__)
	
	def __contains__ (self, v):
		return v in self.__dict__
	
	def __getitem__ (self, v):
		return self.__dict__[v]

	def __setitem__(self, key, value):
		self.__dict__[key] = value
	
	def __delitem__(self, key):
		del self.__dict__[key]

	def values (self):
		return self.__dict__.values()

	def items (self):
		return self.__dict__.items()

	pass

class Doctor (Thing):
	def __init__ (self, name, domain):
		self.name = name
		self.dn = "cn=%s,%s"%(name, domain)
	pass

class Hospital (Thing):
	def __init__ (self, name):
		self.name = name
		self.doctors = Thing ()

		global hospital_domain
		self.dn = "cn=%s,%s"%(name, hospital_domain)
		self.domain = "ou=%s,%s"%(name, hospital_domain)
		
	def add_doctor (self, name):
		setattr(self.doctors, name, Doctor (name, self.domain))
		return getattr(self.doctors, name)
	
	def next_doctor (self):
		return random.choice(self.doctors.values())
	
	def next_type (self):
		global document_types
		return random.choice(document_types)
	
	def next_department (self):
		global hospital_departments
		return random.choice(hospital_departments)
	pass

class Patient (Thing):
	document_count = 0
	
	def __init__ (self, record):
		self.record = record
	
	def next_index (self):
		rz = Patient.document_count
		Patient.document_count += 1
		print('%s (%s)' % ('next_index', Patient.document_count))
		return rz
	
	def add_document (self, **map):
#		print('%s (%s)' % ('add_document', map))
		hos = map['hospital'] 
		map['owner']        = self.record.owner
		map['author']       = map['author'].dn 
		map['hospital']     = hos.dn
		map['type']         = hos.next_type()
		map['department']   = hos.next_department()
#		print('%s (%s)' % ('add_document', map))

		documents_in_db = Document.objects.all()
		filter = [x.prescription for x in documents_in_db]
		if map['prescription'] in filter:
			return None
		
		d = self.record.document_set.create(**map)
		d.save()
		print('add document %s by %s at %s'%(d.owner, d.author, d.hospital))
	pass

class HospitalGen (Thing):
	def __init__ (self, names, drnames):
		self.hospitals = Thing ()
		
		for x in names:
			t = self.add_hospital(x)
			for y in drnames[t.name]:
				t.add_doctor(y)
	
	def add_hospital (self, name):
		setattr(self.hospitals, name, Hospital (name))
		return getattr(self.hospitals, name)
	
	def next (self):
#		print('%s (%s)' % ('next', self.hospitals))
		return random.choice(self.hospitals.values())
	pass

class PatientGen (Thing):
	def __init__ (self, names):
		for x in names:
			self.add_patient(x) # create record here
	
	def add_patient (self, name):
#		print('%s (%s)' % ('add_patient', name))
		global patient_domain
		name2 = "cn=%s,%s"%(name, patient_domain)
		# TODO: once or each?
		records_in_db = Record.objects.all()
		filter = [x.owner for x in records_in_db]
#		print('%s (%s)' % ('filter', filter))
		if name2 in filter:
				return None
		
		year = random.randrange(1990, 2000+1)
		month = random.randrange(1, 12+1)
		day = random.randrange(1, 28+1)
		date = datetime.datetime(year, month, day)
		r = Record (create_date=date, owner=name2)
		r.save()
		print('add %s "%s"'%(name, name2))
	
	def next (self):
		records_in_db = Record.objects.all()
		return Patient (random.choice(records_in_db))			
	pass

class DateGen (Thing):
	def __init__ (self, date):
		self.firstDay = date
		self.time = self.firstDay
	pass

	def next (self):
		delta = datetime.timedelta(
			days=random.randrange(0,100+1),
			hours=random.randrange(0,24+1),
			minutes=random.randrange(0,60+1),
		)
		self.time += delta
		return self.time
	pass

class DocumentGen (Thing):
	def __init__ (self, **map):
		pass
	
	def save (self):
		pass
	pass

# set up context
daygen = DateGen (datetime.datetime(1990, 1, 1, 0, 0))
mangen = PatientGen (patient_names) # create record here
hosgen = HospitalGen (hospital_names, doctor_names)
docgen = DocumentGen ()

print('start to reset database ...')
for count in range(100):
	day = daygen.next()
	man = mangen.next()
	hos = hosgen.next()
	dr  = hos.next_doctor()

	man.add_document(
		create_date=day,
		author=dr,
		hospital=hos,
		prescription='test #%u'%man.next_index(),
		publish_date=datetime.datetime.now(),
	)
print('done')
