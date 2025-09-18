from django.core.management.base import BaseCommand
from api.models import RegistrationCode
import secrets
import string


class Command(BaseCommand):
    help = 'Create a new registration code'

    def add_arguments(self, parser):
        parser.add_argument(
            '--code',
            type=str,
            help='Specific code to create (if not provided, generates random)',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days the code is valid (default: 30)',
        )

    def handle(self, *args, **options):
        code = options['code']
        days = options['days']

        if not code:
            # Generate a random 8-character code
            alphabet = string.ascii_uppercase + string.digits
            code = ''.join(secrets.choice(alphabet) for _ in range(8))

        try:
            registration_code = RegistrationCode.create_code(code, days)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created registration code: {registration_code.code}\n'
                    f'Valid until: {registration_code.expires_at.strftime("%Y-%m-%d %H:%M:%S")}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating registration code: {str(e)}')
            )
