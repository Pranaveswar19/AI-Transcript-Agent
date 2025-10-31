from __future__ import annotations

import json
import re
from typing import Any, Dict, List
from openai import OpenAI

MAX_TWEET = 270
MAX_DISCORD = 1900

_JSON_SCHEMA_HINT = """
Return ONLY valid JSON (no backticks, no extra text) in this exact shape:
{
  "title": "string",
  "linkedin_post": "string",
  "tweet_thread": ["string", "string", "string", "string", "string"],
  "youtube_script": "string",
  "discord_message": "string"
}
"""

def _clip(s: str, n: int) -> str:
    s = (s or "").strip()
    if len(s) <= n:
        return s
    return s[: max(0, n - 1)] + "…"

def _force_list(x, count: int) -> List[str]:
    if isinstance(x, list):
        return [str(i) for i in x][:count]
    if x is None:
        return ["" for _ in range(count)]
    return [str(x)][:count]

def _parse_model_json(raw: str) -> Dict[str, Any]:
    m = re.search(r"\{[\s\S]*\}\s*$", raw)
    candidate = m.group(0) if m else raw
    try:
        return json.loads(candidate)
    except Exception:
        return {}

def _bundle_from_json(data: Dict[str, Any], tweet_count: int) -> Dict[str, Any]:
    title = str(data.get("title", "Repurposed Content")).strip()

    linkedin = str(data.get("linkedin_post", "")).strip()
    tweets = _force_list(data.get("tweet_thread"), tweet_count)
    tweets = [_clip(t.strip(), MAX_TWEET) for t in tweets]

    yt_script = str(data.get("youtube_script", "")).strip()
    discord_msg = str(data.get("discord_message", "")).strip()
    discord_msg = _clip(discord_msg, MAX_DISCORD)

    return {
        "title": title,
        "linkedin_post": linkedin,
        "tweet_thread": tweets,
        "youtube_script": yt_script,
        "discord_message": discord_msg,
    }

def repurpose_text(
    summary: str,
    tweet_count: int = 5,
    brand_voice: str = "clear, friendly, expert; minimal hype",
    audience: str = "busy tech professionals"
) -> Dict[str, Any]:
    """
    Convert a summary into LinkedIn, X (Twitter) thread, YouTube short script, and a Discord-ready message.
    Uses gpt-4o-mini for efficiency. Returns a dict with keys:
    title, linkedin_post, tweet_thread, youtube_script, discord_message.
    """
    if not summary or not summary.strip():
        raise ValueError("repurpose_text received empty summary")

    client = OpenAI()
    prompt = f"""
You are a content repurposing assistant. Convert the SUMMARY into platform-native outputs.
Audience: {audience}
Brand voice: {brand_voice}

General rules:
- Keep language human, specific, and useful.
- Prefer short sentences. Avoid fluff.
- Use emojis sparingly but effectively where asked.

Platform profiles:

- LINKEDIN ✅
  • Hook in line 1 (no clickbait).
  • 6–10 short lines with whitespace.
  • 1–2 actionable takeaways.
  • No hashtags in the body; add 3–5 relevant hashtags at the end.
  • Tone: professional, practical, courteous.

- TWITTER / X ✅ (thread of {tweet_count} tweets)
  • Each tweet ≤ 270 chars.
  • No “(1/5)” numbering; each tweet should stand on its own.
  • Light emojis are OK (0–2 per tweet), minimal or no hashtags.
  • Mix cadence: insights, mini-tips, micro-example, 1 soft CTA max.

- YOUTUBE SHORT SCRIPT ✅ (~120–150 words)
  • 5-beat flow: Hook → Context → 3 key points → Quick CTA → End.
  • Conversational, crisp, no jargon dumps.

- DISCORD MESSAGE ✅ (single post)
  • Start with a bold title and 1–2 fitting emojis.
  • Short intro line, then 4–6 bullet points with emojis (e.g., 🔹, ✅, 🚀).
  • Add a small “What to do next” line.
  • Keep under 1900 characters total.

{_JSON_SCHEMA_HINT}

SUMMARY:
{summary}
"""
    resp = client.responses.create(model="gpt-4o-mini", input=prompt)
    raw = resp.output_text.strip()
    data = _parse_model_json(raw)
    bundle = _bundle_from_json(data, tweet_count=tweet_count)

    bundle["tweet_thread"] = [_clip(t, MAX_TWEET) for t in bundle["tweet_thread"]]
    bundle["discord_message"] = _clip(bundle["discord_message"], MAX_DISCORD)

    if not bundle["discord_message"]:
        bullets = "\n".join(f"🔹 {t}" for t in bundle["tweet_thread"][:5])
        bundle["discord_message"] = _clip(
            f"**{bundle['title']}** 🚀\n\n"
            f"Here are the key takeaways:\n{bullets}\n\n"
            "What to do next: Share one insight or ask me to expand a point!",
            MAX_DISCORD
        )

    return bundle
