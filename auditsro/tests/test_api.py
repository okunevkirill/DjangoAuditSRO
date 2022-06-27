from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from authapp.models import CustomUser
from authapp.serializers import CustomUserSerializer
from mainapp.models import Organization, Company
from mainapp.serializers import OrganizationSerializer, CompanySerializer


class CustomUserApiTestCase(APITestCase):
    def setUp(self):
        self.BASE_URL = '/api/users/'
        self.user_1 = CustomUser.objects.create_user(
            email='supertest@mail.com',
            password='test123456',
            first_name='SuperTest',
            last_name='SuperTest',
            phone='89271111111',
            is_staff=True,
            is_superuser=True,
        )
        self.user_2 = CustomUser.objects.create(
            email='test@mail.com',
            password='test123456',
            first_name='Test',
            last_name='TestNemo',
            phone='89272222222',
        )
        self.user_3 = CustomUser.objects.create_user(
            email='nemo@mail.com',
            password='nemo123456',
            first_name='Nemo',
            last_name='Nemo',
            phone='89273333333',
        )

    def test_get(self):
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = CustomUserSerializer([self.user_1, self.user_2, self.user_3], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_serializer(self):
        serializer_data = CustomUserSerializer([self.user_1, self.user_2], many=True).data
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
                'last_name': 'TestNemo',
                'phone': '89272222222'
            }
        ]
        self.assertEqual(expected_data, serializer_data)

    def test_str_to_model(self):
        expected_data = f"User(pk={self.user_2.pk}, email=test@mail.com)"
        self.assertEqual(expected_data, str(self.user_2))

    def test_filter(self):
        response = self.client.get(self.BASE_URL, data={'email': 'test'})
        serializer_data = CustomUserSerializer([self.user_1, self.user_2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_search(self):
        response = self.client.get(self.BASE_URL, data={'search': 'Nemo'})
        serializer_data = CustomUserSerializer([self.user_2, self.user_3], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_ordering(self):
        response = self.client.get(self.BASE_URL, data={'ordering': 'email'})
        serializer_data = CustomUserSerializer([self.user_3, self.user_1, self.user_2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

        response = self.client.get(self.BASE_URL, data={'ordering': '-created_at'})
        serializer_data = CustomUserSerializer([self.user_3, self.user_2, self.user_1], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def tearDown(self):
        pass


class OrganizationApiTestCase(APITestCase):
    def setUp(self):
        self.BASE_URL = '/api/organizations/'
        self.organization_1 = Organization.objects.create(
            name='KU',
            tax_number='1111111111',
            base_tax_number='1111111111111',
            legal_address='Planet Plyuk',
            site_url='https://ku.plk/',
        )
        self.organization_2 = Organization.objects.create(
            name='KY',
            tax_number='2222222222',
            base_tax_number='2222222222222',
            legal_address='Pipelac',
            site_url='https://ky.plk/',
        )
        self.organization_3 = Organization.objects.create(
            name='Mario',
            tax_number='2223331111',
            base_tax_number='2223333333333',
            legal_address='Mushroom kingdom',
            site_url='https://mario.itl/',
        )
        self.CONTEXT = {'request': APIRequestFactory().get(self.BASE_URL)}

    def test_get(self):
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = OrganizationSerializer(
            [self.organization_1, self.organization_2, self.organization_3],
            many=True,
            context=self.CONTEXT
        ).data
        self.assertEqual(serializer_data, response.data)

    def test_serializer(self):
        serializer_data = OrganizationSerializer([self.organization_1, self.organization_2],
                                                 many=True, context=self.CONTEXT).data
        expected_data = [
            {
                'url': serializer_data[0].get('url'),
                'name': 'KU',
                'tax_number': '1111111111',
                'base_tax_number': '1111111111111',
                'legal_address': 'Planet Plyuk',
                'site_url': 'https://ku.plk/'
            },
            {
                'url': serializer_data[1].get('url'),
                'name': 'KY',
                'tax_number': '2222222222',
                'base_tax_number': '2222222222222',
                'legal_address': 'Pipelac',
                'site_url': 'https://ky.plk/'
            }
        ]
        self.assertEqual(expected_data, serializer_data)

    def test_str_to_model(self):
        expected_data = f"Organization(pk={self.organization_1.pk}, name=KU)"
        self.assertEqual(expected_data, str(self.organization_1))

    def test_filter(self):
        response = self.client.get(self.BASE_URL, data={'name': 'rio'})
        serializer_data = OrganizationSerializer([self.organization_3],
                                                 many=True, context=self.CONTEXT).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

        response = self.client.get(self.BASE_URL, data={'tax_number': '222'})
        serializer_data = OrganizationSerializer([self.organization_2, self.organization_3],
                                                 many=True, context=self.CONTEXT).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def tearDown(self):
        pass


class CompanyApiTestCase(APITestCase):
    def setUp(self):
        self.BASE_URL = '/api/companies/'
        organization = Organization.objects.create(
            name='KU', tax_number='1111111111', base_tax_number='1111111111111',
            legal_address='Planet Plyuk', site_url='https://ku.plk/'
        )
        self.company_1 = Company.objects.create(
            organization_id=organization,
            name='Horns and hooves',
            tax_number='1111111111',
            legal_address='County town N',
            info='Some text',
            info_url='http://127.0.0.1:8000/',
        )
        self.company_2 = Company.objects.create(
            organization_id=organization,
            name='Company',
            tax_number='2222222222',
            legal_address='Distant galaxy',
            info='Some text',
            info_url='https://github.com/',
        )
        self.CONTEXT = {'request': APIRequestFactory().get('/')}

    def test_get(self):
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = CompanySerializer(
            [self.company_1, self.company_2], many=True, context=self.CONTEXT).data
        self.assertEqual(serializer_data, response.data)

    def test_str_to_model(self):
        expected_data = f"Company(pk={self.company_1.pk}, name=Horns and hooves)"
        self.assertEqual(expected_data, str(self.company_1))

    def test_filter(self):
        response = self.client.get(self.BASE_URL, data={'name': 'Company'})
        serializer_data = CompanySerializer([self.company_2], many=True, context=self.CONTEXT).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

        response = self.client.get(self.BASE_URL, data={'tax_number': '111'})
        serializer_data = CompanySerializer([self.company_1],
                                            many=True, context=self.CONTEXT).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def tearDown(self):
        pass
