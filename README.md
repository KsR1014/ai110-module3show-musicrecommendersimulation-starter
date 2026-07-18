# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders (Spotify, YouTube, Netflix) don't "understand" music the
way a person does. They turn every item into a list of numbers and labels, turn
*you* into a profile of preferences, and then compute a **score** for how well
each item matches your profile. They score millions of candidates, **rank** them
from best to worst, and show you only the top handful. My simulation is a tiny,
transparent version of that same idea: score every song, sort by score, show the
best few.

My version prioritizes **matching what the user already likes** over discovery or
novelty. It rewards an exact **genre** match most, an exact **mood** match next,
and then fine-tunes with how **close** a song's energy is to the user's target.
Crucially, for a numerical feature like energy, *closer is better, not higher* — a
user who wants calm music should not be handed a high-energy track just because
its number is large.

### Features used

**`Song`** objects use these attributes (from `data/songs.csv`):

- `genre` (e.g. pop, lofi, rock) — categorical
- `mood` (e.g. happy, chill, intense) — categorical
- `energy` (0.0–1.0) — numerical
- `acousticness` (0.0–1.0) — numerical
- plus `tempo_bpm`, `valence`, `danceability` available for future experiments

**`UserProfile`** stores the user's taste. Example profile I'll test with:

```python
user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.4,
    "likes_acoustic": True,
}
```

- `favorite_genre`
- `favorite_mood`
- `target_energy` (the energy level they *want*, 0.0–1.0)
- `likes_acoustic` (True/False)

### Algorithm Recipe — Scoring Rule (one song)

Each song gets a single score built from weighted parts:

```
score =  2.0 * genre_match          # 1 if song.genre == favorite_genre, else 0
       + 1.0 * mood_match           # 1 if song.mood  == favorite_mood,  else 0
       + 1.0 * (1 - abs(song.energy - target_energy))   # closeness, not size
       + 0.5 * acoustic_bonus       # small nudge if acoustic preference matches
```

- **Genre is weighted highest (2.0), double a mood match (1.0)** because genre is
  the strongest single signal of taste; mood is real but more flexible. The energy
  term contributes a 0–1 closeness score that acts as a tie-breaker; the acoustic
  bonus (0.5) is a light nudge. These weights are *design choices*, and I plan to
  experiment with changing them.
- The energy term uses `1 - abs(difference)` so a **perfect match scores 1.0** and
  a total mismatch scores 0.0 — rewarding closeness to the user's target, not just
  higher numbers.

### Ranking Rule (the list) — data flow

The scoring rule only judges one song at a time. The full flow:

```
INPUT              PROCESS (the loop)                 OUTPUT
User Prefs  ──▶  for each song in songs.csv:   ──▶   Top K
                   score = Scoring Rule(song)         Recommendations
                 then sort all songs by score,
                 highest first
```

1. Run the scoring rule on **every** song in the catalog.
2. **Sort** all songs by score, highest first.
3. Return the **top `k`**.

Both rules are needed: scoring produces the numbers, ranking decides the order and
cutoff. Without ranking I'd have a pile of unordered scores; without scoring the
ranker would have nothing to sort.

### Potential biases I expect

- **Over-prioritizing genre.** With genre weighted 2.0, a fantastic song that
  matches the user's mood and energy perfectly but sits in a *different* genre can
  be buried below a mediocre same-genre song. Great cross-genre matches get ignored.
- **All-or-nothing categories.** Genre and mood are exact string matches, so
  "indie pop" and "pop" — or "chill" and "relaxed" — are treated as complete
  strangers even though they're close. The system has no notion of *similar*
  categories, only *identical* ones.
- **Popularity/novelty blindness.** The recipe only rewards matching what the user
  already likes, so it never surfaces something new or different — it can trap a
  user in a narrow taste bubble (a "filter bubble," like real recommenders).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loading songs from data/songs.csv...
Loaded songs: 10

Top recommendations:

Sunrise City - Score: 3.98
Because: genre match (pop) (+2.0); mood match (happy) (+1.0); energy 0.82 vs target 0.80 (+0.98)

Gym Hero - Score: 2.87
Because: genre match (pop) (+2.0); energy 0.93 vs target 0.80 (+0.87)

Rooftop Lights - Score: 1.96
Because: mood match (happy) (+1.0); energy 0.76 vs target 0.80 (+0.96)

Night Drive Loop - Score: 0.95
Because: energy 0.75 vs target 0.80 (+0.95)

Storm Runner - Score: 0.89
Because: energy 0.91 vs target 0.80 (+0.89)

```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



