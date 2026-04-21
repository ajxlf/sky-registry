from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'sender_name',
        'recipient_name',
        'folder',
        'is_read',
        'created_at',
    )
    list_filter = ('folder', 'is_read', 'created_at')
    search_fields = (
        'subject',
        'body',
        'sender_name',
        'sender_email',
        'recipient_name',
        'recipient_email',
    )
    readonly_fields = ('created_at', 'updated_at')
