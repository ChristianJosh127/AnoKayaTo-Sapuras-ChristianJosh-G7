
from datetime import date

from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import DreamEntry, DreamSymbol


class DreamEntryTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='dreamowner',
            email='owner@example.com',
            password='TestPassword123!'
        )

        self.other_user = CustomUser.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='TestPassword123!'
        )

        self.symbol = DreamSymbol.objects.create(
            name='Snake',
            category='Animal',
            description='A snake appearing in a dream.'
        )

        self.dream = DreamEntry.objects.create(
            user=self.user,
            title='My First Dream',
            dream_text='I dreamed about a snake.',
            dream_date=date(2026, 11, 27)
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse('dream_list'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/?next='))

    def test_user_can_create_dream(self):
        self.client.login(
            username='dreamowner',
            password='TestPassword123!'
        )

        response = self.client.post(
            reverse('dream_create'),
            {
                'title': 'Flying Dream',
                'dream_text': 'I was flying above the ocean.',
                'dream_date': '2026-11-27',
                'symbols': [self.symbol.pk],
            }
        )

        self.assertRedirects(response, reverse('dream_list'))

        dream = DreamEntry.objects.get(title='Flying Dream')

        self.assertEqual(dream.user, self.user)
        self.assertEqual(dream.symbols.count(), 1)

    def test_user_can_only_see_own_dreams(self):
        DreamEntry.objects.create(
            user=self.other_user,
            title='Private Dream',
            dream_text='Another user dream.',
            dream_date=date(2026, 11, 27)
        )

        self.client.login(
            username='dreamowner',
            password='TestPassword123!'
        )

        response = self.client.get(reverse('dream_list'))

        self.assertContains(response, 'My First Dream')
        self.assertNotContains(response, 'Private Dream')

    def test_user_can_update_own_dream(self):
        self.client.login(
            username='dreamowner',
            password='TestPassword123!'
        )

        response = self.client.post(
            reverse('dream_update', args=[self.dream.pk]),
            {
                'title': 'Updated Dream',
                'dream_text': 'I dreamed about flying.',
                'dream_date': '2026-11-27',
                'symbols': [self.symbol.pk],
            }
        )

        self.assertRedirects(response, reverse('dream_list'))

        self.dream.refresh_from_db()
        self.assertEqual(self.dream.title, 'Updated Dream')

    def test_user_can_delete_own_dream(self):
        self.client.login(
            username='dreamowner',
            password='TestPassword123!'
        )

        response = self.client.post(
            reverse('dream_delete', args=[self.dream.pk])
        )

        self.assertRedirects(response, reverse('dream_list'))
        self.assertFalse(
            DreamEntry.objects.filter(pk=self.dream.pk).exists()
        )

    def test_user_cannot_edit_another_users_dream(self):
        self.client.login(
            username='otheruser',
            password='TestPassword123!'
        )

        response = self.client.get(
            reverse('dream_update', args=[self.dream.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_another_users_dream(self):
        self.client.login(
            username='otheruser',
            password='TestPassword123!'
        )

        response = self.client.post(
            reverse('dream_delete', args=[self.dream.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            DreamEntry.objects.filter(pk=self.dream.pk).exists()
        )

    def test_dream_description_is_required(self):
        self.client.login(
            username='dreamowner',
            password='TestPassword123!'
        )

        response = self.client.post(
            reverse('dream_create'),
            {
                'title': 'Empty Dream',
                'dream_text': '',
                'dream_date': '2026-11-27',
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            DreamEntry.objects.filter(title='Empty Dream').exists()
        )
