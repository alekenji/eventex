from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):

    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET / must return status code 200  """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):

        tags = ( ('<form',1),
                 ('<input',6),
                 ('type="text"', 3),
                 ('type="email"',1),
                 ('type="submit"',1) )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):

    def setUp(self):
        data = dict(name='Alexandre', cpf='12345678901',
                    email='alekenji@uol.com.br', phone='11-543210-1234')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        self.assertRedirects(self.response, '/inscricao/1/')

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())

class SubscribePostInvalid(TestCase):

    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
