from django.urls import path
from . import views

app_name = "nibble"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('board/<int:pk>', views.BoardView.as_view(), name='board'),
    path('archive/<int:pk>', views.ArchiveView.as_view(), name='archive'),
    # Card views
    path('card/<int:pk>', views.CardView.as_view(), name='card'),
    path('card/create/', views.CardCreateView.as_view(), name='card_create'),
    path('card/edit/<int:card_id>/<str:field_name>/', views.CardEditView.as_view(), name="card_edit"),
    # Attachment views
    path('attachment/create/', views.AttachmentCreateView.as_view(), name='attachment_create'),
    path('attachment/edit/<int:attachment_id>/', views.AttachmentEditView.as_view(), name="attachment_edit"),
    path('attachment/delete/<int:pk>', views.AttachmentDeleteView.as_view(), name="attachment_delete"),
    # Comment views
    path('comment/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/edit/<int:comment_id>', views.CommentEditView.as_view(), name="comment_edit"),
    path('comment/delete/<int:pk>', views.CommentDeleteView.as_view(), name="comment_delete"),
    # Checklist views
    path('checklist/create', views.ChecklistCreateView.as_view(), name="checklist_create"),
    path('checklist/edit/<int:checklist_id>/<str:field_name>/', views.ChecklistEditView.as_view(), name="checklist_edit"),
    path('checklist/delete/<int:pk>', views.ChecklistDeleteView.as_view(), name="checklist_delete"),
    # Task views
    path('task/create', views.TaskCreateView.as_view(), name="task_create"),
    path('task/edit/<int:task_id>/<str:field_name>/', views.TaskEditView.as_view(), name="task_edit"),
    path('task/delete/<int:pk>', views.TaskDeleteView.as_view(), name="task_delete"),
    # Profile views
    path('profile/<str:handle>',views.ProfileDetailView.as_view(), name='profile'),

]