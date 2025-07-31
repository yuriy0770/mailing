
from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment', 'count_clients')
    search_fields = ('email', 'full_name')

    @admin.display(description="Символы")
    def count_clients(self, client: Client):
        return f'Кол-во символов в комментарии {len(client.comment)}'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'first_send', 'finish_send', 'status')
    list_filter = ('status',)
    filter_horizontal = ('clients',)

@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'date_time', 'status')
    list_filter = ('status',)
    readonly_fields = ('date_time', 'server_response')