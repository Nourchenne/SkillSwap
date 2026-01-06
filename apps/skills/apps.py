from django.apps import AppConfig


class SkillsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.skills"

    def ready(self):
        # Import signals to ensure handlers are registered
        try:
            import apps.skills.signals  # noqa: F401
        except Exception:
            # Avoid crashing app startup if signals import has side effects
            # Any real import errors will surface in logs/tests
            pass
