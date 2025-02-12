from django.db import models
from django.conf import settings

class NibbleProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    specialization = models.CharField(max_length=50, default='')
    bio = models.TextField(default='')
    # TODO: Change to an ImageField
    avatar = models.CharField(max_length=50, default='👤')

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Log(models.Model):
    # TODO: Check out django simple history

    # TODO: Rename and change to FK
    belongs_to = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(NibbleProfile, on_delete=models.CASCADE)
    log_type = models.CharField(max_length=50)
    # TODO: Change to an enum with types "assigned a person", "renamed something", "added Task/Checklist" etc
    target = models.CharField(max_length=50)
    additional = models.CharField(max_length=50, null=True, blank=True)
    # TODO: Rename; it holds additional info like past name of a task or who was assigned

class Comment(models.Model):
    # TODO: Rename and change to FK
    belongs_to = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(NibbleProfile, on_delete=models.CASCADE)
    content = models.TextField()


class Board(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Column(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    order_index = models.IntegerField()

    def __str__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=50)
    order_index = models.IntegerField()
    owner = models.ForeignKey(
        NibbleProfile, on_delete=models.CASCADE, related_name="owner")
    helper = models.ForeignKey(
        NibbleProfile, on_delete=models.CASCADE, related_name="helper")
    # TODO: Change the owner and helper field name
    due_datetime = models.DateTimeField()
    description = models.TextField()
    column = models.ForeignKey(Column, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Attachment(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Label(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, unique=True)
    # TODO: remember to use numbers+# only validation or a color picker in forms

    def __str__(self):
        return self.name

class Checklist(models.Model):
    name = models.CharField(max_length=50)
    order_index = models.IntegerField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    # TODO: An indicator of how many % is already finished

    def __str__(self):
        return self.name

class TaskType(models.Model):
    name = models.CharField(max_length=50)
    # TODO: Add a linked specialization

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    order_index = models.IntegerField()
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    priority = models.CharField(max_length=50)
    # TODO: Create a subclass Priority
    due_datetime = models.DateTimeField()
    points = models.IntegerField()
    assigned_to = models.ForeignKey(NibbleProfile, on_delete=models.CASCADE)
    is_finished = models.BooleanField()

    def __str__(self):
        return self.name
