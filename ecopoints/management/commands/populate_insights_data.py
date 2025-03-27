from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ecopoints.models import Category, Task, CompletedTask
from django.utils import timezone
from datetime import datetime
import random


class Command(BaseCommand):
    help = 'Populate CompletedTask data for Jan, Feb, and first week of March.'

    def handle(self, *args, **options):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("No users found. Create a user first."))
            return

        categories = list(Category.objects.all())
        tasks = list(Task.objects.all())

        if not categories or not tasks:
            self.stdout.write(self.style.ERROR("No categories or tasks found. Add some first."))
            return

        current_year = timezone.now().year

        def random_time_for_day(year, month, day):
            return timezone.make_aware(datetime(year, month, day, random.randint(7, 21), 0))

        def create_entries(month, days, count):
            for _ in range(count):
                day = random.choice(days)
                category = random.choice(categories)
                task_options = Task.objects.filter(category=category)
                if not task_options.exists():
                    continue
                task = random.choice(list(task_options))
                completed_at = random_time_for_day(current_year, month, day)

                CompletedTask.objects.create(
                    user=user,
                    task=task,
                    completed_at=completed_at
                )

        # Populate for January (days 1–28)
        create_entries(month=1, days=range(1, 29), count=15)

        # Populate for February (days 1–28)
        create_entries(month=2, days=range(1, 29), count=15)

        # Populate for March (only days 1–7)
        create_entries(month=3, days=range(1, 8), count=7)

        self.stdout.write(self.style.SUCCESS("Data populated for Jan, Feb, and first week of March."))
