"""
Evidence and Snapshot Service
Assembles evidence packs and creates immutable snapshots for audit trail
"""

from typing import Dict, List
from django.db import transaction
from django.utils import timezone
import secrets
from datetime import timedelta
from ..models import (
    CourseTAS,
    UnitTAS,
    ImmutableSnapshot,
    EvidencePack,
    IndustryEngagement,
)


class EvidenceSnapshotService:
    """
    Service for managing evidence packs and immutable snapshots
    """

    @classmethod
    def create_snapshot(
        cls, course_tas: CourseTAS, reason: str, user
    ) -> ImmutableSnapshot:
        """
        Create an immutable snapshot of the Course TAS and all Unit TAS

        Args:
            course_tas: CourseTAS instance to snapshot
            reason: Reason for creating snapshot (e.g., 'Initial Approval', 'Version Update')
            user: User creating the snapshot

        Returns:
            ImmutableSnapshot instance
        """
        with transaction.atomic():
            # Gather complete TAS state
            snapshot_data = cls._gather_snapshot_data(course_tas)

            # Create snapshot
            snapshot = ImmutableSnapshot.objects.create(
                course_tas=course_tas,
                snapshot_data=snapshot_data,
                version=course_tas.version,
                snapshot_reason=reason,
                sealed_by=user,
            )

            # Generate auditor access link
            snapshot.auditor_link_token = secrets.token_urlsafe(32)
            snapshot.auditor_link_expires_at = timezone.now() + timedelta(days=365)
            snapshot.save()

            return snapshot

    @classmethod
    def _gather_snapshot_data(cls, course_tas: CourseTAS) -> Dict:
        """
        Gather complete state of Course TAS and all related data

        Returns:
            Dict with frozen state
        """
        # Course TAS data
        course_data = {
            "qualification_code": course_tas.qualification_code,
            "qualification_name": course_tas.qualification_name,
            "aqf_level": course_tas.aqf_level,
            "training_package": course_tas.training_package,
            "tga_qualification_snapshot": course_tas.tga_qualification_snapshot,
            "tga_release_version": course_tas.tga_release_version,
            "core_units": course_tas.core_units,
            "elective_units": course_tas.elective_units,
            "total_units": course_tas.total_units,
            "cohort_profile": course_tas.cohort_profile,
            "delivery_model": course_tas.delivery_model,
            "total_hours": course_tas.total_hours,
            "duration_weeks": course_tas.duration_weeks,
            "clusters": course_tas.clusters,
            "resources": course_tas.resources,
            "assessment_overview": course_tas.assessment_overview,
            "validation_plan": course_tas.validation_plan,
            "policy_links": course_tas.policy_links,
            "status": course_tas.status,
            "version": course_tas.version,
            "approved_at": (
                course_tas.approved_at.isoformat() if course_tas.approved_at else None
            ),
            "approved_by": (
                course_tas.approved_by.username if course_tas.approved_by else None
            ),
        }

        # Facilities
        course_data["facilities"] = [
            {
                "name": f.name,
                "type": f.facility_type,
                "location": f.location,
            }
            for f in course_tas.facilities.all()
        ]

        # Industry engagements
        course_data["industry_engagements"] = [
            {
                "employer": e.employer_name,
                "date": e.engagement_date.isoformat(),
                "type": e.engagement_type,
                "outcomes": e.outcomes,
            }
            for e in course_tas.industry_engagements.all()
        ]

        # Unit TAS data
        unit_tas_data = []
        for unit_tas in course_tas.unit_tas_set.all():
            unit_data = {
                "unit_code": unit_tas.unit_code,
                "unit_title": unit_tas.unit_title,
                "unit_type": unit_tas.unit_type,
                "nominal_hours": unit_tas.nominal_hours,
                "tga_unit_snapshot": unit_tas.tga_unit_snapshot,
                "cluster_assignment": unit_tas.cluster_assignment,
                "delivery_sequence": unit_tas.delivery_sequence,
                "assessment_tasks": unit_tas.assessment_tasks,
                "mapping_matrix": unit_tas.mapping_matrix,
                "resources": unit_tas.resources,
                "cohort_context": unit_tas.cohort_context,
                "industry_relevance": unit_tas.industry_relevance,
                "trainers": [
                    {
                        "name": t.user.get_full_name() or t.user.username,
                        "qualifications": t.qualifications,
                        "tae_qualification": t.tae_qualification,
                        "industry_experience_years": t.industry_experience_years,
                    }
                    for t in unit_tas.trainers.all()
                ],
                "facilities": [
                    {"name": f.name, "type": f.facility_type}
                    for f in unit_tas.facilities.all()
                ],
            }
            unit_tas_data.append(unit_data)

        return {
            "course_tas": course_data,
            "unit_tas": unit_tas_data,
            "snapshot_timestamp": timezone.now().isoformat(),
        }

    @classmethod
    def verify_snapshot_integrity(cls, snapshot_id: int) -> Dict:
        """
        Verify that a snapshot has not been tampered with

        Args:
            snapshot_id: ImmutableSnapshot ID

        Returns:
            Dict with verification results
        """
        try:
            snapshot = ImmutableSnapshot.objects.get(id=snapshot_id)
            is_valid = snapshot.verify_integrity()

            return {
                "valid": is_valid,
                "snapshot_id": snapshot.id,
                "checksum": snapshot.checksum,
                "sealed_at": snapshot.sealed_at.isoformat(),
                "sealed_by": (
                    snapshot.sealed_by.username if snapshot.sealed_by else None
                ),
            }
        except ImmutableSnapshot.DoesNotExist:
            return {"valid": False, "error": "Snapshot not found"}

    @classmethod
    def create_evidence_pack(
        cls, course_tas: CourseTAS, snapshot: ImmutableSnapshot, user
    ) -> EvidencePack:
        """
        Assemble evidence pack for audit trail

        Args:
            course_tas: CourseTAS instance
            snapshot: Related ImmutableSnapshot
            user: User creating the evidence pack

        Returns:
            EvidencePack instance
        """
        with transaction.atomic():
            # Gather evidence links
            industry_engagement_links = []
            for engagement in course_tas.industry_engagements.all():
                industry_engagement_links.append(
                    {
                        "id": engagement.id,
                        "employer": engagement.employer_name,
                        "date": engagement.engagement_date.isoformat(),
                        "type": engagement.engagement_type,
                        "summary": engagement.notes[:200] if engagement.notes else "",
                    }
                )

            # Gather trainer credentials
            trainer_credentials = []
            for unit_tas in course_tas.unit_tas_set.all():
                for trainer in unit_tas.trainers.all():
                    trainer_credentials.append(
                        {
                            "unit_code": unit_tas.unit_code,
                            "trainer": trainer.user.get_full_name()
                            or trainer.user.username,
                            "qualifications": trainer.qualifications,
                            "tae_qualification": trainer.tae_qualification,
                            "currency_date": (
                                trainer.last_currency_date.isoformat()
                                if trainer.last_currency_date
                                else None
                            ),
                        }
                    )

            # Gather facility documentation
            facility_documentation = []
            for facility in course_tas.facilities.all():
                facility_documentation.append(
                    {
                        "facility": facility.name,
                        "type": facility.facility_type,
                        "capacity": facility.capacity,
                        "equipment": facility.equipment,
                        "software": facility.software,
                    }
                )

            # Create change log (version history)
            change_log = cls._build_change_log(course_tas)

            # Create evidence pack
            evidence_pack = EvidencePack.objects.create(
                course_tas=course_tas,
                snapshot=snapshot,
                industry_engagement_links=industry_engagement_links,
                policy_documents=course_tas.policy_links,
                trainer_credentials=trainer_credentials,
                facility_documentation=facility_documentation,
                change_log=change_log,
                compiled_by=user,
            )

            return evidence_pack

    @classmethod
    def _build_change_log(cls, course_tas: CourseTAS) -> List[Dict]:
        """
        Build change log from version history

        Returns:
            List of change records
        """
        change_log = []

        # Get all versions of this qualification
        all_versions = CourseTAS.objects.filter(
            tenant=course_tas.tenant, qualification_code=course_tas.qualification_code
        ).order_by("version")

        for version in all_versions:
            change_log.append(
                {
                    "version": version.version,
                    "created_at": version.created_at.isoformat(),
                    "created_by": (
                        version.created_by.username if version.created_by else None
                    ),
                    "status": version.status,
                    "approved_at": (
                        version.approved_at.isoformat() if version.approved_at else None
                    ),
                    "approved_by": (
                        version.approved_by.username if version.approved_by else None
                    ),
                }
            )

        return change_log

    @classmethod
    def generate_auditor_link(cls, snapshot_id: int, expiry_days: int = 365) -> str:
        """
        Generate secure link for auditor access to snapshot

        Args:
            snapshot_id: ImmutableSnapshot ID
            expiry_days: Number of days link remains valid

        Returns:
            Token for auditor access
        """
        try:
            snapshot = ImmutableSnapshot.objects.get(id=snapshot_id)

            # Generate new token if expired or missing
            if (
                not snapshot.auditor_link_token
                or snapshot.auditor_link_expires_at < timezone.now()
            ):
                snapshot.auditor_link_token = secrets.token_urlsafe(32)
                snapshot.auditor_link_expires_at = timezone.now() + timedelta(
                    days=expiry_days
                )
                snapshot.save()

            return snapshot.auditor_link_token
        except ImmutableSnapshot.DoesNotExist:
            return ""

    @classmethod
    def revoke_auditor_link(cls, snapshot_id: int) -> bool:
        """
        Revoke auditor access link

        Args:
            snapshot_id: ImmutableSnapshot ID

        Returns:
            True if successful
        """
        try:
            snapshot = ImmutableSnapshot.objects.get(id=snapshot_id)
            snapshot.auditor_link_token = ""
            snapshot.auditor_link_expires_at = None
            snapshot.save()
            return True
        except ImmutableSnapshot.DoesNotExist:
            return False

    @classmethod
    def get_snapshot_by_token(cls, token: str) -> ImmutableSnapshot:
        """
        Retrieve snapshot by auditor access token

        Args:
            token: Auditor link token

        Returns:
            ImmutableSnapshot if valid, None otherwise
        """
        try:
            snapshot = ImmutableSnapshot.objects.get(
                auditor_link_token=token, auditor_link_expires_at__gt=timezone.now()
            )
            return snapshot
        except ImmutableSnapshot.DoesNotExist:
            return None
