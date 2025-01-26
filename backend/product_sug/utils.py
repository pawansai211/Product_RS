from collections import defaultdict
from .models import Interaction, UserPreferences

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

    # Determine the most preferred product type/description combination
    if preferences:
        most_preferred = max(preferences, key=preferences.get)
        preferred_product_type, preferred_description = most_preferred
        total_interactions = preferences[most_preferred]
        
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
