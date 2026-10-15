from django.apps import AppConfig

from django.db.backends.signals import connection_created
from django.dispatch import receiver


class SakartveloConfig(AppConfig):
    name = 'sakartvelo'


@receiver(connection_created)
def register_sqlite_unicode_lower(connection, **kwargs):
    """Overrides SQLite's default lower() function with Python's unicode-aware .lower()"""
    if connection.vendor == 'sqlite':
        connection.connection.create_function('lower', 1, lambda val: val.lower() if val else val)
