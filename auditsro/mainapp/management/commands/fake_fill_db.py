import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from mainapp.models import Company, Organization, Watchlist

# ToDo Реализовать передачу аргументов в явном виде и реализовать команду через
#  Fake-классы (скрипт не оптимизировал - не является основным функционалом).
#  Поставить защиту транзакций.

NUMBER_USER = 15
NUMBER_ORGANIZATION = 8
NUMBER_COMPANY = 100


class Command(BaseCommand):
    help = (f'Filling the database with fake data (users={NUMBER_USER}, '
            f'organizations={NUMBER_ORGANIZATION}, companies={NUMBER_COMPANY})')

    def handle(self, *args, **options):
        users, organizations, companies = [], [], []
        user_model = get_user_model()
        fake = Faker('ru_RU')

        for _ in range(NUMBER_USER):
            data = dict(
                email=fake.unique.email(),
                is_active=random.choice([True, False]),
                phone=fake.unique.phone_number(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            users.append(user_model(**data))
        user_model.objects.bulk_create(users)
        self.stdout.write('  Users created...')

        for _ in range(NUMBER_ORGANIZATION):
            data = dict(
                name=fake.bank(),
                is_active=random.choice([True, False]),
                tax_number=''.join(random.choice('0123456789') for _ in range(11)),
                base_tax_number=''.join(random.choice('0123456789') for _ in range(13)),
                legal_address=fake.address(),
                site_url=fake.url(),
            )
            organizations.append(Organization(**data))
        Organization.objects.bulk_create(organizations)
        self.stdout.write('  SRO have been created...')

        for _ in range(NUMBER_COMPANY):
            data = dict(
                organization_id=random.choice(organizations),
                name=fake.company(),
                is_active=random.choice([True, False]),
                tax_number=''.join(random.choice('0123456789') for _ in range(11)),
                legal_address=fake.address(),
                verification_date=fake.date_time(),
                info=fake.paragraphs(),
                info_url=fake.url(),
            )
            companies.append(Company(**data))
        Company.objects.bulk_create(companies)
        self.stdout.write('  SRO member companies have been created...')

        for user in users:
            random.shuffle(companies)
            tracked_list = Watchlist.objects.create(user=user)
            tracked_list.companies.add(*companies[:random.randint(0, NUMBER_COMPANY - 1)])
        self.stdout.write('  Watchlists added...')

        self.stdout.write(f'[*] Script {self.__module__!r} ending')
