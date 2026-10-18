"""
ColdCraft Studio - Core Engine
Handles target website scraping, noise removal, and local structured JSON inference via Ollama.
"""

import json
import re
import requests
from bs4 import BeautifulSoup
import ollama


def extract_website_context(url: str, timeout: int = 10) -> str:
    """
    Fetches and sanitizes text content from a prospect's website.
    Extracts high-signal paragraphs, meta descriptions, and headers while
    stripping out scripts, styles, navigation, footer, and boilerplate junk.
    """
    if not url.startswith("http"):
        url = "https://" + url

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except Exception as e:
        return f"Could not fetch website: {str(e)}"

    soup = BeautifulSoup(response.text, "html.parser")

    # Strip out non-content elements and navigational clutter
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "svg", "aside"]):
        tag.decompose()

    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"]

    # Collect meaningful sentences and ignore short navigational fragments
    paragraphs = []
    for elem in soup.find_all(["h1", "h2", "h3", "p"]):
        text = elem.get_text().strip()
        if len(text.split()) > 4:
            paragraphs.append(text)

    clean_text = " ".join(paragraphs)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    return f"Meta Description: {meta_desc}\nKey Details: {clean_text[:2000]}"


def generate_cold_email(
    prospect_name: str,
    company_name: str,
    site_context: str,
    sender_pitch: str,
    goal: str = "Academic Partnership",
    tone: str = "Professional & Consultative",
    length_pref: str = "Balanced (~110 words)",
    model: str = "qwen2.5:3b"
) -> dict:
    """
    Uses the ColdCraft prompt framework to draft a tailored 3-paragraph executive cold outreach
    email via a local Ollama model with strict JSON formatting.
    """
    system_prompt = f"""
You are the ColdCraft AI outbound engine—an executive B2B SDR specialized in high-conversion, non-spammy cold outreach.
Target Tone: {tone}
Strategic Goal: {goal}
Length Constraint: {length_pref} (roughly 90 to 120 words total)

MANDATORY EMAIL SKELETON:
The "email_body" field MUST be formatted with proper line breaks (using '\\n\\n') following this exact layout:

Hi {prospect_name},

[Paragraph 1: 1-2 sentences referencing a concrete initiative, program, or mission observed from {company_name}'s website]

[Paragraph 2: 2-3 sentences showing how our offering ({sender_pitch}) directly aligns with their mission and creates measurable value]

[Paragraph 3: 1 sentence proposing a low-friction, 10-minute discovery call next week]

Best regards,
[Your Name]
[Your Title / Company]

STRICT COPYWRITING RULES:
- Never output a solid wall of text. Every section must be separated by double newlines ('\\n\\n').
- Avoid generic filler buzzwords (e.g., "I hope this email finds you well", "In today's fast-paced digital world").
- Return ONLY a valid JSON object matching the exact schema below. No markdown fences or commentary.

Schema:
{{
  "subject_lines": ["Subject Option 1", "Subject Option 2", "Subject Option 3"],
  "icebreaker": "The isolated first paragraph hook",
  "email_body": "The complete formatted email string with \\n\\n line breaks",
  "call_to_action": "The closing low-friction CTA"
}}
"""

    user_prompt = f"""
Prospect Contact: {prospect_name}
Target Organization: {company_name}
Scraped Website Intel:
---
{site_context}
---
Sender's Value Prop / Offering:
---
{sender_pitch}
---
Draft the ColdCraft tailored outreach email now matching the skeleton.
"""

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        format="json",
        options={
            "temperature": 0.35,
            "num_predict": 600
        }
    )

    return json.loads(response["message"]["content"])