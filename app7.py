import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# -----------------------
# CONFIG + ESTILO
# -----------------------
st.set_page_config(layout="wide")

PURPLE = "#7B2CBF"

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f1117, #1a1d26);
}

.stMetric {
    background: #1a1d26;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #2a2f3a;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 28px;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    color: #CDB4DB;
}

h1, h2, h3 {
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #0f1117;
    color: white;
}

section[data-testid="stSidebar"] label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Fraud Risk Dashboard")

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_df():
    return pd.read_csv("scored_data.csv")

df = load_df()

# -----------------------
# MAPEO
# -----------------------
product_map = {0:"W",1:"C",2:"R",3:"H",4:"S"}
card_map = {0:"visa",1:"mastercard",2:"discover",3:"amex",4:"other"}

df["ProductCD"] = df["ProductCD"].map(product_map)
df["card4"] = df["card4"].map(card_map).fillna("Missing")

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.header("Filters")

product_options = ["All"] + sorted(df["ProductCD"].dropna().unique())
card_options = ["All"] + sorted(df["card4"].dropna().unique())

selected_product = st.sidebar.selectbox("Product", product_options)
selected_card = st.sidebar.selectbox("Card Type", card_options)

threshold = st.sidebar.slider("Threshold", 0.0, 1.0, 0.5, 0.01)

# -----------------------
# FILTER
# -----------------------
mask = pd.Series(True, index=df.index)

if selected_product != "All":
    mask &= (df["ProductCD"] == selected_product)

if selected_card != "All":
    mask &= (df["card4"] == selected_card)

df_f = df[mask].copy()

if len(df_f) == 0:
    st.warning("No data for this filter")
    st.stop()

y = df_f["isFraud"].values
y_proba = df_f["y_proba"].values
y_pred = (y_proba > threshold).astype(int)

# -----------------------
# MÉTRICAS NEGOCIO
# -----------------------
tp = ((y_pred == 1) & (y == 1)).sum()
fp = ((y_pred == 1) & (y == 0)).sum()
fn = ((y_pred == 0) & (y == 1)).sum()

COSTE_FRAUDE = 100
COSTE_ALERTA = 5

loss_fraud = fn * COSTE_FRAUDE
loss_fp = fp * COSTE_ALERTA
total_loss = loss_fraud + loss_fp

# -----------------------
# BEST THRESHOLD (€)
# -----------------------
ths = np.linspace(0, 1, 50)
costs = []

for t in ths:
    yp = (y_proba > t).astype(int)

    fn_t = ((yp == 0) & (y == 1)).sum()
    fp_t = ((yp == 1) & (y == 0)).sum()

    cost = fn_t * COSTE_FRAUDE + fp_t * COSTE_ALERTA
    costs.append(cost)

best_t = ths[np.argmin(costs)]
best_cost = min(costs)

# -----------------------
# DETECTION BREAKDOWN
# -----------------------
st.markdown("## Detection Breakdown")

d1, d2, d3 = st.columns(3)
d1.metric("Fraud Detected (TP)", tp)
d2.metric("Missed Fraud (FN)", fn)
d3.metric("False Alerts (FP)", fp)

# -----------------------
# KPIs NEGOCIO
# -----------------------
st.markdown("## Business Impact")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Transactions", f"{len(df_f):,}")
c2.metric("Fraud Rate", f"{y.mean():.2%}")
c3.metric("Fraud Loss (€)", f"{loss_fraud:,.0f}")
c4.metric("Total Risk Cost (€)", f"{total_loss:,.0f}")
c5.metric("Extra Cost vs Optimal (€)", f"{total_loss - best_cost:,.0f}")

st.caption("Supuestos: 100€ por fraude no detectado, 5€ por alerta falsa")

st.markdown("---")

# -----------------------
# ROW 1
# -----------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud Detection Results")

    cm = confusion_matrix(y, y_pred)

    fig, ax = plt.subplots(figsize=(4,3))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Purples",
        cbar=False,
        linewidths=1,
        linecolor="black",
        annot_kws={"size": 12, "weight": "bold"},
        ax=ax
    )

    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

    st.pyplot(fig)

with col2:
    st.subheader("Fraud by Product")

    fraud_product = (
        df_f.groupby("ProductCD")["isFraud"]
        .mean()
        .sort_values(ascending=False)
    )

    fig2, ax2 = plt.subplots(figsize=(4,3))
    fraud_product.plot(kind="bar", color=PURPLE, ax=ax2)

    ax2.set_ylabel("Fraud Rate")
    st.pyplot(fig2)

# -----------------------
# ROW 2
# -----------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Fraud by Card Type")

    fraud_card = (
        df_f.groupby("card4")["isFraud"]
        .mean()
        .sort_values(ascending=False)
    )

    fig3, ax3 = plt.subplots(figsize=(4,3))
    fraud_card.plot(kind="bar", color=PURPLE, ax=ax3)

    ax3.set_ylabel("Fraud Rate")
    st.pyplot(fig3)

with col4:
    # decisión negocio
    if fn * COSTE_FRAUDE > fp * COSTE_ALERTA:
        decision = "Reducir el threshold para detectar más fraude"
        explanation = "Se está escapando demasiado fraude (alto coste oculto)"
    else:
        decision = "Subir el threshold para reducir falsas alertas"
        explanation = "Hay demasiadas alertas innecesarias (coste operativo)"

    st.write(f"""
### Situación

- Producto más riesgoso: **{fraud_product.idxmax()}**
- Tarjeta más riesgosa: **{fraud_card.idxmax()}**

### Impacto

- Fraude no detectado: **{fn} casos**
- Pérdida estimada: **{loss_fraud:,.0f}€**

### Recomendación

 **{decision}**

Motivo: {explanation}

### Threshold óptimo

- Actual: **{threshold:.2f}**
- Óptimo (€): **{best_t:.2f}**

Estás perdiendo: **{total_loss - best_cost:,.0f}€**

Ajustar el threshold reduce directamente el coste.
""")