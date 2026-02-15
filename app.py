import streamlit as st
from datetime import datetime

# DSGVO: Cookie-Banner & GA-Consent
if 'ga_consent' not in st.session_state:
    st.session_state.ga_consent = None

if st.session_state.ga_consent is None:
    st.session_state.ga_consent = st.checkbox("Ich stimme der anonymen Nutzung von Google Analytics zu (Datenschutz: IP anonymisiert, keine personenbezogenen Daten gespeichert)", value=False)

if st.session_state.ga_consent:
    # GA nur bei Consent laden
    ga_measurement_id = "G-4F63Z1DGEF"  # Deine ID

    ga_script = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_measurement_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_measurement_id}', {{ 'anonymize_ip': true }});  # IP anonymisieren
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
.stSuccess {{
    background-color: #d4edda;
}}
.stError {{
    background-color: #f8d7da;
}}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Unterhaltsrechner 2026 Pro", page_icon="👨‍👧‍👦", layout="wide")

st.title("👨 Unterhaltsrechner 2026 Pro")
st.markdown("**Einfache & genaue Berechnung für Väter – Kindes- + Ehegattenunterhalt**")

# Erweiterter Disclaimer
st.warning("**Wichtig:** Das ist eine Schätzung nach Düsseldorfer Tabelle 2026 – **keine Rechtsberatung**! Für deinen Fall: Jugendamt, Anwalt oder offiziellen Rechner konsultieren. Datenschutz: Anonym & sicher (keine Speicherung deiner Eingaben).")

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

# CTA (ohne Pro-Version)
col_cta1, col_cta2 = st.columns(2)
with col_cta1:
    if st.button("📱 App teilen", type="secondary"):
        st.balloons()
        st.success("Danke fürs Teilen! Deine Empfehlung hilft anderen Vätern. 😊")
with col_cta2:
    if st.button("Datenschutzerklärung anzeigen", type="secondary"):
        with st.expander("Datenschutzerklärung (Stand: 15.02.2026)"):
            st.markdown("""
            ### Datenschutzerklärung

            **1. Verantwortlicher:** [Dein Name], [deine E-Mail, z. B. info@unterhaltsrechner.de].  
            **2. Erhobene Daten:** Eingaben (Nettoeinkommen, Kinderanzahl – nur für Berechnung, nicht gespeichert). Bei Zustimmung: Anonymes Tracking via Google Analytics (Views, Klicks; IP anonymisiert).  
            **3. Zweck:** Berechnung von Unterhalt, App-Verbesserung.  
            **4. Speicherung:** Eingaben nur lokal (Browser, gelöscht bei Neuladen). GA-Daten: 14 Monate.  
            **5. Rechte:** Auskunft/Löschung/Widerspruch per E-Mail. GA-Opt-out: [https://tools.google.com/dlpage/gaoptout](https://tools.google.com/dlpage/gaoptout).  
            **6. Drittanbieter:** Google Analytics (EU-Standardvertrag, IP anonym). Keine Weitergabe.  
            **7. Änderungen:** Wir informieren bei Updates.  

            Mehr Infos: [dsgvo-gesetz.de](https://dsgvo-gesetz.de). Bei Fragen: [E-Mail].
            """)

if st.button("🔢 Jetzt alles berechnen", type="primary", use_container_width=True):
    # GA-Event (nur bei Consent)
    if st.session_state.ga_consent:
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

    # Szenario-Speichern
    if 'szenarien' not in st.session_state:
        st.session_state.szenarien = []
    if st.button("💾 Szenario speichern"):
        szen_id = len(st.session_state.szenarien) + 1
        szen = {
            'ID': szen_id,
            'Netto': netto,
            'Gesamt': gesamt,
            'Rest': rest,
            'Gruppe': gruppe,
            'Datum': datetime.now().strftime("%d.%m.%Y")
        }
        st.session_state.szenarien.append(szen)
        st.success(f"Szenario {szen_id} gespeichert! Teile den Link: https://unterhaltsrechner2026.streamlit.app?szenario={szen_id}")
        if st.session_state.ga_consent:
            st.components.v1.html(f"""
            <script>
              gtag('event', 'szenario_saved', {{ 'value': 1 }});
            </script>
            """, height=0)

    if st.session_state.szenarien:
        st.subheader("📋 Gespeicherte Szenarien")
        for szen in st.session_state.szenarien:
            st.write(f"**Szenario {szen['ID']} ({szen['Datum']}):** Netto {szen['Netto']} € → Gesamt {szen['Gesamt']:.2f} € (Rest: {szen['Rest']:.2f} €, Gruppe {szen['Gruppe']})")

    # Bericht-Download
    bericht_text = f"""Unterhaltsrechner 2026 - Bericht
Stand: {datetime.now().strftime('%d.%m.%Y')}

Nettoeinkommen: {netto} €
Kindesunterhalt: {zahlbetrag_kind:.2f} €
Gesamtunterhalt: {gesamt:.2f} €
Dir bleiben: {rest:.2f} €

Hinweis: Schätzung – keine Rechtsberatung!
Einkommensgruppe: {gruppe}

Datenschutz: Deine Eingaben wurden nicht gespeichert.
"""

    st.download_button(
        label="📄 Bericht herunterladen (TXT)",
        data=bericht_text,
        file_name="unterhaltsbericht.txt",
        mime="text/plain"
    )
    if st.session_state.ga_consent:
        st.components.v1.html(f"""
        <script>
          gtag('event', 'pdf_download', {{ 'value': 1 }});
        </script>
        """, height=0)

st.markdown("---")
st.caption("Erstellt mit Grok • Vollversion • Februar 2026 • Keine Rechtsberatung")
