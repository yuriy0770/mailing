from django.conf import settings
from django.db import models



class Client(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    first_send = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mailings', null=True, blank=True)
    finish_send = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f"Рассылка #{self.id} - {self.message.subject}"

class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=True)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()

    def __str__(self):
        return f"Попытка рассылки #{self.id} по клиенту {self.client.email} - {self.status} ({self.date_time})"