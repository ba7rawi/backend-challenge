from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Label, Task
from tasks.constants import *

class LabelAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.login(username='testuser', password='12345')
        self.label = Label.objects.create(name='Work', owner=self.user)

    def test_get_labels(self):
        response = self.client.get('/labels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_label(self):
        data = {'name': 'Home', 'owner': self.user.id}
        response = self.client.post('/labels/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_label_with_related_tasks(self):
        task = Task.objects.create(title='Task 1', owner=self.user)
        task.label.add(self.label)
        response = self.client.delete(f'/labels/{self.label.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error':'label has related tasks'})

    def test_delete_label(self):
        response = self.client.delete(f'/labels/{self.label.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TaskAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.login(username='testuser', password='12345')
        self.task = Task.objects.create(title='Task 1', owner=self.user, completion_status=UNASSIGNED)

    def test_get_tasks(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        data = {'title': 'Task 2', 'owner': self.user.id, 'completion_status': UNASSIGNED}
        response = self.client.post('/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_task(self):
        data = {'title': 'Updated Task 1'}
        response = self.client.patch(f'/tasks/{self.task.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task 1')

    def test_delete_task(self):
        response = self.client.delete(f'/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
