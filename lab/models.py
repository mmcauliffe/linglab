from django.db import models
from mezzanine.pages.models import Page

from .helper import generate_file_name

# Create your models here.
    

class LabMember(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    
    research_interests = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    picture = models.ImageField(upload_to='people',null=True,blank=True)
    position = models.ForeignKey('Position')
    
    class Meta:
        ordering = ['position__importance','last_name','first_name']
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name,self.last_name)
    
class Collaborator(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    link = models.URLField(max_length=250,null=True,blank=True)
    listable = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['last_name','first_name']
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name,self.last_name)
    
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
            return '%s, %s.' % (authors[0].last_name,authors[0].first_name[0])
        author_string = '%s and %%s' % ('%s, ' * (len(authors)-1))
        author_string = author_string % tuple('%s, %s.' % (x.last_name,x.first_name[0]) for x in authors)
        return author_string
        
    def generate_key(self):
        author_name = self.get_authors()[0].last_name
        first_word = self.title.split(" ")[0]
        key = '%s%d%s' % (author_name,self.year,first_word)
        return key
        
    def get_bibtex(self):
        tex = 
        tex = """@article{%s,
                        title = {%s},
                        author = {%s},
                        journal = {%s},
                        volume = {%d},
                        number = {%d},
                        pages = {%s},
                        year = {%d}
                        }
                """ % (self.generate_key(),self.title,self.get_author_string(),
                        self.journal,self.volume,self.number,self.pages,self.year)
        return tex
    
        
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
            return '%s, %s.' % (authors[0].last_name,authors[0].first_name[0])
        author_string = '%s and %%s' % ('%s, ' * (len(authors)-1))
        author_string = author_string % tuple('%s, %s.' % (x.last_name,x.first_name[0]) for x in authors)
        return author_string
        
    def generate_key(self):
        key = '%s%d%s' % (self.get_authors()[0].last_name,self.year,self.title.split(" ")[0])
        return key
    
    
class Position(models.Model):
    title = models.CharField(max_length = 100)
    importance = models.IntegerField()
    
    def __unicode__(self):
        return self.title
