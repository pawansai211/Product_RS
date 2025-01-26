from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Custom User model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username


# Product model with image upload support
class Product(models.Model):
    PRODUCT_TYPES = [
        ('shirt', 'Shirt'),
        ('pants', 'Pants'),
        ('vest', 'Vest'),
        ('earrings', 'Earrings'),
        ('necklace', 'Necklace'),
        ('bangles', 'Bangles'),
        ('dress', 'Dress'),
        ('skirt', 'Skirt'),
        ('shoes', 'Shoes')
    ]
    
    CATEGORY_CHOICES = [
        ('clothing', 'Clothing'),
        ('accessory', 'Accessory')
    ]
    
    
    product_name = models.CharField(max_length=255, choices=PRODUCT_TYPES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


# Interaction model to track user interactions with products (like, dislike, view)
class Interaction(models.Model):
    INTERACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('view', 'View')
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_CHOICES)
    interaction_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product', 'interaction_type')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.interaction_type})"


# User preferences model to store user preferences based on interaction analysis
class UserPreferences(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    preferred_product_type = models.CharField(max_length=255)
    preferred_description = models.TextField()
    interaction_count = models.IntegerField(default=0)  # Total interactions for this preference
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s preference: {self.preferred_product_type} - {self.preferred_description}"


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)