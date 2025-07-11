"""Test suite for create new contact"""

import json
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from api.models import User
from api.models import Contact, ContactEmail, ContactPhone
from contacts.utils.token.jwt_token import generate_token


class ContactViewTestCase(APITestCase):
    """Test case for create and list contact with multiple email and phone numbers"""

    def setUp(self):
        self.client = APIClient()

        self.contact_url = reverse("contact_view")

        self.user = User.objects.create(
            email="testemail@gmail.com",
            password=make_password("Password@123"),
            name="test name",
        )

        self.contact = Contact.objects.create(
            user=self.user,
            first_name="first name",
            last_name="last name",
            nick_name="nick name",
            web_url="https://web url",
            address="address",
            zip_code="zip 89",
            country="IN",
            birthday="2025-01-01",
            notes="notes",
        )
        self.contact_email = ContactEmail.objects.create(
            contact=self.contact,
            email="testemail1@gamil.com",
            tag="test tag",
            is_primary=0,
        )
        self.contact_phone = ContactPhone.objects.create(
            contact=self.contact, phone="9878656788", tag="test tag", is_primary=0
        )
        access_expiry_web = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRY_WEB))
        self.access_token = generate_token(
            self.user, purpose="access", expiry=access_expiry_web
        )

    def post_contact_data(self, contact_data):
        """Common function to post signup data and return the response"""

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        return self.client.post(
            self.contact_url, json.dumps(contact_data), content_type="application/json"
        )

    def test_create_contact(self):
        """Test to create new contact with valid data"""

        contact_data = {
            "last_name": "last name",
            "first_name": "last name",
            "nick_name": "nick name",
            "web_url": "https://web_url",
            "address": "address",
            "zip_code": "UN890",
            "country": "UN",
            "birthday": "2022-01-01",
            "notes": "notes",
            "phone_numbers": [{"phone": "7865908799", "tag": "test tag"}],
            "emails": [{"email": "test@gmail.com", "tag": "test tag 1"}],
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_create_contact_data(self):
        """Test to create new contact with valid data"""

        contact_data = {
            "last_name": "",
            "first_name": "first name",
            "nick_name": "nick name",
            "web_url": "",
            "address": "",
            "zip_code": "",
            "country": "",
            "birthday": "",
            "notes": "",
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_validate_web_url(self):
        """Test for validate web url"""

        contact_data = {
            "last_name": "last name",
            "web_url": "test web url",
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"]["web_url"],
            "Enter a valid URL (starting with http:// or https://)",
        )

    def test_validate_address(self):
        """Test for validate address"""

        contact_data = {
            "last_name": "last name",
            "address": "address" * 1000,
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"]["address"], "Address too long")

    def test_validate_notes(self):
        """Test for validate notes"""

        contact_data = {
            "last_name": "last name",
            "notes": "address" * 3000,
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"]["notes"], "Note too long")

    def test_validate_country_code(self):
        """Test for validate country code"""

        contact_data = {
            "last_name": "last name",
            "country": "code",
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"]["country"], "Enter a valid 2-letter country code"
        )

    def test_validate_zip_code(self):
        """Test for validate country code"""

        contact_data = {
            "last_name": "last name",
            "zip_code": "123",
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"]["zip_code"], "Invalid zip code format")

    def test_validate_birthday(self):
        """Test for validate birthday"""

        contact_data = {
            "last_name": "last name",
            "birthday": "birthday",
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"]["birthday"],
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
        )

        # future date

        contact_data = {
            "last_name": "last name",
            "birthday": "2050-10-01",
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"]["birthday"],
            "Birthday cannot be a future date",
        )

    def test_validate_emails(self):
        """Test for validate web url"""

        contact_data = {
            "last_name": "last name",
            "emails": [
                {"email": "testemail@gmail.com", "is_primary": 1, "tag": "test tag 1"},
                {"email": "testemail@gmail.com", "is_primary": 1, "tag": "test tag 2"},
                {"email": "testemail1@gamil.com", "is_primary": 0, "tag": "test tag 3"},
            ],
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertIn("emails", response.data["error"])

    def test_validate_phone_numbers(self):
        """Test valdiate phone numbers"""

        contact_data = {
            "last_name": "last name",
            "phone_numbers": [
                {"phone": "7865678909", "is_primary": 1, "tag": "test tag 1"},
                {"phone": "8767", "is_primary": 1, "tag": "test tag 2"},
                {"phone": "7865678909", "is_primary": 0, "tag": "test tag 3"},
                {"phone": "9878656788", "is_primary": 0, "tag": "test tag 3"},
            ],
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone_numbers", response.data["error"])

    def test_missing_phone_number_fields(self):
        """Test valdiate phone numbers"""

        contact_data = {
            "last_name": "last name",
            "phone_numbers": [
                {"phone": "7865678909", "is_primary": 1, "tag": "test tag 1"},
                {
                    "phone": "8767",
                    "is_primary": 1,
                },
                {"tag": "test tag 3"},
            ],
        }

        response = self.post_contact_data(contact_data)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone_numbers", response.data["error"])

    def test_get_contact_details(self):
        """Test successfully list contact details"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.contact_url)
        response.render()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["pager"]["page"], 1)
        self.assertEqual(response.data["pager"]["limit"], 10)
        self.assertEqual(response.data["pager"]["page_count"], 1)
        self.assertEqual(response.data["pager"]["item_count"], 1)
        self.assertIsNone(response.data["pager"]["sort_key"])
        self.assertIsNone(response.data["pager"]["sort_order"])
        self.assertIn("items", response.data)

    def test_invalid_filter_options(self):
        """Test invalid filter options while listing contacts"""

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        query_params = {
            "search": "hello",
            "sort_key": "name",
            "sort_order": "1",
        }
        response = self.client.get(self.contact_url, query_params)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertIn("sort_key", response.data["error"])
        self.assertIn("sort_order", response.data["error"])

    def test_invalid_page(self):
        """Test invalid filter options while listing contacts"""

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        query_params = {
            "page": "2",
        }
        response = self.client.get(self.contact_url, query_params)
        response.render()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"]["page"], "Invalid page")

    def test_valid_filter_options(self):
        """Test valid filter options and return response"""

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        query_params = {
            "search_by": "first_name",
            "search": "first name",
            "sort_key": "first_name",
            "sort_order": "desc",
        }
        response = self.client.get(self.contact_url, query_params)
        response.render()
        self.assertEqual(response.status_code, 200)