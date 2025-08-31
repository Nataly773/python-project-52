from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class UserCRUDTests(TestCase):
    def setUp(self):
        """Базовые данные для тестов"""
        # суперпользователь
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )
        # обычный пользователь
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="12345"
        )
        # статус для задач
        self.status = Status.objects.create(name="New")

    def test_index_view(self):
        """Список пользователей доступен"""
        response = self.client.get(reverse("users:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertContains(response, "admin")

    def test_create_user(self):
        """Регистрация нового пользователя"""
        response = self.client.post(reverse("users:create"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_update_self_user(self):
        """Пользователь может обновить сам себя"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("users:update", args=[self.user.id]), {
            "username": "updateduser",
            "email": "updated@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123",
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, "updateduser")

    def test_update_other_user_forbidden(self):
        """Обычный пользователь не может обновить другого"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("users:update", 
                                            args=[self.admin.id]), 
                                            {
            "username": "hacker",
            "email": "hacker@example.com",
            "password1": "hackpass123",
            "password2": "hackpass123",
        })
        self.admin.refresh_from_db()
        self.assertNotEqual(self.admin.username, "hacker")
        self.assertEqual(response.status_code, 302)  # редирект обратно

    def test_delete_self_user(self):
        """Пользователь может удалить себя, если нет задач"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("users:delete", 
                                            args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_user_in_use(self):
        """Нельзя удалить пользователя, если он исполнитель задачи"""
        self.client.login(username="testuser", 
                          password="12345")
        Task.objects.create(
            name="Test Task",
            status=self.status,
            author=self.admin,
            executor=self.user,
        )
        response = self.client.post(reverse("users:delete", 
                                            args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(id=self.user.id).exists())