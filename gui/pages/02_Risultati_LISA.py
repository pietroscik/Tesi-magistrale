import streamlit as st, pandas as pd
from gui.utils import DATA_DIR, load_dataset, coerce_categories, text_filter, download_df_button, page_header, inject_css

st.set_page_config(page_title="02 – Risultati LISA", page_icon="📍", layout="wide")
inject_css()
page_header("02 – Risultati LISA", "v1.0")

st.markdown("""
L'analisi **LISA** (Local Indicators of Spatial Association) identifica cluster locali:
- **High-High (HH)**, **Low-Low (LL)**, **High-Low (HL)**, **Low-High (LH)**
""")

df = coerce_categories(load_dataset("cluster LISA aggregati.xlsx"))
if df is None:
    st.error("File 'cluster LISA aggregati.xlsx' non trovato."); st.stop()

st.markdown("---")
st.subheader("🔍 Filtri")
variant = st.selectbox("Variante", ["Tutti","W_strict","W_border"])
dfv = df if variant=="Tutti" else df[df["variante"]==variant]
dfv = text_filter(dfv, "Cerca subset/area/dimensione...")

st.markdown("---")
st.subheader("📋 Tabella")
st.dataframe(dfv, use_container_width=True)
download_df_button(dfv, "lisa_filtrato.csv")

st.markdown("---")
st.subheader("📊 Grafici")
cluster_cols = [c for c in ['High-High','Low-Low','High-Low','Low-High'] if c in dfv.columns]
if not cluster_cols:
    st.info("Nessuna colonna cluster trovata."); st.stop()

# composizione %
tot = dfv[["Subset"] + cluster_cols].copy()
tot["Totale"] = tot[cluster_cols].sum(axis=1)
for c in cluster_cols:
    tot[c + "_perc"] = (tot[c] / tot["Totale"]).fillna(0) * 100

import plotly.express as px

tab_table, tab_counts, tab_perc = st.tabs(["📋 Tabella", "📊 Counts (stacked)", "📊 % Composizione"])

with tab_table:
    # Configurazione colonne per conteggi e percentuali
    lisa_config = {
        "High-High": st.column_config.NumberColumn("High-High", format="%d", help="Cluster Alto-Alto"),
        "Low-Low": st.column_config.NumberColumn("Low-Low", format="%d", help="Cluster Basso-Basso"),
        "High-Low": st.column_config.NumberColumn("High-Low", format="%d", help="Outlier Alto-Basso"),
        "Low-High": st.column_config.NumberColumn("Low-High", format="%d", help="Outlier Basso-Alto"),
        "Not Significant": st.column_config.NumberColumn("Non Signif.", format="%d"),
    }
    st.dataframe(dfv, use_container_width=True, column_config=lisa_config)

with tab_counts:
    fig = px.bar(dfv, x="Subset", y=cluster_cols, title="Cluster LISA per Subset (stacked)", template="plotly_white")
    fig.update_layout(barmode="stack", height=520, hovermode="x unified", xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

with tab_perc:
    perc_cols = [c+"_perc" for c in cluster_cols]
    figp = px.bar(tot, x="Subset", y=perc_cols, title="Composizione % cluster LISA",
                  labels={"value":"%","variable":"Cluster"}, template="plotly_white")
    figp.update_layout(barmode="stack", height=520, hovermode="x unified", xaxis_tickangle=-30, yaxis_tickformat=".0f")
    st.plotly_chart(figp, use_container_width=True)

# Confronto Strict vs Border
if variant == "Tutti" and "variante" in df.columns:
    st.markdown("### 🔄 Strict vs Border (Δ Border − Strict)")
    strict = df[df['variante']=='W_strict']
    border = df[df['variante']=='W_border']
    rows=[]
    for _, r in strict.iterrows():
        sb = border[border['Subset']==r['Subset']]
        if len(sb):
            for c in cluster_cols:
                try:
                    rows.append({"Subset":r['Subset'], "Cluster":c, "Delta": float(sb.iloc[0][c]) - float(r[c])})
                except Exception:
                    pass
    if rows:
        dfd = pd.DataFrame(rows)
        st.dataframe(dfd, use_container_width=True)
        figd = px.bar(dfd, x="Subset", y="Delta", color="Cluster", title="Δ Border − Strict per Subset", template="plotly_white")
        figd.update_layout(height=520, xaxis_tickangle=-30)
        st.plotly_chart(figd, use_container_width=True)

st.markdown("---")
st.subheader("🛡️ Robustezza: Accordo Strict vs Border")
st.markdown("Indice di accordo (0-1) tra le classificazioni ottenute con le due matrici di pesi.")
df_agree = coerce_categories(load_dataset("riepilogo_accordo_cluster_strict_vs_border.csv", sep=";", decimal=","))
if df_agree is not None:
    st.dataframe(df_agree, use_container_width=True)
else:
    st.info("Dati di accordo non disponibili.")

st.markdown("---")
st.subheader("📥 Download Dati Aggregati")
xlsx_path = DATA_DIR / "cluster LISA aggregati.xlsx"
if xlsx_path.exists():
    with open(xlsx_path, "rb") as f:
        st.download_button(
            "📥 Scarica Excel Aggregato (LISA)",
            f,
            file_name="cluster_LISA_aggregati.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("File Excel aggregato non trovato.")
