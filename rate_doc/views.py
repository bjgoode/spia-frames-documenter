# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.utils import timezone
from django.views.generic import ListView, DetailView

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy

import csv
import ast
import bs4

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
class AddAffiliation(CreateView):
    model = ReportSourceAffiliation
    form_class = ReportSourceAffiliationForm
    template_name = 'rate_doc/affil-update.html'
    
    def get_success_url(self):
        return reverse_lazy('list-affil', kwargs={'pk':self.kwargs.get('pk')})  
    
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
    def get_success_url(self):
        return reverse_lazy('list-source', kwargs={'pk':self.kwargs.get('pk')})
    
    def form_valid(self, form):
        source_text = form.cleaned_data['source_input']
        source_name, source_born_year = source_text.split(' (')
        source_born_year = source_born_year.split(')')[0]
        source_born_year = source_born_year.split('b.')[-1]
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
    def get_success_url(self):
        return reverse_lazy('list-appeal', kwargs={'pk':self.kwargs.get('pk')})

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
    
class AddAction(CreateView):
    def get_success_url(self):
        return reverse_lazy('list-action', kwargs={'pk':self.kwargs.get('pk')})
    pass

## AJAX Update Classes
class UpdateReport(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'rate_doc/report-update.html'
    pk_url_kwarg = 'report_pk' 
    
    def get_success_url(self):
        return reverse_lazy('detail-report', kwargs={'pk':self.kwargs.get('pk')})
    
    def authors(self):
        return Author.objects.all()
        
    def media_org(self):
        return MediaOrg.objects.all()
        
    def media_type(self):
        return MediaType.objects.all()
        
    def initial_values(self):
        pk = self.kwargs.get('pk')
        media_org = Review.objects.get(pk=pk).report.media_org
        media_type = None
        if media_org:
            media_type = media_org.media_type
        dictionary = {
            'author': Review.objects.get(pk=pk).report.author.values_list('name', flat=True),
            'media_org': [media_org],
            'media_type': [media_type],
        }       
        return dictionary
    
    def form_valid(self, form):
        author_text = ast.literal_eval(form.cleaned_data['author_input'])
        authors = [Author.objects.get_or_create(name=a_t)[0] for a_t in author_text]

        media_org_text = form.cleaned_data['media_org_input']     
        if (MediaOrg.objects.filter(org_name=media_org_text).exists()):
            media_org = MediaOrg.objects.get(org_name=media_org_text)
            
        else:
            media_type_desc = form.cleaned_data['media_type_input']
            media_type, created = MediaType.objects.get_or_create(type_desc=media_type_desc)
            
            media_org = MediaOrg.objects.create(org_name=media_org_text, media_type=media_type)
        
        form.instance.author.set(authors)
        form.instance.media_org = media_org
        form.save()
        
        return super().form_valid(form)
        
        
class UpdateAffiliation(UpdateView):
    model = ReportSourceAffiliation
    form_class = ReportSourceAffiliationForm
    template_name = 'rate_doc/affil-update.html'
    pk_url_kwarg = 'affil_pk' 
      
    def get_success_url(self):
        return reverse_lazy('list-affil', kwargs={'pk':self.kwargs.get('pk')})

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
        
    def initial_values(self):
        pk = self.kwargs.get('affil_pk')       
        dictionary = {
            'affiliation': [ReportSourceAffiliation.objects.get(pk=pk).affiliation],
            'expertise':   [ReportSourceAffiliation.objects.get(pk=pk).expertise],
        }  
        return dictionary


class UpdateSource(UpdateView):
    model = ReportSource
    form_class = ReportSourceForm
    template_name = 'rate_doc/source-update.html'
    pk_url_kwarg = 'source_pk'
    def get_success_url(self):
        return reverse_lazy('list-source', kwargs={'pk':self.kwargs.get('pk')})
        
    def form_valid(self, form):
        source_text = form.cleaned_data['source_input']
        source_name, source_born_year = source_text.split(' (')
        source_born_year = source_born_year.split(')')[0]
        source_born_year = source_born_year.split('b.')[-1]
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
        
    def initial_values(self):
        pk = self.kwargs.get('source_pk')       
        dictionary = {
            'affiliation': [ReportSource.objects.get(pk=pk).affiliation.pk],
            'source_input':      [ReportSource.objects.get(pk=pk).source],
        }  
        return dictionary


class UpdateAppeal(UpdateView):
    model = Appeal
    form_class = AppealForm
    template_name = 'rate_doc/appeal-update.html'
    pk_url_kwarg = 'appeal_pk'
    def get_success_url(self):
        return reverse_lazy('list-appeal', kwargs={'pk':self.kwargs.get('pk')})

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
        
    def initial_values(self):
        pk = self.kwargs.get('appeal_pk')       
        dictionary = {
            'frame_input': Appeal.objects.get(pk=pk).frame.values_list('desc', flat=True),
            'source_input': [Appeal.objects.get(pk=pk).source],
        }  
        return dictionary

class UpdateAction(UpdateView):
    def get_success_url(self):
        return reverse_lazy('list-action', kwargs={'pk':self.kwargs.get('pk')})
    pass
    
class ReviewDetail(DetailView):
    model = Review
    context_object_name = 'doc'
    
class DeleteSource(DeleteView):
    model = ReportSource
    success_url = '/'
    pk_url_kwarg = 'source_pk'
    template_name = 'rate_doc/confirm-delete.html'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        
        rs = ReportSource.objects.get(pk=self.kwargs.get('source_pk'))
        soup = bs4.BeautifulSoup(rs.review.review_html)
        span = soup.find('span', class_=rs.span_class)
        if span:
            span.unwrap()
            rs.review.review_html = str(soup)
            rs.review.save() 
        
        return super().post(request, *args, **kwargs)
        
    def get_success_url(self):
        return reverse_lazy('list-source', kwargs={'pk':self.kwargs.get('pk')})
    
    
class DeleteAffiliation(DeleteView):
    model = ReportSourceAffiliation
    pk_url_kwarg = 'affil_pk'
    template_name = 'rate_doc/confirm-delete.html'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):

        aff = ReportSourceAffiliation.objects.get(pk=self.kwargs.get('affil_pk'))
        soup = bs4.BeautifulSoup(aff.review.review_html)
        span = soup.find('span', class_=aff.span_class)
        if span:
            span.unwrap()
            aff.review.review_html = str(soup)
            aff.review.save()   
        
        return super().post(request, *args, **kwargs)
        
    def get_success_url(self):
        return reverse_lazy('list-affil', kwargs={'pk':self.kwargs.get('pk')}) 
    

class DeleteAppeal(DeleteView):
    model = Appeal
    success_url = '/'
    pk_url_kwarg = 'appeal_pk'
    template_name = 'rate_doc/confirm-delete.html'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):

        html_object = Appeal.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        soup = bs4.BeautifulSoup(html_object.review.review_html)
        span = soup.find('span', class_=html_object.span_class)
        if span:
            span.unwrap()
            html_object.review.review_html = str(soup)
            html_object.review.save()   
        
        return super().post(request, *args, **kwargs)
        
    def get_success_url(self):
        return reverse_lazy('list-appeal', kwargs={'pk':self.kwargs.get('pk')})
    
    
class DeleteAction(DeleteView):
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        
    def get_success_url(self):
        return reverse_lazy('list-action', kwargs={'pk':self.kwargs.get('pk')})
    pass
    

def finalize(request, pk):
    doc = Review.objects.get(pk=pk)
    doc.rated = True
    doc.rated_date = timezone.now()
    
    doc.save()
    
    return HttpResponseRedirect(reverse('rate-doc', kwargs={'pk': doc.id}))
    

def edit_doc(request, pk):
    if request.method == "POST":
        return HttpResponseRedirect(reverse('get-next'))
        
    else:
        doc = Review.objects.get(pk=pk)        
        
        if doc.rated:
            outDict = {
                'doc': doc
            }
            return render(request, template_name='rate_doc/doc_final.html', context=outDict)
            
        else:
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

def preview(request, pk):

    doc = Review.objects.get(pk=pk)        
    
    report = doc.report
    reportSources = doc.reportsource_set
    appeals = doc.appeal_set
    reportsourceaffiliations = doc.reportsourceaffiliation_set
    
    outDict = {
        'doc': doc,
        'report': report,
        'reportsourceaffiliations': reportsourceaffiliations,
        'report_sources': reportSources,
        'appeals': appeals,
    }      
        
    return render(request, template_name='rate_doc/preview.html', context=outDict)

class ReviewList(ListView):
    model = Review
    template_name = "rate_doc/doc_list.html"      


def get_next(request):

    unrated_docs = Review.objects.filter(rated=False)
    assigned_docs = unrated_docs.filter(assignedTo=request.user.pk).order_by('pk')
    
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