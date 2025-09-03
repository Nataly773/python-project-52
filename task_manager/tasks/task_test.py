from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


User = get_user_model()


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаём пользователей
        self.user1 = User.objects.create_user(username='user1', 
                                              password='pass1')
        self.user2 = User.objects.create_user(username='user2',
                                               password='pass2')
        # Создаём статус и метку
        self.status = Status.objects.create(name='New')
        self.label = Label.objects.create(name='Important')
        # Создаём задачу
        self.task = Task.objects.create(
            name='Test Task',
            description='Description',
            author=self.user1,
            status=self.status,
            executor=self.user2
        )
        self.task.labels.add(self.label)

    def test_list_tasks(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_create_task(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.post(
            reverse('tasks:create'),
            {
                'name': 'New Task',
                'description': 'New description',
                'status': self.status.id,
                'executor': self.user2.id,
                'labels': [self.label.id],
            }
        )
        self.assertEqual(Task.objects.count(), 2)
        self.assertRedirects(response, reverse('tasks:index'))

    def test_update_task(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.post(
            reverse('tasks:update', args=[self.task.id]),
            {
                'name': 'Updated Task',
                'description': 'Updated description',
                'status': self.status.id,
                'executor': self.user2.id,
                'labels': [self.label.id],
            }
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertRedirects(response, reverse('tasks:index'))

    def test_delete_task_by_non_author(self):
        self.client.login(username='user2', password='pass2')
        response = self.client.post(reverse('tasks:delete', 
                                            args=[self.task.id]))
        self.assertEqual(Task.objects.count(), 1)
        self.assertRedirects(response, reverse('tasks:index'))
        # Проверяем сообщение об ошибке
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 
                         'Задачу может удалить только ее автор')

    def test_access_requires_login(self):
        response = self.client.get(reverse('tasks:create'))
        self.assertRedirects(response, 
                             '/login/?next=' + reverse('tasks:create')
                             )
