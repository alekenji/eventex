from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET / must return status code 200  """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

class SubscribePostTest(TestCase):

    def setUp(self):
        data = dict(name='Alexandre', cpf='12345678901',
                    email='alekenji@uol.com.br', phone='11-543210-1234')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmacao de inscricao'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'kenjiphp@gmail.com'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['kenjiphp@gmail.com', 'alekenji@uol.com.br']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Alexandre', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('alekenji@uol.com.br', email.body)
        self.assertIn('11-543210-1234', email.body)


class SubscribeInvalidPostTest(TestCase):

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


class SubscribeSuccessMessage(TestCase):

    def test_message(self):
        data = dict(name='Alexandre', cpf='12345678901',
                    email='alekenji@uol.com.br', phone='11-543210-1234')
        self.response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(self.response, 'Inscricao realizada com sucesso!')