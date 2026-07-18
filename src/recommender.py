import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Algorithm Recipe weights (see README "How The System Works")
#   +2.0  exact genre match   (strongest taste signal)
#   +1.0  exact mood match
#   +1.0  energy closeness     scaled by 1 - |song.energy - target|
#   +0.5  acoustic preference match (only when the profile specifies it)
# ---------------------------------------------------------------------------
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5

# Columns in data/songs.csv that must be numbers so we can do math on them.
_INT_FIELDS = {"id"}
_FLOAT_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the catalog of songs to recommend from."""
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score one Song against a UserProfile using the Algorithm Recipe."""
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += GENRE_WEIGHT
            reasons.append(f"genre match ({song.genre}) (+{GENRE_WEIGHT})")

        if song.mood == user.favorite_mood:
            score += MOOD_WEIGHT
            reasons.append(f"mood match ({song.mood}) (+{MOOD_WEIGHT})")

        # Closeness, not size: a perfect energy match earns the full weight.
        closeness = 1.0 - abs(song.energy - user.target_energy)
        energy_points = ENERGY_WEIGHT * closeness
        score += energy_points
        reasons.append(
            f"energy {song.energy:.2f} vs target {user.target_energy:.2f} "
            f"(+{energy_points:.2f})"
        )

        # A song counts as "acoustic" if its acousticness is on the high side.
        song_is_acoustic = song.acousticness >= 0.5
        if song_is_acoustic == user.likes_acoustic:
            score += ACOUSTIC_WEIGHT
            reasons.append(f"acoustic preference match (+{ACOUSTIC_WEIGHT})")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score for the given user."""
        # Judge every song, then rank highest score first and keep the top k.
        ranked = sorted(self.songs, key=lambda s: self._score(user, s)[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining a song's score."""
        score, reasons = self._score(user, song)
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.
    Numeric columns are converted to int/float so we can do math on them later.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in _INT_FIELDS:
                    song[key] = int(value)
                elif key in _FLOAT_FIELDS:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song (dict) against user preferences (dict).
    Returns (score, reasons) where reasons explains where the points came from.
    Required by recommend_songs() and src/main.py
    """
    # Accept either the short keys used in main.py (genre/mood/energy) or the
    # longer profile keys from the README (favorite_genre/favorite_mood/...).
    fav_genre = user_prefs.get("genre", user_prefs.get("favorite_genre"))
    fav_mood = user_prefs.get("mood", user_prefs.get("favorite_mood"))
    target_energy = user_prefs.get("energy", user_prefs.get("target_energy"))

    score = 0.0
    reasons: List[str] = []

    if fav_genre is not None and song.get("genre") == fav_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({song['genre']}) (+{GENRE_WEIGHT})")

    if fav_mood is not None and song.get("mood") == fav_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({song['mood']}) (+{MOOD_WEIGHT})")

    if target_energy is not None and song.get("energy") is not None:
        closeness = 1.0 - abs(song["energy"] - target_energy)
        energy_points = ENERGY_WEIGHT * closeness
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {target_energy:.2f} "
            f"(+{energy_points:.2f})"
        )

    # Optional acoustic preference, only if the profile asks for it.
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None and song.get("acousticness") is not None:
        song_is_acoustic = song["acousticness"] >= 0.5
        if song_is_acoustic == likes_acoustic:
            score += ACOUSTIC_WEIGHT
            reasons.append(f"acoustic preference match (+{ACOUSTIC_WEIGHT})")

    if not reasons:
        reasons.append("no strong matches")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks all songs by score and returns the top k.
    Each item is (song_dict, score, explanation).
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    # sorted() returns a NEW list (leaves `songs` untouched); key=score, high→low.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
