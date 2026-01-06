from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User, UserProfile
from apps.skills.models import SkillCategory, SkillOffer, SkillRequest
from apps.exchanges.models import Exchange
from apps.reviews.models import Review
from apps.communities.models import Community, CommunityMembership
from apps.credits.models import CreditBalance, CreditTransaction
from apps.messaging.models import Conversation, Message


class Command(BaseCommand):
    help = 'Create comprehensive sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create categories
        self.stdout.write('Creating skill categories...')
        categories_data = [
            {'name': 'Technology', 'slug': 'technology', 'icon': '💻', 'description': 'Programming, web development, data science'},
            {'name': 'Languages', 'slug': 'languages', 'icon': '🗣️', 'description': 'Learn or practice any language'},
            {'name': 'Music', 'slug': 'music', 'icon': '🎵', 'description': 'Instruments, theory, and production'},
            {'name': 'Arts & Crafts', 'slug': 'arts-crafts', 'icon': '🎨', 'description': 'Painting, drawing, crafting'},
            {'name': 'Cooking', 'slug': 'cooking', 'icon': '🍳', 'description': 'Cuisines, techniques, and recipes'},
            {'name': 'Fitness', 'slug': 'fitness', 'icon': '💪', 'description': 'Yoga, training, sports'},
            {'name': 'Business', 'slug': 'business', 'icon': '💼', 'description': 'Marketing, finance, management'},
            {'name': 'Photography', 'slug': 'photography', 'icon': '📷', 'description': 'Camera techniques and editing'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = SkillCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat.slug] = cat

        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))

        # Create sample users
        self.stdout.write('Creating users...')
        users_data = [
            {
                'username': 'alice_dev',
                'email': 'alice@example.com',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'location_city': 'San Francisco',
                'location_zip': '94102',
                'bio': 'Full-stack developer with 5 years of experience. Love teaching Python and web development!',
            },
            {
                'username': 'bob_chef',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Smith',
                'location_city': 'San Francisco',
                'location_zip': '94103',
                'bio': 'Professional chef specializing in Italian cuisine. Happy to share cooking secrets!',
            },
            {
                'username': 'carol_artist',
                'email': 'carol@example.com',
                'first_name': 'Carol',
                'last_name': 'Williams',
                'location_city': 'San Francisco',
                'location_zip': '94104',
                'bio': 'Watercolor artist and instructor. Teaching art for 10+ years.',
            },
            {
                'username': 'david_musician',
                'email': 'david@example.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'location_city': 'San Francisco',
                'location_zip': '94105',
                'bio': 'Guitar teacher and performer. All levels welcome!',
            },
            {
                'username': 'emma_linguist',
                'email': 'emma@example.com',
                'first_name': 'Emma',
                'last_name': 'Garcia',
                'location_city': 'San Francisco',
                'location_zip': '94106',
                'bio': 'Native Spanish speaker, fluent in English and French. Love language exchange!',
            },
            {
                'username': 'frank_fitness',
                'email': 'frank@example.com',
                'first_name': 'Frank',
                'last_name': 'Martinez',
                'location_city': 'San Francisco',
                'location_zip': '94107',
                'bio': 'Certified personal trainer and yoga instructor.',
            },
        ]

        users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'location_city': user_data['location_city'],
                    'location_zip': user_data.get('location_zip', ''),
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                # Update profile bio
                user.profile.bio = user_data.get('bio', '')
                user.profile.save()
            users[user.username] = user

        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users (password: password123)'))

        # Create skill offers
        self.stdout.write('Creating skill offers...')
        offers_data = [
            {
                'user': users['alice_dev'],
                'title': 'Python Programming for Beginners',
                'description': 'Learn Python basics, data structures, and object-oriented programming. Perfect for complete beginners!',
                'category': categories['technology'],
                'delivery_method': 'both',
                'session_type': 'one_on_one',
                'duration_hours': 2.0,
                'skill_level': 'beginner',
            },
            {
                'user': users['alice_dev'],
                'title': 'Web Development with Django',
                'description': 'Build full-stack web applications using Django. Covers models, views, templates, and deployment.',
                'category': categories['technology'],
                'delivery_method': 'video_call',
                'session_type': 'one_on_one',
                'duration_hours': 3.0,
                'skill_level': 'intermediate',
            },
            {
                'user': users['bob_chef'],
                'title': 'Italian Cooking Masterclass',
                'description': 'Learn to make authentic pasta, risotto, and tiramisu from scratch!',
                'category': categories['cooking'],
                'delivery_method': 'in_person',
                'session_type': 'small_group',
                'duration_hours': 2.5,
                'skill_level': 'beginner',
                'max_group_size': 4,
            },
            {
                'user': users['carol_artist'],
                'title': 'Watercolor Painting Basics',
                'description': 'Introduction to watercolor techniques, color mixing, and landscape painting.',
                'category': categories['arts-crafts'],
                'delivery_method': 'both',
                'session_type': 'small_group',
                'duration_hours': 2.0,
                'skill_level': 'beginner',
                'max_group_size': 3,
            },
            {
                'user': users['david_musician'],
                'title': 'Guitar Lessons for Beginners',
                'description': 'Learn chords, strumming patterns, and play your first songs!',
                'category': categories['music'],
                'delivery_method': 'both',
                'session_type': 'one_on_one',
                'duration_hours': 1.0,
                'skill_level': 'beginner',
            },
            {
                'user': users['emma_linguist'],
                'title': 'Spanish Conversation Practice',
                'description': 'Practice conversational Spanish with a native speaker. All levels welcome!',
                'category': categories['languages'],
                'delivery_method': 'video_call',
                'session_type': 'one_on_one',
                'duration_hours': 1.0,
                'skill_level': 'intermediate',
            },
            {
                'user': users['frank_fitness'],
                'title': 'Beginner Yoga Session',
                'description': 'Gentle yoga for flexibility and relaxation. Perfect for beginners!',
                'category': categories['fitness'],
                'delivery_method': 'in_person',
                'session_type': 'small_group',
                'duration_hours': 1.0,
                'skill_level': 'beginner',
                'max_group_size': 5,
            },
        ]

        offers = []
        for offer_data in offers_data:
            offer, created = SkillOffer.objects.get_or_create(
                user=offer_data['user'],
                title=offer_data['title'],
                defaults=offer_data
            )
            offers.append(offer)

        self.stdout.write(self.style.SUCCESS(f'- Created {len(offers)} skill offers'))

        # Create skill requests
        self.stdout.write('Creating skill requests...')
        requests_data = [
            {
                'user': users['bob_chef'],
                'title': 'Looking to learn web design',
                'description': 'Want to create a website for my restaurant. Need help with HTML/CSS.',
                'category': categories['technology'],
                'preferred_delivery': 'video_call',
                'urgency': 'medium',
            },
            {
                'user': users['frank_fitness'],
                'title': 'Photography for social media',
                'description': 'Need to improve my Instagram photos for my fitness business.',
                'category': categories['photography'],
                'preferred_delivery': 'in_person',
                'urgency': 'low',
            },
        ]

        for req_data in requests_data:
            SkillRequest.objects.get_or_create(
                user=req_data['user'],
                title=req_data['title'],
                defaults=req_data
            )

        self.stdout.write(self.style.SUCCESS(f'- Created {len(requests_data)} skill requests'))

        # Create communities
        self.stdout.write('Creating communities...')
        communities_data = [
            {
                'name': 'SF Tech Skills',
                'slug': 'sf-tech-skills',
                'description': 'Programming, web development, and tech skills exchange in San Francisco',
                'city': 'San Francisco',
            },
            {
                'name': 'Bay Area Artists',
                'slug': 'bay-area-artists',
                'description': 'Art, design, and creative skills community',
                'city': 'San Francisco',
            },
        ]

        communities = []
        for comm_data in communities_data:
            comm, created = Community.objects.get_or_create(
                slug=comm_data['slug'],
                defaults=comm_data
            )
            communities.append(comm)
            # Add some members
            for user in [users['alice_dev'], users['bob_chef'], users['carol_artist']]:
                CommunityMembership.objects.get_or_create(
                    user=user,
                    community=comm,
                    defaults={'role': 'member'}
                )

        self.stdout.write(self.style.SUCCESS(f'- Created {len(communities)} communities'))

        # Create some completed exchanges and reviews
        self.stdout.write('Creating sample exchanges and reviews...')

        # Exchange 1: Alice taught Bob Python
        exchange1, created = Exchange.objects.get_or_create(
            skill_offer=offers[0],  # Python Programming
            teacher=users['alice_dev'],
            learner=users['bob_chef'],
            defaults={
                'status': 'completed',
                'duration_hours': 2.0,
                'credits_amount': 2,
                'proposed_at': timezone.now() - timedelta(days=10),
                'accepted_at': timezone.now() - timedelta(days=9),
                'completed_at': timezone.now() - timedelta(days=3),
                'teacher_confirmed': True,
                'learner_confirmed': True,
            }
        )

        if created:
            # Create review
            Review.objects.get_or_create(
                exchange=exchange1,
                reviewer=users['bob_chef'],
                reviewee=users['alice_dev'],
                defaults={
                    'rating': 5,
                    'skill_quality': 5,
                    'communication': 5,
                    'reliability': 5,
                    'comment': 'Alice is an amazing teacher! Very patient and explained everything clearly.',
                }
            )

        # Exchange 2: David taught Carol guitar
        if len(offers) >= 5:
            exchange2, created = Exchange.objects.get_or_create(
                skill_offer=offers[4],  # Guitar Lessons
                teacher=users['david_musician'],
                learner=users['carol_artist'],
                defaults={
                    'status': 'completed',
                    'duration_hours': 1.0,
                    'credits_amount': 1,
                    'proposed_at': timezone.now() - timedelta(days=7),
                    'accepted_at': timezone.now() - timedelta(days=6),
                    'completed_at': timezone.now() - timedelta(days=2),
                    'teacher_confirmed': True,
                    'learner_confirmed': True,
                }
            )

            if created:
                Review.objects.get_or_create(
                    exchange=exchange2,
                    reviewer=users['carol_artist'],
                    reviewee=users['david_musician'],
                    defaults={
                        'rating': 5,
                        'skill_quality': 5,
                        'communication': 5,
                        'reliability': 5,
                        'comment': 'Great first lesson! David made learning guitar fun and easy.',
                    }
                )

        # Create a pending exchange
        if len(offers) >= 3:
            Exchange.objects.get_or_create(
                skill_offer=offers[2],  # Italian Cooking
                teacher=users['bob_chef'],
                learner=users['frank_fitness'],
                defaults={
                    'status': 'proposed',
                    'duration_hours': 2.5,
                    'credits_amount': 3,
                    'proposed_at': timezone.now() - timedelta(hours=2),
                }
            )

        self.stdout.write(self.style.SUCCESS('- Created sample exchanges and reviews'))

        # Update user stats
        for user in users.values():
            profile = user.profile
            profile.skills_offered_count = SkillOffer.objects.filter(user=user, is_active=True).count()
            profile.exchanges_completed = Exchange.objects.filter(
                teacher=user, status='completed'
            ).count() + Exchange.objects.filter(
                learner=user, status='completed'
            ).count()
            profile.save()

        # Add bonus credits to some users
        for username in ['alice_dev', 'bob_chef', 'david_musician']:
            user = users[username]
            balance = CreditBalance.objects.get(user=user)
            balance.balance += 10
            balance.save()
            CreditTransaction.objects.create(
                user=user,
                amount=10,
                transaction_type='bonus',
                balance_after=balance.balance,
                description='Welcome bonus for active participation'
            )

        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write('\nTest users created (all with password: password123):')
        for username in users.keys():
            self.stdout.write(f'  • {username}')
        self.stdout.write('\nYou can now:')
        self.stdout.write('  1. Login with any of the above users')
        self.stdout.write('  2. Browse skills at /skills/browse/')
        self.stdout.write('  3. View communities at /communities/')
        self.stdout.write('  4. See exchanges on user dashboards')
