import streamlit as st
from streamlit_ga import GoogleAnalytics

# Dein GA-Tracking-ID (z. B. 'G-XXXXXXXXXX' – erstelle ein Konto auf analytics.google.com)
ga = GoogleAnalytics('G-4F63Z1DGEF')
ga.track()

st.set_page_config(page_title="Unterhaltsrechner 2026 Pro", page_icon="👨‍👧‍👦", layout="wide")

st.title("👨 Unterhaltsrechner 2026 – Komplettversion")
st.markdown("**Kindes- + Ehegattenunterhalt nach Düsseldorfer Tabelle 2026**")

col1, col2 = st.columns(2)
with col1:
    netto = st.number_input("Dein monatliches **Nettoeinkommen** (€)", min_value=0, value=2800, step=50)
    anzahl_kinder = st.number_input("**Anzahl der Kinder** (bei der Ex)", min_value=1, max_value=10, value=2, step=1)
    erwerbstaetig = st.checkbox("Ich bin erwerbstätig", value=True)

with col2:
    weitere_kinder = st.number_input("**Weitere Kinder** in neuer Beziehung", min_value=0, value=0, step=1)
    ehegattenunterhalt = st.checkbox("**Auch Ehegattenunterhalt** berechnen", value=False)

alter_liste = []
for i in range(anzahl_kinder):
    alter = st.number_input(f"Alter Kind {i+1} (Jahre)", min_value=0, max_value=30, value=8, step=1)
    alter_liste.append(alter)

sonderbedarf = st.number_input(
    "**Sonderbedarf** pro Monat (€)", 
    min_value=0, value=0, step=10,
    help="**Sonderbedarf:** Zusätzliche Kosten wie Nachhilfe, Medikamente, Sportgeräte, Brille oder Therapie. Das Jugendamt kann das anerkennen und den Unterhalt erhöhen. Belege immer mit Rechnungen!"
)

umgangskosten = st.number_input(
    "**Umgangskosten** pro Monat (€)", 
    min_value=0, value=0, step=10,
    help="**Umgangskosten:** Fahrkosten, Übernachtungen oder andere Ausgaben für Besuche bei deinen Kindern. Diese können vom Unterhalt abgezogen werden – oft 1/3 der Kosten oder pauschal 100–200 €/Monat."
)

if ehegattenunterhalt:
    st.subheader("Ehegattenunterhalt")
    netto_ex = st.number_input("**Nettoeinkommen der Ex** (€)", min_value=0, value=1200, step=50)
    ehe_dauer = st.number_input("**Dauer der Ehe** (Jahre)", min_value=1, value=8, step=1)
    betreuung = st.checkbox("Ex betreut hauptsächlich die Kinder", value=True)

if st.button("Jetzt alles berechnen", type="primary", use_container_width=True):
    # Kindesunterhalt
    def get_gruppe(netto):
        grenzen = [2100, 2500, 2900, 3300, 3700, 4100, 4500, 4900, 5300, 5700, 6100, 6500, 6900, 7300, 11200]
        for i, g in enumerate(grenzen):
            if netto <= g: return i + 1
        return 15
    gruppe = get_gruppe(netto)

    def bedarf(alter, gruppe):
        basis = [486, 558, 653, 698]
        stufe = 0 if alter <= 5 else 1 if alter <= 11 else 2 if alter <= 17 else 3
        faktor = 1.0
        for g in range(2, gruppe + 1):
            faktor *= 1.05 if g <= 5 else 1.08
        return round(basis[stufe] * faktor)

    brutto_bedarf = sum(bedarf(a, gruppe) for a in alter_liste)
    halbes_kindergeld = 129.50 * anzahl_kinder
    zahlbetrag_kind = max(brutto_bedarf - halbes_kindergeld, 0) + sonderbedarf - umgangskosten

    # Ehegattenunterhalt
    zahlbetrag_ehe = 0
    if ehegattenunterhalt:
        differenz = netto - netto_ex
        if differenz > 0:
            zahlbetrag_ehe = round(differenz * 3/7)
            if betreuung:
                zahlbetrag_ehe = round(zahlbetrag_ehe * 1.15)
        selbstbehalt_ehe = 1600 if erwerbstaetig else 1475
        rest_nach_kind = netto - zahlbetrag_kind
        if rest_nach_kind < selbstbehalt_ehe:
            zahlbetrag_ehe = max(0, rest_nach_kind - selbstbehalt_ehe + 100)

    gesamt = zahlbetrag_kind + zahlbetrag_ehe
    rest = netto - gesamt
    selbstbehalt = 1450 if erwerbstaetig else 1200

    st.subheader("Ergebnis")
    st.success(f"**Kindesunterhalt:** {zahlbetrag_kind:.2f} €")
    if ehegattenunterhalt:
        st.info(f"**Ehegattenunterhalt:** {zahlbetrag_ehe:.2f} €")
    st.success(f"**Gesamtunterhalt:** {gesamt:.2f} €")
    st.info(f"**Dir bleiben danach:** {rest:.2f} €")

    if rest < selbstbehalt:
        st.error(f"⚠️ Unter dem Selbstbehalt von {selbstbehalt} €!")
    else:
        st.success("✅ Selbstbehalt eingehalten.")

st.markdown("---")
st.caption("Erstellt mit Grok • Vollversion • Februar 2026 • Keine Rechtsberatung")
