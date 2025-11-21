import streamlit as st
from gui.utils import DATA_DIR, load_dataset, coerce_categories, text_filter, download_df_button, page_header, inject_css

st.set_page_config(page_title="05 – Modelli Econometrici", page_icon="📈", layout="wide")
inject_css()
page_header("05 – Modelli Econometrici", "v1.0")

st.markdown("""
Confronto tra **OLS, SAR, SDM, GMM, GWR**. Valutazione con **AIC**, diagnostiche, robustezza (HC3, FDR).
""")

model_detail = coerce_categories(load_dataset("riepilogo_modello_dettaglio.csv", sep=";", decimal=","))
gwr_summary = coerce_categories(load_dataset("riepilogo_regressivi.csv", sep=";", decimal=","))

if model_detail is None:
    st.error("File 'riepilogo_modello_dettaglio.csv' non trovato."); st.stop()

st.markdown("---")
st.subheader("🔍 Filtri")
col1, col2, col3 = st.columns(3)
areas = ["Tutte"] + sorted(list(model_detail["Area"].dropna().unique())) if "Area" in model_detail.columns else ["Tutte"]
sizes = ["Tutte"] + sorted(list(model_detail["Dimensione"].dropna().unique())) if "Dimensione" in model_detail.columns else ["Tutte"]
models = ["Tutti"] + sorted(list(model_detail["model"].dropna().unique())) if "model" in model_detail.columns else ["Tutti"]

with col1: area = st.selectbox("Area", areas)
with col2: size = st.selectbox("Dimensione", sizes)
with col3: mdl  = st.selectbox("Modello", models)

dfv = model_detail.copy()
if area != "Tutte" and "Area" in dfv.columns: dfv = dfv[dfv["Area"]==area]
if size != "Tutte" and "Dimensione" in dfv.columns: dfv = dfv[dfv["Dimensione"]==size]
if mdl  != "Tutti" and "model" in dfv.columns: dfv = dfv[dfv["model"]==mdl]
dfv = text_filter(dfv, "Cerca subset/area/modello...")

st.markdown("---")
st.subheader("📋 Dettaglio")

# Configurazione colonne per una migliore leggibilità
column_config = {
    "AIC": st.column_config.NumberColumn("AIC", format="%.2f", help="Akaike Information Criterion (minore è meglio)"),
    "R2": st.column_config.NumberColumn("R²", format="%.4f", help="R-squared"),
    "LogLik": st.column_config.NumberColumn("LogLik", format="%.2f", help="Log-Likelihood"),
    "p_value": st.column_config.NumberColumn("p-value", format="%.4e", help="Significatività statistica"),
    "RMSE": st.column_config.NumberColumn("RMSE", format="%.4f", help="Root Mean Square Error"),
    "Moran_resid_p": st.column_config.NumberColumn("Moran Resid p", format="%.4e", help="P-value Moran sui residui"),
    "BP_p": st.column_config.NumberColumn("BP p", format="%.4e", help="Breusch-Pagan p-value"),
    "AD_p": st.column_config.NumberColumn("AD p", format="%.4e", help="Anderson-Darling p-value"),
}

st.dataframe(
    dfv, 
    use_container_width=True,
    column_config=column_config
)
download_df_button(dfv, "modelli_filtrato.csv")

st.markdown("---")
if "AIC" in dfv.columns and dfv["AIC"].notna().any():
    st.subheader("📊 Confronto AIC")
    import plotly.express as px
    df_aic = dfv[dfv["AIC"].notna()]
    if not df_aic.empty:
        fig_aic = px.box(df_aic, x="model", y="AIC", title="Distribuzione AIC per Modello",
                         template="plotly_white", points="suspectedoutliers")
        fig_aic.update_layout(height=520)
        st.plotly_chart(fig_aic, use_container_width=True)

    st.markdown("### 🔻 Top 20 per AIC (più basso = meglio)")
    
    # Filtra solo i modelli migliori (best_by_AIC == True/VERO)
    if "best_by_AIC" in df_aic.columns:
        # Gestione valori booleani o stringhe "VERO"/"FALSO"
        mask_best = df_aic["best_by_AIC"].astype(str).str.upper().isin(["TRUE", "VERO", "1"])
        df_top = df_aic[mask_best]
    else:
        df_top = df_aic

    st.dataframe(
        df_top.sort_values("AIC", ascending=True).head(20),
        use_container_width=True,
        hide_index=True,
        column_config={"AIC": st.column_config.NumberColumn(format="%.2f")}
    )
else:
    st.info("Colonna AIC non disponibile nei dati filtrati.")

if gwr_summary is not None:
    st.markdown("---")
    st.subheader("🗺️ GWR – Sommario")
    st.dataframe(gwr_summary, use_container_width=True)

st.markdown("---")
st.subheader("📥 Download Diagnostiche Complete")
diagn_path = DATA_DIR / "diagn_summary.csv"
if diagn_path.exists():
    with open(diagn_path, "rb") as f:
        st.download_button(
            "📥 Scarica Diagnostiche (CSV)",
            f,
            file_name="diagn_summary.csv",
            mime="text/csv"
        )

# Check for GWR residuals Moran
gwr_moran = load_dataset("riepilogo_gwr_residui_moran.csv")
if gwr_moran is not None and not gwr_moran.empty:
    st.markdown("---")
    st.subheader("🗺️ GWR – Moran sui Residui")
    st.dataframe(gwr_moran, use_container_width=True)
