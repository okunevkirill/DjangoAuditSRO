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

    def test_str_to_model(self):
        user = CustomUser.objects.create_user(**self.DATA_USER)
        expected_data = f"User(pk={user.pk}, email={self.DATA_USER['email']})"
        self.assertEqual(expected_data, str(user))

    def tearDown(self):
        pass


class OrganizationApiTestCase(APITestCase):
    def setUp(self):
        self.BASE_URL = '/api/organizations/'
        self.DATA_ORGANIZATION_1 = dict(
            name='KU', tax_number='1111111111', base_tax_number='1111111111111',
            legal_address='Planet Plyuk', site_url='https://ku.plk/')
        self.DATA_ORGANIZATION_2 = dict(
            name='KY', tax_number='2222222222', base_tax_number='2222222222222',
            legal_address='Pipelac', site_url='https://ky.plk/')
        self.CONTEXT = {'request': APIRequestFactory().get('/')}

    def test_get(self):
        organization_1 = Organization.objects.create(**self.DATA_ORGANIZATION_1)
        organization_2 = Organization.objects.create(**self.DATA_ORGANIZATION_2)
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = OrganizationSerializer([organization_1, organization_2],
                                                 many=True, context=self.CONTEXT).data
        self.assertEqual(serializer_data, response.data)

    def test_serializer(self):
        organization_1 = Organization.objects.create(**self.DATA_ORGANIZATION_1)
        organization_2 = Organization.objects.create(**self.DATA_ORGANIZATION_2)
        serializer_data = OrganizationSerializer([organization_1, organization_2],
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
        organization = Organization.objects.create(**self.DATA_ORGANIZATION_1)
        expected_data = f"Organization(pk={organization.pk}, name={self.DATA_ORGANIZATION_1['name']})"
        self.assertEqual(expected_data, str(organization))

    def tearDown(self):
        pass


class CompanyApiTestCase(APITestCase):
    def setUp(self):
        self.BASE_URL = '/api/companies/'
        organization = Organization.objects.create(
            name='KU', tax_number='1111111111', base_tax_number='1111111111111',
            legal_address='Planet Plyuk', site_url='https://ku.plk/'
        )
        self.DATA_COMPANY_1 = dict(
            organization_id=organization, name='Horns and hooves', tax_number='1111111111',
            legal_address='County town N', info='Some text', info_url='http://127.0.0.1:8000/'
        )
        self.DATA_COMPANY_2 = dict(
            organization_id=organization, name='Horns and hooves', tax_number='2222222222',
            legal_address='Distant galaxy', info='Some text', info_url='https://github.com/'
        )
        self.CONTEXT = {'request': APIRequestFactory().get('/')}

    def test_get(self):
        company_1 = Company.objects.create(**self.DATA_COMPANY_1)
        company_2 = Company.objects.create(**self.DATA_COMPANY_2)
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = CompanySerializer([company_1, company_2], many=True, context=self.CONTEXT).data
        self.assertEqual(serializer_data, response.data)

    def test_str_to_model(self):
        company = Company.objects.create(**self.DATA_COMPANY_1)
        expected_data = f"Company(pk={company.pk}, name={self.DATA_COMPANY_1['name']})"
        self.assertEqual(expected_data, str(company))

    def tearDown(self):
        pass
