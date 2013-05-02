# Create your views here.
from django.shortcuts import render,redirect,render_to_response
from django.template import RequestContext

from .models import Publication,LabMember,Presentation,Collaborator

def publications(request):
    pubs = Publication.objects.all()
    #pub_format = '%s (%s). %s'
    return render_to_response('lab/publications.html',{'pubs':pubs},context_instance=RequestContext(request))

def people(request):
    members = LabMember.objects.all()
    collabs = Collaborator.objects.filter(listable=True)
    #pub_format = '%s (%s). %s'
    return render_to_response('lab/people.html',{'members':members,'collabs':collabs},context_instance=RequestContext(request))

def presentations(request):
    presents = Presentation.objects.all()
    #pub_format = '%s (%s). %s'
    return render_to_response('lab/presentations.html',{'presents':presents},context_instance=RequestContext(request))
    
def member(request,member_id):
    person = LabMember.objects.get(pk = member_id)
    return render_to_response('lab/member.html',{'person':person},context_instance=RequestContext(request))

def presentation_bibtex(request,pk):
    try:
        pres = Presentation.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return redirect(presentations)
    key = pres.generate_key()
    bib = pres.get_bibtex()
    response = HttpResponse(bib,mimetype='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s.txt' % key
    return response
    
def publication_bibtex(request,pk):
    try:
        pub = Publication.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return redirect(publications)
    key = pub.generate_key()
    bib = pub.get_bibtex()
    response = HttpResponse(bib,mimetype='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s.txt' % key
    return response
    
