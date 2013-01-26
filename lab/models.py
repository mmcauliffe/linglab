from django.db import models
from mezzanine.pages.models import Page

from .helper import generate_file_name

# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name,self.last_name)
    

class LabMember(Person):
    
    research_interests = models.TextField()
    email = models.EmailField()
    picture = models.ImageField(upload_to='people')
    position = models.ForeignKey('Position')
    
    class Meta:
        ordering = ['position__importance','last_name','first_name']
    
class Collaborator(Person):
    link = models.URLField(max_length=250)
    
    class Meta:
        ordering = ['last_name','first_name']
    
class WrittenByLab(models.Model):
    person = models.ForeignKey(LabMember)
    publication = models.ForeignKey('ResearchResult')
    author_number = models.IntegerField()
    
    class Meta:
        ordering = ['author_number']
    
class WrittenByCollab(models.Model):
    person = models.ForeignKey(Collaborator)
    publication = models.ForeignKey('ResearchResult')
    author_number = models.IntegerField()
    
    class Meta:
        ordering = ['author_number']
        
class ResearchResult(models.Model):
    lab_author = models.ManyToManyField(LabMember,through='WrittenByLab')
    collaborator_author = models.ManyToManyField(Collaborator,through='WrittenByCollab')
    year = models.IntegerField()
    title = models.CharField(max_length=500)
    pdf = models.FileField(upload_to = generate_file_name)
    
    class Meta:
        ordering = ['-year','title']
    
    def get_authors(self):
        labs = list(self.lab_authorset.all())
        collabs = list(self.collaborator_authorset.all())
        author_list = []
        for i in range(1,len(labs)+len(collabs)+1):
            if labs[0].author_number < collabs[0].author_number:
                author_list.append(labs.pop(0))
            else:
                author_list.append(collabs.pop(0))
        return author_list
        
    def get_author_string(self):
        authors = self.get_authors()
        if len(authors) == 0:
            return '%s, %s.' % (authors[0].last_name,authors[0].first_name[0])
        author_string = '%s and %%s' % ('%s, ' * (len(authors)-1))
        author_string = author_string % tuple('%s, %s.' % (x.last_name,x.first_name[0]) for x in authors)
        return author_string
        
    def generate_key(self):
        key = '%s%d%s' % (self.get_authors()[0].last_name,self.year,self.title.split(" ")[0])
        return key
    
    
class Publication(ResearchResult):
    journal = models.CharField(max_length=250)
    volume = models.IntegerField()
    number = models.IntegerField()
    pages = models.CharField(max_length=100)
        
    def get_bibtext(self):
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
    
        
class Presentation(ResearchResult):
    conference = models.CharField(max_length = 500)
    location = models.CharField(max_length = 250)
    
    
class Position(models.Model):
    title = models.CharField(max_length = 100)
    importance = models.IntegerField()
