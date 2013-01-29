# Create your views here.
from django.shortcuts import render,redirect,render_to_response
from django.template import RequestContext

from .models import Publication,LabMember,Presentation

def publications(request):
    pubs = Publication.objects.all()
    #pub_format = '%s (%s). %s'
    return render_to_response('lab/publications.html',{'pubs':pubs},context_instance=RequestContext(request))

def people(request):
    members = LabMember.objects.all()
    #pub_format = '%s (%s). %s'
    return render_to_response('lab/people.html',{'members':members},context_instance=RequestContext(request))

def presentations(request):
    presents = Presentation.objects.all()
    #pub_format = '%s (%s). %s'
    return render_to_response('lab/presentations.html',{'presents':presents},context_instance=RequestContext(request))
    
def member(request,member_id):
    person = LabMember.objects.get(pk = member_id)
    return render_to_response('lab/member.html',{'person':person},context_instance=RequestContext(request))
