from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Label, Task
from tasks.constants import *
class LabelModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.label = Label.objects.create(name='Work', owner=self.user)

    def test_label_creation(self):
        self.assertEqual(self.label.name, 'Work')
        self.assertEqual(self.label.owner.username, 'testuser')

    def test_label_str(self):
        self.assertEqual(str(self.label), 'Work')

    def test_label_unique_together(self):
        with self.assertRaises(Exception):
            Label.objects.create(name='Work', owner=self.user)


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(title='Task 1', owner=self.user, completion_status=UNASSIGNED)

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Task 1')
        self.assertEqual(self.task.owner.username, 'testuser')
        self.assertEqual(self.task.completion_status, UNASSIGNED)

    def test_task_str(self):
        self.assertEqual(str(self.task), 'Task 1')

    def test_task_label(self):
        label = Label.objects.create(name='Work', owner=self.user)
        self.task.label.add(label)
        self.assertIn(label, self.task.label.all())
