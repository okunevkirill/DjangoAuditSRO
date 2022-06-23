from rest_framework import status
from rest_framework.test import APITestCase

from authapp.models import CustomUser
from authapp.serializers import CustomUserSerializer


class CustomUserApiTestCase(APITestCase):
    def setUp(self):
        self.BASE_URL = '/api/users/'
        self.DATA_SUPER_USER = dict(
            email='supertest@mail.com', password='test123456',
            first_name='SuperTest', last_name='SuperTest', phone='89271111111',
            is_staff=True, is_superuser=True,
        )
        self.DATA_USER = dict(
            email='test@mail.com', password='test123456', first_name='Test',
            last_name='Test', phone='89272222222',
        )

    def test_get(self):
        user_1 = CustomUser.objects.create_user(**self.DATA_SUPER_USER)
        user_2 = CustomUser.objects.create_user(**self.DATA_USER)
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = CustomUserSerializer([user_1, user_2], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_serializer(self):
        user_1 = CustomUser.objects.create_user(**self.DATA_SUPER_USER)
        user_2 = CustomUser.objects.create_user(**self.DATA_USER)
        serializer_data = CustomUserSerializer([user_1, user_2], many=True).data
        expected_data = [
            {
                'email': 'supertest@mail.com',
                'first_name': 'SuperTest',
                'last_name': 'SuperTest',
                'phone': '89271111111'
            },
            {
                'email': 'test@mail.com',
                'first_name': 'Test',
                'last_name': 'Test',
                'phone': '89272222222'
            }
        ]
        self.assertEqual(expected_data, serializer_data)

    def test_model(self):
        user = CustomUser.objects.create_user(**self.DATA_USER)
        expected_data = f"User(pk={user.pk}, email={self.DATA_USER['email']})"
        self.assertEqual(expected_data, str(user))

    def tearDown(self):
        pass
