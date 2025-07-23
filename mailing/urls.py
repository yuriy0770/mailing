from django.urls import path

from mailing.views import MailingTemplateViews

app_name="mailing"
urlpatterns = [
    path("", MailingTemplateViews.as_view(), name="home")
]