from django.contrib import admin
from .models import Attachment, Board, Card, Checklist, Column, Label, Log, Task, NibbleProfile, Comment, TaskType

admin.site.register(NibbleProfile)
admin.site.register(Log)
admin.site.register(Comment)
admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Card)
admin.site.register(Attachment)
admin.site.register(Label)
admin.site.register(Checklist)
admin.site.register(TaskType)
admin.site.register(Task)