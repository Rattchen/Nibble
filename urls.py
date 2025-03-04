from django.urls import path
from .views import IndexView, BoardView,CardView, ProfileDetailView, CardEditView, ChecklistEditView, TaskEditView, CardCreateView, ChecklistCreateView

app_name = "nibble"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('board/', IndexView.as_view(), name='board_nothing'),
    path('board/<int:pk>', BoardView.as_view(), name='board'),
    path('card/<int:pk>', CardView.as_view(), name='card'),
    path('card/create/', CardCreateView.as_view(), name='card_create'),
    path('card/edit/<int:card_id>/<str:field_name>/', CardEditView.as_view(), name="card_edit"),
    path('checklist/create', ChecklistCreateView.as_view(), name="checklist_create"),
    path('checklist/edit/<int:checklist_id>/<str:field_name>/', ChecklistEditView.as_view(), name="checklist_edit"),
    path('task/edit/<int:task_id>/<str:field_name>/', TaskEditView.as_view(), name="task_edit"),
    path('profile/<str:handle>', ProfileDetailView.as_view(), name='profile'),

]