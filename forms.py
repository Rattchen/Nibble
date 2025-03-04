from django.forms import ModelForm
from .models import Card, Checklist

class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'column']

class ChecklistForm(ModelForm):
    class Meta:
        model = Checklist
        fields = ['name', 'card']
