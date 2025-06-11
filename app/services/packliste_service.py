import tempfile
from collections import defaultdict

import requests
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

API_URL = "https://items.kjg-st-barbara.de/items/Packliste_item"

async def lade_daten_von_api(packliste_id: int):
    params = {
        "filter[item_id][_neq]": "null",
        "filter[Packliste_id][_eq]": str(packliste_id),
        "fields": "item_id.box.name,item_id.box.shelf.name,item_id.box.shelf.room.name",
        "distinct": "item_id"
    }
    try:
        # requests ist synchron; um asynchron zu bleiben, kannst du httpx oder aiohttp nutzen.
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        daten = response.json().get("data", [])
        return daten
    except Exception as e:
        print(f"Fehler beim Laden der API: {e}")
        return []

def gruppiere_daten(daten):
    struktur = defaultdict(lambda: defaultdict(list))
    schon_eingetragen = set()

    for eintrag in daten:
        try:
            box = eintrag["item_id"]["box"]
            raum = box["shelf"]["room"]["name"]
            regal = box["shelf"]["name"]
            kiste = box["name"]

            key = (raum, regal, kiste)
            if key not in schon_eingetragen:
                struktur[raum][regal].append(kiste)
                schon_eingetragen.add(key)
        except KeyError:
            continue
    return struktur

def erstelle_pdf(struktur, pfad):
    c = canvas.Canvas(pfad, pagesize=A4)
    width, height = A4

    KJG_BLAU = HexColor("#005587")
    SEITENRAND = 72
    GRAU_HELL = HexColor("#F0F0F0")

    seitenzahl = 0
    first_page = True

    for raum in sorted(struktur.keys()):
        if not first_page:
            c.showPage()
        else:
            first_page = False

        seitenzahl += 1
        y = height - SEITENRAND

        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(KJG_BLAU)
        c.drawString(SEITENRAND, y, f"Raum: {raum}")
        y -= 40

        for regal in sorted(struktur[raum].keys()):
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(KJG_BLAU)
            c.drawString(SEITENRAND + 20, y, f"Regal: {regal}")
            y -= 30

            c.setFont("Helvetica", 12)
            c.setFillColor(HexColor("#000000"))

            farbe_wechsel = False

            for kiste in sorted(struktur[raum][regal]):
                if y < SEITENRAND + 40:
                    c.showPage()
                    seitenzahl += 1
                    y = height - SEITENRAND
                    c.setFont("Helvetica-Bold", 20)
                    c.setFillColor(KJG_BLAU)
                    c.drawString(SEITENRAND, y, f"Raum: {raum}")
                    y -= 40
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(SEITENRAND + 20, y, f"Regal: {regal}")
                    y -= 30
                    c.setFont("Helvetica", 12)
                    c.setFillColor(HexColor("#000000"))
                    farbe_wechsel = False

                if farbe_wechsel:
                    c.setFillColor(GRAU_HELL)
                    c.rect(SEITENRAND + 35, y - 3, width - (SEITENRAND + 70), 18, fill=1, stroke=0)
                farbe_wechsel = not farbe_wechsel

                c.setFillColor(HexColor("#000000"))
                c.drawString(SEITENRAND + 40, y, f"☐ {kiste}")
                y -= 18

        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor("#666666"))
        footer_text = f"Seite {seitenzahl}"
        text_width = c.stringWidth(footer_text, "Helvetica", 10)
        c.drawString(width - SEITENRAND - text_width, SEITENRAND / 2, footer_text)

    c.save()

async def generiere_packliste_pdf(packliste_id: int):
    daten = await lade_daten_von_api(packliste_id)
    if not daten:
        return None

    struktur = gruppiere_daten(daten)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        erstelle_pdf(struktur, tmp.name)
        return tmp.name
