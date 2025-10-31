import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


def _extract_youtube_id(url: str) -> str:
    parsed = urlparse(url)
    if "youtube.com" in parsed.netloc and parsed.path == "/watch":
        from urllib.parse import parse_qs
        v = parse_qs(parsed.query).get("v", [None])[0]
        if v and re.fullmatch(r"[A-Za-z0-9_-]{11}", v):
            return v
    if "youtu.be" in parsed.netloc and parsed.path:
        cand = parsed.path.lstrip("/")
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", cand):
            return cand
    if "youtube.com" in parsed.netloc and parsed.path.startswith("/shorts/"):
        parts = parsed.path.split("/")
        if len(parts) >= 3 and re.fullmatch(r"[A-Za-z0-9_-]{11}", parts[2]):
            return parts[2]
    m = re.search(r"v=([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    raise ValueError("Could not extract a valid YouTube video ID from the URL.")


def _segments_to_text(segments) -> str:
    """
    Works for both:
    - old api: list[dict] with keys 'text', 'start', 'duration'
    - v1.x api: list[FetchedTranscriptSnippet] objects with .text attribute
    """
    parts = []
    for seg in segments:
        if isinstance(seg, dict):
            txt = seg.get("text", "")
        else:
            txt = getattr(seg, "text", "")
        if txt:
            parts.append(txt)
    return " ".join(parts).strip()


def extract_youtube_transcript(url: str, language_priority: list[str] | None = None) -> str:
    vid = _extract_youtube_id(url)
    try:
        ytt = YouTubeTranscriptApi()
        if hasattr(ytt, "list"):
            tlist = ytt.list(vid)
            if language_priority:
                for lang in language_priority:
                    try:
                        t = tlist.find_transcript([lang])
                        return _segments_to_text(t.fetch())
                    except Exception:
                        pass
            t = next(iter(tlist))
            return _segments_to_text(t.fetch())

        if hasattr(YouTubeTranscriptApi, "list_transcripts"):
            tlist = YouTubeTranscriptApi.list_transcripts(vid)
            if language_priority:
                for lang in language_priority:
                    try:
                        t = tlist.find_transcript([lang])
                        return _segments_to_text(t.fetch())
                    except Exception:
                        pass
            t = next(iter(tlist))
            return _segments_to_text(t.fetch())

        if hasattr(YouTubeTranscriptApi, "get_transcript"):
            items = YouTubeTranscriptApi.get_transcript(vid)
            return _segments_to_text(items)

        raise RuntimeError("Unsupported youtube-transcript-api version: no usable methods found.")

    except TranscriptsDisabled:
        raise RuntimeError("This video has transcripts disabled.")
    except NoTranscriptFound:
        raise RuntimeError("No transcript found. Choose a video with subtitles.")
    except StopIteration:
        raise RuntimeError("No transcripts are available for this video.")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch transcript: {e}")


def extract_content(url: str) -> str:
    return extract_youtube_transcript(url, language_priority=["en"])
