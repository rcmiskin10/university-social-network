from django.dispatch import Signal


notify = Signal(providing_args=['target', 'sender', 'recipient', 'action', 'affected_users'])