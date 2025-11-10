import streamlit as st
from gui.utils import page_header, inject_css

st.set_page_config(page_title="01 – Dati & Metodi", page_icon="📚", layout="wide")
inject_css()
page_header("01 – Dati & Metodi", "v1.0")

st.markdown("""
## Fonti dati e preprocessing
- Bilanci AIDA; classificazioni UE per PMI; variabili economico-finanziarie; coordinate puntuali delle imprese.
- Standardizzazioni e normalizzazioni coerenti con la letteratura; costruzione dell’**ISP** come indicatore sintetico (versione finale di tesi).
- Segmentazioni per **dimensione** e **macro-area**.

## Matrici di prossimità
- **W_strict**: contiguità senza confini amministrativi.
- **W_border**: contiguità che incorpora i confini (effetti di bordo).

## Misure spaziali
- **Moran I (globale)**: autocorrelazione spaziale complessiva.
- **LISA**: cluster locali (HH, LL, HL, LH).
- **Gi\\*** (Getis-Ord): hotspot/coldspot.

## Modelli
- **OLS** (baseline), **SAR**, **SDM**, **GMM**, **GWR**.
- Valutazione tramite **AIC**, diagnostiche, robustezza (HC3, FDR dove opportuno).

> Vedere le pagine successive per risultati, tabelle e mappe.
""")
