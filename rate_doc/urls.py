from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path(r'<int:pk>/rate', login_required(edit_doc), name='rate-doc'),
    path(r'<int:pk>/report-affiliation/add/', login_required(AddAffiliation.as_view()), name='add-affiliation'),
    path(r'<int:pk>/report-source/add/', login_required(AddSource.as_view()), name='add-source'),
    path(r'<int:pk>/report-appeal/add/', login_required(AddAppeal.as_view()), name='add-appeal'),
    path(r'docs/', login_required(ReviewList.as_view()), name='doc-list'),
    path(r'success/', TemplateView.as_view(template_name='rate_doc/success.html'),name='success'),
    path(r'get-next/', get_next, name='get-next'),
    path(r'export/', login_required(Export), name='export'),
]