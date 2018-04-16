from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from swiftseqweb.views import WWW, GenerateWorkflow, Ajax

urlpatterns = [
    # Front-end URL Patterns
    url(r'^$', TemplateView.as_view(template_name='swiftseqweb/www/home.html'), name='index'),
    url(r'^prebuilt-workflows/$', WWW.PrebuiltWorkflows.as_view(), name='prebuilt-workflows'),
    url(r'^learn-more/$', WWW.LearnMore.as_view(), name='learn-more'),

    # Generate Workflow URL Patterns
    url(r'^generate-workflow/$', GenerateWorkflow.Index.as_view(), name='generate-workflow-index'),
    url(r'^generate-workflow/questions/$', GenerateWorkflow.Questions.as_view(), name='questions'),
    url(r'^generate-workflow/generate/$', GenerateWorkflow.Generate.as_view(), name='generate'),
    url(r'^generate-workflow/process-workflow/$', GenerateWorkflow.Process.as_view(), name='process-workflow'),
    url(r'^generate-workflow/download-complete/$',
        TemplateView.as_view(template_name='swiftseqweb/generate_workflow/download_complete.html'),
        name='download-complete'),
    # Ajax URLs for generate-workflow
    url(r'^generate-workflow/generate/get-parameters-for-program/(?P<program_id>\d+)/$',
        Ajax.GetParametersForProgram.as_view(), name='get-parameters-for-program'),
    url(r'^generate-workflow/generate/get-program-set/(?P<step_id>\d+)/(?P<program_set_id>\d+)/$',
        Ajax.GetProgramSet.as_view(), name='get-program-set'),
    url(r'^generate-workflow/generate/get-parameters-line/(?P<parameter_name>[\w\-]+)/$',
        Ajax.GetParametersLine.as_view(), name='get-parameters-line'),
    url(r'^generate-workflow/generate/get-program-attrs/(?P<program_id>\d+)/$',
        Ajax.GetProgramAttrs.as_view(), name='get-program-attrs'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)