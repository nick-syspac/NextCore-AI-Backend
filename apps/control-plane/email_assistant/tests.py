from django.test import TestCase
from django.utils import timezone
from .models import (
    StudentMessage, DraftReply, MessageTemplate,
    ConversationThread, ToneProfile, ReplyHistory
)


class StudentMessageModelTest(TestCase):
    def test_create_student_message(self):
        message = StudentMessage.objects.create(
            tenant='test-tenant',
            student_name='John Doe',
            student_email='john@example.com',
            message_type='email',
            subject='Assessment Query',
            message_body='I have a question about my assignment.',
            priority='medium'
        )
        self.assertIsNotNone(message.message_number)
        self.assertTrue(message.message_number.startswith('MSG-'))
        self.assertEqual(message.status, 'new')
    
    def test_auto_generated_message_number(self):
        message1 = StudentMessage.objects.create(
            tenant='test-tenant',
            student_name='Jane Smith',
            student_email='jane@example.com',
            subject='Test',
            message_body='Test message'
        )
        message2 = StudentMessage.objects.create(
            tenant='test-tenant',
            student_name='Bob Johnson',
            student_email='bob@example.com',
            subject='Test',
            message_body='Test message'
        )
        self.assertNotEqual(message1.message_number, message2.message_number)


class DraftReplyModelTest(TestCase):
    def setUp(self):
        self.message = StudentMessage.objects.create(
            tenant='test-tenant',
            student_name='Test Student',
            student_email='test@example.com',
            subject='Test Subject',
            message_body='Test body'
        )
    
    def test_create_draft_reply(self):
        draft = DraftReply.objects.create(
            student_message=self.message,
            reply_body='Thank you for your message.',
            tone_used='professional',
            formality_level=3
        )
        self.assertIsNotNone(draft.draft_number)
        self.assertTrue(draft.draft_number.startswith('DRAFT-'))
        self.assertGreater(draft.word_count, 0)
    
    def test_word_count_calculation(self):
        draft = DraftReply.objects.create(
            student_message=self.message,
            reply_body='This is a test reply with exactly ten words.',
            tone_used='professional'
        )
        self.assertEqual(draft.word_count, 9)


class MessageTemplateModelTest(TestCase):
    def test_create_template(self):
        template = MessageTemplate.objects.create(
            tenant='test-tenant',
            name='Assessment Response',
            template_type='assessment',
            template_body='Hi {student_name}, regarding your assessment...',
            default_tone='professional'
        )
        self.assertIsNotNone(template.template_number)
        self.assertTrue(template.template_number.startswith('TMPL-'))
        self.assertTrue(template.is_active)


class ConversationThreadModelTest(TestCase):
    def test_create_thread(self):
        thread = ConversationThread.objects.create(
            tenant='test-tenant',
            student_email='student@example.com',
            student_name='Test Student',
            subject='Ongoing Discussion'
        )
        self.assertIsNotNone(thread.thread_number)
        self.assertTrue(thread.thread_number.startswith('THREAD-'))
        self.assertTrue(thread.is_active)


class ToneProfileModelTest(TestCase):
    def test_create_tone_profile(self):
        profile = ToneProfile.objects.create(
            tenant='test-tenant',
            name='Empathetic Support',
            tone_descriptor='empathetic',
            formality_level=3,
            empathy_level=5
        )
        self.assertIsNotNone(profile.profile_number)
        self.assertTrue(profile.profile_number.startswith('TONE-'))


class ReplyHistoryModelTest(TestCase):
    def setUp(self):
        self.message = StudentMessage.objects.create(
            tenant='test-tenant',
            student_name='Test Student',
            student_email='test@example.com',
            subject='Test',
            message_body='Test'
        )
        self.draft = DraftReply.objects.create(
            student_message=self.message,
            reply_body='Test reply',
            tone_used='professional'
        )
    
    def test_create_reply_history(self):
        history = ReplyHistory.objects.create(
            student_message=self.message,
            draft_reply=self.draft,
            final_reply_body='Final reply',
            final_subject='Re: Test',
            time_to_send_seconds=120,
            estimated_manual_time_seconds=300,
            sent_by='trainer@example.com'
        )
        self.assertIsNotNone(history.history_number)
        self.assertTrue(history.history_number.startswith('HIST-'))
        self.assertEqual(history.time_saved_seconds, 180)
        self.assertGreater(history.time_saved_percentage, 0)
