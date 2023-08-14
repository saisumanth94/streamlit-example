import streamlit as st
import pandas as pd
import ast  # For literal string to dictionary conversion



# Sample data
chunk_size = 1000
def skip_function(row):
    # Identify data quality issues and return True for rows to skip
    if len(row) != expected_number_of_columns:
        return True  # Skip rows with unexpected number of columns
    if any(pd.isnull(row)):
        return True  # Skip rows with missing values
    if any(isinstance(value, str) and value.startswith('Error') for value in row):
        return True  # Skip rows with values starting with 'Error'
    return False

# Define the expected number of columns in your CSV data
expected_number_of_columns = 5

# Load CSV data in chunks using pandas
chunk_generator = pd.read_csv("https://www.dropbox.com/scl/fi/95u61nwabeg4os09rllyq/Overture1.csv?rlkey=pvfhtomhosz67ayzqcqy7iwyb&dl=1", chunksize=chunk_size,skiprows=skip_function)

# Initialize an empty list to store chunks
chunks = []

for chunk in chunk_generator:
    # Process each chunk (e.g., analyze, transform, etc.)
    chunks.append(chunk)

# Concatenate all chunks into a final dataset
df = pd.concat(chunks, ignore_index=True)




# Create a DataFrame
# df = pd.read_csv("https://www.dropbox.com/scl/fi/95u61nwabeg4os09rllyq/Overture1.csv?rlkey=pvfhtomhosz67ayzqcqy7iwyb&dl=1,nrows=1000")

# Convert string data to dictionaries
# df['address'] = df['address'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})

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


def main():
    st.title("Dynamic Pivot-Like Tool in Streamlit")

    # Allow users to select columns, rows, and aggregation function
    selected_columns = st.multiselect("Select Columns:", df.columns)
    selected_index = st.multiselect("Select Rows:", df.columns)
    aggregation_function = st.selectbox("Select Aggregation Function:", ['mean', 'sum', 'min', 'max','count'])

    if selected_index == "None":
        selected_index = None
    


    if selected_columns  and selected_index is not None and aggregation_function:
        # Pivot the data based on selected columns, rows, and aggregation function
        pivot_df = df.pivot_table(index=selected_index, columns=selected_columns, values='confidence', aggfunc=aggregation_function)

        # Show pivot table
        st.subheader("Pivot Table")
        st.write(pivot_df)

if __name__ == "__main__":
    main()
