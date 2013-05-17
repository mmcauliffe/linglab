# Create your views here.
from django.shortcuts import render,redirect,render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import ListView,DetailView

from .models import Publication,LabMember,Presentation,Collaborator,Experiment

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
    
class PresentationListView(ListView):
    model = Presentation
    context_object_name = 'pres'
    template_name = 'lab/presentations.html'
    
class PublicationListView(ListView):
    model = Publication
    context_object_name = 'pubs'
    template_name = 'lab/publications.html'
    
class MemberDetailView(DetailView):
    model = LabMember
    template_name = 'lab/member.html'
    context_object_name = 'member'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['pubs'] = context['member'].publication_set.all()
        context['pres'] = context['member'].presentation_set.all()
        return context

class MemberListView(ListView):
    model = LabMember
    context_object_name = 'members'
    template_name = 'lab/people.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MemberListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['collabs'] = Collaborator.objects.all()
        return context

class ExperimentListView(ListView):
    model = Experiment
    context_object_name = 'exp'
    template_name = 'lab/experiments.html'
    queryset = Experiment.objects.filter(status = 'O')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ExperimentListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['PI'] = None
        pis = LabMember.objects.filter(position__importance = 1)
        if len(pis) > 0:
            context['PI'] = pis[0]
        return context
    

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
    #response['Content-Disposition'] = 'attachment; filename=%s.txt' % key
    return response
    
def publication_bibtex(request,pk):
    try:
        pub = Publication.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return redirect(publications)
    key = pub.generate_key()
    bib = pub.get_bibtex()
    response = HttpResponse(bib,mimetype='text/plain')
    #response['Content-Disposition'] = 'attachment; filename=%s.txt' % key
    return response
    
