from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from agents.extractor import extract_content
from agents.summarizer import summarize_text
from agents.repurposer import repurpose_text


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _save_text(kind: str, text: str) -> Path:
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    file_path = out_dir / f"{kind}_{_timestamp()}.txt"
    file_path.write_text(text, encoding="utf-8")
    return file_path


def _save_bundle(bundle: dict) -> None:
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = _timestamp()
    (out_dir / f"title_{stamp}.txt").write_text(bundle.get("title", ""), encoding="utf-8")
    (out_dir / f"linkedin_{stamp}.txt").write_text(bundle.get("linkedin_post", ""), encoding="utf-8")
    (out_dir / f"tweets_{stamp}.txt").write_text("\n\n".join(bundle.get("tweet_thread", [])), encoding="utf-8")
    (out_dir / f"yt_script_{stamp}.txt").write_text(bundle.get("youtube_script", ""), encoding="utf-8")
    (out_dir / f"discord_{stamp}.txt").write_text(bundle.get("discord_message", ""), encoding="utf-8")


def main() -> None:
    print("🎥 AI Content Repurposing (YouTube → Summary → Repurpose → Discord)")
    print("-----------------------------------------------------------------")
    print("Select source type:")
    print("  1) YouTube Video")
    choice = input("Enter choice [1]: ").strip()

    if choice != "1":
        print("❌ Invalid choice. Only '1' (YouTube) is supported right now.")
        return

    yt_link = input("Paste YouTube link (must have subtitles): ").strip()
    if not yt_link:
        print("❌ Please provide a valid YouTube link.")
        return

    print("\n📥 Extracting transcript...")
    try:
        transcript = extract_content(yt_link)
        if not transcript.strip():
            print("❌ Got an empty transcript. The video may lack captions.")
            return
        print(f"✅ Extracted {len(transcript)} characters.")
        print("\n--- TRANSCRIPT PREVIEW (first 600 chars) ---\n")
        print(transcript[:600] + ("…" if len(transcript) > 600 else ""))

        t_path = _save_text("transcript", transcript)
        print(f"\n💾 Saved transcript to: {t_path.resolve()}")

    except Exception as e:
        print(f"\n❌ Error during extraction: {e}")
        return

    print("\n🧠 Summarizing…")
    try:
        summary = summarize_text(transcript, bullets=5)
        print("\n--- SUMMARY ---\n")
        print(summary)

        s_path = _save_text("summary", summary)
        print(f"\n💾 Saved summary to: {s_path.resolve()}")

    except Exception as e:
        print(f"\n❌ Error during summarization: {e}")
        return

    print("\n✍️ Repurposing content for platforms…")
    try:
        bundle = repurpose_text(
            summary,
            tweet_count=5,
            brand_voice="direct, calm, helpful; crisp verbs; minimal hype",
            audience="product builders, indie devs, and tech learners"
        )

        print("\n--- LINKEDIN ---\n")
        print(bundle.get("linkedin_post", ""))

        print("\n--- TWEETS ---\n")
        for i, tw in enumerate(bundle.get("tweet_thread", []), start=1):
            print(f"{i}. {tw}")

        print("\n--- YOUTUBE SCRIPT (~1 min) ---\n")
        print(bundle.get("youtube_script", ""))

        print("\n--- DISCORD MESSAGE ---\n")
        print(bundle.get("discord_message", ""))

        _save_bundle(bundle)
        print("\n💾 Saved LinkedIn, tweets, YouTube script, and Discord message to /outputs/")

    except Exception as e:
        print(f"\n❌ Error during repurposing: {e}")
        return

    print("\n✅ All done!")

if __name__ == "__main__":
    main()
