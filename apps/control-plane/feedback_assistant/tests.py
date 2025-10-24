from django.test import TestCase
from django.contrib.auth.models import User
from .models import FeedbackTemplate, GeneratedFeedback, FeedbackCriterion, FeedbackLog


class FeedbackTemplateModelTests(TestCase):
    """Test cases for FeedbackTemplate model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.template = FeedbackTemplate.objects.create(
            name="Test Feedback Template",
            description="Testing feedback generation",
            tenant="test-tenant",
            created_by=self.user,
            feedback_type='formative',
            sentiment='constructive',
            tone='professional',
            positivity_level=7,
            directness_level=5,
            formality_level=7
        )
    
    def test_template_creation(self):
        """Test that FeedbackTemplate is created with correct attributes"""
        self.assertEqual(self.template.name, "Test Feedback Template")
        self.assertEqual(self.template.tenant, "test-tenant")
        self.assertEqual(self.template.positivity_level, 7)
        self.assertTrue(self.template.template_number.startswith('FBT-'))
    
    def test_template_number_auto_generation(self):
        """Test that template_number is automatically generated"""
        self.assertIsNotNone(self.template.template_number)
        self.assertTrue(len(self.template.template_number) > 10)
    
    def test_sentiment_description(self):
        """Test sentiment description generation"""
        description = self.template.get_sentiment_description()
        self.assertIsNotNone(description)
        self.assertIn("positive", description.lower())


class GeneratedFeedbackModelTests(TestCase):
    """Test cases for GeneratedFeedback model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.template = FeedbackTemplate.objects.create(
            name="Test Template",
            tenant="test-tenant",
            created_by=self.user,
            feedback_type='formative',
            sentiment='constructive'
        )
        self.feedback = GeneratedFeedback.objects.create(
            template=self.template,
            student_id="S12345",
            student_name="John Doe",
            assessment_title="Python Quiz",
            score=85.0,
            max_score=100.0,
            feedback_text="Great work! You demonstrated excellent understanding of Python concepts."
        )
    
    def test_feedback_creation(self):
        """Test that GeneratedFeedback is created correctly"""
        self.assertEqual(self.feedback.student_id, "S12345")
        self.assertEqual(self.feedback.student_name, "John Doe")
        self.assertTrue(self.feedback.feedback_number.startswith('FDB-'))
    
    def test_word_count_calculation(self):
        """Test that word count is calculated on save"""
        self.assertGreater(self.feedback.word_count, 0)
        expected_words = len(self.feedback.feedback_text.split())
        self.assertEqual(self.feedback.word_count, expected_words)
    
    def test_percentage_score_calculation(self):
        """Test percentage score calculation"""
        percentage = self.feedback.get_percentage_score()
        self.assertEqual(percentage, 85.0)
    
    def test_percentage_score_with_no_max(self):
        """Test percentage calculation when max_score is None"""
        feedback = GeneratedFeedback.objects.create(
            template=self.template,
            student_id="S99999",
            student_name="Test User",
            feedback_text="Test feedback"
        )
        self.assertIsNone(feedback.get_percentage_score())


class FeedbackCriterionTests(TestCase):
    """Test cases for FeedbackCriterion model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.template = FeedbackTemplate.objects.create(
            name="Test Template",
            tenant="test-tenant",
            created_by=self.user
        )
        self.criterion = FeedbackCriterion.objects.create(
            template=self.template,
            criterion_name="Understanding",
            description="Demonstrates understanding",
            excellent_feedback="Excellent understanding!",
            good_feedback="Good understanding.",
            satisfactory_feedback="Satisfactory understanding.",
            needs_improvement_feedback="Needs work.",
            weight=0.5,
            display_order=1
        )
    
    def test_criterion_creation(self):
        """Test that FeedbackCriterion is created correctly"""
        self.assertEqual(self.criterion.criterion_name, "Understanding")
        self.assertEqual(self.criterion.weight, 0.5)
    
    def test_get_feedback_for_excellent_score(self):
        """Test getting feedback for excellent performance"""
        feedback = self.criterion.get_feedback_for_score(90)
        self.assertEqual(feedback, "Excellent understanding!")
    
    def test_get_feedback_for_good_score(self):
        """Test getting feedback for good performance"""
        feedback = self.criterion.get_feedback_for_score(75)
        self.assertEqual(feedback, "Good understanding.")
    
    def test_get_feedback_for_satisfactory_score(self):
        """Test getting feedback for satisfactory performance"""
        feedback = self.criterion.get_feedback_for_score(60)
        self.assertEqual(feedback, "Satisfactory understanding.")
    
    def test_get_feedback_for_poor_score(self):
        """Test getting feedback for poor performance"""
        feedback = self.criterion.get_feedback_for_score(40)
        self.assertEqual(feedback, "Needs work.")


class FeedbackLogTests(TestCase):
    """Test cases for FeedbackLog model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.template = FeedbackTemplate.objects.create(
            name="Test Template",
            tenant="test-tenant",
            created_by=self.user
        )
        self.log = FeedbackLog.objects.create(
            template=self.template,
            action='generate_batch',
            performed_by=self.user,
            feedbacks_generated=5,
            total_time=10.5,
            average_sentiment=0.75,
            average_personalization=0.85
        )
    
    def test_log_creation(self):
        """Test that FeedbackLog is created correctly"""
        self.assertEqual(self.log.action, 'generate_batch')
        self.assertEqual(self.log.feedbacks_generated, 5)
    
    def test_average_time_calculation(self):
        """Test that average time per feedback is calculated"""
        expected_avg = 10.5 / 5
        self.assertEqual(self.log.average_time_per_feedback, expected_avg)
