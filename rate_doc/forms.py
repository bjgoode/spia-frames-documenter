from django import forms
from django_select2.forms import Select2TagWidget, Select2TagMixin

from .models import *

class TagWidget(Select2TagWidget):
    
    def build_attrs(self, *args, **kwargs):
        """Add select2's tag attributes."""
        self.attrs.setdefault('data-minimum-input-length', 1)
        self.attrs.setdefault('data-tags', 'true')
        self.attrs.setdefault('data-token-separators', '[","]')
        return super(Select2TagMixin, self).build_attrs(*args, **kwargs)
        

class AffiliationForm(forms.ModelForm):
    class Meta:
        model=Affiliation
        fields='__all__'
        
class AppealForm(forms.ModelForm):
    class Meta:
        model=Appeal
        fields='__all__'
        widgets = {
            'frame': TagWidget,        
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
    class Meta:
        model=Report
        exclude = ['report_text_html']
        widgets = {
            'media_org': TagWidget,
            'author': TagWidget,     
        }

class ReportSourceForm(forms.ModelForm):
    class Meta:
        model=ReportSource
        exclude = ['report']
        widgets = {
            'affiliation': TagWidget,
            'expertise': TagWidget,
            'source': TagWidget,     
        }
    
class ReportSourceAffiliationForm(forms.ModelForm):
    class Meta:
        model=ReportSourceAffiliation
        fields='__all__'
        widgets = {
            'affiliation': TagWidget,
            'expertise': TagWidget,    
        }

class SourceForm(forms.ModelForm):
    class Meta:
        model=Source
        fields='__all__'
        