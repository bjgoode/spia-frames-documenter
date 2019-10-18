from django import forms
from .models import *      


class AffiliationForm(forms.ModelForm):
    class Meta:
        model=Affiliation
        fields='__all__'
        
class AppealForm(forms.ModelForm):
    frame_input = forms.CharField(
        label='Frame',
        required=True,
        widget = forms.SelectMultiple(choices=[]),    
    )
    
    review_html = forms.CharField(
        required=True,
        widget=forms.HiddenInput(),    
    )

    field_order = [
        'text',
        'frame_input',
        'source',
        'is_explicit',
        'is_source',
    ]     
    
    class Meta:
        model=Appeal
        exclude=('frame','review','report')
        widgets = {
            'span_class': forms.HiddenInput(),    
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model=Author
        fields='__all__'

class ExpertiseForm(forms.ModelForm):
    class Meta:
        model=Expertise
        fields='__all__'

class FrameForm(forms.ModelForm):
      class Meta:
        model=Frame
        fields='__all__'
    
class MediaOrgForm(forms.ModelForm):
    class Meta:
        model=MediaOrg
        fields='__all__'
    
class MediaTypeForm(forms.ModelForm):
    class Meta:
        model=MediaType
        fields='__all__'

class ReportForm(forms.ModelForm):

    author_input = forms.CharField(
        label='Author(s)',
        required=True,
        widget = forms.SelectMultiple(choices=[]),    
    )
    media_org_input = forms.CharField(
        label='Media Organization',
        required=True,
        widget=forms.Select(choices=[]),  
    )
    media_type_input = forms.CharField(
        label='Media Type',
        required=False,
        widget=forms.Select(choices=[])    
    )

    field_order = [
        'title',
        'author_input',
        'media_org_input',
        'media_type_input',
        'section',
        'page',    
    ]    
    
    class Meta:
        model=Report
        exclude = [
            'author',
            'media_org',
            'report_text_html',  
        ]

class ReportSourceForm(forms.ModelForm):

    source_input = forms.CharField(
        label='Source',
        required=True,
        widget = forms.Select(choices=[]),    
    )    
    
    review_html = forms.CharField(
        required=True,
        widget=forms.HiddenInput(),    
    )

    field_order = [
        'text',
        'source_input',
        'affiliation',
    ]     
    
    class Meta:
        model=ReportSource
        exclude = ['report','review','expertise','source']
        widgets = {
            'span_class': forms.HiddenInput(),    
        }
    
class ReportSourceAffiliationForm(forms.ModelForm):

    affiliation_input = forms.CharField(
        label='Affiliation',
        required=True, 
        widget = forms.Select(choices=[]),
    )
    expertise_input = forms.CharField(
        label='Expertise',
        required=True,
        widget = forms.Select(choices=[]),    
    )
    
    review_html = forms.CharField(
        required=True,
        widget=forms.HiddenInput(),    
    )

    field_order = [
        'text',
        'affiliation_input',
        'expertise_input',
    ]   
    
    class Meta:
        model=ReportSourceAffiliation
        exclude=('affiliation','expertise','review')
        widgets = {
            'span_class': forms.HiddenInput(),    
        } 

class SourceForm(forms.ModelForm):
    class Meta:
        model=Source
        fields='__all__'
        