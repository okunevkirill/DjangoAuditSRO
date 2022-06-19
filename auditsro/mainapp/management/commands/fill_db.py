import csv
from datetime import datetime
from pathlib import Path

from django.core.management import BaseCommand
from django.db import IntegrityError

from mainapp.models import Company, Organization

DATA_NAUFOR = {
    'name': 'НАУФОР',
    'tax_number': '7712088223',
    'base_tax_number': '1027700141523',
    'legal_address': '129090, г. Москва, 1-й Коптельский переулок, д.18, строение 1',
    'site_url': 'https://naufor.ru/',
}

# [*] Ограничение на размер списка добавляемых за один запрос компаний к БД
# ввёл специально - можем работать с большим размером данных.
# По приблизительной оценке размер 1 элемента равен 720 байт.
COMPANY_LIST_SIZE = 300


class Command(BaseCommand):
    help = "Filling the database with real data obtained through scraping"

    def add_arguments(self, parser):
        parser.add_argument(
            '-p', '--path',
            type=str,
            default='naufor.csv',
            help='Path to the file with data on participating companies',
        )

    def handle(self, *args, **options):
        path_to_file = Path(options['path'])

        if not path_to_file.exists() or not path_to_file.is_file():
            raise FileNotFoundError('Source data file not found')
        # ---------------------------------------------------------------------
        # Блок создания компании для которой загружаются данные
        organization = Organization.objects.filter(tax_number=DATA_NAUFOR['tax_number'])
        if organization:
            organization.delete()
        organization = Organization.objects.create(**DATA_NAUFOR)
        # ToDo По всему скрипту заменить `print` на логгер
        self.stdout.write(f"  {DATA_NAUFOR['name']!r} organization was created...")
        # ---------------------------------------------------------------------
        with open(path_to_file, encoding='utf-8') as _file:
            reader = csv.DictReader(_file)
            # -----------------------------------------------------------------
            # Блок проверки корректности файла
            fields = set(map(lambda x: x.name, Company._meta.get_fields()))
            if not all((x in fields for x in reader.fieldnames)):
                raise ValueError('Incorrect column names in file')
            # -----------------------------------------------------------------
            companies = []
            for index, data in enumerate(reader, start=1):
                data['organization_id'] = organization
                # -------------------------------------------------------------
                # Блок привидения даты проверки к нужному формату
                verification_date = data.get('verification_date')
                if verification_date:
                    data['verification_date'] = datetime.strptime(verification_date, '%d.%m.%Y')
                else:
                    data['verification_date'] = None  # Модель позволяет хранить None
                # -------------------------------------------------------------
                companies.append(Company(**data))
                if index % COMPANY_LIST_SIZE == 0:
                    self._save_companies(companies)
                    companies = []
            else:
                self._save_companies(companies)
                self.stdout.write(f"  Companies have been created...")
            # -----------------------------------------------------------------
            self.stdout.write(f'[*] Script {self.__module__!r} ending')

    def _save_companies(self, companies):
        try:
            Company.objects.bulk_create(companies)
        except IntegrityError:
            for company in companies:
                try:
                    company.save()
                except IntegrityError:
                    self.stdout.write(f"  [!] Failed to work out the {company!r} company")
