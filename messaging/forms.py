from django import forms
# import Django forms

from .models import Message
# import Message model


class MessageForm(forms.ModelForm):
    # form based on Message model

    class Meta:
        model = Message
        # connect form to Message model

        fields = ['recipient_name', 'recipient_email', 'subject', 'body']
        # fields used in the form

        widgets = {
            # customize how form inputs look in HTML

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
        # custom validation for form

        cleaned = super().clean()
        # get cleaned data

        action = self.data.get('action', 'send')
        # check if user clicked "send" or "save draft"

        if action == 'send':
            # only validate required fields when sending

            missing = []

            if not cleaned.get('recipient_email') and not cleaned.get('recipient_name'):
                missing.append('recipient')
                # require at least recipient email or name

            if not cleaned.get('subject'):
                missing.append('subject')
                # require subject

            if not cleaned.get('body'):
                missing.append('message')
                # require message body

            if missing:
                # raise error if something is missing
                raise forms.ValidationError(
                    f"Please fill in the {', '.join(missing)} before sending."
                )

        return cleaned
        # return validated data