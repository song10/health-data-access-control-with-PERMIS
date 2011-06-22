# Create your views here.

from django.http import HttpResponse
#import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
#from django.contrib.auth.decorators import login_required

#@login_required
@staff_member_required
def record (request):
	return HttpResponse("Hello, world. You're at the poll index.")
