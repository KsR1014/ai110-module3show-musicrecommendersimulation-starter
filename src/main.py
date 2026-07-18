"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:  # when run from inside src/ (e.g. `python main.py`)
    from recommender import load_songs, recommend_songs


# A set of diverse taste profiles used to stress-test the scoring logic.
# The last one is an "adversarial" profile with conflicting preferences
# (high energy but a sad/moody vibe) to see how the scorer handles conflict.
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    "Adversarial: High-Energy but Sad": {"genre": "synthwave", "mood": "moody", "energy": 0.95},
}


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for a single named profile."""
    print("=" * 60)
    print(f"PROFILE: {name}  ->  {user_prefs}")
    print("=" * 60)
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    """Load songs, then score and rank them for each test profile."""
    songs = load_songs("data/songs.csv")
    print()
    for name, user_prefs in PROFILES.items():
        run_profile(name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
