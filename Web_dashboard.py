import streamlit as st
import plotly.express as px
import analysis as f   #  analysis file

st.set_page_config(page_title="Marketing Dashboard", layout="wide")

# ---------------- HEADER ----------------
st.title(" Marketing Funnel & Conversion Performance Analysis")

st.markdown("""
Analyzing user journey from clicks to conversions to identify drop-offs and optimize campaign effectiveness.

**Dataset:**  
Nykaa Marketing Campaign Performance Dataset; Real-World Inspired E-commerce Campaign Data for Marketing Analytics & ROI.
""")

# ---------------- EXECUTIVE SUMMARY ----------------
st.info(f"""
📌 **Executive Summary**

- Significant drop-off of **{f.funnel_df['Drop_off_Rate'].max():.1f}%** observed at **{f.funnel_df.loc[f.funnel_df['Drop_off_Rate'].idxmax(), 'Stage']}**, indicating weak engagement at this stage.  
- **{f.channel_quality.iloc[0]['Campaign_Type']}** delivers the highest conversion rate (**{f.channel_quality.iloc[0]['Lead_to_Conv_Rate']:.2f}%**), making it the most effective channel.  
- Opportunity to optimize underperforming channels and scale high-ROI campaigns for better overall performance.
""")

# ---------------- KPI SECTION ----------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Impressions", f"{int(f.funnel_df.loc[0,'Value']):,}")
col2.metric("Clicks", f"{int(f.funnel_df.loc[1,'Value']):,}")
col3.metric("Leads", f"{int(f.funnel_df.loc[2,'Value']):,}")
col4.metric("Conversions", f"{int(f.funnel_df.loc[3,'Value']):,}")
# ---------------- FUNNEL ----------------
st.subheader("🔻 Funnel Visualization")

fig = px.funnel(
    f.funnel_df,
    x='Value',
    y='Stage',
    color='Stage'
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- DROP-OFF ----------------
st.subheader("🚨 Drop-off Insight")

max_idx = f.funnel_df['Drop_off_Rate'].idxmax()
stage = f.funnel_df.loc[max_idx, 'Stage']
drop = f.funnel_df.loc[max_idx, 'Drop_off_Rate']

st.error(f"Biggest Drop-off at **{stage}** → {drop:.2f}% users lost")
st.info("Focus optimization efforts on this stage to improve overall conversion.")

# ---------------- CHANNEL PERFORMANCE ----------------
st.subheader("📈 Channel Performance")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        f.channel_quality,
        x='Campaign_Type',
        y='Lead_to_Conv_Rate',
        color='Campaign_Type',
        title="Lead → Conversion Rate"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        f.channel_quality,
        x='Campaign_Type',
        y='ROI',
        color='Campaign_Type',
        title="ROI by Channel"
    )
    st.plotly_chart(fig2, use_container_width=True)
# ---------------- CONVERSION TREND ----------------
st.subheader("📈 Conversion Trend Over Time")
trend_fig = py.line(
    f.conversion_trend,
    x='Date',
    y='Conversions',
    markers=True
)

st.plotly_chart(trend_fig, use_container_width=True)


# ---------------- TRAFFIC TO LEAD (FULL BREAKDOWN) ----------------
st.subheader(" Traffic to Lead Conversion Breakdown")

# --- Channel ---
fig1 = px.bar(
    f.traffic_lead_channel,
    y='Campaign_Type',
    x='Traffic_to_Lead_Rate',
    color='Campaign_Type',
    orientation='h',
    text_auto='.2f'
)
fig1.update_traces(textposition='outside')
fig1.update_layout(title="Traffic to Lead by Channel")
st.plotly_chart(fig1, use_container_width=True)

# --- Audience ---
fig2 = px.bar(
    f.traffic_lead_audience,
    y='Target_Audience',
    x='Traffic_to_Lead_Rate',
    color='Target_Audience',
    orientation='h',
    text_auto='.2f'
)
fig2.update_traces(textposition='outside')
fig2.update_layout(title=" Traffic to Lead by Audience")
st.plotly_chart(fig2, use_container_width=True)

# --- Language ---

fig3 = px.bar(
    f.traffic_lead_lang,
    y='Language',
    x='Traffic_to_Lead_Rate',
    color='Language',
    orientation='h',
    text_auto='.2f'
)
fig3.update_traces(textposition='outside')
fig3.update_layout(title="Traffic to Lead by Language")
st.plotly_chart(fig3, use_container_width=True)
# ---------------- SMART INSIGHTS ----------------
st.subheader("🧠 Key Insights & Recommendations")

best = f.channel_quality.iloc[0]
worst = f.channel_quality.iloc[-1]

max_idx = f.funnel_df['Drop_off_Rate'].idxmax()
stage = f.funnel_df.loc[max_idx, 'Stage']
drop = f.funnel_df.loc[max_idx, 'Drop_off_Rate']

st.success(f"✅ Best Channel: {best['Campaign_Type']} ({best['Lead_to_Conv_Rate']:.2f}% conversion)")
st.error(f"❌ Underperforming Channel: {worst['Campaign_Type']}")
st.warning(f"⚠️ Highest drop-off at {stage} ({drop:.2f}%)")

st.markdown("### 📢 Recommended Actions")

if drop > 80:
    st.markdown("- Improve ad creatives and audience targeting to reduce top-funnel loss")
elif drop > 50:
    st.markdown("- Optimize landing page and user journey to improve engagement")
else:
    st.markdown("- Funnel is efficient, focus on scaling conversions")

st.markdown(f"- Increase investment in **{best['Campaign_Type']}** channel due to high conversion performance")
st.markdown(f"- Re-evaluate strategy for **{worst['Campaign_Type']}** to improve ROI and conversions")

# ---------------- DATA VIEW ----------------
with st.expander("📂 View Dataset"):
    st.dataframe(f.df)
