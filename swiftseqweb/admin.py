from django.contrib import admin
from swiftseqweb.models import *


class ParameterInline(admin.StackedInline):
    model = Parameter
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class StepAdmin(admin.ModelAdmin):
    list_display = ('name', 'required', 'multiple_programs')


class ProgramAdmin(admin.ModelAdmin):
    inlines = [ParameterInline]
    list_display = ('name', 'step', 'walltime', 'help_url')


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class PrebuiltWorkflowAdmin(admin.ModelAdmin):
    list_display = ('title', 'workflow_file')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(PrebuiltWorkflow, PrebuiltWorkflowAdmin)
admin.site.site_header = 'SwiftSeqGUI Administration'
