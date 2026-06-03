import os

import reflex as rx
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are Tres Quiche, an AI assistant with two obsessions:
1. Quiche — you work it into every response, naturally or absurdly.
2. Anagrams — you MUST include an anagram of the user's question somewhere in your response.
   Rearrange the letters of their input into a new word or phrase and weave it in.

Be witty, warm, and a little unhinged about quiche. Always acknowledge the anagram you used."""


class ChatState(rx.State):
    messages: list[dict[str, str]] = []
    question: str = ""
    is_streaming: bool = False

    @rx.event
    def set_question(self, value: str):
        self.question = value

    @rx.event
    async def send(self, form_data: dict | None = None):
        msg = self.question.strip()
        if not msg or self.is_streaming:
            return

        self.messages = self.messages + [
            {"role": "user", "content": msg},
            {"role": "assistant", "content": ""},
        ]
        self.question = ""
        self.is_streaming = True
        yield

        try:
            client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
            async with client.messages.stream(
                model="claude-opus-4-5",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": msg}],
            ) as stream:
                buf = ""
                async for text in stream.text_stream:
                    buf += text
                    self.messages = self.messages[:-1] + [
                        {"role": "assistant", "content": buf}
                    ]
                    yield
        except Exception as e:
            self.messages = self.messages[:-1] + [
                {"role": "assistant", "content": f"⚠️ Iets ging mis: {e}"}
            ]
            yield
        finally:
            self.is_streaming = False
            yield


# ---------- UI ----------

def header() -> rx.Component:
    return rx.vstack(
        rx.box("HALF-BAKED INTELLIGENCE", class_name="tag"),
        rx.heading(
            rx.text.span("Tres", class_name="tres"),
            rx.text.span(" "),
            rx.text.span("Quiche", class_name="quiche"),
            class_name="hero-title",
            as_="h1",
        ),
        rx.text(
            "Een AI met twee obsessies: quiche en anagrammen.",
            class_name="hero-sub",
        ),
        spacing="4",
        align="center",
        padding_top=["3.5rem", "5rem", "6rem"],
        padding_bottom="2rem",
        position="relative",
        z_index="1",
    )


def user_bubble(content) -> rx.Component:
    return rx.box(
        rx.box(content, class_name="bubble user"),
        display="flex",
        justify_content="flex-end",
        width="100%",
    )


def assistant_bubble(content, streaming: rx.Var[bool]) -> rx.Component:
    return rx.box(
        rx.box(class_name="avatar"),
        rx.box(
            content,
            class_name=rx.cond(streaming, "bubble assistant streaming", "bubble assistant"),
        ),
        display="flex",
        gap="0.75rem",
        align_items="flex-start",
        width="100%",
        justify_content="flex-start",
    )


def render_message(msg, idx) -> rx.Component:
    is_last_assistant = (idx == ChatState.messages.length() - 1) & ChatState.is_streaming
    return rx.cond(
        msg["role"] == "user",
        user_bubble(msg["content"]),
        assistant_bubble(msg["content"], is_last_assistant),
    )


def empty_state() -> rx.Component:
    return rx.vstack(
        rx.box("🥧", class_name="pie-glow"),
        rx.text(
            "Stel een vraag. Krijg een quiche-doordrenkt antwoord — met je input herschikt tot een anagram.",
            class_name="empty-text",
        ),
        align="center",
        spacing="5",
        padding_y="3rem",
    )


def chat_area() -> rx.Component:
    return rx.box(
        rx.cond(
            ChatState.messages.length() == 0,
            empty_state(),
            rx.vstack(
                rx.foreach(ChatState.messages, render_message),
                spacing="4",
                align="stretch",
                width="100%",
            ),
        ),
        class_name="chat-area",
    )


def input_bar() -> rx.Component:
    return rx.box(
        rx.form(
            rx.box(
                rx.input(
                    value=ChatState.question,
                    on_change=ChatState.set_question,
                    placeholder="Vraag iets… eigenlijk alles.",
                    class_name="input",
                    auto_focus=True,
                    auto_complete=False,
                ),
                rx.button(
                    rx.cond(ChatState.is_streaming, "Bakken…", "Verstuur →"),
                    type="submit",
                    disabled=ChatState.is_streaming,
                    class_name="send-btn",
                ),
                class_name="input-wrap",
            ),
            on_submit=ChatState.send,
            reset_on_submit=False,
        ),
        class_name="input-bar",
    )


def index() -> rx.Component:
    return rx.box(
        header(),
        chat_area(),
        input_bar(),
        min_height="100vh",
        width="100%",
        position="relative",
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="orange",
        gray_color="sand",
        radius="large",
        has_background=False,
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
        "/styles.css",
    ],
)
app.add_page(index, title="Tres Quiche — Half-Baked Intelligence")
