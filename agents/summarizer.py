from __future__ import annotations

from typing import List
from openai import OpenAI


def _chunk_text(text: str, max_chars: int = 12000) -> List[str]:
    """
    Very simple char-based chunker to keep prompts within a safe context window.
    (We use chars instead of tokens to keep it dependency-free here.)
    """
    if len(text) <= max_chars:
        return [text]
    chunks: List[str] = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i + max_chars])
        i += max_chars
    return chunks


def _summarize_chunk(client: OpenAI, chunk: str, bullets: int) -> str:
    prompt = f"""
You are a precise content summarizer.
Summarize the following text into:
- {bullets} concise bullet points (no fluff, no emojis)
- One short 2–3 sentence paragraph

TEXT:
{chunk}
"""
    resp = client.responses.create(model="gpt-4o-mini", input=prompt)
    return resp.output_text.strip()


def summarize_text(content: str, bullets: int = 5) -> str:
    """
    Summarize long content. If the content exceeds max_chars, we:
    1) summarize in chunks, then
    2) combine those partial summaries into one final output.
    """
    if not content or not content.strip():
        raise ValueError("summarize_text received empty content.")

    client = OpenAI()

    chunks = _chunk_text(content)
    partials: List[str] = []
    for ch in chunks:
        partials.append(_summarize_chunk(client, ch, bullets))

    if len(partials) == 1:
        return partials[0]

    joined = "\n\n---\n\n".join(partials)
    combine_prompt = f"""
You are a precise editor. Combine the following chunk summaries into a single cohesive result:
- Keep exactly {bullets} bullet points
- Followed by a crisp 2–3 sentence paragraph
- Remove repetition, keep key ideas

CHUNK SUMMARIES:
{joined}
"""
    final = client.responses.create(model="gpt-4o-mini", input=combine_prompt)
    return final.output_text.strip()
