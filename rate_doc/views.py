# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy

import csv
import ast

from .models import Review
from .forms import *

# Create your views here.

class ReviewUpdate(UpdateView):
    model = Review
    fields = [
        'report',
        ]
        
    template_name = "rate_doc/doc_edit.html"
    
    def form_valid(self, form):
        form.instance.ratedBy = self.request.user
        form.instance.rated = True
        form.save()
        return HttpResponseRedirect(reverse('get-next'))

## AJAX Add Classes    
class AddAffiliation(FormView):
    model = ReportSourceAffiliation
    form_class = ReportSourceAffiliationForm
    template_name = 'rate_doc/affil-update.html'
    success_url = reverse_lazy('success')   
    
    def form_valid(self, form):                
        
        affiliation = Affiliation.objects.get_or_create(name=form.cleaned_data['affiliation_input'])[0]
        expertise = Expertise.objects.get_or_create(desc=form.cleaned_data['expertise_input'])[0]

        review = Review.objects.get(pk=self.kwargs.get('pk',None))
        review.review_html = form.cleaned_data['review_html']
        review.save()

        form.instance.affiliation = affiliation
        form.instance.expertise = expertise
        form.instance.review = review
        form.save()
        
        return super().form_valid(form)
        
    def affiliations(self):
        return Affiliation.objects.all()
        
    def expertise(self):
        return Expertise.objects.all()
        
    
class AddSource(CreateView):
    model = ReportSource
    form_class = ReportSourceForm
    template_name = 'rate_doc/source-update.html'
    success_url = reverse_lazy('success')
    
    def form_valid(self, form):
        source_text = form.cleaned_data['source_input']
        source_name, source_born_year = source_text.split(' (')
        source_born_year = source_born_year.split(')')[0]
        source = Source.objects.get_or_create(name=source_name,year_born=source_born_year)[0]

        review = Review.objects.get(pk=self.kwargs.get('pk',None))
        review.review_html = form.cleaned_data['review_html']
        review.save()

        form.instance.source = source
        form.instance.report = review.report
        form.instance.review = review
        form.save()
        
        return super().form_valid(form)
        
    def affiliations(self):
        return
        
    def sources(self):
        return Source.objects.all()
    
class AddAppeal(CreateView):
    model = Appeal
    form_class = AppealForm
    template_name = 'rate_doc/appeal-update.html'
    success_url = reverse_lazy('success')

    def form_valid(self, form):

        review = Review.objects.get(pk=self.kwargs.get('pk',None))
        review.review_html = form.cleaned_data['review_html']
        review.save()        
        
        form.instance.report = review.report
        form.instance.review = review
        form.save()
        
        frame_desc = ast.literal_eval(form.cleaned_data['frame_input'])
        frames = [Frame.objects.get_or_create(desc=f)[0] for f in frame_desc]
        form.instance.frame.set(frames)
        
        return super().form_valid(form)    
    
    def frames(self):
        return Frame.objects.all()
    

## AJAX Update Classes
class UpdateReport(UpdateView):
    model = Report
    success_url = '/'
        
class UpdateAffiliation(UpdateView):
    model = ReportSourceAffiliation
    success_url = '/'
    
class DeleteAffiliation(DeleteView):
    model = ReportSourceAffiliation
    success_url = '/'

def edit_doc(request, pk):
    if request.method == "POST":
        return HttpResponseRedirect(reverse('get-next'))
        
    else:
        doc = Review.objects.get(pk=pk)        
        
        report_form = ReportForm(instance=doc.report)
        reportSource_form = ReportSourceForm()
        appeal_form = AppealForm
        reportsourceaffiliation_form = ReportSourceAffiliationForm
        
        outDict = {
            'doc': doc,
            'report_form': report_form,
            'reportsourceaffiliation_form': reportsourceaffiliation_form,
            'reportSource_form': reportSource_form,
            'appeal_form': appeal_form,
        }      
        
    return render(request, template_name='rate_doc/doc_edit.html', context=outDict)


class ReviewList(ListView):
    model = Review
    template_name = "rate_doc/doc_list.html"      


def get_next(request):

    unrated_docs = Review.objects.filter(rated=False)
    assigned_docs = unrated_docs.filter(assignedTo=request.user.pk)
    
    if unrated_docs:
        if assigned_docs:
            doc = assigned_docs.first()
        else:
            doc = Review.objects.filter(rated=False,assignedTo=None).first()
            doc.assignedTo = request.user
            doc.save()
        
        return HttpResponseRedirect(reverse('rate-doc', kwargs={'pk':doc.pk}))
        
    return HttpResponseRedirect(reverse('index'))
    
def Export(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="document_ratings.csv"'

    writer = csv.writer(response, quoting=csv.QUOTE_ALL)
    
    fields = [
        'pk',
        'rated',  
        'ratedBy__username',
        'articleTopic',
        'productName',
        'companyName',
        'dateOfApprovalOrLaunch',
        'countryOfLaunch',
        'otherCompanies',
        'otherProducts',
        'article_title',
        'subject',
        'company',
        'publication_title',
        'publication_date',
        'publication_subject',
        'source_type',
        'document_type',
        'html',
    ]    

    writer.writerow(fields)    
    
    docs = Review.objects.all().values_list(*fields)
    for doc in docs:
        writer.writerow(doc)
        
    return response