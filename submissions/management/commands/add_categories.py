"""
Management command to add categories to the database
Usage: python manage.py add_categories
"""
from django.core.management.base import BaseCommand
from submissions.models import Category


class Command(BaseCommand):
    help = 'Add default categories to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing categories before adding new ones',
        )

    def handle(self, *args, **options):
        # Default categories to add
        categories_data = [
            {
                'name_ar': 'كهرباء',
                'name_en': 'Electricity'
            },
            {
                'name_ar': 'مياه',
                'name_en': 'Water'
            },
            {
                'name_ar': 'صرف صحي',
                'name_en': 'Sewage'
            },
            {
                'name_ar': 'إنترنت',
                'name_en': 'Internet'
            },
            {
                'name_ar': 'هاتف',
                'name_en': 'Phone'
            },
            {
                'name_ar': 'طرق',
                'name_en': 'Roads'
            },
            {
                'name_ar': 'إنارة',
                'name_en': 'Lighting'
            },
            {
                'name_ar': 'أخرى',
                'name_en': 'Other'
            },
        ]

        if options['clear']:
            Category.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('All existing categories have been deleted.')
            )

        created_count = 0
        updated_count = 0

        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name_ar=category_data['name_ar'],
                defaults={'name_en': category_data['name_en']}
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created category: {category.name_ar} ({category.name_en})'
                    )
                )
            else:
                # Update existing category if name_en is different
                if category.name_en != category_data['name_en']:
                    category.name_en = category_data['name_en']
                    category.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'↻ Updated category: {category.name_ar} ({category.name_en})'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(
                            f'○ Category already exists: {category.name_ar} ({category.name_en})'
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully processed categories: {created_count} created, {updated_count} updated'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Total categories in database: {Category.objects.count()}'
            )
        )

