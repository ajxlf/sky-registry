from django.db import models


class Message(models.Model):
    FOLDER_INBOX = 'inbox'
    FOLDER_SENT = 'sent'
    FOLDER_DRAFT = 'draft'

    FOLDER_CHOICES = [
        (FOLDER_INBOX, 'Inbox'),
        (FOLDER_SENT, 'Sent'),
        (FOLDER_DRAFT, 'Drafts'),
    ]

    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    recipient_name = models.CharField(max_length=100, blank=True)
    recipient_email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    folder = models.CharField(
        max_length=10, choices=FOLDER_CHOICES, default=FOLDER_INBOX
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject or '(no subject)'
