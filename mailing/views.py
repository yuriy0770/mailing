import threading

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils import timezone

from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from .utils import send_mailing_emails


# Классы для Клиентов

class ClientList(ListView):
    model = Client
    template_name = 'clients_list.html'
    context_object_name = 'clients'

class ClientCreate(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('clients_list')

class ClientUpdate(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('clients_list')

class ClientDelete(DeleteView):
    model = Client
    template_name = 'client_confirm_delete.html'
    success_url = reverse_lazy('clients_list')

# Классы для Сообщений

class MessageList(ListView):
    model = Message
    template_name = 'messages_list.html'
    context_object_name = 'messages'

class MessageCreate(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('messages_list')

class MessageUpdate(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('messages_list')

class MessageDelete(DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('messages_list')

# Класы для Рассылок

class MailingList(ListView):
    model = Mailing
    template_name = 'mailings_list.html'
    context_object_name = 'mailings'

class MailingCreate(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailings_list')

class MailingUpdate(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailings_list')

class MailingDelete(DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings_list')


class MailingAttemptList(ListView):
    model = MailingAttempt
    template_name = 'mailing_attempts_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        mailing_id = self.kwargs.get('mailing_id')
        return MailingAttempt.objects.filter(mailing_id=mailing_id).order_by('-date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = Mailing.objects.get(id=self.kwargs.get('mailing_id'))
        return context


@require_POST
def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.status == 'finished':
        messages.error(request, 'Рассылка уже завершена и не может быть отправлена снова.')
        return redirect('mailings_list')

    # Запуск отправки в отдельном потоке, чтобы не блокировать HTTP-запрос
    thread = threading.Thread(target=send_mailing_emails, args=(mailing,))
    thread.start()

    messages.success(request, 'Рассылка запущена на отправку.')
    return redirect('mailings_list')