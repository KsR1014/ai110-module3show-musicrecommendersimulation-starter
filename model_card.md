# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0** — a small, transparent, rule-based music recommender.

---

## 2. Intended Use  

VibeMatch takes a short description of a listener's taste (a favorite genre, a
favorite mood, and a target energy level) and returns a ranked list of songs from
a small catalog that best match that taste, along with a plain-language reason for
each pick. It assumes the user can describe their preference in these simple terms
and that a single snapshot of taste is enough — it does not track listening history
or learn over time. This is built for **classroom exploration**, not real users: the
goal is to make the mechanics of a recommender visible and easy to reason about,
not to power a production music app.

---

## 3. How the Model Works  

Every song carries a few labels and numbers: a genre (pop, lofi, rock…), a mood
(happy, chill, intense…), and an energy level from calm to hype. The user gives the
same kind of description of what they want. To recommend, the model acts like a
judge scoring each song on a scorecard: a song earns the most points for being in
the user's favorite genre, some points for matching their mood, and extra points
for having an energy level *close* to what the user asked for. The energy rule is
important — it rewards **closeness, not loudness**, so someone who wants calm music
is not handed a high-energy track just because its number is big. After every song
has a score, the model simply sorts them from highest to lowest and shows the top
few. Compared to the starter code (which just returned the first few songs), I added
the real scoring rule, the closeness-based energy score, a short "reasons" list so
each pick can explain itself, and the ranking step that sorts and trims to the top k.

---

## 4. Data  

The catalog is a small CSV of **10 songs**. Each row has an id, title, artist, and
seven descriptive fields: genre, mood, energy, tempo, valence (positivity),
danceability, and acousticness. The genres represented are pop, lofi, rock,
ambient, jazz, synthwave, and indie pop; the moods include happy, chill, intense,
relaxed, focused, and moody. I did not add or remove any data — I used the starter
catalog as-is. Because it is so small and lightly skewed toward pop and lofi, large
parts of real musical taste are missing: there is no hip-hop, classical, country,
metal, or non-English music, and each genre has only one or two examples, so the
system has very little room to offer variety within a genre.

---

## 5. Strengths  

The system works best for users whose taste lines up cleanly with the labels in the
catalog — a "chill lofi at low energy" user or an "intense rock at high energy" user
gets a top result that matches on genre, mood, **and** energy all at once, which
feels exactly right. It correctly captures the idea that closeness in energy matters:
a calm-music user is never handed the loudest track, and songs drift up or down the
list as their energy approaches the target. It also reliably *separates* opposite
users — the pop and lofi profiles return almost completely different lists — which
shows the scoring is genuinely reacting to preferences rather than returning a fixed
set. And because every recommendation ships with a reasons string, the results are
easy to trust and debug: you can always see exactly which points a song earned.

---

## 6. Limitations and Bias 

The clearest weakness I found in testing is that the system **over-prioritizes
genre**. A genre match is worth +2.0, which is more than any other single signal,
so a song in the "right" genre almost always beats a song that matches the user's
mood and energy but sits in a different genre. For example, the "High-Energy Pop"
user gets *Gym Hero* (pop, but mood = intense) ranked as their #2 song, above
*Rooftop Lights* which actually matches their happy mood — simply because *Gym
Hero* shares the pop label. A second limitation is that genre and mood are
**exact-match only**: "indie pop" earns zero genre points for a "pop" fan even
though they are nearly the same, so close-but-not-identical tastes are punished.
Finally, the catalog is tiny (10 songs) and genre-skewed, so any user whose
favorite genre appears only once or twice gets very little variety and the same
handful of songs recycle to the top of every related list.

---

## 7. Evaluation  

### Profiles tested

I stress-tested the scorer with four profiles, including one deliberately
"adversarial" profile with conflicting signals (very high energy paired with a
sad/moody vibe):

```
============================================================
PROFILE: High-Energy Pop  ->  {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
============================================================
1. Sunrise City - Score: 3.92
   Because: genre match (pop) (+2.0); mood match (happy) (+1.0); energy 0.82 vs target 0.90 (+0.92)
2. Gym Hero - Score: 2.97
   Because: genre match (pop) (+2.0); energy 0.93 vs target 0.90 (+0.97)
3. Rooftop Lights - Score: 1.86
   Because: mood match (happy) (+1.0); energy 0.76 vs target 0.90 (+0.86)
4. Storm Runner - Score: 0.99
   Because: energy 0.91 vs target 0.90 (+0.99)
5. Night Drive Loop - Score: 0.85
   Because: energy 0.75 vs target 0.90 (+0.85)
```

```
============================================================
PROFILE: Chill Lofi  ->  {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4}
============================================================
1. Midnight Coding - Score: 3.98
   Because: genre match (lofi) (+2.0); mood match (chill) (+1.0); energy 0.42 vs target 0.40 (+0.98)
2. Library Rain - Score: 3.95
   Because: genre match (lofi) (+2.0); mood match (chill) (+1.0); energy 0.35 vs target 0.40 (+0.95)
3. Focus Flow - Score: 3.00
   Because: genre match (lofi) (+2.0); energy 0.40 vs target 0.40 (+1.00)
4. Spacewalk Thoughts - Score: 1.88
   Because: mood match (chill) (+1.0); energy 0.28 vs target 0.40 (+0.88)
5. Coffee Shop Stories - Score: 0.97
   Because: energy 0.37 vs target 0.40 (+0.97)
```

```
============================================================
PROFILE: Deep Intense Rock  ->  {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
============================================================
1. Storm Runner - Score: 3.99
   Because: genre match (rock) (+2.0); mood match (intense) (+1.0); energy 0.91 vs target 0.90 (+0.99)
2. Gym Hero - Score: 1.97
   Because: mood match (intense) (+1.0); energy 0.93 vs target 0.90 (+0.97)
3. Sunrise City - Score: 0.92
   Because: energy 0.82 vs target 0.90 (+0.92)
4. Rooftop Lights - Score: 0.86
   Because: energy 0.76 vs target 0.90 (+0.86)
5. Night Drive Loop - Score: 0.85
   Because: energy 0.75 vs target 0.90 (+0.85)
```

```
============================================================
PROFILE: Adversarial: High-Energy but Sad  ->  {'genre': 'synthwave', 'mood': 'moody', 'energy': 0.95}
============================================================
1. Night Drive Loop - Score: 3.80
   Because: genre match (synthwave) (+2.0); mood match (moody) (+1.0); energy 0.75 vs target 0.95 (+0.80)
2. Gym Hero - Score: 0.98
   Because: energy 0.93 vs target 0.95 (+0.98)
3. Storm Runner - Score: 0.96
   Because: energy 0.91 vs target 0.95 (+0.96)
4. Sunrise City - Score: 0.87
   Because: energy 0.82 vs target 0.95 (+0.87)
5. Rooftop Lights - Score: 0.81
   Because: energy 0.76 vs target 0.95 (+0.81)
```

### What surprised me

The biggest surprise was how often *Gym Hero* shows up near the top even for users
who did **not** ask for intense gym music. For the "Happy Pop" user, *Gym Hero*
lands at #2. In plain language: the system sees that *Gym Hero* is labeled "pop"
and has high energy, and those two things alone earn enough points to beat a song
that actually matches the user's happy mood. The recommender doesn't understand
that "happy pop" and "gym pop" *feel* different — it only counts label matches and
measures the energy gap, so a loud pop workout song looks like a great fit for
anyone who likes energetic pop.

### Comparing profiles (plain language)

- **High-Energy Pop vs. Chill Lofi:** These are near opposites and the outputs
  prove the scorer is reacting to preferences, not returning the same list. The pop
  user gets bright, high-energy tracks (*Sunrise City*, *Gym Hero*); the lofi user
  gets calm, low-energy study tracks (*Midnight Coding*, *Library Rain*). This makes
  sense: flipping the target energy from 0.9 to 0.4 flips which songs sit "close" to
  the user, and changing the genre flips which songs earn the +2.0 bonus.
- **High-Energy Pop vs. Deep Intense Rock:** Both want energy ~0.9, so they *share*
  several songs (*Storm Runner*, *Gym Hero*, *Sunrise City* all appear in both), but
  the order differs. The rock user puts *Storm Runner* first (genre + mood + energy
  all match), while for the pop user *Storm Runner* drops to #4 because it earns
  energy points only. This shows the genre/mood labels — not just energy — are doing
  real work in the ranking.
- **Deep Intense Rock vs. Adversarial (High-Energy Sad):** Both target very high
  energy, yet the adversarial user's #1 is *Night Drive Loop* — a **lower-energy**
  (0.75) song. That is the conflict surfacing: the genre + mood match (+3.0) on a
  synthwave/moody track outweighs a better energy fit on a song with the wrong
  labels. It's valid given my weights, but it exposes that two matching labels can
  overpower the numerical preference the user cared most about.

### Sensitivity experiment (genre 2.0 → 1.0, energy 1.0 → 2.0)

I temporarily halved the genre weight and doubled the energy weight, then re-ran
all profiles. The **top pick barely changed**, but the score *gaps* compressed: a
pure energy-match like *Storm Runner* jumped from 0.99 to 1.98 for the pop user,
making non-genre songs far more competitive. On this 10-song catalog the change
made results more *different* (flatter, more variety-leaning) rather than clearly
more *accurate* — a good sign that on a larger catalog this weighting would break
the genre monopoly and surface more cross-genre picks.

---

## 8. Future Work  

The most valuable next step would be to fix the **exact-match problem** by treating
similar genres and moods as partially matching — for example, giving "indie pop" a
share of the pop points instead of zero, so close tastes are not punished. I would
also let users express more than one preference (a small list of favorite genres or
moods, and maybe weights they control themselves) to handle more complex tastes. To
improve variety, I could add a diversity step that avoids stacking near-identical
songs at the top, and I could bring the currently unused features (tempo, valence,
danceability, acousticness) into the score so it captures more of what makes a song
feel a certain way. Finally, the explanations could be turned into friendlier
sentences ("Great energy match and it's your favorite genre") rather than a list of
point values.

---

## 9. Personal Reflection  

Building this made it concrete that a recommender is really just "score everything,
then sort" — there is no magic, only a scorecard and a ranking. The most interesting
discovery was how much the **weights** quietly steer everything: because a genre
match was worth double a mood match, a workout song kept surfacing for users who
just wanted happy pop, and I never explicitly told it to do that; the weighting did.
That changed how I think about the music apps I use every day: when a service keeps
recommending the same kind of thing, it is probably not "understanding" me so much
as reflecting whichever signals its designers decided to weight most heavily, which
is exactly where bias and filter bubbles can sneak in.
