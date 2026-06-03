# 🥧 Tres Quiche — `hipster` branch

> Een herwerking van de Tres Quiche chat met **[Reflex](https://reflex.dev)** —
> een pure-Python framework dat compileert naar React + Next.js. Donker thema,
> gradient-glow, glass-bubbels, gestreamde anagram-antwoorden. Klaar voor Series A.

## Wat is anders dan `main`?

| | `main` | `hipster` |
|---|---|---|
| Backend | FastAPI + Jinja2 | Reflex (pure Python) |
| Frontend | HTML/CSS/JS + HTMX-ish fetch | Auto-gegenereerd React via Reflex |
| Streaming | `StreamingResponse` van plain text | Reactive state (`yield` in async event) |
| Styling | Custom CSS | Custom CSS + Radix theme (dark, orange accent) |

## Starten in GitHub Codespaces

### 1 — Maak een Anthropic-account aan

1. Ga naar [console.anthropic.com](https://console.anthropic.com)
2. Maak een account aan
3. Ga naar **API Keys → Create Key**
4. Kopieer de sleutel (begint met `sk-ant-...`) — je ziet hem maar één keer!

### 2 — Open de Codespace

Klik op **Code → Open with Codespaces → New codespace** en wacht tot dependencies geïnstalleerd zijn.

### 3 — Voeg je API-sleutel toe

```
cp .env.example .env
```
Open `.env` en zet je sleutel:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### 4 — Start de app

```
make dev
```

De Reflex dev-server start op poort **3000** (frontend) en **8000** (backend).
Codespaces forward't 3000 automatisch — klik op de preview.

> Eerste keer duurt het ~30s: Reflex installeert Node deps en bouwt de Next.js-app.

---

## Beschikbare commando's

| Commando | Wat doet het? |
|---|---|
| `make install` | Installeert Python-deps en initialiseert Reflex |
| `make dev` | Start de app met hot-reload |
| `make run` | Start in productiemodus |
| `make clean` | Verwijdert build-artefacten (`.web/`, caches) |

## Bestanden

| Bestand | Wat doet het? |
|---|---|
| `tres_quiche/tres_quiche.py` | De hele app — state, UI, Anthropic streaming |
| `assets/styles.css` | Custom CSS: gradient bg, glass bubbels, animaties |
| `rxconfig.py` | Reflex configuratie |
| `.env` | Je geheime API-sleutel (nooit committen) |

## Wil je iets aanpassen?

- **Andere persoonlijkheid?** Pas `SYSTEM_PROMPT` aan in `tres_quiche/tres_quiche.py`
- **Andere accentkleur?** Wijzig `accent_color` in `rx.theme(...)` (Radix kleuren: orange, tomato, ruby, amber, ...) én de CSS-variabelen in `assets/styles.css`
- **Ander model?** Verander `claude-opus-4-5` in `tres_quiche/tres_quiche.py`
