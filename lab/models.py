from collections import OrderedDict
from django.db import models
from mezzanine.pages.models import Page

from .helper import generate_file_name

# Create your models here.
    

class LabMember(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    
    keywords = models.CharField(max_length=250)
    research_interests = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    picture = models.ImageField(upload_to='people',null=True,blank=True)
    position = models.ForeignKey('Position')
    
    class Meta:
        ordering = ['position__importance','last_name','first_name']
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name,self.last_name)
        
    def get_bib_name(self):
        return u'%s, %s.' % (self.last_name, self.first_name[0])
    
class Collaborator(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    link = models.URLField(max_length=250,null=True,blank=True)
    listable = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['last_name','first_name']
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name,self.last_name)
        
    def get_bib_name(self):
        return u'%s, %s.' % (self.last_name, self.first_name[0])
    
class WrittenByLab(models.Model):
    person = models.ForeignKey(LabMember)
    publication = models.ForeignKey('Publication')
    author_number = models.IntegerField()
    
    class Meta:
        ordering = ['author_number']
    
class WrittenByCollab(models.Model):
    person = models.ForeignKey(Collaborator)
    publication = models.ForeignKey('Publication')
    author_number = models.IntegerField()
    
    class Meta:
        ordering = ['author_number']
    
class PresentedByLab(models.Model):
    person = models.ForeignKey(LabMember)
    publication = models.ForeignKey('Presentation')
    author_number = models.IntegerField()
    
    class Meta:
        ordering = ['author_number']
    
class PresentedByCollab(models.Model):
    person = models.ForeignKey(Collaborator)
    publication = models.ForeignKey('Presentation')
    author_number = models.IntegerField()
    
    class Meta:
        ordering = ['author_number']
    
    
class Publication(models.Model):
    STATE_CHOICES = (('published','Published'),
                    ('in press','In press'),
                    ('under review','Under review'),
                    ('under revision','Under revision'),
                    )
    lab_author = models.ManyToManyField(LabMember,through='WrittenByLab')
    collaborator_author = models.ManyToManyField(Collaborator,through='WrittenByCollab')
    year = models.IntegerField()
    title = models.CharField(max_length=500)
    pdf = models.FileField(upload_to = generate_file_name,null=True,blank=True)
    
    journal = models.CharField(max_length=250)
    volume = models.IntegerField(null=True,blank=True)
    number = models.IntegerField(null=True,blank=True)
    pages = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=50,choices=STATE_CHOICES)
    
    class Meta:
        ordering = ['-year','title']
    
    def get_authors(self):
        labs = list(WrittenByLab.objects.filter(publication=self))
        collabs = list(WrittenByCollab.objects.filter(publication=self))
        author_list = labs+collabs
        author_list.sort(key=lambda x: x.author_number)
        author_list = [x.person for x in author_list]
        return author_list
        
    def get_author_string(self):
        authors = self.get_authors()
        if len(authors) == 1:
            return authors[0].get_bib_name()
        author_string = '%sand %%s' % ('%s, ' * (len(authors)-1))
        author_string = author_string % tuple(x.get_bib_name()  for x in authors)
        return author_string
    
    def get_extra(self):
        extra = ', '.join([x for x in [self.volume,self.number,self.pages] if x is not None])
        if extra != '':
            extra = ', '+extra
        return extra
    
    def generate_file_name(self):
        title = self.title.replace(" ",'')[:20]
        key = '%d%s' % (self.year,title)
        return key
        
    def generate_key(self):
        author_name = self.get_authors()[0].last_name
        first_word = self.title.split(" ")[0]
        key = '%s%d%s' % (author_name,self.year,first_word)
        return key
        
    def get_bibtex(self):
        tex = "@article{%s,\ntitle = {%s},\nauthor = {%s},\njournal = {%s},\nyear = {%d}%s\n}" 
        extra = OrderedDict({'volume': self.volume, 'number': self.number,'pages': self.pages})
        extra = ['%s = {%s}' % (k, str(v)) for k, v in extra.items() if v is not None]
        extra = ',\n'.join(extra)
        if extra != '':
            extra = ',\n' + extra
        return tex % (self.generate_key(),self.title,self.get_author_string(),
                        self.journal,self.year,extra)
    
        
class Presentation(models.Model):
    lab_author = models.ManyToManyField(LabMember,through='PresentedByLab')
    collaborator_author = models.ManyToManyField(Collaborator,through='PresentedByCollab')
    year = models.IntegerField()
    title = models.CharField(max_length=500)
    pdf = models.FileField(upload_to = generate_file_name,null=True,blank=True)
    
    conference = models.CharField(max_length = 500)
    location = models.CharField(max_length = 250)
    
    class Meta:
        ordering = ['-year','title']
    
    def get_authors(self):
        labs = list(PresentedByLab.objects.filter(publication=self))
        collabs = list(PresentedByCollab.objects.filter(publication=self))
        author_list = labs+collabs
        author_list.sort(key=lambda x: x.author_number)
        author_list = [x.person for x in author_list]
        return author_list
        
    def get_author_string(self):
        authors = self.get_authors()
        if len(authors) == 1:
            return authors[0].get_bib_name()
        author_string = '%sand %%s' % ('%s, ' * (len(authors)-1))
        author_string = author_string % tuple(x.get_bib_name() for x in authors)
        return author_string
        
    def generate_file_name(self):
        title = self.title.replace(" ",'')[:20]
        key = '%d%s' % (self.year,title)
        return key
        
    def generate_key(self):
        key = '%s%d%s' % (self.get_authors()[0].last_name,self.year,self.title.split(" ")[0])
        return key
        
    def get_bibtex(self):
        tex = "@inproceedings{%s,\ntitle = {%s},\nauthor = {%s},\npublisher = {Proceedings of the %s},\nyear = {%d}\n}" 
        return tex % (self.generate_key(),self.title,self.get_author_string(),
                        ', '.join([self.conference,self.location]),self.year)
    
    
class Position(models.Model):
    title = models.CharField(max_length = 100)
    importance = models.IntegerField()
    
    class Meta:
        ordering = ['importance','title']
        
    def __unicode__(self):
        return self.title

class Experiment(models.Model):
    STATUS_CHOICES = (('N','Not available'),
                    ('O','Ongoing'),
                    ('F','Finished'),
                    )
    title = models.CharField(max_length = 250)
    description = models.CharField(max_length = 1000)
    requirements = models.CharField(max_length = 500)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES)
    reimbursement_and_time = models.CharField(max_length = 250)
    contact = models.ForeignKey(LabMember)
    
    class Meta:
        ordering = ['status','title']
