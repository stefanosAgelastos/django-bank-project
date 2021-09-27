from django.core.management.base import BaseCommand
from bank.models import Rank


class Command(BaseCommand):
    def handle(self, **options):
        print('Provisioning ...')
        if not Rank.objects.all():
            Rank.objects.create(name='Platinum', value=90)
            Rank.objects.create(name='Gold', value=75)
            Rank.objects.create(name='Silver', value=50)
            Rank.objects.create(name='Bronze', value=10)
