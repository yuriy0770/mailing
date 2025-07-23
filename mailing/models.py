from django.db import models

class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Created', 'Создана'),
        ('Started', 'Запущена'),
        ('Finished', 'Завершена'),
    ]
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

class MailingAttempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Success', 'Успешно'), ('Fail', 'Не успешно')])
    server_response = models.TextField()