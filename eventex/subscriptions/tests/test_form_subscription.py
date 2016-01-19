from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):

    def setUp(self):
        self.form = SubscriptionForm()


    def test_form_has_fields(self):
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(self.form.fields))


    def test_cpf_is_digit(self):
        formx = self.make_validate_form(cpf='ABCD5678901')
        #self.assertFormErrorMessage(formx, 'cpf', 'CPF deve conter apenas numeros')
        self.assertFormErrorCode(formx, 'cpf', 'digits')


    def test_cpf_has_11_digits(self):
        formx = self.make_validate_form(cpf='1234')
        #self.assertFormErrorMessage(formx, 'cpf', 'CPF deve ter 11 numeros')
        self.assertFormErrorCode(formx, 'cpf', 'length')


    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)


    def assertFormErrorMessage(self, formx, field, msg):
        errors = formx.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)


    def make_validate_form(self, **kwargs):
        valid = dict(name='Alexandre',
                     cpf='12345678901',
                     email='alekenji@uol.com.br',
                     phone='11-543210-1234')

        data = dict(valid, **kwargs)
        formx = SubscriptionForm(data)
        formx.is_valid()

        return formx
