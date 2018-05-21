import os
import json
import time
import uuid

from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from swiftseqweb.models import PrebuiltWorkflow, Question, Answer, Step, Program, Parameter


class WWW(object):
    class PrebuiltWorkflows(View):
        def get(self, request):
            context = {
                'prebuilts': PrebuiltWorkflow.objects.all()
            }
            return render(request, 'swiftseqweb/prebuilt_workflows/prebuilt_workflows.html', context)

    class LearnMore(View):
        def get(self, request):
            return render(request, 'swiftseqweb/www/learn_more.html')


class GenerateWorkflow(object):
    class Index(View):
        def get(self, request):
            return HttpResponseRedirect(reverse('questions'))

    class Questions(View):
        def get(self, request):
            db_questions = Question.objects.all()
            question_sets = list()
            for i, question in enumerate(db_questions):
                answers = question.answer_set.all()
                question_sets.append({
                    'question': question,
                    'answers': answers,
                    'data': {
                        'order': i
                    }
                })

            context = {
                'question_sets': question_sets,
                'num_questions': len(question_sets),
                'q': db_questions
            }
            return render(request, 'swiftseqweb/generate_workflow/questions.html', context)

    class Generate(View):
        def get(self, request):
            context = {'nodata': True}
            return render(request, 'swiftseqweb/generate_workflow/generate.html', context)

        def post(self, request):
            context = {'nodata': False}
            post_questions = {post: request.POST[post] for post in request.POST if 'question_id' in post}

            # Get question-answers in context
            context['question_sets'] = [
                {
                    'question': Question.objects.get(pk=question.split('_')[-1]),
                    'answer': Answer.objects.get(pk=answer_id)
                }
                for question, answer_id in post_questions.items()
            ]

            # Calculate which steps should be displayed
            answers_ids = set([int(v) for v in post_questions.values()])
            context['steps'] = [
                step for step in Step.objects.all()
                if any([rule.issubset(answers_ids) for rule in step.get_rules()])
            ]

            return render(request, 'swiftseqweb/generate_workflow/generate.html', context)

    class Process(View):
        def post(self, request):
            output_data = dict()
            post = request.POST

            # Add questions data to output data
            input_questions = [key for key in post if key.startswith('question-')]
            for input_question in input_questions:
                ques_id = input_question.split('-')[1]
                ques = Question.objects.get(pk=ques_id).programmatic_name
                ans_id = post[input_question]
                ans = Answer.objects.get(pk=ans_id).programmatic_name
                output_data[ques] = ans

            # Get step checkboxes that were checked
            option_checkboxes = [key for key in post if key.startswith('option-checkbox-')]
            checked_steps = list()
            for val in option_checkboxes:
                checked_steps.append(val.split('-')[2])

            # Get a set of all programSet IDs
            program_set_ids = set()
            for key in post.keys():
                if key.startswith('programSet-'):
                    program_set_ids.add(key.split('__')[0].split('-')[1])

            # Iterate through each programSet
            for program_set_id in program_set_ids:
                program_set_name = 'programSet-' + program_set_id

                # Get step, add to output data
                step_id = post[program_set_name + '__step']
                step_name = Step.objects.get(pk=step_id).name
                if step_name not in output_data:
                    output_data[step_name] = {}
                if step_id not in checked_steps:
                    continue

                # Get program, add to output data
                program_id = post[program_set_name + '__program']
                program_name = Program.objects.get(pk=program_id).name
                output_data[step_name][program_name] = dict()

                # Get program attributes, add to output data
                program_attr_keys = [key for key in post if key.startswith(program_set_name + '__programAttr-')]
                for program_attr_key in program_attr_keys:
                    program_attr_name = program_attr_key.split('__')[1].split('-')[1]
                    output_data[step_name][program_name][program_attr_name] = post[program_attr_key]

                # Get program parameters, add to output data
                program_parameter_keys = [key for key in post if key.startswith(program_set_name + '__parameter-')]
                num_parameters = int(len(program_parameter_keys) / 2)
                output_data[step_name][program_name]['params'] = dict()
                for i in range(num_parameters):
                    param_pk = post[program_set_name + '__parameter-{}__key'.format(i)]
                    if param_pk == '':
                        continue
                    param_name = Parameter.objects.get(pk=param_pk).name
                    param_val = post[program_set_name + '__parameter-{}__value'.format(i)]
                    output_data[step_name][program_name]['params'][param_name] = param_val

            # Get user-provided filename
            filename = post['download-filename'].strip()
            if not filename:
                filename = 'SwiftSeq_workflow_config_{}'.format(time.strftime('%d%b%Y'))
            elif filename.endswith('.json'):
                filename.replace('.json', '')
            file_content = json.dumps(output_data, indent=2)

            # Write out JSON file contents for linked download
            json_out_filepath = os.path.join(settings.MEDIA_ROOT, filename + '.json')
            download_rel_url = os.path.join(settings.MEDIA_URL, filename + '.json')
            if not os.path.isdir(settings.MEDIA_ROOT):
                os.mkdir(settings.MEDIA_ROOT)
            if os.path.isfile(json_out_filepath):
                append_uuid = str(uuid.uuid4())[:8]
                json_out_filepath = os.path.join(
                    settings.MEDIA_ROOT,
                    filename + '_{}.json'.format(append_uuid)
                )
                download_rel_url = os.path.join(
                    settings.MEDIA_URL,
                    filename + '_{}.json'.format(append_uuid)
                )
            with open(json_out_filepath, 'w') as json_out:
                json_out.write(file_content + '\n')

            return render(request, 'swiftseqweb/generate_workflow/download_complete.html', {
                'relative_download_link': download_rel_url,
                'full_download_link': os.path.join(settings.FQDN, download_rel_url.strip('/'))
            })


class Ajax(object):
    class GetProgramAttrs(View):
        def get(self, request, program_id):
            program = Program.objects.get(pk=program_id)
            data = {
                'help_url': program.help_url,
                'walltime': program.walltime,
                'notes': program.notes
            }
            return HttpResponse(json.dumps(data))

    class GetParametersForProgram(View):
        def get(self, request, program_id):
            data = list()
            parameters = Program.objects.get(pk=program_id).parameter_set.all()
            for parameter in parameters:
                data.append({'id': parameter.id, 'text': parameter.name})
            return HttpResponse(json.dumps(data))

    class GetProgramSet(View):
        def get(self, request, step_id, program_set_id):
            context = {'step': Step.objects.get(pk=step_id), 'program_set_id': program_set_id}
            return render(request, 'swiftseqweb/ajax/program_set.html', context)

    class GetParametersLine(View):
        def get(self, request, parameter_name):
            context = {'parameter_name': parameter_name}
            return render(request, 'swiftseqweb/ajax/parameters_line.html', context)
