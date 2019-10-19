import csv

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, DatabaseError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)
        parser.add_argument('file', type=str)

    def load_csv(self, file_path):
        with open(file_path) as f:
            for item in csv.DictReader(f):
                yield item

    def handle(self, *args, **options):
        model_name = options.get('model')
        file_path = options.get('file')

        try:
            model_class = apps.get_model(*model_name.split('.', 1))
            data_set = self.load_csv(file_path)
            fields = model_class._meta.get_fields()
            with transaction.atomic():
                for obj in data_set:
                    instance = model_class()
                    for field in fields:
                        if field.name in obj:
                            setattr(instance, field.name,
                                    obj.get(field.name).strip().lower())
                    instance.save()
                print("Csv file imported successfully.")
        except DatabaseError as e:
            print("Failed to handle insert query please "
                  "check the data and model constraints : {}".format(e))
        except Exception as e:
            print("Failed to load model due to following error : {}".format(e))
