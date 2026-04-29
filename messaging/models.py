from django.db import models
# import Django models


class Message(models.Model):
    # model to store messages

    FOLDER_INBOX = 'inbox'
    FOLDER_SENT = 'sent'
    FOLDER_DRAFT = 'draft'
    # constants for message folders

    FOLDER_CHOICES = [
        (FOLDER_INBOX, 'Inbox'),
        (FOLDER_SENT, 'Sent'),
        (FOLDER_DRAFT, 'Drafts'),
    ]
    # choices used for folder field

    sender_name = models.CharField(max_length=100)
    # name of sender

    sender_email = models.EmailField()
    # email of sender

    recipient_name = models.CharField(max_length=100, blank=True)
    # name of recipient (optional)

    recipient_email = models.EmailField(blank=True)
    # email of recipient (optional)

    subject = models.CharField(max_length=200, blank=True)
    # message subject (optional)

    body = models.TextField(blank=True)
    # message content (optional)

    folder = models.CharField(
        max_length=10,
        choices=FOLDER_CHOICES,
        default=FOLDER_INBOX
    )
    # folder where message is stored (inbox, sent, draft)

    is_read = models.BooleanField(default=False)
    # mark message as read or unread

    created_at = models.DateTimeField(auto_now_add=True)
    # time when message is created

    updated_at = models.DateTimeField(auto_now=True)
    # time when message is last updated

    class Meta:
        ordering = ['-created_at']
        # show newest messages first

    def __str__(self):
        # display message in admin or shell
        return self.subject or '(no subject)'