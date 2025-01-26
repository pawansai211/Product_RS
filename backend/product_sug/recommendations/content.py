from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from product_sug.models import Product, UserPreferences

def recommend_products_cb(user):
    preferences = UserPreferences.objects.filter(user=user)
    preferred_type = preferences.first().preferred_product_type
    preferred_description = preferences.first().preferred_description

    # Compute cosine similarity based on descriptions
    products = Product.objects.filter(product_name=preferred_type, description=preferred_description)
    product_descriptions = [product.description for product in products]

    vectorizer = TfidfVectorizer()
    product_vectors = vectorizer.fit_transform(product_descriptions)
    
    similarities = cosine_similarity(product_vectors, product_vectors)
    
    # Get the average cosine similarity for each product
    avg_similarities = similarities.sum(axis=1) / similarities.shape[1]

    # Get top N most similar products
    recommended_product_indices = avg_similarities.argsort()[::-1][:5]  # Sort by average similarity

    return recommended_product_indices
