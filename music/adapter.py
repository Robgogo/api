from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_redirect_url(self, request):
        path = 'auth/register/complete/'
        return path
    
    def get_email_confirmation_url(self, request, emailconfirmation):
        path = 'auth/account-confirm-email/'+emailconfirmation.key+'/'
        return settings.URL_FRONT+path

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        return super().send_confirmation_mail(request, emailconfirmation, signup)
    
    def respond_email_verification_sent(self, request, user):
        """
        We don't need this redirect.
        """
        pass
    