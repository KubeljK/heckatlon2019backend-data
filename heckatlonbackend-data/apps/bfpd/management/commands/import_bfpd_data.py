from django.core.management.base import BaseCommand

import apps.bfpd.dataimport as dataimport


class Command(BaseCommand):
    help = 'Import bfpd data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dirpath', dest='dir_path', type=str,
            help='Path do directory containing csv files.'
            )
        
    def handle(self, *args, **options):
        if options['dir_path']:
            dir_path = options['dir_path']

        else:
            raise ValueError("Dirpath parameter is required!")
        
        dataimport.import_data(dir_path)
        self.stdout.write(self.style.SUCCESS('Successfully synced %s.'%dir_path))
