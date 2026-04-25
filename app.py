import streamlit as st
import pandas as pd

st.set_page_config(page_title="Food Delivery App", layout="wide")

# ---------- SESSION STORAGE ----------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}

if "restaurants" not in st.session_state:
    st.session_state.restaurants = {
        "Pizza Hub": [{"item": "Pizza", "price": 250}, {"item": "Burger", "price": 120}]
    }

if "orders" not in st.session_state:
    st.session_state.orders = []

# ---------- ROLE SELECT ----------
st.sidebar.title("Login")
role = st.sidebar.selectbox("Select Role", ["User", "Restaurant", "Admin"])

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

login = st.sidebar.button("Login")

# ---------- USER APP ----------
if role == "User" and login:
    st.title("🍔 Food Ordering")

    st.subheader("Restaurants")

    for rest, menu in st.session_state.restaurants.items():
        st.write(f"### {rest}")

        for item in menu:
            if st.button(f"Order {item['item']} - ₹{item['price']} ({rest})"):
                order = {
                    "user": username,
                    "restaurant": rest,
                    "item": item["item"],
                    "status": "Placed"
                }
                st.session_state.orders.append(order)
                st.success("Order Placed!")

    st.subheader("Your Orders")

    for order in st.session_state.orders:
        if order["user"] == username:
            st.write(order)

# ---------- RESTAURANT PANEL ----------
elif role == "Restaurant" and login:
    st.title("🍽️ Restaurant Dashboard")

    rest_name = username

    if rest_name not in st.session_state.restaurants:
        st.session_state.restaurants[rest_name] = []

    st.subheader("Add Menu Item")

    item_name = st.text_input("Item Name")
    price = st.number_input("Price", min_value=0)

    if st.button("Add Item"):
        st.session_state.restaurants[rest_name].append(
            {"item": item_name, "price": price}
        )
        st.success("Item Added!")

    st.subheader("Your Menu")
    st.write(st.session_state.restaurants[rest_name])

    st.subheader("Orders")

    for order in st.session_state.orders:
        if order["restaurant"] == rest_name:
            st.write(order)

            if st.button(f"Mark Delivered {order['item']}"):
                order["status"] = "Delivered"

# ---------- ADMIN PANEL ----------
elif role == "Admin" and login:
    st.title("👑 Admin Panel")

    if username == "admin" and password == "admin123":

        st.subheader("All Restaurants")
        st.write(st.session_state.restaurants)

        st.subheader("All Orders")
        st.write(st.session_state.orders)

        st.subheader("Stats")

        total_orders = len(st.session_state.orders)
        st.metric("Total Orders", total_orders)

    else:
        st.error("Invalid Admin Login")

# ---------- DEFAULT ----------
else:
    st.title("Welcome to Food Delivery App")
    st.write("Please login from sidebar")
