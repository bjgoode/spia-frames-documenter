from django import forms
#from django_select2.forms import Select2TagWidget, Select2TagMixin
from .models import *

#class TagWidget(Select2TagWidget):
#    
#    def build_attrs(self, *args, **kwargs):
#        """Add select2's tag attributes."""
#        self.attrs.setdefault('data-minimum-input-length', 1)
#        self.attrs.setdefault('data-tags', 'true')
#        self.attrs.setdefault('data-token-separators', '[","]')
#        return super(Select2TagMixin, self).build_attrs(*args, **kwargs)
#
#    def optgroups(self, name, value, attrs=None):
#        values = value[0].split(',') if value[0] else []
#        selected = set(values)
#        subgroup = [self.create_option(name, v, v, selected, i) for i, v in enumerate(values)]
#        return [(None, subgroup, 0)]
#        
#    def value_from_datadict(self, data, files, name):
#        values = super(TagWidget, self).value_from_datadict(data, files, name)
#        return ",".join(values)
        

class AffiliationForm(forms.ModelForm):
    class Meta:
        model=Affiliation
        fields='__all__'
        
class AppealForm(forms.ModelForm):
    class Meta:
        model=Appeal
        fields='__all__'
#        widgets = {
#            'frame': TagWidget,        
#        }

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
#        widgets = {
#            'media_org': TagWidget,
#            'author': TagWidget,     
#        }

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
        