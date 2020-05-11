from django.apps import AppConfig

# from __future__ import unicode_literals

# class FamilyConfig(AppConfig):
#     name = 'family'


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        import user.signals
