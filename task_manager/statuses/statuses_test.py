from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Status


User = get_user_model()


class StatusCRUDTest(TestCase):
    def setUp(self):
        # создаем юзера и логинимся
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        # создаем статус для тестов update/delete
        self.status = Status.objects.create(name="В работе")

    def test_list_statuses(self):
        response = self.client.get(reverse("statuses:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "В работе")

    def test_create_status(self):
        response = self.client.post(
            reverse("statuses:create"),
            {"name": "Новый"},
            follow=True,
        )
        self.assertRedirects(response, reverse("statuses:index"))
        self.assertTrue(Status.objects.filter(name="Новый").exists())

    def test_update_status(self):
        response = self.client.post(
            reverse("statuses:update", args=[self.status.id]),
            {"name": "Обновлено"},
            follow=True,
        )
        self.assertRedirects(response, reverse("statuses:index"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Обновлено")

    def test_delete_status(self):
        response = self.client.post(
            reverse("statuses:delete", args=[self.status.id]),
            follow=True,
        )
        self.assertRedirects(response, reverse("statuses:index"))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_access_requires_login(self):
        self.client.logout()

    # GET-запрос без follow=True, чтобы проверить редирект
        response = self.client.get(reverse("statuses:index"))

    # Формируем ожидаемый URL с параметром next
        login_url = f"{reverse('login')}?next={reverse('statuses:index')}"
        self.assertRedirects(response, login_url)

