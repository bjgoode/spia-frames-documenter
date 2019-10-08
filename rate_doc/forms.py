from django import forms
#from django_select2.forms import Select2TagWidget, Select2TagMixin
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
    class Meta:
        model=Report
        exclude = ['report_text_html']

class ReportSourceForm(forms.ModelForm):

    source_input = forms.CharField(
        label='Source',
        required=True,
        widget = forms.Select(choices=[]),    
    )    

    field_order = [
        'text',
        'source_input',
        'affiliation',
    ]     
    
    class Meta:
        model=ReportSource
        exclude = ['report','review','expertise','source']
    
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

    field_order = [
        'text',
        'affiliation_input',
        'expertise_input',
    ]    
    
    class Meta:
        model=ReportSourceAffiliation
        exclude=('affiliation','expertise','review')

class SourceForm(forms.ModelForm):
    class Meta:
        model=Source
        fields='__all__'
        