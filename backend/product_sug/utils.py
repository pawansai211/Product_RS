from collections import defaultdict

from django.utils import timezone
from .models import Interaction, UserPreferences, Product

def update_user_preferences(user):
    """Update or create user preferences based on most interacted product types and descriptions."""
    
    # Fetch all interactions for the user
    interactions = Interaction.objects.filter(user=user)
    
    preferences = defaultdict(int)
    
    # Loop through the interactions and accumulate the interaction count for each product's type and description
    for interaction in interactions:
        product = interaction.product
        description = product.description  # e.g., color
        product_type = product.product_name  # e.g., shirt, pants
        
        key = (product_type, description)
        preferences[key] += interaction.interaction_count

    # Iterate through all the accumulated preferences and update or create preference records
    for (preferred_product_type, preferred_description), total_interactions in preferences.items():
        # Update or create the user preference record
        user_pref, created = UserPreferences.objects.update_or_create(
            user=user,
            preferred_product_type=preferred_product_type,
            preferred_description=preferred_description,
            defaults={'interaction_count': total_interactions}
        )

        if created:
            print(f"New preference created for {user.username}: {preferred_product_type} - {preferred_description}")
        else:
            print(f"Preference updated for {user.username}: {preferred_product_type} - {preferred_description}")
def delete_data_created_today():
    # Get today's date at midnight (start of the day)
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Filter the products created today
    fake_data = Product.objects.filter(created_at__gte=today_start)
    
    # Delete the filtered products
    deleted_count, _ = fake_data.delete()
    
    print(f"Deleted {deleted_count} product(s) created today.")
