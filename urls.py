from django.urls import path
from .views import IndexView, BoardView, CardView, ProfileDetailView, CardEditView, ChecklistEditView, TaskEditView, CardCreateView, ChecklistCreateView, TaskCreateView, TaskDeleteView, CommentCreateView, AttachmentCreateView, AttachmentEditView, AttachmentDeleteView, CommentEditView, CommentDeleteView

app_name = "nibble"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('board/<int:pk>', BoardView.as_view(), name='board'),
    path('card/<int:pk>', CardView.as_view(), name='card'),
    path('card/create/', CardCreateView.as_view(), name='card_create'),
    path('card/edit/<int:card_id>/<str:field_name>/', CardEditView.as_view(), name="card_edit"),
    path('attachment/create/', AttachmentCreateView.as_view(), name='attachment_create'),
    path('attachment/edit/<int:attachment_id>/', AttachmentEditView.as_view(), name="attachment_edit"),
    path('attachment/delete/<int:pk>', AttachmentDeleteView.as_view(), name="attachment_delete"),
    path('comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/edit/<int:comment_id>', CommentEditView.as_view(), name="comment_edit"),
    path('comment/delete/<int:pk>', CommentDeleteView.as_view(), name="comment_delete"),
    path('checklist/create', ChecklistCreateView.as_view(), name="checklist_create"),
    path('checklist/edit/<int:checklist_id>/<str:field_name>/', ChecklistEditView.as_view(), name="checklist_edit"),
    path('task/create', TaskCreateView.as_view(), name="task_create"),
    path('task/edit/<int:task_id>/<str:field_name>/', TaskEditView.as_view(), name="task_edit"),
    path('task/delete/<int:pk>', TaskDeleteView.as_view(), name="task_delete"),
    path('profile/<str:handle>', ProfileDetailView.as_view(), name='profile'),

]