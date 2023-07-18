import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from basics.functions import generate_form_errors, get_auto_id
from . models import Task
from . forms import TodoTaskForm


# ADD TASK AND RETRIEVE TASK
@login_required(login_url='accounts:existing_user')
def todo_index(request):
    form = TodoTaskForm()
    data = Task.objects.filter(is_deleted=False)
    # INSERT NEW DATA --> POST SIGNAL
    if request.method == 'POST':
        form = TodoTaskForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Task)
            data.creator = request.user
            data.updater = request.user
            data.save()
            response_data = {
                "status": "true",
                "title": "New Task",
                "message": "New task Successfully Created.",
                "redirect": 'true',
                "redirect_url": reverse('tasklists:toDo')
            }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message[0].messages[0]
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        context = {
            'title': "Task",
            'is_bootstrap': True,
            'is_todo': True,
            "redirect": True,
            'tasks': data,
            'form': form,
        }
        return render(request, "tasklists/index.html", context=context)


@login_required(login_url='accounts:existing_user')
def delete(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        # SET is_deleted True; better than delete entire row from db
        # task.is_deleted = True
        # task.save()
        # remove_data(pk)

        task.delete()
        return redirect('tasklists:toDo')
    else:
        context = {
            'title': "Delete Task",
            'is_bootstrap': True,
            'is_todo': True,
        }
        return render(request, "tasklists/delete.html", context=context)


@login_required(login_url='accounts:existing_user')
def changestatus(request, pk):
    # status set to 1 for completed task and save
    data = Task.objects.get(pk=pk)
    data.status = 1
    data.save()
    return redirect('tasklists:toDo')


@login_required(login_url='accounts:existing_user')
def edittask(request, pk):
    instance = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TodoTaskForm(request.POST or None, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updater_id = request.user.pk
            data.save()
            response_data = {
                "status": "true",
                "title": "Update Task",
                "message": "Update task Success.",
                "redirect": 'true',
                "redirect_url": reverse('tasklists:toDo')
            }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message[0].messages[0]
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = TodoTaskForm(request.POST or None, instance=instance)
        context = {
            'title': "Update Task",
            'is_bootstrap': True,
            'is_todo': True,
            "redirect": True,
            'form': form,
        }
        return render(request, "tasklists/edit_task_detail.html", context=context)
