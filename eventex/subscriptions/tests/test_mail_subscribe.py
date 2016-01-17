from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):

    def setUp(self):
        data = dict(name='Alexandre', cpf='12345678901',
                    email='alekenji@uol.com.br', phone='11-543210-1234')
        self.client.post(r('subscriptions:new'), data)
        self.mail = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmacao de inscricao'
        self.assertEqual(expect, self.mail.subject)

    def test_subscription_email_from(self):
        expect = 'kenjiphp@gmail.com'

        self.assertEqual(expect, self.mail.from_email)

    def test_subscription_email_to(self):
        expect = ['kenjiphp@gmail.com', 'alekenji@uol.com.br']

        self.assertEqual(expect, self.mail.to)

    def test_subscription_email_body(self):

        contents =[
            'Alexandre',
            '12345678901',
            'alekenji@uol.com.br',
            '11-543210-1234'
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.mail.body)
