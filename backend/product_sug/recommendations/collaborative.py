from surprise import Dataset, Reader, KNNBasic
import pandas as pd
from product_sug.models import Interaction

def recommend_products_cf(interactions_df, user_id, top_n):
    # Get all products the user has interacted with
    interacted_products = interactions_df[interactions_df["user__id"] == user_id]["product__id"].unique()
    
    # Count interactions per product (popularity-based recommendation)
    product_popularity = interactions_df.groupby("product__id")["interaction_count"].sum()
    
    # Sort products by interaction count (most popular first)
    recommended_products = product_popularity.sort_values(ascending=False).head(top_n)
    
    # Filter out products the user has already interacted with
    recommendations = [prod for prod in recommended_products.index if prod not in interacted_products]
    
    print(f"Popular Product Recommendations for User {user_id}: {recommendations[:top_n]}")
    return recommendations[:top_n]


# def get_interactions_df():
#     # Fetch interactions with correct column names
#     interactions = Interaction.objects.all()
    
#     # Create DataFrame from the query
#     interactions_df = pd.DataFrame(list(interactions.values('user__id', 'product__id', 'interaction_count')))
    
#     # Print column names to verify correct columns
#     print(interactions_df.columns)
    
#     # Rename columns for consistency if needed
#     interactions_df.columns = ['UserID', 'ProductID', 'interaction_count']
    
#     return interactions_df

# def train_collaborative_filtering(interactions_df):

#     interactions = Interaction.objects.all()
#     interactions_df = pd.DataFrame(list(interactions.values('user__id', 'product__id', 'interaction_count')))
#     # Ensure correct columns are used
#     print(interactions_df.columns)  # Verify column names
    
#     # Using correct column names
#     reader = Reader(rating_scale=(1, interactions_df["interaction_count"].max()))
#     data = Dataset.load_from_df(interactions_df[["user__id", "product__id", "interaction_count"]], reader)
    
#     # Build the full trainset
#     trainset = data.build_full_trainset()

#     # Set similarity options and fit the KNNBasic algorithm
#     sim_options = {"name": "cosine", "user_based": True}
#     algo = KNNBasic(sim_options=sim_options)
#     algo.fit(trainset)
    
#     return algo

# def recommend_products_cf(algo, user_id, interactions_df, top_n):
#     # Ensure the 'ProductID' column exists and fetch unique products
#     all_products = interactions_df["product__id"].unique()


#     # Get the products that the user has already interacted with
#     interacted_products = interactions_df[interactions_df["user__id"] == user_id]["product__id"].unique()

#     # List of products to predict (those not interacted with)
#     products_to_predict = [p for p in all_products if p not in interacted_products]

#     # Generate predictions for products the user hasn't interacted with
#     predictions = [(product_id, algo.predict(user_id, product_id).est) for product_id in products_to_predict]

#     # Sort predictions by score and get the top N
#     recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)[:top_n]

#     print(f"Collaborative Recommendations for User {user_id}: {recommendations}")
#     return recommendations
