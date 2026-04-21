from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient_name', 'recipient_email', 'subject', 'body']
        widgets = {
            'recipient_name': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Enter recipient name',
                }
            ),
            'recipient_email': forms.EmailInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Enter recipient email or name',
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Enter message subject',
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'class': 'form-input form-input--textarea',
                    'placeholder': 'Type your message here...',
                    'rows': 10,
                }
            ),
        }

    def clean(self):
        cleaned = super().clean()
        action = self.data.get('action', 'send')
        if action == 'send':
            missing = []
            if not cleaned.get('recipient_email') and not cleaned.get('recipient_name'):
                missing.append('recipient')
            if not cleaned.get('subject'):
                missing.append('subject')
            if not cleaned.get('body'):
                missing.append('message')
            if missing:
                raise forms.ValidationError(
                    f"Please fill in the {', '.join(missing)} before sending."
                )
        return cleaned
