from django.contrib import messages as flash_messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MessageForm
from .models import Message

from django.urls import reverse


CURRENT_USER_NAME = 'John Doe'
CURRENT_USER_EMAIL = 'john.doe@skyengineering.com'


def _filtered(qs, query):
    query = (query or '').strip()
    if not query:
        return qs
    return qs.filter(
        Q(subject__icontains=query)
        | Q(sender_name__icontains=query)
        | Q(recipient_name__icontains=query)
        | Q(recipient_email__icontains=query)
        | Q(body__icontains=query)
    ).distinct()


def inbox(request):
    query = request.GET.get('q', '').strip()
    message_list = _filtered(
        Message.objects.filter(folder=Message.FOLDER_INBOX), query
    )
    return render(
        request,
        'messaging/inbox.html',
        {
            'message_list': message_list,
            'active_folder': 'inbox',
            'query': query,
        },
    )


def sent(request):
    query = request.GET.get('q', '').strip()
    message_list = _filtered(
        Message.objects.filter(folder=Message.FOLDER_SENT), query
    )
    return render(
        request,
        'messaging/sent.html',
        {
            'message_list': message_list,
            'active_folder': 'sent',
            'query': query,
        },
    )


def drafts(request):
    query = request.GET.get('q', '').strip()
    message_list = _filtered(
        Message.objects.filter(folder=Message.FOLDER_DRAFT), query
    )
    return render(
        request,
        'messaging/drafts.html',
        {
            'message_list': message_list,
            'active_folder': 'drafts',
            'query': query,
        },
    )


def compose(request):
    initial = {
        'recipient_name': request.GET.get('recipient_name', ''),
        'recipient_email': request.GET.get('recipient_email', ''),
        'subject': request.GET.get('subject', ''),
        'body': request.GET.get('body', ''),
    }
    if request.method == 'POST':
        form = MessageForm(request.POST)
        action = request.POST.get('action', 'send')
        if form.is_valid():
            message = form.save(commit=False)
            message.sender_name = CURRENT_USER_NAME
            message.sender_email = CURRENT_USER_EMAIL
            if action == 'draft':
                message.folder = Message.FOLDER_DRAFT
                message.save()
                flash_messages.success(request, 'Draft saved.')
                return redirect('messaging:drafts')
            message.folder = Message.FOLDER_SENT
            message.save()
            flash_messages.success(request, 'Message sent.')
            return redirect('messaging:sent')
    else:
        form = MessageForm(initial=initial)

    return render(
        request,
        'messaging/compose.html',
        {
            'form': form,
            'active_folder': 'compose',
        },
    )


def view_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.folder == Message.FOLDER_INBOX and not message.is_read:
        message.is_read = True
        message.save(update_fields=['is_read', 'updated_at'])

    active_folder = {
        Message.FOLDER_INBOX: 'inbox',
        Message.FOLDER_SENT: 'sent',
        Message.FOLDER_DRAFT: 'drafts',
    }.get(message.folder, 'inbox')

    return render(
        request,
        'messaging/view.html',
        {
            'message': message,
            'active_folder': active_folder,
        },
    )


def edit_draft(request, pk):
    message = get_object_or_404(Message, pk=pk, folder=Message.FOLDER_DRAFT)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        action = request.POST.get('action', 'send')
        if form.is_valid():
            updated = form.save(commit=False)
            updated.sender_name = CURRENT_USER_NAME
            updated.sender_email = CURRENT_USER_EMAIL
            if action == 'draft':
                updated.folder = Message.FOLDER_DRAFT
                updated.save()
                flash_messages.success(request, 'Draft updated.')
                return redirect('messaging:drafts')
            updated.folder = Message.FOLDER_SENT
            updated.save()
            flash_messages.success(request, 'Message sent.')
            return redirect('messaging:sent')
    else:
        form = MessageForm(instance=message)

    return render(
        request,
        'messaging/edit.html',
        {
            'form': form,
            'message': message,
            'active_folder': 'drafts',
        },
    )


def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    folder = message.folder
    if request.method == 'POST':
        message.delete()
        flash_messages.success(request, 'Message deleted.')
        return redirect({
            Message.FOLDER_INBOX: 'messaging:inbox',
            Message.FOLDER_SENT: 'messaging:sent',
            Message.FOLDER_DRAFT: 'messaging:drafts',
        }[folder])
    return redirect('messaging:view', pk=message.pk)


def reply(request, pk):
    original = get_object_or_404(Message, pk=pk)

    subject = original.subject or ''
    if not subject.lower().startswith('re:'):
        subject = f'Re: {subject}'

    return redirect(
        f"{reverse('messaging:compose')}?recipient_name={original.sender_name}"
        f"&recipient_email={original.sender_email}"
        f"&subject={subject}"
    )


def forward(request, pk):
    original = get_object_or_404(Message, pk=pk)

    subject = original.subject or ''
    if not subject.lower().startswith('fwd:'):
        subject = f'Fwd: {subject}'

    return redirect(
        f"{reverse('messaging:compose')}?subject={subject}"
    )


def _url(name):
    from django.urls import reverse

    return reverse(name)
