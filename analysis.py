import pandas as pd
from pathlib import Path

DATA = Path(__file__).parent / "data" / "social_media_data.csv"
OUT = Path(__file__).parent / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["Date"])
df["Engagements"] = df[["Likes","Comments","Shares","Saves"]].sum(axis=1)
df["Engagement_Rate_%"] = (df["Engagements"] / df["Reach"].replace(0, pd.NA) * 100).fillna(0)

summary = df.groupby("Platform").agg(
    Posts=("Post_ID","count"), Total_Reach=("Reach","sum"),
    Total_Engagements=("Engagements","sum"),
    Avg_Engagement_Rate=("Engagement_Rate_%","mean")
).round(2)
summary.to_csv(OUT/"platform_summary.csv")

content = df.groupby("Content_Type").agg(
    Posts=("Post_ID","count"), Avg_Engagement_Rate=("Engagement_Rate_%","mean"),
    Total_Engagements=("Engagements","sum")
).round(2).sort_values("Avg_Engagement_Rate",ascending=False)
content.to_csv(OUT/"content_type_summary.csv")

hour = df.groupby("Post_Hour")["Engagement_Rate_%"].mean().round(2).sort_values(ascending=False)
hour.to_csv(OUT/"posting_hour_summary.csv",header=["Avg_Engagement_Rate_%"])

print("Platform summary:\\n",summary)
print("\\nContent type summary:\\n",content)
print("\\nBest demo posting hours (ranked):\\n",hour.head(5))
print("\\nSaved summaries to outputs/")
