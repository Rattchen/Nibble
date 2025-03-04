from django.forms import ModelForm
from .models import Card, Checklist, Task

class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'column']

class ChecklistForm(ModelForm):
    class Meta:
        model = Checklist
        fields = ['name', 'card']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'checklist', 'task_type', 'priority', 'due_datetime', 'points', 'assigned_to']