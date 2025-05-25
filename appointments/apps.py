from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'
    verbose_name = 'Appointment Booking System'

    def ready(self):
        import appointments.signals

        # Start the scheduler
        from django.conf import settings
        run_scheduler = getattr(settings, 'RUN_SCHEDULER_IN_DEBUG', False)
        if not settings.DEBUG or run_scheduler:
            try:
                from appointments.scheduler import start
                start()
            except Exception as e:
                print(f"Error starting appointment scheduler: {e}")
