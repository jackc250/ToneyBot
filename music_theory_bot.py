import os
import json
import random
from datetime import date
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from mingus.core import scales, chords, intervals

# ------------------- Load env + init client -------------------
load_dotenv()
client = OpenAI()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ------------------- Puns -------------------
def toney_pun_of_the_day() -> str:
    puns = [
        "I’m very a-chord-ing to your needs.",
        "Let’s resolve this—no more sus-pense.",
        "I can C# that you’re ready to learn.",
        "Don’t fret—your theory will scale up.",
        "I’ll be brief… like a rest.",
        "We’ll stay major, even in minor setbacks.",
        "Let’s triad our best today.",
        "This will be note-worthy.",
        "Time to face the music… theory!",
        "I’m key to your success."
    ]
    today = date.today().toordinal()
    random.seed(today)
    return random.choice(puns)

# ------------------- System prompt -------------------
SYSTEM_PROMPT = """You are ToneyBot — a witty, friendly assistant that teaches practical music theory.
You love subtle music puns but never at the expense of clarity.
Be concise, encouraging, and show steps with short examples.
Prefer note names with sharps by default unless the key favors flats, and mention enharmonics if useful.
When you call tools, do it only when they add concrete musical data (notes, degrees, intervals)."""

# ------------------- Tools -------------------
def tool_get_scale(tonic: str, scale_type: str) -> Dict[str, Any]:
    scale_map = {
        "major": scales.Major,
        "ionian": scales.Major,
        "natural_minor": scales.NaturalMinor,
        "aeolian": scales.NaturalMinor,
        "harmonic_minor": scales.HarmonicMinor,
        "melodic_minor": scales.MelodicMinor,
        "dorian": scales.Dorian,
        "phrygian": scales.Phrygian,
        "lydian": scales.Lydian,
        "mixolydian": scales.Mixolydian,
        "locrian": scales.Locrian,
        "minor_pentatonic": scales.MinorPentatonic,
        "major_pentatonic": scales.MajorPentatonic,
        "blues": scales.Blues
    }
    st = scale_type.lower().strip()
    if st not in scale_map:
        raise ValueError(f"Unsupported scale_type '{scale_type}'. Try: {', '.join(scale_map.keys())}")
    scl = scale_map[st](tonic)
    notes_list = scl.ascending()
    return {"tonic": tonic, "scale_type": st, "notes": notes_list, "degree_count": len(notes_list)}

def tool_identify_chord(note_names: List[str]) -> Dict[str, Any]:
    cleaned = [n.strip().upper().replace("B#", "C").replace("E#", "F") for n in note_names]
    candidates = set()
    for i in range(len(cleaned)):
        rotated = cleaned[i:] + cleaned[:i]
        name = chords.determine(rotated)
        for c in name:
            candidates.add(c)
    return {"input": note_names, "candidates": sorted(candidates)}

def tool_transpose(note_name: str, interval_name: str) -> Dict[str, Any]:
    up = intervals.interval(note_name, interval_name)
    return {"from": note_name, "by": interval_name, "to": up}

def tool_roman_numerals_in_key(tonic: str, scale_type: str = "major") -> Dict[str, Any]:
    s = tool_get_scale(tonic, scale_type)["notes"]
    triads = []
    rn_major = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
    rn_minor_nat = ["i", "ii°", "III", "iv", "v", "VI", "VII"]
    for i in range(7):
        root = s[i]
        third = s[(i + 2) % 7]
        fifth = s[(i + 4) % 7]
        name = chords.determine([root, third, fifth])
        triads.append({
            "degree": i + 1,
            "roman": (rn_major if scale_type.lower() in ["major", "ionian"] else rn_minor_nat)[i],
            "notes": [root, third, fifth],
            "names": name
        })
    return {"key": f"{tonic} {scale_type}", "triads": triads}

TOOL_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "tool_get_scale",
            "description": "Return the scale notes for a given tonic and scale type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tonic": {"type": "string"},
                    "scale_type": {"type": "string"}
                },
                "required": ["tonic", "scale_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_identify_chord",
            "description": "Identify chord names from a set of note names.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note_names": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["note_names"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_transpose",
            "description": "Transpose a note by a given interval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note_name": {"type": "string"},
                    "interval_name": {"type": "string"}
                },
                "required": ["note_name", "interval_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_roman_numerals_in_key",
            "description": "Diatonic triads and roman numerals for the key.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tonic": {"type": "string"},
                    "scale_type": {"type": "string", "default": "major"}
                },
                "required": ["tonic"]
            }
        }
    }
]

TOOL_IMPLS = {
    "tool_get_scale": tool_get_scale,
    "tool_identify_chord": tool_identify_chord,
    "tool_transpose": tool_transpose,
    "tool_roman_numerals_in_key": tool_roman_numerals_in_key
}

# ------------------- Model call -------------------
def call_model(messages, tools=TOOL_SCHEMA):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.3,
    )
    message = resp.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")
            try:
                result = TOOL_IMPLS[name](**args)
            except Exception as e:
                result = {"error": str(e)}
            messages.append({"role": "assistant", "tool_calls": [tool_call], "content": None})
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": name, "content": json.dumps(result)})

        follow = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.3
        )
        return follow.choices[0].message.content
    else:
        return message.content

# ------------------- Main CLI -------------------
def main():
    print("🎵 Welcome to ToneyBot — your pun-loving music theory sidekick! Type 'quit' to exit.")
    print("🎤 Pun of the day:", toney_pun_of_the_day())

    # Intro once — not stored in main conversation history
    intro_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Introduce yourself as ToneyBot and give one example music task I can try."}
    ]
    print(call_model(intro_messages))

    # Main conversation history starts clean
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        user = input("\nYou: ").strip()
        if user.lower() in {"quit", "exit"}:
            break
        messages.append({"role": "user", "content": user})
        try:
            answer = call_model(messages)
            print(f"\nToneyBot: {answer}")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()