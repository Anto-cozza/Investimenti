import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calcolatore Investimenti")

st.title("💰 Calcolatore di Investimenti 💰")

# Input utente in due colonne
col1, col2 = st.columns(2)

with col1:
    capitale_iniziale = st.number_input("Capitale iniziale (€):", min_value=0, value=1000, step=100)
    contributo_mensile = st.number_input("Contributo mensile (€):", min_value=0, value=100, step=10)
    tasso_interesse = st.slider("Tasso di interesse annuale (%):", 0.0, 20.0, 5.0, 0.1)

with col2:
    anni = st.slider("Periodo (anni):", 1, 50, 10)
    inflazione = st.slider("Inflazione annuale (%):", 0.0, 10.0, 2.0, 0.1)
    freq = st.selectbox("Frequenza capitalizzazione:", ["Annuale", "Semestrale", "Trimestrale", "Mensile"])

# Calcolo periodi
periodi_per_anno = {"Annuale": 1, "Semestrale": 2, "Trimestrale": 4, "Mensile": 12}[freq]
tasso_periodo = tasso_interesse / 100 / periodi_per_anno
inflazione_periodo = inflazione / 100 / periodi_per_anno
periodi_totali = anni * periodi_per_anno
contributo_periodo = contributo_mensile * 12 / periodi_per_anno

# Calcolo valori
valori = [capitale_iniziale]
valore = capitale_iniziale

for _ in range(periodi_totali):
    interesse = valore * tasso_periodo
    valore += interesse + contributo_periodo
    valori.append(valore)

# Calcolo valori reali (con inflazione)
valori_reali = [valori[i] * (1 - inflazione_periodo) ** i for i in range(len(valori))]

# Calcolo contributi totali
contributi = [capitale_iniziale + contributo_periodo * i for i in range(periodi_totali + 1)]

# Risultati principali
st.header("Risultati")
valore_finale = valori[-1]
valore_reale = valori_reali[-1]
contributo_totale = capitale_iniziale + (contributo_periodo * periodi_totali)
interesse_guadagnato = valore_finale - contributo_totale

col1, col2 = st.columns(2)
with col1:
    st.metric("Valore finale", f"€{valore_finale:,.2f}")
    st.metric("Valore reale (con inflazione)", f"€{valore_reale:,.2f}")
with col2:
    st.metric("Totale contributi", f"€{contributo_totale:,.2f}")
    st.metric("Interesse guadagnato", f"€{interesse_guadagnato:,.2f}")

# Grafico
st.subheader("Grafico dell'investimento")
fig, ax = plt.subplots(figsize=(10, 5))
x = [i / periodi_per_anno for i in range(periodi_totali + 1)]

ax.plot(x, valori, label="Valore nominale", color="blue", linewidth=2)
ax.plot(x, valori_reali, label="Valore reale", color="green", linewidth=2)
ax.plot(x, contributi, label="Contributi", color="red", linestyle="--")

ax.set_xlabel("Anni")
ax.set_ylabel("Valore (€)")
ax.grid(True, alpha=0.3)
ax.legend()

st.pyplot(fig)

# Suggerimenti
st.subheader("Suggerimenti per l'investimento")
st.info("""
- Un aumento di 1% nel tasso di rendimento può avere un impatto significativo sul lungo termine.
- Iniziare a investire presto è spesso più importante del tasso di rendimento.
- L'inflazione riduce il potere d'acquisto nel tempo, quindi considera sempre il valore reale.
- Diversificare gli investimenti può aiutare a gestire i rischi.
""")
