"""
Management command to migrate existing Django users to UserAccount model.

This command creates UserAccount records for existing Django User instances
and updates TenantUser relationships to reference the new UserAccount.

Usage:
    python manage.py migrate_users_to_supabase [--dry-run] [--email=user@example.com]
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from users.models import UserAccount
from tenants.models import TenantUser


class Command(BaseCommand):
    help = 'Migrate existing Django users to UserAccount model for Supabase integration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Perform a dry run without making changes',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Migrate only a specific user by email',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        email_filter = options.get('email')

        self.stdout.write(self.style.WARNING(
            '\n' + '='*80 + '\n'
            'USER MIGRATION TO SUPABASE INTEGRATION\n'
            '='*80 + '\n'
        ))

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made\n'))

        # Get users to migrate
        users_query = User.objects.all()
        if email_filter:
            users_query = users_query.filter(email=email_filter)

        users = list(users_query)
        total_users = len(users)

        if total_users == 0:
            self.stdout.write(self.style.WARNING('No users found to migrate.'))
            return

        self.stdout.write(f'Found {total_users} user(s) to process.\n')

        migrated = 0
        skipped = 0
        errors = 0

        for user in users:
            try:
                self.stdout.write(f'\nProcessing user: {user.email} (ID: {user.id})')

                # Check if UserAccount already exists
                existing_account = UserAccount.objects.filter(primary_email=user.email).first()
                
                if existing_account:
                    self.stdout.write(self.style.WARNING(
                        f'  ⚠ UserAccount already exists for {user.email} - Skipping'
                    ))
                    skipped += 1
                    continue

                if not dry_run:
                    with transaction.atomic():
                        # Create UserAccount (without Supabase ID - will be linked on first login)
                        user_account = UserAccount.objects.create(
                            primary_email=user.email,
                            full_name=f"{user.first_name} {user.last_name}".strip() or user.username,
                            is_active=user.is_active,
                            supabase_user_id=None,  # Will be set when user logs in via Supabase
                        )

                        # Update TenantUser relationships
                        tenant_memberships = TenantUser.objects.filter(user=user)
                        membership_count = tenant_memberships.count()

                        if membership_count > 0:
                            for membership in tenant_memberships:
                                membership.user_account = user_account
                                membership.save(update_fields=['user_account'])

                            self.stdout.write(self.style.SUCCESS(
                                f'  ✓ Created UserAccount and updated {membership_count} tenant membership(s)'
                            ))
                        else:
                            self.stdout.write(self.style.SUCCESS(
                                f'  ✓ Created UserAccount (no tenant memberships found)'
                            ))

                        migrated += 1
                else:
                    # Dry run - just report what would happen
                    tenant_memberships = TenantUser.objects.filter(user=user)
                    membership_count = tenant_memberships.count()
                    
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Would create UserAccount for {user.email}'
                    ))
                    if membership_count > 0:
                        self.stdout.write(f'  ✓ Would update {membership_count} tenant membership(s)')
                    
                    migrated += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'  ✗ Error migrating user {user.email}: {str(e)}'
                ))
                errors += 1

        # Summary
        self.stdout.write('\n' + '='*80)
        self.stdout.write('MIGRATION SUMMARY')
        self.stdout.write('='*80)
        self.stdout.write(f'Total users processed: {total_users}')
        self.stdout.write(self.style.SUCCESS(f'Migrated: {migrated}'))
        self.stdout.write(self.style.WARNING(f'Skipped: {skipped}'))
        self.stdout.write(self.style.ERROR(f'Errors: {errors}'))
        
        if dry_run:
            self.stdout.write('\n' + self.style.WARNING(
                'This was a DRY RUN. Run without --dry-run to apply changes.'
            ))
        else:
            self.stdout.write('\n' + self.style.SUCCESS('Migration complete!'))
            self.stdout.write(self.style.WARNING(
                '\nIMPORTANT: Users must now:\n'
                '1. Use Supabase password reset to set their password\n'
                '2. Log in via Supabase authentication\n'
                '3. Their Supabase user ID will be linked on first login\n'
            ))
