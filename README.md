# ColdCraft Studio

A local-first B2B cold outreach tool. It reads a prospect's website, finds a relevant talking point, and drafts a personalized cold email using open-weight models running on your own machine through Ollama. No API keys, no per-email cost, and no data leaves your computer.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [How It Works](#how-it-works)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Why Local Inference](#why-local-inference)
8. [Contributing](#contributing)
9. [License](#license)

## Overview

Effective cold outreach is slow and expensive to do well:

- Mass templates read as robotic, often land in spam, and convert poorly.
- Manual prospect research takes 10 to 15 minutes per lead.
- Cloud AI APIs speed up drafting but add per-request costs and send your pitch and lead data to third-party servers.

ColdCraft Studio automates the research and drafting steps locally. Give it a prospect URL and a short description of your offer, and it produces a ready-to-review email, typically within a few seconds on modern hardware, at no marginal cost.

## Features

- **Website scraping:** Fetches the prospect's page with BeautifulSoup and removes scripts, navigation, and cookie banners so only the core business messaging remains.
- **Local inference:** Runs `qwen2.5:3b` (default) or `llama3.2:1b` through Ollama. Nothing is sent over the internet except the request to fetch the prospect's page.
- **Structured three-paragraph emails:** Output is constrained to a JSON schema so every draft contains a personalized opening, a value proposition tied to the prospect, and a low-friction call to action.
- **Email preview:** Displays the draft inside a simple email-client layout for quick review and copying.
- **One-click send via `mailto:`:** Opens your default mail application (Outlook, Apple Mail, Thunderbird, and others) with the recipient, subject, and body pre-filled.
- **CSV export:** Downloads lead details, subject lines, and email bodies for import into a CRM or for bulk review.

## How It Works

```
Prospect URL
    |
    v
Web scraper (BeautifulSoup)
    Removes scripts and menus, extracts headline and body text
    |
    v
Streamlit interface
    Collects your offer, objective, and preferred tone
    |
    v
Local Ollama model (qwen2.5:3b)
    Generates the email as schema-constrained JSON
    |
    v
Output
    Email preview, mailto: link, and CSV export
```

## Requirements

- Python 3.10 or later
- [Ollama](https://ollama.com/) installed and running
- Enough free memory to run a 3B-parameter model (roughly 4 GB or more is recommended)

## Installation

1. Pull the models with Ollama:

   ```bash
   ollama pull qwen2.5:3b
   ollama pull llama3.2:1b
   ```

2. Clone or download this repository and move into its directory.

3. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Make sure Ollama is running, then start the app:

```bash
python -m streamlit run app.py
```

Streamlit will open the interface in your browser, usually at `http://localhost:8501`. From there:

1. Enter the prospect's website URL.
2. Describe your offer, your goal for the email, and the tone you want.
3. Generate the draft and review it in the preview panel.
4. Send it through your mail client with the `mailto:` button, or export your drafts as a CSV.

Always review and edit a draft before sending. Local models are fast and free, but they can misread a website.

## Why Local Inference

- **No marginal cost:** Generating a draft costs nothing beyond your own hardware and electricity.
- **Privacy:** Your pitch, your offer details, and your lead lists stay on your machine.
- **Independence:** No rate limits, pricing changes, or model deprecations from an outside provider.

## Contributing

Contributions are welcome. To propose a change:

1. Fork the repository.
2. Create a branch for your change.
3. Commit your work with a clear message.
4. Open a pull request describing what you changed and why.

Bug reports and feature suggestions can be submitted as issues.
