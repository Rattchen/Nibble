from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.db.models import F
from django.db.models.functions import ExtractYear
from .models import Board, Card, NibbleProfile

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

