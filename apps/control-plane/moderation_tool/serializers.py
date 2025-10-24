from rest_framework import serializers
from .models import ModerationSession, AssessorDecision, OutlierDetection, BiasScore, ModerationLog


class ModerationSessionSerializer(serializers.ModelSerializer):
    fairness_score = serializers.SerializerMethodField()
    
    class Meta:
        model = ModerationSession
        fields = '__all__'
        read_only_fields = ('session_number', 'created_at', 'updated_at', 'outliers_detected', 
                           'bias_flags_raised', 'decisions_compared', 'average_agreement_rate')
    
    def get_fairness_score(self, obj):
        return obj.get_fairness_score()


class AssessorDecisionSerializer(serializers.ModelSerializer):
    percentage_score = serializers.SerializerMethodField()
    
    class Meta:
        model = AssessorDecision
        fields = '__all__'
        read_only_fields = ('decision_number', 'created_at', 'is_outlier', 'has_bias_flag')
    
    def get_percentage_score(self, obj):
        return obj.get_percentage_score()


class OutlierDetectionSerializer(serializers.ModelSerializer):
    decision_details = AssessorDecisionSerializer(source='decision', read_only=True)
    
    class Meta:
        model = OutlierDetection
        fields = '__all__'
        read_only_fields = ('outlier_number', 'detected_at')


class BiasScoreSerializer(serializers.ModelSerializer):
    severity_label = serializers.SerializerMethodField()
    
    class Meta:
        model = BiasScore
        fields = '__all__'
        read_only_fields = ('bias_number', 'calculated_at')
    
    def get_severity_label(self, obj):
        return obj.get_severity_label()


class ModerationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationLog
        fields = '__all__'
        read_only_fields = ('timestamp',)


# Request serializers
class CompareDecisionsRequestSerializer(serializers.Serializer):
    student_id = serializers.CharField(required=True)
    submission_id = serializers.CharField(required=False, allow_blank=True)


class DetectOutliersRequestSerializer(serializers.Serializer):
    threshold = serializers.FloatField(required=False, min_value=0.5, max_value=5.0)
    auto_flag = serializers.BooleanField(default=True)


class CalculateBiasRequestSerializer(serializers.Serializer):
    assessor_id = serializers.CharField(required=False, allow_blank=True)
    bias_types = serializers.ListField(
        child=serializers.ChoiceField(choices=BiasScore.BIAS_TYPE_CHOICES),
        required=False
    )
