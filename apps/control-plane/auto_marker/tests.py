from django.test import TestCase
from django.contrib.auth.models import User
from .models import AutoMarker, MarkedResponse, MarkingCriterion, CriterionScore, MarkingLog


class AutoMarkerModelTests(TestCase):
    """Test cases for AutoMarker model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.auto_marker = AutoMarker.objects.create(
            title="Test Auto Marker",
            description="Testing semantic similarity marking",
            tenant="test-tenant",
            created_by=self.user,
            answer_type='short_answer',
            question_text="What is Python?",
            model_answer="Python is a high-level, interpreted programming language known for its simplicity and readability.",
            max_marks=10,
            similarity_model='sentence_transformers',
            similarity_threshold=0.70,
            partial_credit_enabled=True,
            min_similarity_for_credit=0.40,
            use_keywords=True,
            keywords=['Python', 'programming language', 'high-level', 'interpreted']
        )
    
    def test_auto_marker_creation(self):
        """Test that AutoMarker is created with correct attributes"""
        self.assertEqual(self.auto_marker.title, "Test Auto Marker")
        self.assertEqual(self.auto_marker.tenant, "test-tenant")
        self.assertEqual(self.auto_marker.max_marks, 10)
        self.assertTrue(self.auto_marker.marker_number.startswith('AMK-'))
    
    def test_marker_number_auto_generation(self):
        """Test that marker_number is automatically generated"""
        self.assertIsNotNone(self.auto_marker.marker_number)
        self.assertTrue(len(self.auto_marker.marker_number) > 10)
    
    def test_get_marking_statistics(self):
        """Test marking statistics calculation"""
        stats = self.auto_marker.get_marking_statistics()
        self.assertEqual(stats['total_marked'], 0)
        self.assertEqual(stats['avg_similarity'], 0.0)
        self.assertEqual(stats['needs_review'], 0)


class MarkedResponseModelTests(TestCase):
    """Test cases for MarkedResponse model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.auto_marker = AutoMarker.objects.create(
            title="Test Marker",
            tenant="test-tenant",
            created_by=self.user,
            question_text="What is Python?",
            model_answer="Python is a high-level programming language.",
            max_marks=10,
            similarity_threshold=0.70,
            min_similarity_for_credit=0.40,
            use_keywords=True,
            keywords=['Python', 'programming']
        )
        self.response = MarkedResponse.objects.create(
            auto_marker=self.auto_marker,
            student_id="S12345",
            student_name="John Doe",
            response_text="Python is a popular programming language used for many applications."
        )
    
    def test_response_creation(self):
        """Test that MarkedResponse is created correctly"""
        self.assertEqual(self.response.student_id, "S12345")
        self.assertEqual(self.response.student_name, "John Doe")
        self.assertTrue(self.response.response_number.startswith('RSP-'))
    
    def test_word_count_calculation(self):
        """Test that word count is calculated on save"""
        self.assertGreater(self.response.word_count, 0)
        expected_words = len(self.response.response_text.split())
        self.assertEqual(self.response.word_count, expected_words)
    
    def test_calculate_marks_full_credit(self):
        """Test marks calculation for high similarity"""
        self.response.similarity_score = 0.85
        self.response.keyword_match_score = 0.90
        self.response.calculate_marks()
        
        self.assertGreater(self.response.marks_awarded, 0)
        self.assertEqual(self.response.marks_awarded, self.auto_marker.max_marks)
    
    def test_calculate_marks_partial_credit(self):
        """Test marks calculation for partial credit"""
        self.response.similarity_score = 0.55  # Between min and threshold
        self.response.keyword_match_score = 0.50
        self.response.calculate_marks()
        
        self.assertGreater(self.response.marks_awarded, 0)
        self.assertLess(self.response.marks_awarded, self.auto_marker.max_marks)
    
    def test_calculate_marks_no_credit(self):
        """Test marks calculation for low similarity"""
        self.response.similarity_score = 0.20  # Below minimum
        self.response.keyword_match_score = 0.10
        self.response.calculate_marks()
        
        self.assertEqual(self.response.marks_awarded, 0)
    
    def test_review_flagging(self):
        """Test that low confidence triggers review flag"""
        self.response.similarity_score = 0.50
        self.response.calculate_marks()
        
        # Should be flagged due to low confidence
        if self.response.confidence_score < 0.70:
            self.assertTrue(self.response.requires_review)


class MarkingCriterionTests(TestCase):
    """Test cases for MarkingCriterion model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.auto_marker = AutoMarker.objects.create(
            title="Test Marker",
            tenant="test-tenant",
            created_by=self.user,
            question_text="Test question",
            model_answer="Test answer",
            max_marks=10
        )
        self.criterion = MarkingCriterion.objects.create(
            auto_marker=self.auto_marker,
            criterion_name="Understanding",
            description="Demonstrates understanding of concepts",
            expected_content="Should explain key concepts clearly",
            weight=0.5,
            max_points=5,
            criterion_keywords=['concept', 'understanding'],
            required=True,
            display_order=1
        )
    
    def test_criterion_creation(self):
        """Test that MarkingCriterion is created correctly"""
        self.assertEqual(self.criterion.criterion_name, "Understanding")
        self.assertEqual(self.criterion.weight, 0.5)
        self.assertEqual(self.criterion.max_points, 5)
        self.assertTrue(self.criterion.required)
    
    def test_criterion_string_representation(self):
        """Test string representation of criterion"""
        expected = "Understanding (50.0%)"
        self.assertEqual(str(self.criterion), expected)


class MarkingLogTests(TestCase):
    """Test cases for MarkingLog model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.auto_marker = AutoMarker.objects.create(
            title="Test Marker",
            tenant="test-tenant",
            created_by=self.user,
            question_text="Test question",
            model_answer="Test answer",
            max_marks=10
        )
        self.log = MarkingLog.objects.create(
            auto_marker=self.auto_marker,
            action='mark_batch',
            performed_by=self.user,
            similarity_model='sentence_transformers',
            model_version='1.0',
            responses_processed=5,
            total_time=10.5
        )
    
    def test_log_creation(self):
        """Test that MarkingLog is created correctly"""
        self.assertEqual(self.log.action, 'mark_batch')
        self.assertEqual(self.log.responses_processed, 5)
        self.assertEqual(self.log.total_time, 10.5)
    
    def test_average_time_calculation(self):
        """Test that average time per response is calculated"""
        expected_avg = 10.5 / 5
        self.assertEqual(self.log.average_time_per_response, expected_avg)
    
    def test_log_with_score_change(self):
        """Test logging score adjustments"""
        log = MarkingLog.objects.create(
            auto_marker=self.auto_marker,
            action='adjust_score',
            performed_by=self.user,
            similarity_model='sentence_transformers',
            responses_processed=1,
            total_time=1.0,
            original_score=7.5,
            new_score=8.5,
            adjustment_reason="Corrected marking error"
        )
        
        self.assertEqual(log.original_score, 7.5)
        self.assertEqual(log.new_score, 8.5)
        self.assertIsNotNone(log.adjustment_reason)
