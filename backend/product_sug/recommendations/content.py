
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from product_sug.models import Product, UserPreferences, Interaction

def recommend_products_cb(user):
    # Step 1: Fetch user preferences
    preferences = UserPreferences.objects.filter(user=user)
    if not preferences.exists():
        return []  # Return empty if no preferences are found

    preferred_type = preferences.first().preferred_product_type
    preferred_description = preferences.first().preferred_description

    # Step 2: Get all products that match the preferred type and description
    products = Product.objects.filter(product_name=preferred_type, description=preferred_description)

    # Step 3: Exclude products the user has interacted with (liked, disliked, viewed)
    interacted_products = Interaction.objects.filter(user=user).values_list('product_id', flat=True)
    filtered_products = products.exclude(id__in=interacted_products)

    # Step 4: Generate content-based recommendations using the filtered products
    product_descriptions = [product.description for product in filtered_products]

    # If no products left after filtering, return empty
    if not product_descriptions:
        return []

    # Step 5: Vectorize the product descriptions
    vectorizer = TfidfVectorizer()
    product_vectors = vectorizer.fit_transform(product_descriptions)

    # Step 6: Calculate cosine similarity between products
    similarities = cosine_similarity(product_vectors, product_vectors)

    # Step 7: Get the average cosine similarity for each product
    avg_similarities = similarities.sum(axis=1) / similarities.shape[1]

    # Step 8: Get the top N most similar products (e.g., top 5)
    recommended_product_indices = avg_similarities.argsort()[::-1][:5]

    # Convert filtered_products QuerySet to a list so we can index it
    filtered_product_list = list(filtered_products)

    # Now index the list using the recommended indices
    recommended_products = [filtered_product_list[i] for i in recommended_product_indices]

    return recommended_products
