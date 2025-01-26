from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status, generics
import django_filters
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Interaction, UserPreferences, CustomUser
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer, InteractionSerializer, \
    UserPreferencesSerializer, CustomUserSerializer
from .utils import update_user_preferences
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
# from product_sug.recommendations.collaborative import recommend_products_cf, train_collaborative_filtering
from .recommendations.content import recommend_products_cb

class CurrentUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Return user data
        user = request.user
        print(request.user)
        return Response({
            "username": user.username,
            "email": user.email
        })

class SignupView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()  # Create the user
            token = Token.objects.get(user=user)
            return Response({
                "message": "User created successfully!",
                "token": token.key  # Return the token here
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user using Django's authentication system
        user = authenticate(username=username, password=password)

        if user is not None:
            # Log the user in using Django's session system
            token, created = Token.objects.get_or_create(user=user)  # Create or get the token
            return Response({
                "message": "Login successful",
                "token": token.key,
                "user_id": user.id
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# View to upload products
class ProductUploadView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product uploaded successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductFilter(django_filters.FilterSet):
    # Filter by product name (e.g., shirt, pants)
    product_name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains')
    
    # Filter by category (e.g., clothing, accessory)
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
    
    # You can add more filters based on other fields as needed.
    class Meta:
        model = Product
        fields = ['product_name', 'category']

class ProductPagination(PageNumberPagination):
    page_size = 10  # Number of products per page
    page_size_query_param = 'page_size'  # Allow clients to change the page size with a query parameter
    max_page_size = 100  # Maximum allowed page size

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()  # Retrieve all products
    serializer_class = ProductSerializer  # Use the ProductSerializer to serialize the data

    
    
    # # Apply filtering using DjangoFilterBackend and the ProductFilter class
    # filter_backends = (DjangoFilterBackend, django_filters.OrderingFilter)
    # filterset_class = ProductFilter  # Use the ProductFilter class
    
    # # Add ordering functionality
    # ordering_fields = ['product_name', 'category', 'created_at', 'price']
    # ordering = ['created_at']  # Default ordering by created_at
    
    # # Add pagination
    # pagination_class = ProductPagination

# View to handle user interactions (like, dislike, view)
class UserInteractionView(APIView):
    def post(self, request):
        # Use the logged-in user (request.user)
        user = request.user

        # If the user is not authenticated, return an error
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the product_id and interaction_type from the request data
        product_id = request.data.get('product_id')
        interaction_type = request.data.get('interaction_type')
        interaction_count = request.data.get('interaction_count', 1)

        # Validate the interaction data
        if not all([product_id, interaction_type]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that interaction type is either 'like' or 'dislike'
        if interaction_type not in ['like', 'dislike']:
            return Response({"error": "Invalid interaction type."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the product from the database
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create or update the interaction
        interaction, created = Interaction.objects.get_or_create(
            user=user,
            product=product,
            interaction_type=interaction_type,
            defaults={'interaction_count': interaction_count}
        )
        
        if not created:
            # If the interaction already exists, increment the interaction count
            interaction.interaction_count += interaction_count
            interaction.save()

        # Optionally, update the user's preferences after each interaction
        update_user_preferences(user)

        return Response({"message": "Interaction recorded successfully!"}, status=status.HTTP_200_OK)


# View to get product recommendations for a user
# class ProductRecommendationView(APIView):
#     # permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
#     def get(self, request, user_id):
#         # Step 1: Get the 'top_n' parameter from the request, default to 5
#         top_n = 5
#         user_id = int(request.GET.get("user_id", user_id))
        
#         # Step 2: Connect to the SQLite database
#         interactions = Interaction.objects.all().values('user__id', 'product__id', 'interaction_count')
#         products = Product.objects.all().values('id', 'product_name', 'description', 'category')

#         # Convert to DataFrame
#         interactions_df = pd.DataFrame(list(interactions))
#         print("interaction df", interactions_df)
#         products_df = pd.DataFrame(list(products))
#         # Step 4: Train the collaborative filtering model using the interactions DataFrame
#         algo = train_collaborative_filtering(interactions_df)

#         # Step 5: Generate hybrid recommendations for the user
#         recommendations = recommend_products_cf(user_id, interactions_df, algo, top_n)

#         # Step 6: Convert recommendations to (product_id, score) tuples, with int64 to int conversion
#         recommendations = [(int(product_id), float(score)) for product_id, score in recommendations]

        

#         # Step 8: Return the recommendations as a JSON response
#         return JsonResponse({"recommendations": recommendations})

class ProductRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Ensure the user_id matches the authenticated user
        if request.user.id != user_id:
            raise NotFound("User not found or not authorized to access this resource.")

        # Call the recommendation function with the current user
        recommended_product_indices = recommend_products_cb(request.user)

        # Get the recommended products based on the indices returned
        recommended_products = Product.objects.filter(id__in=recommended_product_indices)

        # Serialize the products
        serializer = ProductSerializer(recommended_products, many=True)

        # Return the response with the serialized data
        return Response(serializer.data)
class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]  # Ensure the user is authenticated via token
    permission_classes = [IsAuthenticated]  # Only authenticated users can access their profile

    def get(self, request):
        user = request.user  # The authenticated user from the token
        
        # Manually prepare user data
        user_data = {
            "username": user.username,
            "email": user.email,
        }
        
        # Fetch related preferences for the user
        preferences = UserPreferences.objects.filter(user=user)
        
        # Serialize the user preferences using the UserPreferencesSerializer
        preferences_data = UserPreferencesSerializer(preferences, many=True).data
        
        # Add the preferences data to the user_data dictionary
        user_data['preferences'] = preferences_data
        
        return Response(user_data)