from django.forms import ModelForm
from .models import Card, Checklist, Task, Comment

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
        fields = ['name', 'checklist', 'task_type', 'priority', 'due_date', 'due_time', 'points', 'assigned_to']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['card', 'author', 'content']