import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are Tres Quiche, an AI assistant with two obsessions:
1. Quiche — you work it into every response, naturally or absurdly.
2. Anagrams — you MUST include an anagram of the user's question somewhere in your response.
   Rearrange the letters of their input into a new word or phrase and weave it in.

Be witty, warm, and a little unhinged about quiche. Always acknowledge the anagram you used."""


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(message: str = Form(...)):
    """Stream a response from Claude."""

    def generate():
        with client.messages.stream(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message}],
        ) as stream:
            for text in stream.text_stream:
                # HTMX-friendly: stream plain text chunks
                yield text

    return StreamingResponse(generate(), media_type="text/plain")
