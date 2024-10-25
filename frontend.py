import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import warnings
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import scipy.sparse
import joblib
from streamlit_tags import st_tags
from deap import base, creator, tools, algorithms


# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)  #

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Configure the path to your dataset
DATASET_PATH = "./models/itemset_metrics.csv"
APRIORI_RULESET_PATH = './models/apriori_ruleset.pkl'
TFIDF_MATRIX_PATH = './models/tfidf_matrix.npz'
VECTORIZER_PATH = './models/vectorizer.joblib'



# Load the dataset
@st.cache_resource
def load_data():
    data = pd.read_csv(DATASET_PATH)
    return data

# load ruleset
@st.cache_resource
def load_apriori_rule_set():
    rule_set = pd.read_pickle(APRIORI_RULESET_PATH)
    return rule_set

# Function to preprocess text (tokenization, stopwords removal)
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalnum() and t not in stopwords.words('english')]
    return ' '.join(tokens)

# Calculate Jaccard Similarity
def jaccard_similarity(query, document):
    set_query = set(query.split())
    set_document = set(document.split())
    intersection = len(set_query.intersection(set_document))
    union = len(set_query.union(set_document))
    return intersection / union if union != 0 else 0


def generate_recommendations(rules, selected_item_name):
    # Filter rules to recommend items based on the selected item code
    recommendations = rules[rules['antecedents'].apply(lambda x: selected_item_name in x)]
    recommendations = recommendations.sort_values(by='lift', ascending=False)

    # Return top recommended items
    return recommendations.head(5)

# Load the data
data = load_data()
rules = load_apriori_rule_set()
# Load the tfidf_matrix and vectorizer
tfidf_matrix = scipy.sparse.load_npz(TFIDF_MATRIX_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

data['Processed_Description'] = data['PART_DESCRIPTION'].apply(preprocess)

# Set up the Streamlit app
st.title("Procurement Search and Recommendation System")


tab1, tab2, tab3, tab4 = st.tabs(["Description Based Discovery", "Apriori Recommendations", "Constraint Based Search", "Genetic Algorithm Multi-Item Order Constraint Solver"])

with tab1:
    st.write("## Item Discovery")

    # Search input
    search_query = st.text_input("Enter item description to search:")

    # Dropdown to select similarity method
    similarity_method = st.selectbox("Select Similarity Matching Method", 
                                    ["TFIDF Cosine Similarity", "Jaccard Similarity"])

    if search_query:
        # Preprocess the search query
        processed_query = preprocess(search_query)

        if similarity_method == "TFIDF Cosine Similarity":
            # Compute TF-IDF and cosine similarity
            query_vec = vectorizer.transform([processed_query])
            similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        else:
            # Compute Jaccard similarity
            similarities = data['Processed_Description'].apply(
                lambda desc: jaccard_similarity(processed_query, desc)
            ).values

        # Get top 5 most relevant items
        top_indices = np.argsort(similarities)[-5:][::-1]
        top_items = data.iloc[top_indices]

        # Display results
        st.write("### Top Matching Items:")
        st.dataframe(top_items[['ITEM_NAME','ITEM_CODE', 'SUPPLIER_NAME','SUPPLIER_CODE','PART_DESCRIPTION','PRICE_mean','DAYS_TAKEN_TO_DELIVER_mean','CERTIFICATIONS']])


with tab2:
    selected_item_name = st.selectbox("Select Item Name for Recommendations", data['ITEM_NAME'].unique())

    if selected_item_name:
        recommendations = generate_recommendations(rules, selected_item_name)
        st.write(f"### Recommended Items for '{selected_item_name}':")
        if not recommendations.empty:
            st.dataframe(recommendations[['consequents','antecedent support','consequent support','support','confidence','lift']])
        else:
            st.write("No recommendations found for this item.")

with tab3:
    st.write("## Constraint-Based Supplier Search")

    # Select the item for which to search suppliers
    selected_item = st.selectbox("Select Item", data['ITEM_NAME'].unique())

    # Set constraints for the search
    max_price = st.number_input("Enter Maximum Price", min_value=0, max_value=5000,value=5000)
    max_delivery_days = st.number_input("Enter Maximum Delivery Days", min_value=0, max_value=130, value=60)
    certifications_required = st_tags(
        label='Specific region compliance Required:',
        text='Press enter to add more',
        value=[],
        suggestions=['Asia',
        'Australia',
        'Canada',
        'Europe',
        'Global Certification',
        'India',
        'US'],
        maxtags=10,
        key='1'
    )

    # Optional: If faulted items column is present

    max_faulted_items = st.number_input("Enter Maximum Faulted Items", min_value=0,max_value=1, value=1)


    # Perform the constraint-based search
    if st.button("Find Suppliers"):
        # Apply the constraints to filter the data
        filtered_data = data[data['ITEM_NAME'] == selected_item]
        filtered_data = filtered_data[filtered_data['PRICE_mean'] <= max_price]
        filtered_data = filtered_data[data['DAYS_TAKEN_TO_DELIVER_mean'] <= max_delivery_days]
        filtered_data = filtered_data[filtered_data['FAULTED_PARTS_RATE_mean'] <= max_faulted_items]

        # Filter by certifications
        if certifications_required:
            filtered_data = filtered_data[
                filtered_data['CERTIFICATIONS'].apply(lambda x: all(cert in x for cert in certifications_required))
            ]

        # Display the matching suppliers
        if not filtered_data.empty:
            st.write("### Matching Suppliers:")
            st.dataframe(filtered_data[['ITEM_NAME','ITEM_CODE', 'SUPPLIER_NAME','SUPPLIER_CODE','PART_DESCRIPTION','PRICE_mean','DAYS_TAKEN_TO_DELIVER_mean','CERTIFICATIONS',"FAULTED_PARTS_RATE_mean"]])
        else:
            st.write("No suppliers found matching the constraints.")

with tab4:
    st.write("## Genetic Algorithm Supplier Search")

    # Select multiple items for which to search suppliers
    selected_items = st.multiselect("Select Items", data['ITEM_NAME'].unique())

    # Set constraints for the search
    max_price = st.number_input("Enter Maximum Price", min_value=0.0, max_value=5000.0, value=5000.0)
    max_delivery_days = st.number_input("Enter Maximum Delivery Days", min_value=0.0, max_value=130.0, value=60.0)
    certifications_required = st_tags(
        label='Specific region compliance Required:',
        text='Press enter to add more',
        value=[],
        suggestions=['Asia', 'Australia', 'Canada', 'Europe', 'Global Certification', 'India', 'US'],
        maxtags=10,
        key='2'
    )

    # Optional: If faulted items column is present
    if 'FAULTED_ITEMS' in data.columns:
        max_faulted_items = st.number_input("Enter Maximum Faulted Items", min_value=0, max_value=1, value=1)
    else:
        max_faulted_items = None

    # Define the genetic algorithm
    def evaluate(individual):
        total_price = 0
        total_delivery_days = 0
        for item, supplier in zip(selected_items, individual):
            item_data = data[(data['ITEM_NAME'] == item) & (data['SUPPLIER_NAME'] == supplier)]
            if not item_data.empty:
                total_price += item_data['PRICE_mean'].values[0]
                total_delivery_days += item_data['DAYS_TAKEN_TO_DELIVER_mean'].values[0]
            else:
                return float('inf'), float('inf')
        return total_price, total_delivery_days

    def genetic_algorithm():
        suppliers = data['SUPPLIER_NAME'].unique()
        creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("attr_supplier", np.random.choice, suppliers)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_supplier, n=len(selected_items))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("evaluate", evaluate)

        population = toolbox.population(n=50)
        algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, verbose=False)

        best_individual = tools.selBest(population, k=1)[0]
        return best_individual

    # Perform the genetic algorithm search
    if st.button("Find Best Supplier Combination"):
        if selected_items:
            best_supplier_combination = genetic_algorithm()
            st.write("### Best Supplier Combination:")
            for item, supplier in zip(selected_items, best_supplier_combination):
                st.write(f"Item: {item}, Supplier: {supplier}")
        else:
            st.write("Please select at least one item.")