from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.obj = Subscription(name = 'Alexandre',
                                cpf = '12345678901',
                                email = 'kenjiphp@gmail.com',
                                phone = '11-123451234',
                                paid=False)
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Alexandre', str(self.obj))

    def test_paid_default_to_False(self):
        self.assertEqual(False, self.obj.paid)