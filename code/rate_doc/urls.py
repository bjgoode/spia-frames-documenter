from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path(r'<int:pk>/rate', login_required(edit_doc), name='rate-doc'),
    path(r'<int:pk>/preview', login_required(preview), name='preview-doc'),
    path(r'<int:pk>/finalize', login_required(finalize), name='finalize-doc'),

    path(r'<int:pk>/report/<int:report_pk>/update/', login_required(UpdateReport.as_view()), name='update-report'),
    path(r'<int:pk>/report/detail/', login_required(ReviewDetail.as_view(template_name='rate_doc/report-detail.html')), name='detail-report'),
    path(r'<int:pk>/report/html/', login_required(ReviewDetail.as_view(template_name='rate_doc/report-html.html')), name='report-html'),        
    
    path(r'<int:pk>/report-affiliation/add/', login_required(AddAffiliation.as_view()), name='add-affiliation'),
    path(r'<int:pk>/report-affiliation/list/', login_required(ReviewDetail.as_view(template_name ='rate_doc/affil-list.html')), name='list-affil'),
    path(r'<int:pk>/report-affiliation/<int:affil_pk>/update/', login_required(UpdateAffiliation.as_view()), name='update-affiliation'),
    path(r'<int:pk>/report-affiliation/<int:affil_pk>/delete/', login_required(DeleteAffiliation.as_view()), name='delete-affiliation'),
    
    path(r'<int:pk>/report-source/add/', login_required(AddSource.as_view()), name='add-source'),
    path(r'<int:pk>/report-source/list/', login_required(ReviewDetail.as_view(template_name ='rate_doc/source-list.html')), name='list-source'),
    path(r'<int:pk>/report-source/<int:source_pk>/update/', login_required(UpdateSource.as_view()), name='update-source'),
    path(r'<int:pk>/report-source/<int:source_pk>/delete/', login_required(DeleteSource.as_view()), name='delete-source'),
    
    path(r'<int:pk>/report-appeal/add/', login_required(AddAppeal.as_view()), name='add-appeal'),
    path(r'<int:pk>/report-appeal/list/', login_required(ReviewDetail.as_view(template_name ='rate_doc/appeal-list.html')), name='list-appeal'),
    path(r'<int:pk>/report-appeal/<int:appeal_pk>/update/', login_required(UpdateAppeal.as_view()), name='update-appeal'),
    path(r'<int:pk>/report-appeal/<int:appeal_pk>/delete/', login_required(DeleteAppeal.as_view()), name='delete-appeal'),
    
    path(r'<int:pk>/report-action/add/', login_required(AddReportAction.as_view()), name='add-action'),
    path(r'<int:pk>/report-action/list/', login_required(ReviewDetail.as_view(template_name ='rate_doc/action-list.html')), name='list-action'),
    path(r'<int:pk>/report-action/<int:action_pk>/update/', login_required(UpdateReportAction.as_view()), name='update-action'),
    path(r'<int:pk>/report-action/<int:action_pk>/delete/', login_required(DeleteReportAction.as_view()), name='delete-action'),
    
    path(r'docs/', login_required(ReviewList.as_view()), name='doc-list'),
    path(r'success/', TemplateView.as_view(template_name='rate_doc/success.html'),name='success'),
    path(r'get-next/', get_next, name='get-next'),
    path(r'export/', login_required(Export), name='export'),
]