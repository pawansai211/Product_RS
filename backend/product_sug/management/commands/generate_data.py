from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, randint
from product_sug.models import CustomUser, Product, Interaction, ProductSuggestion

class Command(BaseCommand):
    help = 'Generates fake data for users, products, interactions, and product suggestions'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generate fake users
        self.stdout.write(self.style.SUCCESS('Generating fake users...'))
        users = self.generate_fake_users(fake, 10)  # Generate 10 fake users
        self.stdout.write(self.style.SUCCESS(f'{len(users)} fake users generated.'))

        # Generate fake products
        self.stdout.write(self.style.SUCCESS('Generating fake products...'))
        products = self.generate_fake_products(fake, 10)  # Generate 10 fake products
        self.stdout.write(self.style.SUCCESS(f'{len(products)} fake products generated.'))

        # Generate fake interactions
        self.stdout.write(self.style.SUCCESS('Generating fake interactions...'))
        self.generate_fake_interactions(users, products, 20)  # Generate 20 interactions
        self.stdout.write(self.style.SUCCESS('Fake interactions generated.'))

        # Generate fake product suggestions
        self.stdout.write(self.style.SUCCESS('Generating fake product suggestions...'))
        self.generate_fake_product_suggestions(users, products, 10)  # Generate 10 suggestions
        self.stdout.write(self.style.SUCCESS('Fake product suggestions generated.'))

    def generate_fake_users(self, fake, n):
        """Generate fake users."""
        users = []
        for _ in range(n):
            user = CustomUser.objects.create(
                email=fake.email(),
                username=fake.user_name(),
                password=fake.password()
            )
            users.append(user)
        return users

    def generate_fake_products(self, fake, n):
        """Generate fake products."""
        products = []
        for _ in range(n):
            product = Product.objects.create(
                product_name=choice(['shirt', 'pants', 'vest', 'earrings', 
                                     'necklace', 'bangles', 'dress', 'skirt', 'shoes']),
                category=choice(['clothing', 'accessory']),
                description=fake.color_name() + ", " + fake.word()  # Description can be color and size, for example
            )
            products.append(product)
        return products

    def generate_fake_interactions(self, users, products, n):
        """Generate fake interactions (likes, dislikes, views)."""
        interaction_types = ['like', 'dislike', 'view']
        for _ in range(n):
            user = choice(users)
            product = choice(products)
            interaction_type = choice(interaction_types)

            # Check if the interaction already exists
            interaction = Interaction.objects.filter(
                user=user,
                product=product,
                interaction_type=interaction_type
            ).first()

            if interaction:
                # Optionally, update the interaction_count if interaction exists
                interaction.interaction_count += 1
                interaction.save()
            else:
                # Create a new interaction if none exists
                Interaction.objects.create(
                    user=user,
                    product=product,
                    interaction_type=interaction_type,
                    interaction_count=randint(1, 10)  # Random interaction count between 1 and 10
                )


    def generate_fake_product_suggestions(self, users, products, n):
        """Generate fake product suggestions."""
        for _ in range(n):
            ProductSuggestion.objects.create(
                user=choice(users),
                product=choice(products),
                suggestion_reason=Faker().sentence()
            )
