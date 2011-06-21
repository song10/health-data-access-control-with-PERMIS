import datetime
from center.models import Record, Document
 
print('start to reset database ...')
records = [
    (datetime.datetime(2007, 4, 1, 0, 0), 'cn=Alice,o=Citizen,c=Taiwan', None),
    (datetime.datetime(2008, 5, 1, 0, 0), 'cn=Bruce,o=Citizen,c=Taiwan', None),
    (datetime.datetime(2009, 6, 6, 0, 0), 'cn=Clark,o=Citizen,c=Taiwan', None),
]

records_in_db = Record.objects.all()
filter = [x.owner for x in records_in_db]
for x in records:
    if x[1] in filter:
        continue
    
    r = Record (create_date=x[0], owner=x[1], policy=x[2])
    r.save()
    print('add %s'%x[1])

print('done')
