import threading
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from .utils import send_mailing_emails


# Классы для Клиентов
@method_decorator(cache_page(60*15), name='dispatch')
class ClientList(ListView):
    model = Client
    template_name = 'clients_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)

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

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists():
            return Client.objects.none()

        return Client.objects.filter(owner=user)

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

def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='started').count()
    # Получатели в рассылках — уникальные
    unique_clients = Client.objects.filter(mailing__isnull=False).distinct().count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
    }
    return render(request, 'home.html', context)

@login_required
def user_stats(request):
    user = request.user

    mailings = user.mailings.all()
    total_mailings = mailings.count()

    success_attempts = MailingAttempt.objects.filter(
        mailing__owner=user, status='success'
    ).count()

    failed_attempts = MailingAttempt.objects.filter(
        mailing__owner=user, status='failed'
    ).count()

    total_messages_sent = success_attempts  # можно считать так

    context = {
        'total_mailings': total_mailings,
        'success_attempts': success_attempts,
        'failed_attempts': failed_attempts,
        'total_messages_sent': total_messages_sent,
    }
    return render(request, 'user_stats.html', context)