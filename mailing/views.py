from django.views.generic import TemplateView

from mailing.models import Mailing


class MailingTemplateViews(TemplateView):
    model = Mailing
    fields = "__all__"