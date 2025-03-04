from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView, DetailView, View
from django.db.models.functions import ExtractYear
from .models import Board, Card, Column, NibbleProfile, Checklist, Task
from .forms import CardForm, ChecklistForm

class IndexView(TemplateView):
    template_name = 'nibble/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Hi, welcome to Nibble'
        return context

class BoardView(DetailView):
    model = Board
    template_name = 'nibble/board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board = self.get_object()
        context["columns"] = board.columns.all()
        for column in context['columns']:
            column.card_list = column.cards.all()
        return context

class CardView(DetailView):
    # TODO: rename to CardDetailView
    model = Card
    template_name = 'nibble/card.html'

class CardCreateView(View):
    def post(self, request):
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.column = get_object_or_404(Column, id=request.POST["column"])
            card.save()
            context = {"card":card}
            response = render_to_string('nibble/partials/card-small.html', context)
            return HttpResponse(response)
        return JsonResponse({"success":False, "errors":form.errors}, status=400)
        """
        card = get_object_or_404(Card, id=1)
        context = {'card':card}

        """

class CardEditView(View):
    def get(self, request, card_id, field_name):
        card = get_object_or_404(Card, id=card_id)
        field_value = getattr(card, field_name)

        context = {
            "card_id":card_id, "field_name":field_name, 
            "field_value": field_value
            }

        if field_name == "owner" or field_name == "helper":
            user_list = NibbleProfile.objects.all()
            context["user_list"] = user_list

        response = render_to_string('nibble/forms/card_edit_form.html', context)
        return HttpResponse(response)
    
    def post(self, request, card_id, field_name):
        card = get_object_or_404(Card, id=card_id)

        if field_name == "owner" or field_name == "helper":
            user = get_object_or_404(NibbleProfile, id=request.POST.get(field_name, "").strip())
            setattr(card, field_name, user)   
        else:
            setattr(card, field_name, request.POST.get(field_name, "").strip())

        card.save()
        context = {
            "card_id":card.id, "field_name":field_name,
            "field_value": getattr(card, field_name)
            }
        response = render_to_string('nibble/forms/card_field.html', context)
        return HttpResponse(response)

class ChecklistEditView(View):
    def get(self, request, checklist_id, field_name):
        checklist = get_object_or_404(Checklist, id=checklist_id)
        field_value = getattr(checklist, field_name)

        context = {
            "checklist_id":checklist_id, "field_name":field_name, 
            "field_value": field_value
            }

        response = render_to_string('nibble/forms/checklist_edit_form.html', context)
        return HttpResponse(response)

    def post(self, request, checklist_id, field_name):
        checklist = get_object_or_404(Checklist, id=checklist_id)
        setattr(checklist, field_name, request.POST.get(field_name, "").strip())
        checklist.save()
        context = {
            "checklist_id":checklist.id, "field_name":field_name,
            "field_value": getattr(checklist, field_name)
            }
        response = render_to_string('nibble/forms/checklist_field.html', context)
        return HttpResponse(response)

class ChecklistCreateView(View):
    def post(self, request):
        form = ChecklistForm(request.POST)
        if form.is_valid():
            checklist = form.save()
            context = {"checklist":checklist}
            response = render_to_string('nibble/partials/checklist.html', context)
            return HttpResponse(response)
        return JsonResponse({"success":False, "errors":form.errors}, status=400)

class TaskEditView(View):
    def get(self, request, task_id, field_name):
        task = get_object_or_404(Task, id=task_id)
        field_value = getattr(task, field_name)

        context = {
            "task_id":task_id, "field_name":field_name, 
            "field_value": field_value
            }
        if field_name == "assigned_to":
            user_list = NibbleProfile.objects.all()
            context["user_list"] = user_list
            
        response = render_to_string('nibble/forms/task_edit_form.html', context)
        return HttpResponse(response)

    def post(self, request, task_id, field_name):
        task = get_object_or_404(Task, id=task_id)
        if field_name == "assigned_to":
            user = get_object_or_404(NibbleProfile, id=request.POST.get(field_name, "").strip())
            setattr(task, field_name, user)   
        else:
            setattr(task, field_name, request.POST.get(field_name, "").strip())
        task.save()
        context = {
            "task_id":task.id, "field_name":field_name,
            "field_value": getattr(task, field_name)
            }
        response = render_to_string('nibble/forms/task_field.html', context)
        return HttpResponse(response)


class ProfileDetailView(DetailView):
    model = NibbleProfile
    template_name = 'nibble/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(NibbleProfile, handle=self.kwargs["handle"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        #context["assigned_tasks"] = profile.user_tasks.all()
        years = (profile.user_tasks
        .annotate(year=ExtractYear("due_datetime"))
        .values("year")
        .distinct()
        .order_by("-year"))

        tasks_by_year = {}

        for year in years:
            year_value = year['year']
            tasks_by_year[year_value] = profile.user_tasks.filter(due_datetime__year=year_value)

        context["tasks_by_year"] = tasks_by_year
        return context

