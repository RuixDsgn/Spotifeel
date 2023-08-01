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

    def select_genres_and_artists(self, mood, adjectives):
        if mood not in ["happy", "sad", "angry", "fearful"]:
            return None, None

        if len(adjectives) != 3:
            return None, None

        # Get the numerical values of the selected adjectives for the given mood
        mood_adjectives = {
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