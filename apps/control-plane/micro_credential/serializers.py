from rest_framework import serializers
from .models import MicroCredential, MicroCredentialVersion, MicroCredentialEnrollment


class MicroCredentialSerializer(serializers.ModelSerializer):
    created_by_details = serializers.SerializerMethodField()
    enrollment_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    delivery_mode_display = serializers.CharField(
        source="get_delivery_mode_display", read_only=True
    )

    class Meta:
        model = MicroCredential
        fields = [
            "id",
            "tenant",
            "title",
            "code",
            "description",
            "duration_hours",
            "delivery_mode",
            "delivery_mode_display",
            "target_audience",
            "learning_outcomes",
            "source_units",
            "compressed_content",
            "tags",
            "skills_covered",
            "industry_sectors",
            "aqf_level",
            "assessment_strategy",
            "assessment_tasks",
            "price",
            "max_participants",
            "prerequisites",
            "status",
            "status_display",
            "gpt_generated",
            "gpt_model_used",
            "generation_time_seconds",
            "created_by",
            "created_by_details",
            "enrollment_count",
            "created_at",
            "updated_at",
            "published_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "gpt_generated",
            "gpt_model_used",
            "generation_time_seconds",
        ]

    def get_created_by_details(self, obj):
        if obj.created_by:
            return {
                "id": obj.created_by.id,
                "username": obj.created_by.username,
                "email": obj.created_by.email,
                "first_name": obj.created_by.first_name,
                "last_name": obj.created_by.last_name,
            }
        return None

    def get_enrollment_count(self, obj):
        return obj.enrollments.count()


class MicroCredentialVersionSerializer(serializers.ModelSerializer):
    created_by_details = serializers.SerializerMethodField()

    class Meta:
        model = MicroCredentialVersion
        fields = [
            "id",
            "micro_credential",
            "version_number",
            "change_summary",
            "content_snapshot",
            "created_by",
            "created_by_details",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_created_by_details(self, obj):
        if obj.created_by:
            return {
                "id": obj.created_by.id,
                "username": obj.created_by.username,
                "first_name": obj.created_by.first_name,
                "last_name": obj.created_by.last_name,
            }
        return None


class MicroCredentialEnrollmentSerializer(serializers.ModelSerializer):
    micro_credential_details = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = MicroCredentialEnrollment
        fields = [
            "id",
            "micro_credential",
            "micro_credential_details",
            "student_name",
            "student_email",
            "student_id",
            "status",
            "status_display",
            "enrolled_at",
            "started_at",
            "completed_at",
            "withdrawn_at",
            "progress_data",
        ]
        read_only_fields = ["id", "enrolled_at"]

    def get_micro_credential_details(self, obj):
        return {
            "id": obj.micro_credential.id,
            "code": obj.micro_credential.code,
            "title": obj.micro_credential.title,
            "duration_hours": obj.micro_credential.duration_hours,
        }
