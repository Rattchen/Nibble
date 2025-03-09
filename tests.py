from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Task, NibbleProfile, Board, Column, Card, Checklist

class TaskProfilePointsTest(TestCase):
    def setUp(self):
        UserModel = get_user_model()

        self.user1 = UserModel.objects.create(username="user1", password="password")
        self.user2 = UserModel.objects.create(username="user2", password="password")
       
        self.profile1 = NibbleProfile.objects.create(user=self.user1, handle="profile1", points=0, specialization="", avatar="👤")
        self.profile2 = NibbleProfile.objects.create(user=self.user2, handle="profile2", points=0, specialization="", avatar="👤")

        
        self.board = Board.objects.create(name="TestBoard")
        self.column = Column.objects.create(name="TestColumn", board=self.board)
        self.card = Card.objects.create(name="TestCard", column=self.column)
        self.checklist = Checklist.objects.create(name="TestChecklist", card=self.card)

        self.task_finished_unassigned = Task.objects.create(name="Finished unassigned test task", checklist=self.checklist, points=3, assigned_to=None, is_finished=True)
        self.task_unfinished_unassigned = Task.objects.create(name="NOT finished unassigned test task", checklist=self.checklist, points=7, assigned_to=None, is_finished=False)
        self.task_finished_assigned_p1 = Task.objects.create(name="Finished unassigned test task", checklist=self.checklist, points=3, assigned_to=self.profile1, is_finished=True)
        self.task_unfinished_assigned_p2 = Task.objects.create(name="NOT finished unassigned test task", checklist=self.checklist, points=7, assigned_to=self.profile2, is_finished=False)

    def test_task_creation(self):
        """Tests what happens when the unfinished task is created with an assignee; it shouldn't reward points."""
        pass

    def test_task_deletion(self):
        """Tests if deleting the task removes the points from the assignee."""
        pass

    def test_task_completion(self):
        """Tests if the points are correctly given to the assignee."""
        pass

    def test_task_decompletion(self):
        """Tests if the points are correctly taken from the assignee after changing the is_finished state."""
        pass

    def test_task_assignment(self):
        """Tests if assigning the person to the task correcntly rewards them with points."""
        pass

    def test_task_deassignment(self):
        """Tests if removing the assignee correctly removes points from their profile."""
        pass

    def test_task_reassignment(self):
        """Tests if reassigning the task moves the points to the new assignee."""
        pass

    def test_task_multiple_completion_changes(self):
        """Tests if changing the state of is_finished attribute properly calculates points."""
        pass
