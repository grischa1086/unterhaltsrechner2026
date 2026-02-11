import streamlit as st

st.set_page_config(
    page_title="Unterhaltsrechner 2026",
    page_icon="👨‍👧‍👦",
    layout="centered"
)

st.title("👨 Unterhaltsrechner 2026")
st.markdown("**Einfache Schätzung für Väter – nach Düsseldorfer Tabelle (Stand 2026)**")

st.write("Gib deine Daten ein. Das Tool nutzt die aktuellen Mindestsätze (1. Einkommensgruppe) + halbes Kindergeld.")

netto = st.number_input("Dein monatliches **Nettoeinkommen** (€)", min_value=0, value=2800, step=50)
anzahl_kinder = st.number_input("**Anzahl der Kinder**", min_value=1, max_value=10, value=2, step=1)

alter_liste = []
for i in range(anzahl_kinder):
    alter = st.number_input(f"Alter Kind {i+1} (Jahre)", min_value=0, max_value=30, value=8, step=1)
    alter_liste.append(alter)

if st.button("Jetzt berechnen", type="primary", use_container_width=True):
    def bedarfssatz(alter):
        if alter <= 5: return 486
        elif alter <= 11: return 558
        elif alter <= 17: return 653
        else: return 698

    brutto_bedarf = sum(bedarfssatz(a) for a in alter_liste)
    halbes_kindergeld = 129.50 * anzahl_kinder
    zahlbetrag = max(brutto_bedarf - halbes_kindergeld, 0)

    restbetrag = netto - zahlbetrag
    selbstbehalt = 1450

    st.subheader("Ergebnis")
    st.success(f"**Geschätzter monatlicher Zahlbetrag:** {zahlbetrag:.2f} €")
    st.info(f"**Dir bleiben danach:** {restbetrag:.2f} €")

    if restbetrag < selbstbehalt:
        st.error(f"⚠️ Achtung: Du liegst unter dem Selbstbehalt von {selbstbehalt} €!")
    else:
        st.success(f"✅ Selbstbehalt ({selbstbehalt} €) wird eingehalten.")

    st.caption("**Hinweis:** Vereinfachte Schätzung nach Düsseldorfer Tabelle 2026. Keine Rechtsberatung!")

st.markdown("---")
st.caption("Erstellt mit Grok • Februar 2026")
