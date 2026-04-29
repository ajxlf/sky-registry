from django.contrib import admin
# import Django admin

from .models import Message
# import Message model


@admin.register(Message)
# register Message model in admin panel

class MessageAdmin(admin.ModelAdmin):
    # customize how Message appears in admin

    list_display = (
        'subject',
        'sender_name',
        'recipient_name',
        'folder',
        'is_read',
        'created_at',
    )
    # fields shown in admin list page (table view)

    list_filter = ('folder', 'is_read', 'created_at')
    # filters on right side (filter messages by folder, read status, date)

    search_fields = (
        'subject',
        'body',
        'sender_name',
        'sender_email',
        'recipient_name',
        'recipient_email',
    )
    # fields that can be searched in admin search bar

    readonly_fields = ('created_at', 'updated_at')
    # these fields cannot be edited in admin (auto timestamps)