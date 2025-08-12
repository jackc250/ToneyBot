# 🎵 ToneyBot — Your Pun-Loving Music Theory Assistant

ToneyBot is a Python-based CLI chatbot that teaches and explores **music theory**.  
It’s powered by [OpenAI’s GPT models](https://platform.openai.com/) and the [mingus](https://bspaans.github.io/python-mingus/) library, with a dash of humor thanks to its daily “pun of the day.”

---

## ✨ Features

- 🎼 **Scale Finder** — Get the notes for any scale type in any key.
- 🎹 **Chord Identifier** — Name chords from a set of notes.
- 🔄 **Note Transposition** — Transpose notes by intervals (m3, P5, etc.).
- 🔢 **Roman Numerals** — See diatonic triads and roman numeral analysis for a key.
- 😂 **Daily Pun** — Lighten your theory session with some musical humor.
- 🖥 **Interactive CLI** — Type commands directly in your terminal.
- 🚫 **No Repeat Intros** — ToneyBot greets you once, then gets straight to business.

---

## 🚀 Setup

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/ToneyBot.git
cd ToneyBot
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your API key
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Then edit `.env` and insert your [OpenAI API key](https://platform.openai.com/api-keys):
```
OPENAI_API_KEY=sk-your_api_key_here
```

---

## 🎯 Usage

Run ToneyBot:
```bash
python3 music_theory_bot.py
```

Example session:
```
🎵 Welcome to ToneyBot — your pun-loving music theory sidekick! Type 'quit' to exit.
🎤 Pun of the day: Don’t fret—your theory will scale up.

ToneyBot: Hello! I'm ToneyBot, your friendly guide to practical music theory, here to help you hit all the right notes! 🎶
Here's a fun task for you: Try identifying the notes in a C major scale. Once you've got that down, we can explore chords or even transpositions! Give it a shot!

You: Give me the diatonic triads in G major
ToneyBot: Sure! In G major, the diatonic triads are:
I: G B D
ii: A C E
iii: B D F#
IV: C E G
V: D F# A
vi: E G B
vii°: F# A C
```

---

## 🎵 Example Prompts to Try

- **Scales**
  - `Give me the notes of D♭ harmonic minor`
  - `Show me the A mixolydian scale`

- **Chords**
  - `Identify the chord C E G#`
  - `What chord is made from the notes F A C E`

- **Transposition**
  - `Transpose C up a minor third`
  - `Transpose F# down a perfect fifth`

- **Roman Numerals**
  - `What are the roman numerals in A major`
  - `Show me diatonic triads in E minor`

---

## 📂 File Structure
```
ToneyBot/
├── music_theory_bot.py   # Main CLI script
├── requirements.txt      # Python dependencies
├── .env.example          # API key placeholder
├── .gitignore            # Keeps secrets & temp files out of Git
└── README.md             # This file
```

---

## 🛡 License
MIT License — feel free to fork and modify.

---

## 💡 Notes
- ToneyBot uses the default model `gpt-4o-mini` for speed and low cost.
- All API calls are usage-based — keep an eye on your [OpenAI dashboard](https://platform.openai.com/usage) if using heavily.
- The `.env` file containing your key should **never** be committed to GitHub.

**NOTICE** You must use your own API Key. 
- Set one up at https://platform.openai.com/
- Once your API Key is set up and funds are in your OpenAI account, the 3 errors in music_theory_bot.py should go away.