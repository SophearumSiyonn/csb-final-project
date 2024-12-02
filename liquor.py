import streamlit as st
import pandas as pd
import json

# Load liquors data from a JSON file
def load_liquors_from_json(file_name):
    with open(file_name, 'r') as f:
        return pd.DataFrame(json.load(f))

liquor_df = load_liquors_from_json("liquors.json")

# Inject CSS from an external file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Custom CSS to style the sidebar
st.markdown(
    """
    <style>
        /* Style the sidebar link to look like a hyperlink without underline */
        .sidebar .sidebar-content a {
            color: #1f77b4;
            text-decoration: none;
            font-size: 18px;
        }
        .sidebar .sidebar-content a:hover {
            color: #ff5733;
            text-decoration: none;
        }
        .sidebar .sidebar-content ul {
            list-style-type: none;  /* Remove default bullets */
            padding-left: 0;
        }
    </style>
    """, unsafe_allow_html=True
)

local_css("styles.css")

# Streamlit App
st.title(" ✦❘༻  L I K O R  ༺❘✦ ")

st.markdown(
    "<p style='font-family: Times New Roman;'>Find the perfect drink based on your preferences!<p>",
    unsafe_allow_html=True,
)

# Age Verification Step
if "verified" not in st.session_state:
    # Show the age verification form if not verified
    st.subheader("Age Verification")
    age = st.number_input("Please enter your age:", min_value=0, max_value=120, value=21)

    if st.button("Submit"):
        if age >= 18:
            st.session_state.verified = True
            st.success("Age verified successfully. You can now browse the site!")
        else:
            st.session_state.verified = False
            st.error("Sorry, you must be at least 18 years old to access this site.")
        st.rerun()  # Refresh to navigate based on the age input
else:
    # Initialize session state for cart if it doesn't exist
    if "cart" not in st.session_state:
        st.session_state.cart = []

    # Sidebar for navigation
    page = st.sidebar.radio("Navigate", ("Home", "Your Cart"))

    # Home Page (Product Listing)
    if page == "Home":
        # Search Bar
        st.sidebar.header("Search")
        search_query = st.sidebar.text_input("Search by Name or Type", "").strip().lower()

        # User input for preferences
        st.sidebar.header("Your Preferences")
        selected_taste = st.sidebar.selectbox("Select Taste Profile", options=["Any"] + list(liquor_df["Taste"].unique()))
        budget = st.sidebar.slider("Budget ($)", min_value=0, max_value=100, value=(0, 60))

        # Filter recommendations based on user input
        filtered_liquors = liquor_df[
            ((liquor_df["Taste"] == selected_taste) | (selected_taste == "Any")) &
            (liquor_df["Price"] >= budget[0]) &
            (liquor_df["Price"] <= budget[1])
        ]

        # Apply search filter for Name or Type
        if search_query:
            filtered_liquors = filtered_liquors[
                filtered_liquors["Name"].str.lower().str.contains(search_query) |
                filtered_liquors["Type"].str.lower().str.contains(search_query)
            ]

        # Display recommendations
        if not filtered_liquors.empty:
            st.markdown(
                "<h3 style='font-family: Times New Roman;'>Pick Your Choose</h3>",
                unsafe_allow_html=True,
            )

            for index, row in filtered_liquors.iterrows():
                st.markdown(
                    f"""
                    <div class="recommendation-card">
                        <h3>{row['Name']}</h3>
                        <p>Type: {row['Type']}</p>
                        <p>Taste: {row['Taste']}</p>
                        <p>Price: <strong>${row['Price']}</strong></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                # Add to Cart functionality using session_state
                if st.button(f"Add {row['Name']} to Cart"):
                    st.session_state.cart.append({"Name": row['Name'], "Price": row['Price']})
                    st.success(f"Added {row['Name']} to your cart.")

        else:
            st.subheader("No Result.")
            st.write("Try adjusting your preferences or search query.")

    # Cart Page (Display Cart and Total Purchase)
    elif page == "Your Cart":
        if st.session_state.cart:
            cart_total = sum(item['Price'] for item in st.session_state.cart)
            st.markdown(
                "<h3 style='font-family: Times New Roman;'>Your Cart</h3>",
                unsafe_allow_html=True,
            )
            st.write(f"Total: ${cart_total:.2f}")
            st.write("Items in Cart:")
            
            # Display cart items
            for item in st.session_state.cart:
                st.write(f"- {item['Name']} (${item['Price']})")
            
            # Checkout Button
            if st.button("Proceed to Checkout"):
                st.session_state.cart = []  # Clear the cart after checkout
                st.session_state.thank_you = True  # Trigger thank you message
        else:
            st.write("Your cart is empty. Add some drinks from the Home page!")

    # Thank you popup
    if getattr(st.session_state, "thank_you", False):
        st.write("🎉 Thank you for your purchase! 🥳")
        del st.session_state.thank_you  # Reset the thank you state after showing the message
