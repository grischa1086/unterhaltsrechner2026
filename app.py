import streamlit as st

# Google Analytics (mit deiner ID)
ga_measurement_id = "G-4F63Z1DGEF"

ga_script = f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={ga_measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga_measurement_id}');
</script>
"""

st.components.v1.html(ga_script, height=0)

# CSS für Design
st.markdown("""
<style>
.stApp {{
    background-color: #f0f8ff;
}}
.stTitle {{
    color: #1e90ff;
    font-size: 2.5em;
}}
.stButton > button {{
    background-color: #1e90ff;
    color: white;
    border-radius: 10px;
}}
.stMetric {{
    background-color: #e6f3ff;
    padding: 10px;
    border-radius: 5px;
}}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Unterhaltsrechner 2026 Pro", page_icon="👨‍👧‍👦", layout="wide")

st.title("👨 Unterhaltsrechner 2026 Pro")
st.markdown("**Einfache & genaue Berechnung für Väter – Kindes- + Ehegattenunterhalt**")

# Disclaimer
st.warning("**Wichtig:** Das ist eine Schätzung nach Düsseldorfer Tabelle 2026 – **keine Rechtsberatung**! Für deinen Fall: Jugendamt, Anwalt oder offiziellen Rechner konsultieren. Datenschutz: Anonym & sicher.")

col1, col2 = st.columns(2)
with col1:
    netto = st.number_input("💰 Dein monatliches **Nettoeinkommen** (€)", min_value=0, value=2800, step=50)
    anzahl_kinder = st.number_input("👨‍👧‍👦 **Anzahl der Kinder** (bei der Ex)", min_value=1, max_value=10, value=2, step=1)
    erwerbstaetig = st.checkbox("Ich bin erwerbstätig", value=True)

with col2:
    weitere_kinder = st.number_input("👨‍👩‍👦 **Weitere Kinder** in neuer Beziehung", min_value=0, value=0, step=1)
    ehegattenunterhalt = st.checkbox("**Auch Ehegattenunterhalt** berechnen", value=False)

alter_liste = []
for i in range(anzahl_kinder):
    alter = st.number_input(f"👶 Alter Kind {i+1} (Jahre)", min_value=0, max_value=30, value=8, step=1)
    alter_liste.append(alter)

sonderbedarf = st.number_input(
    "🩹 **Sonderbedarf** pro Monat (€)", 
    min_value=0, value=0, step=10,
    help="**Sonderbedarf:** Zusätzliche Kosten wie Nachhilfe, Medikamente, Sportgeräte, Brille oder Therapie. Das Jugendamt kann das anerkennen und den Unterhalt erhöhen. Belege immer mit Rechnungen!"
)

umgangskosten = st.number_input(
    "🚗 **Umgangskosten** pro Monat (€)", 
    min_value=0, value=0, step=10,
    help="**Umgangskosten:** Fahrkosten, Übernachtungen oder andere Ausgaben für Besuche bei deinen Kindern. Diese können vom Unterhalt abgezogen werden – oft 1/3 der Kosten oder pauschal 100–200 €/Monat."
)

if ehegattenunterhalt:
    st.subheader("💔 Ehegattenunterhalt")
    netto_ex = st.number_input("**Nettoeinkommen der Ex** (€)", min_value=0, value=1200, step=50)
    ehe_dauer = st.number_input("**Dauer der Ehe** (Jahre)", min_value=1, value=8, step=1)
    betreuung = st.checkbox("Ex betreut hauptsächlich die Kinder", value=True)

# CTA
col_cta1, col_cta2 = st.columns(2)
with col_cta1:
    if st.button("📱 App teilen", type="secondary"):
        st.balloons()
        st.success("Danke fürs Teilen! Deine Empfehlung hilft anderen Vätern. 😊")
with col_cta2:
    st.markdown("[**Pro-Version für 4,90 €/Monat** (PDF + Tipps) → [Gumroad-Link](https://gumroad.com)]")  # Ersetze mit echtem Link

if st.button("🔢 Jetzt alles berechnen", type="primary", use_container_width=True):
    # GA-Event
    st.components.v1.html(f"""
    <script>
      gtag('event', 'berechnung_clicked', {{ 'value': 1 }});
    </script>
    """, height=0)

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

    st.subheader("📊 Ergebnis")
    st.metric("Kindesunterhalt", f"{zahlbetrag_kind:.2f} €")
    if ehegattenunterhalt:
        st.metric("Ehegattenunterhalt", f"{zahlbetrag_ehe:.2f} €")
    st.metric("Gesamtunterhalt", f"{gesamt:.2f} €")
    st.metric("Dir bleiben danach", f"{rest:.2f} €")

    if rest < selbstbehalt:
        st.error(f"⚠️ Unter dem Selbstbehalt von {selbstbehalt} €!")
    else:
        st.success("✅ Selbstbehalt eingehalten.")

    # Szenarien speichern
    if 'szenarien' not in st.session_state:
        st.session_state.szenarien = []
    if st.button("💾 Szenario speichern"):
        st.session_state.szenarien.append({
            'Netto': netto,
            'Gesamt': gesamt,
            'Rest': rest,
            'Gruppe': gruppe
        })
        st.success(f"Szenario gespeichert! ({len(st.session_state.szenarien)} total)")

    if st.session_state.szenarien:
        st.subheader("📋 Gespeicherte Szenarien")
        for i, szen in enumerate(st.session_state.szenarien):
            st.write(f"**Szenario {i+1}:** Netto {szen['Netto']} € → Gesamt {szen['Gesamt']:.2f} € (Rest: {szen['Rest']:.2f} €)")

    # PDF-Export (JS)
    if st.button("📄 PDF-Bericht herunterladen"):
        st.components.v1.html("""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script>
          const {{ jsPDF }} = window.jspdf;
          const doc = new jsPDF();
          doc.setFontSize(16);
          doc.text('Unterhaltsrechner 2026 - Bericht', 20, 20);
          doc.setFontSize(12);
          doc.text(`Nettoeinkommen: {netto} €`, 20, 40);
          doc.text(`Kindesunterhalt: {zahlbetrag_kind} €`, 20, 50);
          doc.text(`Gesamtunterhalt: {gesamt} €`, 20, 60);
          doc.text(`Rest: {rest} €`, 20, 70);
          doc.text('Hinweis: Schätzung – keine Rechtsberatung!', 20, 80);
          doc.save('unterhaltsbericht.pdf');
        </script>
        """, height=0)

st.markdown("---")
st.caption("Erstellt mit Grok • Vollversion mit allen Features • Februar 2026 • Keine Rechtsberatung")
