# 🥧 Tres Quiche

> Een AI-chatbot die in elk antwoord een anagram van jouw vraag verwerkt — en het altijd over quiche heeft.

## Starten in GitHub Codespaces

### Stap 1 — Maak een Anthropic-account aan

1. Ga naar [console.anthropic.com](https://console.anthropic.com)
2. Maak een account aan
3. Ga naar **API Keys → Create Key**
4. Kopieer de sleutel (begint met `sk-ant-...`) — je ziet hem maar één keer!

### Stap 2 — Open de Codespace

1. Klik op **Code → Open with Codespaces → New codespace**
2. Wacht tot de omgeving klaar is (dependencies worden automatisch geïnstalleerd)

### Stap 3 — Voeg je API-sleutel toe

Maak een `.env` bestand aan op basis van het voorbeeld:
```
cp .env.example .env
```
Open `.env` en vul je sleutel in:
```
ANTHROPIC_API_KEY=sk-ant-...
```
> ⚠️ Commit dit bestand nooit naar GitHub. Het staat al in `.gitignore`, dus dat gaat automatisch goed.

### Stap 4 — Start de app

```
make dev
```

Codespaces opent automatisch een preview. Stel een vraag!

---

## Beschikbare commando's

| Commando | Wat doet het? |
|---|---|
| `make install` | Installeert alle dependencies |
| `make dev` | Start de app met auto-reload (voor ontwikkeling) |
| `make run` | Start de app zonder auto-reload (voor productie) |

## Hoe werkt het?

| Bestand | Wat doet het? |
|---|---|
| `main.py` | De backend — ontvangt je vraag, stuurt hem naar Claude, streamt het antwoord terug |
| `templates/index.html` | De frontend — de chatinterface in je browser |
| `.env` | Je geheime API-sleutel (wordt nooit geüpload naar GitHub) |

## Wil je iets aanpassen?

- **Andere persoonlijkheid?** Pas `SYSTEM_PROMPT` aan in `main.py`
- **Ander model?** Verander `claude-opus-4-5` naar een ander Claude-model
- **Andere stijl?** Pas de CSS aan in `templates/index.html`
