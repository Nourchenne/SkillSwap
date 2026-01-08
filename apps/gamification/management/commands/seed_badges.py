from django.core.management.base import BaseCommand
from apps.gamification.models import Badge

class Command(BaseCommand):
    help = 'Seeds the initial badges'

    def handle(self, *args, **options):
        badges = [
            {
                'slug': 'first-swap',
                'name': 'First Swap',
                'description': 'Awarded for completing your first skill exchange.',
                'icon': '🤝',
                'criteria_description': 'Complete 1 exchange'
            },
            {
                'slug': 'power-teacher',
                'name': 'Power Teacher',
                'description': 'Awarded for teaching 5 sessions.',
                'icon': '🎓',
                'criteria_description': 'Teach 5 sessions'
            },
            {
                'slug': 'expert',
                'name': 'Expert',
                'description': 'Received 10 5-star reviews.',
                'icon': '⭐',
                'criteria_description': '10 5-star reviews'
            },
            {
                'slug': 'community-pillar',
                'name': 'Community Pillar',
                'description': 'Been a member for 1 year.',
                'icon': '🏛️',
                'criteria_description': '1 year membership'
            }
        ]

        for b_data in badges:
            badge, created = Badge.objects.get_or_create(
                slug=b_data['slug'],
                defaults=b_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created badge: {badge.name}"))
            else:
                self.stdout.write(f"Badge already exists: {badge.name}")
