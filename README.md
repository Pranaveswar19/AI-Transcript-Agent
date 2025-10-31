# AI Transcript Repurposing Agent

A production-ready AI-powered system that transforms YouTube video transcripts into multi-platform content including LinkedIn posts, Twitter threads, YouTube scripts, and Discord messages.

## Overview

This intelligent agent extracts YouTube video transcripts, generates concise summaries, and automatically repurposes content for multiple social media platforms with platform-specific formatting and tone optimization.

## Features

### Multi-Platform Content Generation
- **LinkedIn Posts**: Professional formatting with hooks, actionable takeaways, and relevant hashtags
- **Twitter/X Threads**: Character-optimized tweets (≤270 chars) with natural flow
- **YouTube Scripts**: Conversational 120-150 word scripts with 5-beat structure
- **Discord Messages**: Formatted messages with emojis and bullet points (≤1900 chars)

### Intelligent Processing
- Automatic YouTube transcript extraction (supports youtube.com, youtu.be, and /shorts/)
- AI-powered summarization with chunking for long transcripts
- Context-aware content repurposing with customizable brand voice
- Automatic timestamp generation for all outputs

### Production Features
- Robust error handling and validation
- Support for multiple YouTube URL formats
- Language preference support (defaults to English)
- Automatic output file organization

## Tech Stack

- **Python 3.8+**: Core programming language
- **OpenAI GPT-4o-mini**: AI summarization and content generation
- **YouTube Transcript API**: Transcript extraction
- **Multi-agent Architecture**: Modular design with specialized agents

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Pranaveswar19/AI-Transcript-Agent.git
   cd AI-Transcript-Agent
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the root directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Basic Usage

Run the main script:
```bash
python main.py
```

Follow the interactive prompts:
1. Select source type (currently supports YouTube)
2. Paste YouTube video URL
3. Wait for processing

The agent will:
- Extract the video transcript
- Generate a concise summary
- Create platform-specific content
- Save all outputs to the `/outputs` directory

### Output Files

All generated content is saved with timestamps in the `outputs/` directory:

- `transcript_YYYYMMDD_HHMMSS.txt` - Raw video transcript
- `summary_YYYYMMDD_HHMMSS.txt` - AI-generated summary
- `linkedin_YYYYMMDD_HHMMSS.txt` - LinkedIn post
- `tweets_YYYYMMDD_HHMMSS.txt` - Twitter thread
- `yt_script_YYYYMMDD_HHMMSS.txt` - YouTube script
- `discord_YYYYMMDD_HHMMSS.txt` - Discord message

### Supported YouTube URL Formats

```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/shorts/VIDEO_ID
```

**Note**: Videos must have subtitles/captions available.

## Project Structure

```
AI-Transcript-Agent/
├── agents/
│   ├── __init__.py
│   ├── extractor.py      # YouTube transcript extraction
│   ├── summarizer.py     # AI-powered summarization
│   └── repurposer.py     # Multi-platform content generation
├── outputs/              # Generated content (auto-created)
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Agent Architecture

### 1. Extractor Agent (`extractor.py`)
- Extracts YouTube video IDs from various URL formats
- Fetches transcripts using YouTube Transcript API
- Handles multiple API versions
- Language preference support

### 2. Summarizer Agent (`summarizer.py`)
- Chunks long transcripts for processing
- Generates concise bullet-point summaries
- Combines multi-chunk summaries intelligently
- Uses GPT-4o-mini for cost efficiency

### 3. Repurposer Agent (`repurposer.py`)
- Platform-specific content generation
- Brand voice customization
- Audience targeting
- Character limit enforcement (Twitter, Discord)
- JSON-structured output validation

## Customization

### Brand Voice & Audience

Modify the default settings in `main.py`:

```python
bundle = repurpose_text(
    summary,
    tweet_count=5,
    brand_voice="your brand voice here",  # e.g., "professional, witty, data-driven"
    audience="your target audience"       # e.g., "startup founders and CTOs"
)
```

### Summary Length

Adjust bullet points in `main.py`:

```python
summary = summarize_text(transcript, bullets=5)  # Change to 3, 7, 10, etc.
```

### Tweet Thread Length

Change tweet count in `main.py`:

```python
tweet_count=5  # Modify to generate more or fewer tweets
```

## Error Handling

The agent handles common errors gracefully:

- **No subtitles available**: Clear error message with instructions
- **Invalid URL**: URL validation and helpful feedback
- **API errors**: Retry logic and informative error messages
- **Empty transcripts**: Validation before processing
- **Network issues**: Timeout handling and error recovery

## API Costs

This system uses OpenAI's GPT-4o-mini model for cost efficiency:

- **Average cost per video**: $0.001 - $0.003
- **Model**: gpt-4o-mini (10x cheaper than GPT-4)
- **Cost monitoring**: Track usage at [OpenAI Platform](https://platform.openai.com/usage)

## Requirements

### Core Dependencies
- `openai>=1.50.0` - OpenAI API client
- `python-dotenv>=1.0.1` - Environment variable management
- `youtube-transcript-api>=0.6.2` - YouTube transcript extraction

### Optional Dependencies
- `streamlit>=1.38.0` - For potential web UI
- `trafilatura>=1.8.2` - Web content extraction
- `pypdf>=4.3.1` - PDF processing
- `jinja2>=3.1.4` - Template engine
- `tiktoken>=0.7.0` - Token counting
- `tweepy>=4.14.0` - Twitter API (if needed)
- `langchain>=0.3.1` - LLM framework

## License

MIT License - Feel free to use this in your projects.

## Author

**Pranav**
GitHub: [@Pranaveswar19](https://github.com/Pranaveswar19)

---

**Built with Python and OpenAI | Production-Ready AI Agent System**
