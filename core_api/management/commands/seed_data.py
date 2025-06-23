from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core_api.models import TradeItem

class Command(BaseCommand):
    help = 'Seed database with test data'

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(username='demo', defaults={'password': 'demo1234'})
        TradeItem.objects.get_or_create(
            title='Sample Item',
            description='A test item',
            owner=user,
            interests='Another item'
        )
        self.stdout.write(self.style.SUCCESS('Seed data created.'))