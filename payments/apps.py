from django.apps import AppConfig

class PaymentsConfig(AppConfig):
    defaults_auto_filed="django.db.models.BigAutoField"
    name="payments"

    def ready (self):
        import payments.signals
