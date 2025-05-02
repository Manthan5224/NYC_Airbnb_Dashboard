import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="NYC Airbnb Dashboard")

df = pd.read_csv("data/clean_airbnb.csv")

# --- Sidebar ---
st.sidebar.header("🔍 Filters")
neighborhood = st.sidebar.multiselect("Neighborhood", df["neighbourhood"].unique())
room_type = st.sidebar.selectbox("Room Type", ["All"] + df["room_type"].unique().tolist())
price_range = st.sidebar.slider("Price Range ($)", 0, int(df["price"].max()), (0, 500))

# Filter data
filtered_df = df.copy()
if neighborhood:
    filtered_df = filtered_df[filtered_df["neighbourhood"].isin(neighborhood)]
if room_type != "All":
    filtered_df = filtered_df[filtered_df["room_type"] == room_type]
filtered_df = filtered_df[(filtered_df["price"] >= price_range[0]) & (filtered_df["price"] <= price_range[1])]

# --- Sidebar Insights ---
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Quick Insights")

if not filtered_df.empty:
    neigh_price = filtered_df.groupby("neighbourhood")["price"].mean()
    most_exp = neigh_price.idxmax()
    most_exp_price = neigh_price.max()

    least_exp = neigh_price.idxmin()
    least_exp_price = neigh_price.min()

    top_room = filtered_df["room_type"].value_counts().idxmax()
    top_room_count = filtered_df["room_type"].value_counts().max()

    avg_rating = filtered_df["rating"].mean()

    st.sidebar.markdown(f"🏆 **Most Expensive**: {most_exp} (${most_exp_price:.0f})")
    st.sidebar.markdown(f"💸 **Cheapest**: {least_exp} (${least_exp_price:.0f})")
    st.sidebar.markdown(f"🛏️ **Top Room**: {top_room} ({top_room_count} listings)")
    st.sidebar.markdown(f"⭐ **Avg Rating**: {avg_rating:.2f}")
else:
    st.sidebar.warning("No data for selected filters.")

# --- Main ---
st.title("🏠 NYC Airbnb Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Listings", len(filtered_df))
col2.metric("Avg Price", f"${filtered_df['price'].mean():.0f}")
col3.metric("Avg Reviews", f"{filtered_df['number_of_reviews'].mean():.1f}")

c1, c2 = st.columns(2)

# Donut chart - Room Type Distribution
room_data = filtered_df["room_type"].value_counts().reset_index()
room_data.columns = ['room_type', 'count']
fig1 = px.pie(room_data, names='room_type', values='count', title="Room Type Breakdown", hole=0.4)
fig1.update_traces(textposition='inside', textinfo='percent+label',
                   marker=dict(colors=['#A259FF', '#CBA5FF', '#E2D5FF']))
fig1.update_layout(paper_bgcolor='#F9F9FB', plot_bgcolor='#FFFFFF')
c1.plotly_chart(fig1, use_container_width=True)

# Bar chart - Avg Price by Room Type
room_price_avg = filtered_df.groupby("room_type")["price"].mean().reset_index()
fig2 = px.bar(
    room_price_avg,
    x="room_type",
    y="price",
    color="room_type",
    text="price",
    title="💰 Average Price by Room Type",
    height=450,
    color_discrete_sequence=['#A259FF']
)
fig2.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
fig2.update_layout(showlegend=False, paper_bgcolor='#F9F9FB', plot_bgcolor='#FFFFFF')
c2.plotly_chart(fig2, use_container_width=True)

# Map section
st.subheader("🗺️ Map of Listings")
map_df = filtered_df[["latitude", "longitude", "price", "availability_365", "neighbourhood", "room_type"]].dropna().sample(min(len(filtered_df), 300))
fig3 = px.scatter_mapbox(
    map_df,
    lat="latitude",
    lon="longitude",
    color="price",
    size="availability_365",
    hover_data=["neighbourhood", "price", "room_type"],
    color_continuous_scale="Turbo",
    zoom=10,
    height=650,
    mapbox_style="open-street-map"
)
fig3.update_layout(paper_bgcolor='#F9F9FB')
st.plotly_chart(fig3, use_container_width=True)