from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.tasks.models import Task

User = get_user_model()


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        self.label = Label.objects.create(name="Initial Label")

    def test_list_labels(self):
        response = self.client.get(reverse("labels:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_create_label(self):
        response = self.client.post(reverse("labels:create"), {"name": "New Label"})
        self.assertRedirects(response, reverse("labels:index"))
        self.assertTrue(Label.objects.filter(name="New Label").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "The label was successfully created.")

    def test_update_label(self):
        response = self.client.post(
            reverse("labels:update", args=[self.label.pk]),
            {"name": "Updated Label"},
        )
        self.assertRedirects(response, reverse("labels:index"))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated Label")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Label successfully updated")

    def test_delete_label_not_in_use(self):
        response = self.client.post(reverse("labels:delete", args=[self.label.pk]))
        self.assertRedirects(response, reverse("labels:index"))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Label successfully deleted")

    def test_delete_label_in_use(self):
        task = Task.objects.create(
            name="Test Task", description="Task desc", status_id=1, author=self.user
        )
        task.labels.add(self.label)
        response = self.client.post(reverse("labels:delete", args=[self.label.pk]))
        self.assertRedirects(response, reverse("labels:index"))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Cannot delete label because it is in use")

