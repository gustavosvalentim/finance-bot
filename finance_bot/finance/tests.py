from django.test import TestCase
from rest_framework.test import APIClient

from finance_bot.finance import models


class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = models.User.objects.create(name='Test user')
        self.category = models.Category.objects.create(name='Test category', limit=1000, is_income=False, user=self.user)

    def test_subcategories_cant_exceed_category_limit(self):
        models.Subcategory.objects.create(category=self.category, limit=500)
        response = self.client.post('/finance/subcategories/', {'category': self.category.id, 'limit': 600})

        self.assertEqual(response.status_code, 400)
