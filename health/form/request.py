#!/usr/bin/python
# -*- 
#coding: utf-8 -*-

'''
Created on Jun 3, 2011

@author: song10
'''
from suds.client import Client
from Thing import Thing

class My (object):
	issuer = "cn=song10,ou=admin,o=goverment,c=tw"
	
class Xacml (object):
	string = "http://www.w3.org/2001/XMLSchema#string"
	resource_id = "urn:oasis:names:tc:xacml:1.0:resource:resource-id"
	action_id = "urn:oasis:names:tc:xacml:1.0:action:action-id"
	
class Permis (object):
	permisRole = "urn:oid:1.2.826.0.1.3344810.1.1.14"
	
class Attribute (Thing):

	def __init__ (self, **args):
		self.name = None
		self.type = None
		self.value = None
		self.issuer = None
		self.__dict__.update(args)

	def say (self, **args):
		issuer_template = ''
		if self.issuer:
			issuer_template = ' Issuer="%(issuer)s"'%self
		self.issuer_template = issuer_template
		
		template = '''\
<xacml-context:Attribute AttributeId="%(name)s" DataType="%(type)s"%(issuer_template)s>
	<xacml-context:AttributeValue>%(value)s</xacml-context:AttributeValue>
</xacml-context:Attribute>
'''
		if not ('quiet' in args and args['quiet']):
			print(template%self)

		return template%self

class Elem (Thing):

	def __init__ (self):
		self.Attributes = Thing ()

	def add_attribute (self, attr):
		self.Attributes.set(attr.name, attr)

	def say (self, **args):
		template = '''\
<xacml-context:%(tag)s>
%(attributes)s
</xacml-context:%(tag)s>'''
		attr = ''
		for x in self.Attributes:
			attr += self.Attributes.get(x).say(quiet=True)
		
		t = Thing ()
		t.tag = args['tag']
		t.attributes = attr
		
		if not ('quiet' in args and args['quiet']):
			print(template%t)
			
		return template%t

class Subject (Elem):

	def __init__ (self):
		super(Subject, self).__init__()
		self.SubjectCategory = Thing ()

	def say (self, **args):
		return super(Subject, self).say(tag='Subject', **args)
		
class Resource (Elem):

	def __init__ (self):
		super(Resource, self).__init__()
		self.ResourceContent = Thing ()

	def say (self, **args):
		return super(Resource, self).say(tag='Resource', **args)
		
class Action (Elem):

	def __init__ (self):
		super(Action, self).__init__()
		pass

	def say (self, **args):
		return super(Action, self).say(tag='Action', **args)
		
class Environment (Elem):

	def __init__ (self):
		super(Environment, self).__init__()
		pass

	def say (self, **args):
		return super(Environment, self).say(tag='Environment', **args)
		

class Request (Thing):

	def __init__ (self):
		self.subject = Subject ()
		self.resource = Resource ()
		self.action = Action ()
		self.environment = Environment ()

	def __unicode__ (self):
		template = '<li>%(name)s : %(value)s %(type)s</li>'
		env = ''
		for x in sorted(self.environment.Attributes):
			y = self.environment.Attributes.get(x)
			d = {'name':y.name, 'value':y.value, 'type':"(%s)"%y.type}
			d['type'] = ''
			s = template % d
			env += s

		template = '''
<ul>
<li>Role : %(role)s</li>
<li>Action : %(action)s</li>
<li>Resource: %(resource)s</li>
%(env)s
</ul>
'''
		d = dict(
				role=self.subject.Attributes.user.value,
				resource=self.resource.Attributes.res.value,
				action=self.action.Attributes.act.value,
				env=env,
				)
		return template % d

	def say (self, **args):
		template = '''\
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
	xmlns:urn="urn:oasis:names:tc:xacml:2.0:context:schema:os">
	<soapenv:Header />
	<soapenv:Body>
		<xacml-context:Request
			xmlns:xacml-context="urn:oasis:names:tc:xacml:2.0:context:schema:os"
			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
			xsi:schemaLocation="urn:oasis:names:tc:xacml:2.0:context:schema:os http://docs.oasis-open.org/xacml/access_control-xacml-2.0-context-schema-os.xsd">
			%(subject)s
			%(resource)s
			%(action)s
			%(environment)s
		</xacml-context:Request>
	</soapenv:Body>
</soapenv:Envelope>
'''
		t = Thing ()
		t.subject = self.subject.say(quiet=True)
		t.resource = self.resource.say(quiet=True)
		t.action = self.action.say(quiet=True)
		t.environment = self.environment.say(quiet=True)
		
		if not ('quiet' in args and args['quiet']):
			print(template%t)
			
		return template%t

class Response (Thing):
	
	def __init__ (self, res):
		self.parse(res)
		
	def parse (self, res):
		result = res.getChild('soapenv:Envelope').getChild('soapenv:Body').getChild('urn:Response').getChild('urn:Result')
		deci = result.getChild('urn:Decision').getText()
		stat = result.getChild('urn:Status').getChild('urn:StatusCode').getAttribute('Value').getValue()
		self.Decision = deci
		self.StatusCode = stat.split(':')[-1]
	
	def say (self, **args):
		template = '''\
Decision="%(Decision)s", StatusCode="%(StatusCode)s"'''
		if not ('quiet' in args and args['quiet']):
			print(template%self)
		
		return template%self


def query (message): 
	url = "http://localhost:1104/axis2/services/AuthzService?wsdl" 
	client = Client(url)
	client.service.XACMLAuthzRequest(__inject={'msg':message.encode()})
	recvdata = client.last_received() 
#	senddata = client.last_sent() 
#	f = file('ss.txt', 'wb') 
#	f.write(str(senddata)) 
#	f.close() 
#	print senddata 
#	print '--------------------------------' 
#	print recvdata
#	print '--------------------------------' 
	return recvdata 

if __name__ == '__main__':
	req = Request ()
	subj = Attribute (name=Permis.permisRole, type=Xacml.string, value='patient', issuer=My.issuer)
	reso = Attribute (name=Xacml.resource_id, type=Xacml.string, value='http://localhost/center/document/6/')
	acti = Attribute (name=Xacml.action_id, type=Xacml.string, value='read')
#	arg0 = Attribute (name='arg0', type='String', value='testArg')
#	arg1 = Attribute (name='arg1', type='String', value='testArgEnv Yes')
	env0 = Attribute (name='subject', type='String', value='cn=Bruce,o=citizen,c=tw')
	env1 = Attribute (name='owner', type='String', value='cn=Bruce,o=citizen,c=tw')
	env2 = Attribute (name='test', type='String', value='123')
	req.subject.Attributes.role = subj
	req.resource.Attributes.res = reso
	req.action.Attributes.act = acti
#	req.action.add_attribute(arg0)
#	req.action.add_attribute(arg1)
	req.environment.add_attribute(env0)
	req.environment.add_attribute(env1)
#	req.environment.add_attribute(env2)
#	req.say()
	pass

	res = query(req.say(quiet=True))
	Response (res).say()
#	print(res)

#	env1.value += 'X'
#	res = query(req.say(quiet=True))
#	Response (res).say()
#
#	env1.value = env1.value[:-1]
#	res = query(req.say(quiet=True))
#	Response (res).say()
