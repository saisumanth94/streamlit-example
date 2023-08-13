import streamlit as st
import pandas as pd
import ast  # For literal string to dictionary conversion

# Sample data


# Create a DataFrame
df = pd.read_csv('usa_500000.csv')

# Convert string data to dictionaries
df['address'] = df['address'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})

# Function to check if value is present and return 1 or 0
def presence_to_int(value):
    if pd.isna(value):
        return 0
    return 1

# Create new columns for presence of email, phone, social, and website
df['has_email'] = df['email'].apply(presence_to_int)
df['has_phone'] = df['phone'].apply(presence_to_int)
df['has_social'] = df['social'].apply(presence_to_int)
df['has_website'] = df['website'].apply(presence_to_int)

# Create new columns for presence of brand_name and brand_wikidata
df['has_brand_name'] = df['brand_name'].apply(presence_to_int)
df['has_brand_wikidata'] = df['brand_wikidata'].apply(presence_to_int)

# Create custom deciles for 'confidence' column
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6,0.7,0.8,0.9,1]  # Define custom bins based on your requirements
labels = [1, 2, 3, 4, 5, 6,7,8,9,10]  # Deciles corresponding to the bins
df['confidence_decile'] = pd.cut(df['confidence'], bins=bins, labels=labels, right=False)

# Group by 'confidence_decile' and calculate min and max confidence
grouped = df.groupby('confidence_decile')['confidence'].agg(['min', 'max'])

def main():
    st.title("Pivot-Like Tool in Streamlit")

    # Show original data
    st.subheader("Original Data")
    st.write(df)

    # Allow users to select columns for pivot
    # Allow users to select index, columns, and values for pivot
    selected_index = st.selectbox("Select Index Column:", df.columns)
    selected_columns = st.multiselect("Select Columns:", df.columns)
    selected_values = st.selectbox("Select Values Column:", df.columns)

    if selected_index and selected_columns and selected_values:
        # Pivot the data based on selected index, columns, and values
        pivot_df = df.pivot_table(index=selected_index, columns=selected_columns, values=selected_values)

        # Show pivot table
        st.subheader("Pivot Table")
        st.write(pivot_df)

if __name__ == "__main__":
    main()
