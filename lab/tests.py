"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from lab.models import *
from django.test import TestCase
from django.core.files import File


class SimpleTest(TestCase):
    def setUp(self):
        """
        Set up for testing models.
        """
        self.p1 = Position.objects.create(title='Grad student', importance=3)
        self.p2 = Position.objects.create(title='Undergrad', importance=4)
        self.lm1 = LabMember.objects.create(first_name='Michael',last_name='McAuliffe',position=self.p1)
        self.lm2 = LabMember.objects.create(first_name='Sophie',last_name='Walters',position=self.p2)
        self.cl = Collaborator.objects.create(first_name = 'Grant', last_name = 'McGuire')
        
        self.pres1 = Presentation.objects.create(year=2012,title='Blah blah blah',conference='Blah academy',location='Vancouver, BC',pdf=File(open('/home/speecon/Downloads/NWLC_presentation.pdf')))
        PresentedByLab.objects.create(person=self.lm1,publication=self.pres1,author_number = 1)
        PresentedByLab.objects.create(person=self.lm2,publication=self.pres1,author_number = 2)
        self.pres2 = Presentation.objects.create(year=2012,title='Blah blah blah',conference='Blah academy',location='Vancouver, BC')
        PresentedByLab.objects.create(person=self.lm1,publication=self.pres2,author_number = 1)
        PresentedByCollab.objects.create(person=self.cl,publication=self.pres2,author_number = 2)
        PresentedByLab.objects.create(person=self.lm2,publication=self.pres2,author_number = 3)
        
        self.pub1 = Publication.objects.create(year=2012,title='Blah blah blah',journal='Journal of Blah',state='published')
        WrittenByLab.objects.create(person=self.lm1,publication=self.pub1,author_number = 1)
        WrittenByLab.objects.create(person=self.lm2,publication=self.pub1,author_number = 2)
        self.pub2 = Publication.objects.create(year=2012,title='Blah blah blah',journal='Journal of Blah',state='published',volume=2,pages='1440-1442')
        WrittenByLab.objects.create(person=self.lm1,publication=self.pub2,author_number = 1)
        WrittenByCollab.objects.create(person=self.cl,publication=self.pub2,author_number = 2)
        WrittenByLab.objects.create(person=self.lm2,publication=self.pub2,author_number = 3)
        
        self.exp1 = Experiment.objects.create(title = 'Experiment title',description = 'Blah blah.',requirements = 'So many requirements', reimbursement_and_time = '$10 per hour for one hour',status = 'O', contact = self.lm2)
    
        self.exp2 = Experiment.objects.create(title = 'Experiment title',description = 'Blah blah.',requirements = 'So many requirements', reimbursement_and_time = '$10 per hour for one hour',status = 'F', contact = self.lm2)
   
    def test_views(self):
        response = self.client.get("/lab/people/")
        self.assertEqual(response.status_code,200)
        response = self.client.get("/lab/member/1/")
        self.assertEqual(response.status_code,200)
        response = self.client.get("/lab/publications/")
        self.assertEqual(response.status_code,200)
        response = self.client.get("/lab/presentations/")
        self.assertEqual(response.status_code,200)
        response = self.client.get("/lab/studies/")
        self.assertEqual(response.status_code,200)
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code,200)
        response = self.client.get("/")
        self.assertEqual(response.status_code,200)
    
    def test_lab_presentations(self):
        self.assertEqual(self.pres1.get_authors(), [self.lm1,self.lm2])
        self.assertEqual(self.pres1.generate_key(), 'McAuliffe2012Blah')
    
    def test_colab_presentations(self):
        self.assertEqual(self.pres2.get_authors(), [self.lm1,self.cl,self.lm2])
        self.assertEqual(self.pres2.generate_key(), 'McAuliffe2012Blah')
    
    def test_lab_pubs(self):
        self.assertEqual(self.pub1.get_authors(), [self.lm1,self.lm2])
        self.assertEqual(self.pub1.generate_key(), 'McAuliffe2012Blah')
    
    def test_colab_pubs(self):
        self.assertEqual(self.pub2.get_authors(), [self.lm1,self.cl,self.lm2])
        self.assertEqual(self.pub2.generate_key(), 'McAuliffe2012Blah')
        
    def test_pubs_bibtex(self):
        tex = "@article{McAuliffe2012Blah,\ntitle = {Blah blah blah},\nauthor = {McAuliffe, M., McGuire, G., and Walters, S.},\njournal = {Journal of Blah},\nyear = {2012},\nvolume = {2},\npages = {1440-1442}\n}" 
        self.assertEqual(self.pub2.get_bibtex(), tex)
