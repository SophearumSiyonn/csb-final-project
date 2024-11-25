import streamlit as st
import pandas as pd

# Sample database of liquors
LIQUORS = [
    {"Name": "Jack Daniel's", "Type": "Whiskey", "Taste": "Smoky", "Price": 30},
    {"Name": "Grey Goose", "Type": "Vodka", "Taste": "Smooth", "Price": 40},
    {"Name": "Bacardi", "Type": "Rum", "Taste": "Sweet", "Price": 20},
    {"Name": "Hennessy", "Type": "Cognac", "Taste": "Rich", "Price": 60},
    {"Name": "Johnnie Walker", "Type": "Whiskey", "Taste": "Rich", "Price": 50},
    {"Name": "Patrón", "Type": "Tequila", "Taste": "Citrusy", "Price": 45},
    {"Name": "Absolut", "Type": "Vodka", "Taste": "Neutral", "Price": 25},
    {"Name": "Captain Morgan", "Type": "Rum", "Taste": "Spicy", "Price": 25},
]

# Convert the database to a DataFrame
liquor_df = pd.DataFrame(LIQUORS)

# Streamlit App
st.title("🍸 Liquor Recommendation App")
st.write("Find the perfect drink based on your preferences!")

# User input for preferences
st.sidebar.header("Your Preferences")
selected_type = st.sidebar.selectbox("Select Liquor Type", options=["Any"] + list(liquor_df["Type"].unique()))
selected_taste = st.sidebar.selectbox("Select Taste Profile", options=["Any"] + list(liquor_df["Taste"].unique()))
budget = st.sidebar.slider("Budget ($)", min_value=10, max_value=100, value=(10, 60))

# Filter recommendations based on user input
filtered_liquors = liquor_df[
    ((liquor_df["Type"] == selected_type) | (selected_type == "Any")) &
    ((liquor_df["Taste"] == selected_taste) | (selected_taste == "Any")) &
    (liquor_df["Price"] >= budget[0]) &
    (liquor_df["Price"] <= budget[1])
]

# Display recommendations
if not filtered_liquors.empty:
    st.subheader("🥂 Recommended Liquors")
    for index, row in filtered_liquors.iterrows():
        st.write(f"**{row['Name']}**")
        st.write(f"- Type: {row['Type']}")
        st.write(f"- Taste: {row['Taste']}")
        st.write(f"- Price: ${row['Price']}")
        st.write("---")
else:
    st.subheader("😞 No recommendations found.")
    st.write("Try adjusting your preferences.")

# Footer
st.write("### Cheers to a great drink! 🥃")
