from django.core.management.base import BaseCommand

import apps.bfpd.dataexport as dataexport


class Command(BaseCommand):
    help = 'Import bfpd data.'

    def handle(self, *args, **options):
        dataexport.create_joined_tables()
        self.stdout.write(self.style.SUCCESS('Successfully synced tables.'))
