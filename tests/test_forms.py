from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverFormTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "username",
            "password1": "user12test",
            "password2": "user12test",
            "license_number": "ABC12345",
            "first_name": "user_first_name",
            "last_name": "user_last_name",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data, form_data)

    def check_validate_errors(self, form_data, error_message):
        # form = DriverLicenseUpdateForm(data=form_data)
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"], [error_message])

    def test_license_number_is_too_short(self):
        form_data = {"license_number": "ABC1234"}
        error_message = "License number should consist of 8 characters"
        DriverFormTests.check_validate_errors(self, form_data=form_data, error_message=error_message)

    def test_license_number_is_too_long(self):
        form_data = {"license_number": "ABC123456"}
        error_message = "License number should consist of 8 characters"
        DriverFormTests.check_validate_errors(self, form_data=form_data, error_message=error_message)

    def test_license_number_dont_have_prefix_with_three_letters(self):
        form_data = {"license_number": "AB123456"}
        error_message = "First 3 characters should be uppercase letters"
        DriverFormTests.check_validate_errors(self, form_data=form_data, error_message=error_message)

    def test_license_number_dont_have_prefix_with_three_uppercase_letters(self):
        form_data = {"license_number": "abc12345"}
        error_message = "First 3 characters should be uppercase letters"
        DriverFormTests.check_validate_errors(self, form_data=form_data, error_message=error_message)

    def test_license_number_dont_have_postfix_with_five_numbers(self):
        form_data = {"license_number": "ABCD2345"}
        error_message = "Last 5 characters should be digits"
        DriverFormTests.check_validate_errors(self, form_data=form_data, error_message=error_message)

