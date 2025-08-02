from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Создать группу Менеджеры и назначить права'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='manager')
        permissions = Permission.objects.filter(codename__in=[
            'view_mailing', 'add_mailing', 'change_mailing',
            'view_message', 'add_message', 'change_message',
            'view_recipient', 'add_recipient', 'change_recipient',
        ])
        group.permissions.set(permissions)
        group.save()
        self.stdout.write(self.style.SUCCESS('Группа Менеджеры создана и права назначены'))