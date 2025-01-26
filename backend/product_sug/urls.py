from django.urls import path

from .views import ProductUploadView, UserInteractionView, \
    ProductRecommendationView, ProductListView, SignupView, LoginView, \
        CurrentUserView, UserProfileView

urlpatterns = [
    path('upload_product/', ProductUploadView.as_view(), name='upload_product'),
    path('user_interaction/', UserInteractionView.as_view(), name='user_interaction'),
    path('product_recommendations/<int:user_id>/', ProductRecommendationView.as_view(), name='product_recommendations'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('current_user/', CurrentUserView.as_view(), name='current-user'),
    path('user_profile/', UserProfileView.as_view(), name='user-profile'),
    
]
