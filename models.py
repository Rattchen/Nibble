from django.db import models
from django.conf import settings

class NibbleProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="nibbleProfile")
    handle = models.CharField(max_length=30, unique=True) 
    # TODO: automatic creation and update when user changes their nickname
    points = models.IntegerField(default=0)
    specialization = models.CharField(max_length=50, default='')
    # TODO: Many specializations
    bio = models.TextField(default='', null=True, blank=True)
    # TODO: Change to an ImageField
    avatar = models.CharField(max_length=50, default='👤')

    def __str__(self):
        return f"@{self.handle} ({self.user.username})"


class Board(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Label(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, unique=True)
    # TODO: remember to use numbers+# only validation or a color picker in forms

    def __str__(self):
        return self.name

class Column(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    order_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=50)
    order_index = models.IntegerField(null=True, blank=True)
    owner = models.ForeignKey(
        NibbleProfile, null=True, blank=True, on_delete=models.CASCADE, related_name="owner")
    helper = models.ForeignKey(
        NibbleProfile, null=True, blank=True, on_delete=models.CASCADE, related_name="helper")
    # TODO: Change the owner and helper field names
    label = models.ManyToManyField(Label, blank=True)
    due_datetime = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="cards")

    def __str__(self):
        return self.name

class Attachment(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="attachments")

    def __str__(self):
        return self.name

class Checklist(models.Model):
    name = models.CharField(max_length=50)
    order_index = models.IntegerField(null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="checklists")
    # TODO: An indicator of how many % is already finished

    def __str__(self):
        return f"\'{self.name}\' in \'{self.card.name}\' card"

class TaskType(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=5, null=True, blank=True) # TODO: Change to ImageField
    # TODO: Add a linked specialization

    def __str__(self):
        return self.name

class Task(models.Model):
    class Priority(models.TextChoices):
        HIGH = "H", "High"
        NORMAL = "N", "Normal"
        LOW = "L", "Low"

    PRIORITY_DETAILS = {
        Priority.HIGH: {"color":"#c70404", "icon":"🔴", "associated_character":"꜒", "label": Priority.HIGH.label, "value": Priority.HIGH.value},
        Priority.NORMAL: {"color":"#c7c004", "icon":"🟡", "associated_character":"꜔", "label": Priority.NORMAL.label, "value": Priority.HIGH.value},
        Priority.LOW: {"color":"#14c704", "icon":"🟢", "associated_character":"꜖", "label": Priority.LOW.label, "value": Priority.HIGH.value},
    }

    name = models.CharField(max_length=100)
    order_index = models.IntegerField(null=True, blank=True)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name="tasks")
    task_type = models.ForeignKey(TaskType, null=True, blank=True, on_delete=models.CASCADE)
    priority = models.CharField(max_length=1, choices=Priority.choices, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    points = models.IntegerField()
    assigned_to = models.ForeignKey(NibbleProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="user_tasks")
    is_finished = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cached_assigned_to = self.assigned_to
        self.cached_is_finished = self.is_finished

    def save(self, *args, **kwargs):
        changed_assignee = False
        changed_status = False

        if self.pk: #If editing an already existing task
            if self.cached_assigned_to != self.assigned_to:
                changed_assignee = True
            if self.cached_is_finished != self.is_finished:
                changed_status = True
        else: #If a new task
            if self.assigned_to and self.is_finished:
                print(f"My assignee has {self.assigned_to.points} pts")
                self.assigned_to.points = models.F("points") + self.points
                self.assigned_to.save()

        if changed_assignee:
            print(F"New assignee is {self.assigned_to}, old assignee was {self.cached_assigned_to}")
            # Deduct points from the old assignee
            self.cached_assigned_to.points = models.F("points") - self.points
            self.cached_assigned_to.save()
            # Give points to the new assignee
            self.assigned_to.points = models.F("points") + self.points
            self.assigned_to.save()
        if changed_status:
            if self.is_finished and self.assigned_to:
                self.assigned_to.points = models.F("points") + self.points
                self.assigned_to.save()
            elif not self.is_finished and self.assigned_to:
                self.assigned_to.points = models.F("points") - self.points
                self.assigned_to.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print(f"Attempting to delete an item {self.name}")
        if self.is_finished and self.assigned_to:
            self.assigned_to.points = models.F("points") - self.points
            self.assigned_to.save()
        super().delete(*args, **kwargs)
        #For future me: remember that even after super().delete() you can access values with no need for caching in init

    def get_priority_info(self):
        return self.PRIORITY_DETAILS.get(self.priority, {})

    def __str__(self):
        return self.name


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
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="comments")
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(NibbleProfile, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.author} commented on {self.card}"
