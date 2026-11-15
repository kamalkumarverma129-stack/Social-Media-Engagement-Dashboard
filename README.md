# Social Media Engagement Dashboard

A beginner-friendly Data Analytics internship project using **Python, Pandas, Streamlit and Plotly**.

## Features
- KPIs: engagements, reach, average engagement rate, number of posts
- Platform and content-type filters
- Engagement trend over time
- Engagement rate by content type
- Engagement totals by platform
- Engagement rate by posting hour
- Top-performing posts table
- CSV upload and filtered-data download
- Separate analysis script that exports summary CSVs

## Dataset
`data/social_media_data.csv` contains **synthetic/demo data** (120 sample posts). It is not scraped from Instagram or YouTube and must not be represented as real account analytics. Replace it with your own exported data or permitted API data for real conclusions.

### Expected columns
`Date, Platform, Content_Type, Post_ID, Likes, Comments, Shares, Impressions, Reach, Saves, Post_Hour`

## Run locally (Windows)
1. Install Python (if not already installed).
2. Open this folder in VS Code.
3. Open Terminal and run:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   python -m pip install -r requirements.txt
   python -m streamlit run app.py
   ```
4. Open the local URL shown in terminal (usually `http://localhost:8501`).
5. To create analysis summaries:
   ```powershell
   python analysis.py
   ```

## Publish on GitHub
1. Create a GitHub repository named `Social-Media-Engagement-Dashboard`.
2. Upload/extract this project folder on your computer.
3. In VS Code, open the project folder and use **Source Control > Initialize Repository**.
4. Stage files, commit with message `Initial commit - Social Media Engagement Dashboard`.
5. Select **Publish to GitHub** and choose Public (or Private if instructed).
   Alternatively use GitHub website: repository > **Add file > Upload files**, drag project files (not the ZIP), then **Commit changes**.
6. Verify README and files are visible in the repository.

## Power BI (optional)
- Open Power BI Desktop > Get Data > Text/CSV > select `data/social_media_data.csv`.
- In Power Query, set `Date` to Date type and numeric metrics to Whole Number.
- Add measures:
  ```DAX
  Total Engagements = SUM('social_media_data'[Likes]) + SUM('social_media_data'[Comments]) + SUM('social_media_data'[Shares]) + SUM('social_media_data'[Saves])
  Engagement Rate % = DIVIDE([Total Engagements], SUM('social_media_data'[Reach])) * 100
  ```
- Suggested visuals: KPI cards, line chart (Date vs Total Engagements), bar chart (Content_Type vs Engagement Rate %), bar chart (Platform vs Total Engagements), table of top posts.
- Use slicers for Platform and Content_Type.

## Recommendations framework
- Compare average engagement rate by content type; test the top-performing formats more often.
- Compare platform-level reach and engagement separately; high reach does not always mean high engagement.
- Use posting-hour analysis only as a starting hypothesis. Test the top 2–3 hours over several weeks.
- Prioritize shares, saves and comments as deeper engagement signals—not likes alone.
- Review results weekly and compare similar post formats and audience sizes.

## Project deliverables
- `app.py` — interactive dashboard
- `analysis.py` — analysis and CSV summary exports
- `data/social_media_data.csv` — synthetic dataset
- `outputs/` — generated summaries (created after running analysis.py)
- `requirements.txt` — dependencies
