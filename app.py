import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Social Media Engagement Dashboard", page_icon="📈", layout="wide")
st.title("📈 Social Media Engagement Dashboard")
st.caption("Analyze post performance, engagement, reach and content patterns.")

default_file = Path(__file__).parent / "data" / "social_media_data.csv"
uploaded = st.sidebar.file_uploader("Upload your CSV (optional)", type=["csv"])
df = pd.read_csv(uploaded if uploaded else default_file)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
required = ["Date","Platform","Content_Type","Likes","Comments","Shares","Impressions","Reach","Saves"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"CSV is missing columns: {', '.join(missing)}")
    st.stop()
df["Engagements"] = df["Likes"] + df["Comments"] + df["Shares"] + df["Saves"]
df["Engagement_Rate_%"] = (df["Engagements"] / df["Reach"].replace(0, pd.NA) * 100).fillna(0)

platforms = st.sidebar.multiselect("Platform", sorted(df["Platform"].dropna().unique()), default=sorted(df["Platform"].dropna().unique()))
types = st.sidebar.multiselect("Content type", sorted(df["Content_Type"].dropna().unique()), default=sorted(df["Content_Type"].dropna().unique()))
filtered = df[df["Platform"].isin(platforms) & df["Content_Type"].isin(types)].copy()
if filtered.empty:
    st.warning("No rows match these filters.")
    st.stop()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total engagements", f'{filtered["Engagements"].sum():,}')
c2.metric("Total reach", f'{filtered["Reach"].sum():,}')
c3.metric("Avg. engagement rate", f'{filtered["Engagement_Rate_%"].mean():.2f}%')
c4.metric("Posts analyzed", f'{len(filtered):,}')

left,right=st.columns(2)
with left:
    daily=filtered.groupby("Date",as_index=False)["Engagements"].sum()
    st.plotly_chart(px.line(daily,x="Date",y="Engagements",title="Engagement trend over time"),use_container_width=True)
with right:
    by_type=filtered.groupby("Content_Type",as_index=False)["Engagement_Rate_%"].mean().sort_values("Engagement_Rate_%",ascending=False)
    st.plotly_chart(px.bar(by_type,x="Content_Type",y="Engagement_Rate_%",title="Average engagement rate by content type"),use_container_width=True)
left,right=st.columns(2)
with left:
    by_platform=filtered.groupby("Platform",as_index=False)["Engagements"].sum()
    st.plotly_chart(px.bar(by_platform,x="Platform",y="Engagements",title="Engagements by platform"),use_container_width=True)
with right:
    hourly=filtered.groupby("Post_Hour",as_index=False)["Engagement_Rate_%"].mean().sort_values("Post_Hour")
    if "Post_Hour" in filtered.columns:
        st.plotly_chart(px.line(hourly,x="Post_Hour",y="Engagement_Rate_%",markers=True,title="Engagement rate by posting hour (0–23)"),use_container_width=True)

st.subheader("Top-performing posts")
cols=[c for c in ["Date","Platform","Content_Type","Post_ID","Likes","Comments","Shares","Reach","Engagement_Rate_%"] if c in filtered.columns]
st.dataframe(filtered.sort_values("Engagement_Rate_%",ascending=False)[cols].head(10),use_container_width=True)
st.download_button("Download filtered data",filtered.to_csv(index=False).encode("utf-8"),"filtered_engagement_data.csv","text/csv")
st.info("Demo data is synthetic. Replace it with your own exported/API data before making real business decisions.")
