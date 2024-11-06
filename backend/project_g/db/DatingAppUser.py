from typing import List
from enum import Enum
from datetime import datetime
from __future__ import annotations

class DatingApp(Enum):
    BUMBLE = 'bumble'
    TINDER = 'tinder'

class Gender(Enum):
    MAN = 'man'
    WOMAN = 'woman'
    NON_BINARY = 'non binary'
    OTHER = 'other'

class Prompt:
    def __init__(self, question: str, answer: str):  
        self.question = question
        self.answer = answer

class DatingAppUser:
    def __init__(self):
        self.name: str = ""
        self.age: int = None
        self.profession: str = ""
        self.education: str = ""
        self.height: str = ""
        self.physical_activity_frequency: str = "" 
        self.education_level: str = ""
        self.drinking_frequency: str = ""
        self.smoking_frequency: str = ""
        self.gender: str = ""
        self.weed_smoking_frequency: str = ""
        self.relationship_type: str = ""
        self.relationship_goals = ""
        self.family_plans: str = ""
        self.star_sign: str = ""
        self.political_leaning: str = ""
        self.religion: str = ""
        self.current_location: str = ""
        self.dating_app: str = ""
        self.top_spotify_artists: List[str] = []
        self.anthem: str = ""
        self.interests: List[str] = []
        self.pets: str = ""
        self.communication_style: str = ""
        self.love_language: str = ""
        self.sleeping_habits: str = ""
        self.dietary_preference: str = ""
        self.bio: str = ""
        self.home_town = ""
        self.time_scraped: datetime = None
        self.prompts: List[Prompt] = []
        self.residential_location = ""
        self.vaccination_status = ""
        self.languages = []
        self.personality_type = ""

# Builder class. Build a user piece by piece or without some pieces
class DatingAppUserBuilder:
    def __init__(self, dating_app:str):
        self.user = DatingAppUser()
        self.user.dating_app = dating_app
        self.user.time_scraped = datetime.now()

    def with_name(self, name: str) -> DatingAppUserBuilder:
        self.user.name = name.strip()
        return self

    def with_age(self, age: int) -> DatingAppUserBuilder:
        self.user.age = age
        return self
    
    def with_height(self, height: str) -> DatingAppUserBuilder:
        self.user.height = height

    def with_profession(self, profession: str) -> DatingAppUserBuilder:
        if profession: self.user.profession = profession
        return self

    def with_location(self, current_location: str, residential_location: str, home_town: str) -> DatingAppUserBuilder:
        if current_location: self.current_location = current_location
        if residential_location: self.residential_location = residential_location
        if home_town: self.home_town = home_town
        return self

    def add_prompt(self, question: str, answer: str) -> DatingAppUserBuilder:
        prompt = Prompt(question, answer)
        self.user.prompts.append(prompt)
        return self
    
    def with_freqeuncies(self, 
                        physical_activity_frequency,
                        drinking_frequency,
                        smoking_frequency, 
                        weed_smoking_frequency) -> DatingAppUserBuilder:

        if physical_activity_frequency: self.user.physical_activity_frequency = physical_activity_frequency
        if drinking_frequency: self.user.drinking_frequency = drinking_frequency
        if smoking_frequency: self.user.smoking_frequency = smoking_frequency
        if weed_smoking_frequency: self.user.weed_smoking_frequency = weed_smoking_frequency
        return self

    def add_spotify_artist(self, artist) -> DatingAppUserBuilder:
        if artist: self.user.top_spotify_artists.append(artist)
        return self
    
    def with_anthem(self, anthem: str) -> DatingAppUserBuilder:
        if anthem: self.user.anthem = anthem
        return self

    def build(self) -> DatingAppUser:
        if not self.user.name or self.user.age:
            raise ValueError("Name and Age are required")
        return self.user


