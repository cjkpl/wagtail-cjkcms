from django.core.management.base import BaseCommand
import csv
from os.path import exists
from django.apps import apps


class Command(BaseCommand):
    help = "Creating --model_name objects for --app_name according the file --path specified"

    _LAZY_LOADS = {}

    def get_model(self, app, model):
        """Wrapper around django's get_model."""
        if "get_model" not in self._LAZY_LOADS:
            self._lazy_load_get_model()

        _get_model = self._LAZY_LOADS["get_model"]
        return _get_model(app, model)

    def _lazy_load_get_model(self):
        """Lazy loading of get_model.
        get_model loads django.conf.settings, which may fail if
        the settings haven't been configured yet.
        """
        from django import apps as django_apps

        self._LAZY_LOADS["get_model"] = django_apps.apps.get_model

    def add_arguments(self, parser):
        parser.add_argument("--path", required=True, type=str, help="file path")
        parser.add_argument("--model_name", required=True, type=str, help="model name")
        parser.add_argument(
            "--app_name",
            required=True,
            type=str,
            help="django app name that the model is connected to",
        )
        parser.add_argument(
            "--refresh",
            type=str,
            help="if refresh=yes, clear all data in the model before import.",
        )
        parser.add_argument(
            "--delimiter", type=str, help="delimiter for csv file", default=","
        )

    def handle(self, *args, **options):
        file_path = options["path"]
        if not exists(file_path):
            self.stdout.write(f"File path does not exist: {file_path}")
            return
        app_name = options["app_name"]
        if not apps.is_installed(app_name):
            self.stdout.write(f"App name is not installed: {app_name}")
            return
        _model = self.get_model(options["app_name"], options["model_name"])
        if options["refresh"] == "yes":
            self.stdout.write(f"Refreshing model: {_model.__name__}")
            _model.objects.all().delete()
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=",", quotechar="'")
            header = next(reader)
            for row in reader:
                _object_dict = dict(zip(header, row))
                _model.objects.create(**_object_dict)
                str_from_dict = "\n".join(f"{k}\t{v}" for k, v in _object_dict.items())
                self.stdout.write(f"Created: {str_from_dict}")
