from django.apps import AppConfig
# import base AppConfig class from Django


class MessagingConfig(AppConfig):
    # configuration class for messaging app

    default_auto_field = 'django.db.models.BigAutoField'
    # default type for auto-generated primary keys (ID field)

    name = 'messaging'
    # name of the app (must match folder name)