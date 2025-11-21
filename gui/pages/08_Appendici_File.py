
import streamlit as st
import pandas as pd
import pathlib
import sys

# --- PATH GUARD: assicura che la root del repo sia in sys.path ---
APP_DIR = pathlib.Path(__file__).resolve().parent.parent   # .../gui
ROOT_DIR = APP_DIR.parent                                   # repo root
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
# ---------------------------------------------------------------

from gui.utils import page_header, inject_css

st.set_page_config(page_title="Appendici", page_icon="📎", layout="wide")
inject_css()
page_header("Appendici", "Consultazione file di log e di output grezzi.")

st.markdown("""
Questa sezione permette di ispezionare il contenuto di alcuni file di output e di log generati durante le analisi,
al fine di garantire la massima trasparenza e riproducibilità.
""")

# Definisci i percorsi dei file
base_path = ROOT_DIR
files_to_display = {
    "Modelli Econometrici": {
        "path": base_path / "04_econometric_models",
        "files": [
            "Coefficienti_robusti_HC3_full.csv",
            "Coefficienti_robusti_HC3_sample.csv",
            "risultati_modelli_dimensioni_stepwise.txt",
            "stepwise_by_dimensione.xlsx",
        ]
    },
    "Documentazione": {
        "path": base_path,
        "files": [
            "sintesi ipotesi.xlsx",
        ]
    },
    "Log Analisi Spaziale": {
        "path": base_path / "05_analysis_spatial" / "05_logs",
        "files": [
            "_REPORT_FINALE_MODELLI_MIGLIORI.txt",
            "robustezza_e_riepiloghi_finali.txt",
            "analisi_dimensione_macroarea_borderfree.txt",
            "analisi_dimensione_macroarea.txt",
            "analisi_k_nazionale.txt",
            "analisi_regressiva_dimensione_macroarea.txt",
            "autocorrelazione_globale.txt",
        ]
    }
}

# Mostra i file
for section, data in files_to_display.items():
    st.subheader(f"📂 {section}")
    folder_path = data["path"]
    for filename in data["files"]:
        file_path = folder_path / filename
        with st.expander(f"📄 {filename}"):
            if file_path.exists():
                try:
                    if file_path.suffix.lower() == ".csv":
                        df = pd.read_csv(file_path)
                        st.dataframe(df)
                    elif file_path.suffix.lower() == ".xlsx":
                        df = pd.read_excel(file_path)
                        st.dataframe(df)
                    else:
                        content = file_path.read_text(encoding="utf-8")
                        st.code(content, language="text")
                except Exception as e:
                    st.error(f"Errore nella lettura del file {filename}: {e}")
            else:
                st.warning(f"File non trovato: {file_path}")

st.sidebar.info(
    "**Tesi di Laurea Magistrale**\n\n"
    "Analisi Spaziale delle Performance delle Imprese Italiane\n\n"
    "**Autore:** Pietro Maietta\n\n"
    "---\n\n"
    "🌐 **Dashboard Online:**\n"
    "[pietromaietta.streamlit.app](https://pietromaietta.streamlit.app/)"
)
