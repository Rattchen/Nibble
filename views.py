from django.apps import apps
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView, DetailView, View
from django.db.models.functions import ExtractYear
from .models import Board, Card, Column, NibbleProfile, Checklist, Task, TaskType
from .forms import CardForm, ChecklistForm, TaskForm

class IndexView(TemplateView):
    template_name = 'nibble/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['message'] = f'Hi, welcome to Nibble, {user.username}!'
        context['user'] = user
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

class TaskCreateView(View):
    def get(self, request):
        checklist_id = request.GET['checklist_id']

        task_types = TaskType.objects.all()
        user_list = NibbleProfile.objects.all()
        priority_choices = Task.PRIORITY_DETAILS
        context = {'checklist_id':checklist_id, 'task_types':task_types, 'user_list':user_list, 'priorities':priority_choices}
        response = render_to_string('nibble/forms/task_create_form.html', context)
        return HttpResponse(response)

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            context = {"task":task, 'checklist':task.checklist}
            response = render_to_string('nibble/partials/task.html', context)
            return HttpResponse(response)
        else:
            print(form.errors) # Temporary line while working on the View
        return JsonResponse({"success":False, "errors":form.errors}, status=400)

class TaskEditView(View):
    def get(self, request, task_id, field_name):
        task = get_object_or_404(Task, id=task_id)
        field_value = getattr(task, field_name)

        context = {
            "task_id":task_id, "field_name":field_name, 
            "field_value": field_value, 'checklist_id': task.checklist.id
            }

        if field_name == "assigned_to":
            user_list = NibbleProfile.objects.all()
            context["user_list"] = user_list
        elif field_name == "priority":
            priority_choices = Task.PRIORITY_DETAILS
            context["priorities"] = priority_choices
        elif field_name == "task_type":
            task_types = TaskType.objects.all()
            context["task_types"] = task_types

        response = render_to_string('nibble/forms/task_edit_form.html', context)
        return HttpResponse(response)

    def post(self, request, task_id, field_name):
        task = get_object_or_404(Task, id=task_id)
        if field_name == "assigned_to":
            user = get_object_or_404(NibbleProfile, id=request.POST.get(field_name, "").strip())
            setattr(task, field_name, user)
        elif field_name == "is_finished":
            if request.POST:
                task.is_finished = True
            else:
                task.is_finished = False
        else:
            setattr(task, field_name, request.POST.get(field_name, "").strip())
        task.save()

        context = {'task':task, 'checklist': task.checklist}     
        response = render_to_string('nibble/partials/task.html', context)
        return HttpResponse(response)

class TaskDeleteView(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        context={'task':task, 'checklist':task.checklist}
        response = render_to_string('nibble/forms/delete_confirmation_modal.html', context)
        return HttpResponse(response)

    def delete(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        task.delete()
        return HttpResponse(status=200)


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
        .annotate(year=ExtractYear("due_date"))
        .values("year")
        .distinct()
        .order_by("-year"))

        tasks_by_year = {}

        for year in years:
            year_value = year['year']
            tasks_by_year[year_value] = profile.user_tasks.filter(due_date__year=year_value)

        context["tasks_by_year"] = tasks_by_year
        return context

