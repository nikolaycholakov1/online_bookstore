from django.apps import AppConfig


class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'online_bookstore.apps.book'

    def ready(self):
        import online_bookstore.apps.book.signals
        result = super().ready()
        return result
