import requests

class PlaylistGenerator:
    def __init__(self):
        # Sample Adjective-Genre Mapping Dictionary (based on previous example)
        self.adjective_genre_mapping = {

            "Excited": ["pop", "dance"],
            "Joyful": ["pop", "indie pop"],
            "Energetic": ["rock", "electronic"],
            "Content": ["chill", "acoustic"],
            "Optimistic": ["pop", "indie pop"],
            "Playful": ["pop", "indie pop"],
            "Grateful": ["chill", "acoustic"],
            "Amused": ["pop", "indie pop"],
            "Carefree": ["pop", "reggae"],

            "Melancholic": ["indie", "folk"],
            "Gloomy": ["alternative", "indie"],
            "Heartbroken": ["indie", "pop"],
            "Lonely": ["indie", "folk"],
            "Despairing": ["alternative", "indie"],
            "Mournful": ["indie", "folk"],
            "Sorrowful": ["indie", "pop"],
            "Depressed": ["alternative", "indie"],
            "Regretful": ["indie", "pop"],

            "Furious": ["metal", "hard rock"],
            "Irritated": ["punk", "alternative"],
            "Enraged": ["metal", "hard rock"],
            "Annoyed": ["punk", "alternative"],
            "Hostile": ["metal", "hard rock"],
            "Frustrated": ["punk", "alternative"],
            "Resentful": ["metal", "hard rock"],
            "Livid": ["punk", "alternative"],
            "Agitated": ["metal", "hard rock"],

            "Terrified": ["ambient", "soundtrack"],
            "Anxious": ["ambient", "soundtrack"],
            "Panicked": ["ambient", "soundtrack"],
            "Nervous": ["ambient", "soundtrack"],
            "Apprehensive": ["ambient", "soundtrack"],
            "Startled": ["ambient", "soundtrack"],
            "Timid": ["ambient", "soundtrack"],
            "Dreadful": ["ambient", "soundtrack"],
            "Jittery": ["ambient", "soundtrack"]        }

        # Define the mapping of adjectives to their numerical values (modify as needed)
        self.adjective_values = {
            "Excited": 8,
            "Joyful": 7,
            "Energetic": 6,
            "Content": 5,
            "Optimistic": 7,
            "Playful": 6,
            "Grateful": 5,
            "Amused": 7,
            "Carefree": 6,

            "Melancholic": 8,
            "Gloomy": 7,
            "Heartbroken": 6,
            "Lonely": 5,
            "Despairing": 7,
            "Mournful": 6,
            "Sorrowful": 5,
            "Depressed": 7,
            "Regretful": 6,

            "Furious": 8,
            "Irritated": 7,
            "Enraged": 6,
            "Annoyed": 5,
            "Hostile": 7,
            "Frustrated": 6,
            "Resentful": 5,
            "Livid": 7,
            "Agitated": 6,

            "Terrified": 8,
            "Anxious": 7,
            "Panicked": 6,
            "Nervous": 5,
            "Apprehensive": 7,
            "Startled": 6,
            "Timid": 5,
            "Dreadful": 7,
            "Jittery": 6
        }
        
        # Get the numerical values of the selected adjectives for the given mood
        self.mood_adjectives = {
            "happy": {
                "adjectives": ["Excited", "Joyful", "Energetic", "Content", "Optimistic", "Playful", "Grateful", "Amused", "Carefree"],
                "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
            },
            "sad": {
                "adjectives": ["Melancholic", "Gloomy", "Heartbroken", "Lonely", "Despairing", "Mournful", "Sorrowful", "Depressed", "Regretful"],
                "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
            },
            "angry": {
                "adjectives": ["Furious", "Irritated", "Enraged", "Annoyed", "Hostile", "Frustrated", "Resentful", "Livid", "Agitated"],
                "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
            },
            "fearful": {
                "adjectives": ["Terrified", "Anxious", "Panicked", "Nervous", "Apprehensive", "Startled", "Timid", "Dreadful", "Jittery"],
                "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
            }
        }
    
    def select_genres_and_artists(self, mood, adjectives):
        if mood not in ["happy", "sad", "angry", "fearful"]:
            return None, None

        if len(adjectives) != 3:
            return None, None

        # Get the adjectives and their numerical values associated with the selected mood
        mood_info = self.mood_adjectives.get(mood)
        if not mood_info:
            return None, None

        selected_adjectives = mood_info["adjectives"]
        adjective_values = mood_info["numerical_values"]

        # Use the adjective-genre mapping to fetch genres based on the adjectives' numerical values
        selected_genres = set()
        for adjective, value in zip(selected_adjectives, adjective_values):
            if adjective in adjectives:
                selected_genres.update(self.adjective_genre_mapping.get(adjective, []))

        # Fetch artists based on the selected genres from the Spotify Web API
        selected_artists = self.fetch_artists_from_spotify(selected_genres)

        return list(selected_genres), selected_artists

    def get_adjective_value(self, adjective):
        return self.adjective_values.get(adjective, 0)

    def fetch_artists_from_spotify(self, genres):
        # Implement the logic to fetch artists based on the selected genres from the Spotify Web API
        # and return a list of artists.

        # For simplicity, let's assume you have a list of artists for each genre in the selected genres
        # Example:
        artists_by_genre = {
            "pop": ["Artist1", "Artist2", "Artist3"],
            "rock": ["Artist4", "Artist5", "Artist6"],
            # ... (artists for other genres)
        }

        artists = []
        for genre in genres:
            if genre in artists_by_genre:
                artists.extend(artists_by_genre[genre])

        return artists

# Example usage:
playlist_generator = PlaylistGenerator()
selected_mood = "happy"
selected_adjectives = ["Excited", "Joyful", "Energetic"]
selected_genres, selected_artists = playlist_generator.select_genres_and_artists(selected_mood, selected_adjectives)

print("Selected Genres:", selected_genres)
print("Selected Artists:", selected_artists)