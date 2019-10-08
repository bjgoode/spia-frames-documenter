# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django import forms



# Create your models here.

# Models for Rating Frames/Sources/Affiliations
class Affiliation(models.Model):
    name = models.CharField(max_length = 100)
    
    
class Appeal(models.Model):
    frame = models.ManyToManyField('Frame')
    source = models.ManyToManyField('Source')
    text = models.TextField()
    is_explicit = models.BooleanField()
    is_support = models.BooleanField()
#    action foreign key????

class Author(models.Model):
    name = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

class Expertise(models.Model):
    desc = models.CharField(max_length = 45)
    
    def __str__(self):
        return self.desc

class Frame(models.Model):
    desc = models.CharField(max_length = 45)    
    
class MediaOrg(models.Model):
    org_name = models.CharField(max_length = 100)
    media_type = models.ForeignKey('MediaType', on_delete=models.CASCADE)
    
class MediaType(models.Model):
    type_desc = models.CharField(max_length = 45)    

class Report(models.Model):
    title = models.CharField(max_length = 255)
    section = models.CharField(max_length = 45, null=True, blank=True)
    page = models.PositiveIntegerField(null=True)
    media_org = models.ForeignKey('MediaOrg', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ManyToManyField('Author')
    report_text_html = models.TextField()

class ReportSource(models.Model):
    affiliation = models.ForeignKey('ReportSourceAffiliation', on_delete=models.CASCADE)
    expertise = models.ManyToManyField('Expertise')
    source = models.ForeignKey('Source', on_delete=models.CASCADE)
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    text = models.TextField()
    review = models.ForeignKey('Review', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return '{} ({}) - {}'.format(self.source.name, self.source.year_born, self.affiliation.affiliation.name)
    
class ReportSourceAffiliation(models.Model):
    affiliation = models.ForeignKey('Affiliation', on_delete=models.CASCADE)
    expertise = models.ForeignKey('Expertise', on_delete=models.CASCADE)
    text = models.TextField()
    review = models.ForeignKey('Review', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return '{} - {}'.format(self.affiliation.name, self.expertise.desc)

class Source(models.Model):
    name = models.CharField(max_length = 255)
    year_born = models.IntegerField() #add validation
    
    def __str__(self):
        return "{} (b.{})".format(self.name, self.year_born)

# Model for rating users.
class Review(models.Model):

    assignedTo = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='assigned_user'
        )    
    
    rated = models.BooleanField(default=False)
    rated_date = models.DateTimeField(null=True, blank=True)
    
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    