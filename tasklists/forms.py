from django import forms
from django.forms import DateInput, ImageField, FileField, FileInput
from django.forms import Select
from django.forms import TextInput
from .models import Task
from django.utils.translation import gettext_lazy as _

Choice_Priority = [
    ('', 'Open this select priority'),
    ('1', 'High priority'),
    ('2', 'Middle priority'),
    ('3', 'Low priority'),
]

Choice_Status = [
    ('', 'Open this select status'),
    ('1', 'Completed'),
    ('2', 'Working'),
    ('3', 'Pending'),
]


class TodoTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        fields = ['name', 'priority', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control',
                                     'placeholder': 'task task task'}),
            'priority': Select(attrs={'class': 'required form-select  ',
                                      'placeholder': 'Select priority'},
                               choices=Choice_Priority),
            'status': Select(attrs={'class': 'required form-select  ',
                                    'placeholder': 'Select status'},
                             choices=Choice_Status),
        }
        error_messages = {
            'name': {
                'required': _("Task field is required."),
            },
            'priority': {
                'required': _("Priority field is required."),
            },
            'status': {
                'required': _("Status field is required."),
            },
        }
        labels = {
            "name": "Task",
            "priority": "Select priority",
            "status": "Select status",
        }
