from django.urls import path

from mailing import views

urlpatterns = [
    # Клиенты
    path('clients/', views.ClientList.as_view(), name='clients_list'),
    path('clients/add/', views.ClientCreate.as_view(), name='client_add'),
    path('clients/<int:pk>/edit/', views.ClientUpdate.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', views.ClientDelete.as_view(), name='client_delete'),

    # Сообщения
    path('messages/', views.MessageList.as_view(), name='messages_list'),
    path('messages/add/', views.MessageCreate.as_view(), name='message_add'),
    path('messages/<int:pk>/edit/', views.MessageUpdate.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', views.MessageDelete.as_view(), name='message_delete'),

    # Рассылки
    path('mailings/', views.MailingList.as_view(), name='mailings_list'),
    path('mailings/add/', views.MailingCreate.as_view(), name='mailing_add'),
    path('mailings/<int:pk>/edit/', views.MailingUpdate.as_view(), name='mailing_edit'),
    path('mailings/<int:pk>/delete/', views.MailingDelete.as_view(), name='mailing_delete'),
    path('mailings/<int:mailing_id>/attempts/', views.MailingAttemptList.as_view(), name='mailing_attempts_list'),

    # Отправка рассылки вручную
    path('mailings/<int:pk>/send/', views.send_mailing, name='mailing_send'),
]

urlpatterns += [
    path('', views.home, name='home'),
]

urlpatterns += [
    path('stats/', views.user_stats, name='user_stats'),
]