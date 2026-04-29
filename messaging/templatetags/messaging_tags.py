from django import template
from messaging.models import Message

register = template.Library()


@register.simple_tag
def unread_inbox_count():
    return Message.objects.filter(
        folder=Message.FOLDER_INBOX,
        is_read=False,
    ).count()
