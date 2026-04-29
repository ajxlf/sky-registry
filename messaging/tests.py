from django.contrib.auth.models import User
# import User model for authentication

from django.test import TestCase
# base class for writing tests

from django.urls import reverse
# used to get URLs by name

from messaging.models import Message
# import Message model


class MessagingViewsTests(TestCase):
    # test class for messaging views

    def setUp(self):
        # runs before each test

        self.user = User.objects.create_user(
            username="testuser",
            password="sky1234"
        )
        # create test user

        self.client.login(username="testuser", password="sky1234")
        # log in user

        self.inbox_msg = Message.objects.create(
            sender_name="Sarah Johnson",
            sender_email="sarah.johnson@skyengineering.com",
            recipient_name="John Doe",
            recipient_email="john.doe@skyengineering.com",
            subject="Project Update - Q1 Planning",
            body="Hi team, here is the latest on Q1 planning.",
            folder=Message.FOLDER_INBOX,
            is_read=False,
        )
        # create sample inbox message

        self.draft_msg = Message.objects.create(
            sender_name="John Doe",
            sender_email="john.doe@skyengineering.com",
            recipient_name="Engineering Team",
            subject="Q1 Performance Review Summary",
            body="Draft body",
            folder=Message.FOLDER_DRAFT,
        )
        # create sample draft message

    def test_inbox_redirects_if_not_logged_in(self):
        # test that inbox requires login

        self.client.logout()

        response = self.client.get(reverse("messaging:inbox"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('messaging:inbox')}",
        )

    def test_inbox_lists_inbox_messages(self):
        # test inbox page shows messages

        response = self.client.get(reverse("messaging:inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project Update - Q1 Planning")

    def test_drafts_lists_drafts(self):
        # test drafts page shows drafts

        response = self.client.get(reverse("messaging:drafts"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Q1 Performance Review Summary")

    def test_view_marks_inbox_as_read(self):
        # test opening message marks it as read

        self.assertFalse(self.inbox_msg.is_read)

        self.client.get(reverse("messaging:view", args=[self.inbox_msg.pk]))

        self.inbox_msg.refresh_from_db()

        self.assertTrue(self.inbox_msg.is_read)

    def test_inbox_badge_counts_only_unread_inbox_messages(self):
        # test unread badge only shows unread inbox messages

        self.inbox_msg.is_read = True
        self.inbox_msg.save(update_fields=["is_read"])

        Message.objects.create(
            sender_name="John Doe",
            sender_email="john.doe@skyengineering.com",
            recipient_name="Ops Team",
            recipient_email="ops@skyengineering.com",
            subject="Unsent draft",
            body="Still drafting",
            folder=Message.FOLDER_DRAFT,
            is_read=False,
        )
        # create draft (should NOT count in inbox badge)

        response = self.client.get(reverse("messaging:inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "folder-nav__badge")

    def test_compose_send_creates_sent_message(self):
        # test sending message creates "sent" message

        response = self.client.post(
            reverse("messaging:compose"),
            {
                "recipient_name": "Alex Thompson",
                "recipient_email": "alex.thompson@skyengineering.com",
                "subject": "Hello",
                "body": "Test body",
                "action": "send",
            },
        )

        self.assertRedirects(response, reverse("messaging:sent"))

        self.assertTrue(
            Message.objects.filter(
                subject="Hello",
                folder=Message.FOLDER_SENT
            ).exists()
        )

    def test_compose_save_draft(self):
        # test saving message as draft

        response = self.client.post(
            reverse("messaging:compose"),
            {
                "recipient_name": "",
                "recipient_email": "",
                "subject": "Later",
                "body": "",
                "action": "draft",
            },
        )

        self.assertRedirects(response, reverse("messaging:drafts"))

        self.assertTrue(
            Message.objects.filter(
                subject="Later",
                folder=Message.FOLDER_DRAFT
            ).exists()
        )

    def test_delete_message(self):
        # test deleting a message

        response = self.client.post(
            reverse("messaging:delete", args=[self.inbox_msg.pk])
        )

        self.assertRedirects(response, reverse("messaging:inbox"))

        self.assertFalse(
            Message.objects.filter(pk=self.inbox_msg.pk).exists()
        )

    def test_edit_draft_and_send(self):
        # test editing draft and sending it

        response = self.client.post(
            reverse("messaging:edit", args=[self.draft_msg.pk]),
            {
                "recipient_name": "Engineering Team",
                "recipient_email": "engineering@skyengineering.com",
                "subject": "Q1 Performance Review Summary",
                "body": "Final body",
                "action": "send",
            },
        )

        self.assertRedirects(response, reverse("messaging:sent"))

        self.draft_msg.refresh_from_db()

        self.assertEqual(self.draft_msg.folder, Message.FOLDER_SENT)
        # check it moved to sent

        self.assertEqual(self.draft_msg.body, "Final body")
        # check content updated