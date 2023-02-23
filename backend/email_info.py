'''This module contains the details for the email server to send emails from'''

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'feedback.scottbradyapps@gmail.com'
EMAIL_HOST_PASSWORD = 'qqrfxteygyraancq'
EMAIL_PORT = 587
EMAIL_USE_SSL = False
