"""
TAS Orchestrator Service
Manages workflow state machine and wizard flow for Course TAS and Unit TAS creation
"""

from django.db import transaction
from django.utils import timezone
from typing import Dict, List, Optional
from ..models import CourseTAS, UnitTAS, ComplianceCheck


class TASOrchestrator:
    """
    Orchestrates the TAS creation workflow with state machine management
    States: Draft → Review → Approved → Published
    """

    VALID_TRANSITIONS = {
        "draft": ["review"],
        "review": ["draft", "approved"],
        "approved": ["published", "draft"],
        "published": ["archived"],
        "archived": [],
    }

    @classmethod
    def create_course_tas(cls, tenant, qualification_data, user) -> CourseTAS:
        """
        Create a new Course TAS from qualification data

        Args:
            tenant: Tenant instance
            qualification_data: Dict with qualification details from TGA
            user: User creating the TAS

        Returns:
            CourseTAS instance in draft state
        """
        with transaction.atomic():
            course_tas = CourseTAS.objects.create(
                tenant=tenant,
                qualification_code=qualification_data["code"],
                qualification_name=qualification_data["name"],
                aqf_level=qualification_data["aqf_level"],
                training_package=qualification_data.get("training_package", ""),
                tga_qualification_snapshot=qualification_data.get("tga_snapshot", {}),
                tga_release_version=qualification_data.get("release_version", ""),
                status="draft",
                version=1,
                is_current_version=True,
                created_by=user,
            )

            return course_tas

    @classmethod
    def generate_unit_tas_set(cls, course_tas, user) -> List[UnitTAS]:
        """
        Generate Unit TAS records for all units in the Course TAS

        Args:
            course_tas: CourseTAS instance
            user: User generating the units

        Returns:
            List of UnitTAS instances
        """
        unit_tas_list = []

        with transaction.atomic():
            # Generate for core units
            for unit in course_tas.core_units:
                unit_tas = UnitTAS.objects.create(
                    course_tas=course_tas,
                    unit_code=unit["code"],
                    unit_title=unit["title"],
                    unit_type="core",
                    nominal_hours=unit.get("nominal_hours", 0),
                    tga_unit_snapshot=unit.get("tga_snapshot", {}),
                    status="draft",
                    version=1,
                    created_by=user,
                )
                unit_tas_list.append(unit_tas)

            # Generate for elective units
            for unit in course_tas.elective_units:
                unit_tas = UnitTAS.objects.create(
                    course_tas=course_tas,
                    unit_code=unit["code"],
                    unit_title=unit["title"],
                    unit_type="elective",
                    nominal_hours=unit.get("nominal_hours", 0),
                    tga_unit_snapshot=unit.get("tga_snapshot", {}),
                    status="draft",
                    version=1,
                    created_by=user,
                )
                unit_tas_list.append(unit_tas)

        return unit_tas_list

    @classmethod
    def transition_status(cls, tas_instance, new_status: str, user) -> bool:
        """
        Transition TAS status following state machine rules

        Args:
            tas_instance: CourseTAS or UnitTAS instance
            new_status: Target status
            user: User performing the transition

        Returns:
            True if transition successful, False otherwise
        """
        current_status = tas_instance.status

        # Validate transition
        if new_status not in cls.VALID_TRANSITIONS.get(current_status, []):
            raise ValueError(
                f"Invalid transition from '{current_status}' to '{new_status}'. "
                f"Valid transitions: {cls.VALID_TRANSITIONS.get(current_status, [])}"
            )

        # Check compliance for certain transitions
        if new_status == "approved":
            # Ensure no blocking (Red) compliance issues
            if isinstance(tas_instance, CourseTAS):
                red_issues = ComplianceCheck.objects.filter(
                    entity_type="course",
                    entity_id=tas_instance.id,
                    status="red",
                    resolved=False,
                ).count()

                if red_issues > 0:
                    raise ValueError(
                        f"Cannot approve: {red_issues} blocking compliance issue(s) found. "
                        "Resolve all Red issues before approval."
                    )

        # Perform transition
        with transaction.atomic():
            tas_instance.status = new_status

            if new_status == "review":
                tas_instance.submitted_for_review_at = timezone.now()
                tas_instance.submitted_by = user
            elif new_status == "approved":
                tas_instance.approved_at = timezone.now()
                tas_instance.approved_by = user
            elif new_status == "published":
                tas_instance.published_at = timezone.now()

            tas_instance.updated_at = timezone.now()
            tas_instance.save()

        return True

    @classmethod
    def create_new_version(cls, course_tas, change_reason: str, user) -> CourseTAS:
        """
        Create a new version of an existing Course TAS

        Args:
            course_tas: Existing CourseTAS instance
            change_reason: Reason for version change
            user: User creating the version

        Returns:
            New CourseTAS instance (incremented version)
        """
        with transaction.atomic():
            # Mark current versions as not current
            CourseTAS.objects.filter(
                tenant=course_tas.tenant,
                qualification_code=course_tas.qualification_code,
                is_current_version=True,
            ).update(is_current_version=False)

            # Create new version
            new_version = CourseTAS.objects.create(
                tenant=course_tas.tenant,
                qualification_code=course_tas.qualification_code,
                qualification_name=course_tas.qualification_name,
                aqf_level=course_tas.aqf_level,
                training_package=course_tas.training_package,
                tga_qualification_snapshot=course_tas.tga_qualification_snapshot,
                tga_release_version=course_tas.tga_release_version,
                core_units=course_tas.core_units,
                elective_units=course_tas.elective_units,
                total_units=course_tas.total_units,
                cohort_profile=course_tas.cohort_profile,
                delivery_model=course_tas.delivery_model,
                total_hours=course_tas.total_hours,
                duration_weeks=course_tas.duration_weeks,
                clusters=course_tas.clusters,
                resources=course_tas.resources,
                assessment_overview=course_tas.assessment_overview,
                validation_plan=course_tas.validation_plan,
                policy_links=course_tas.policy_links,
                version=course_tas.version + 1,
                is_current_version=True,
                status="draft",
                created_by=user,
            )

            # Copy M2M relationships
            new_version.facilities.set(course_tas.facilities.all())
            new_version.industry_engagements.set(course_tas.industry_engagements.all())

        return new_version

    @classmethod
    def get_workflow_state(cls, tas_instance) -> Dict:
        """
        Get current workflow state and available actions

        Returns:
            Dict with current state and valid next transitions
        """
        current_status = tas_instance.status

        return {
            "current_status": current_status,
            "valid_transitions": cls.VALID_TRANSITIONS.get(current_status, []),
            "can_edit": current_status in ["draft"],
            "can_approve": current_status == "review",
            "can_publish": current_status == "approved",
            "submitted_at": tas_instance.submitted_for_review_at,
            "approved_at": tas_instance.approved_at,
            "published_at": tas_instance.published_at,
        }
