import os
import openai
import json
import datetime
from dotenv import load_dotenv
from cachetools import TTLCache


client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY')) # This is the OpenAI API client

class ChatGPTClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def ask_question(self, question):
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=question,
            max_tokens=150
        )
        return response.choices[0].text.strip()

class HoroscopeService:
    def __init__(self):
        # Cache clear every 7 days and starts storning from sunday
        self.horoscope_cache = TTLCache(maxsize=100, ttl=604800)
        self.match_cache = TTLCache(maxsize=100, ttl=604800)


    def get_horoscope(self, birthdate: str):
        """Fetches horoscope details for the given birthdate."""
        
        # get week number of the year for the current date
        current_week = datetime.datetime.now().isocalendar()[1]

        # Create a unique cache key based on birthdate and year
        cache_key = f"{birthdate}-{current_week}"

        if cache_key in self.horoscope_cache:
            return self.horoscope_cache[cache_key]

        question = (
            "You are an expert astrologer with deep knowledge of Western, Indian (Vedic), and Chinese astrology. "
            "Generate a structured JSON response for the birthdate {birthdate}, considering their birth year ({birth_year}). "
            "Your response must include:\n"
            "1. 'indian_sign': The Indian zodiac sign based on Vedic astrology.\n"
            "2. 'western_sign': The Western zodiac sign.\n"
            "3. 'chinese_sign': The corresponding Chinese zodiac animal for the **birth year ({birth_year})**.\n"
            "4. 'horoscope': A well-researched, unified single weekly horoscope based on insights from Indian, Western, and Chinese astrology for {current_date}.\n"
            "Ensure the response is in valid JSON format without extra explanation."
        ).format(birthdate=birthdate, birth_year=birthdate[:4], current_date=current_date)

        try:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an expert astrologer."},
                  {"role": "user", "content": question}],
            max_tokens=300,
            temperature=0.7
            )
            #print the response and response type
            print(response)
            print(type(response))
            result = response.choices[0].message.content
            self.horoscope_cache[cache_key] = result 
            return result
        except Exception as e:
            return {"error": f"Failed to generate horoscope: {str(e)}"}

    def get_astrology_matches(self, birthdate: str):
            """Fetches famous people who match the astrology profile (Western + Chinese)."""
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")

            # Create a unique cache key based on birthdate and date of request
            cache_key = f"{birthdate}-{current_date}"

            if cache_key in self.match_cache:
                return self.match_cache[cache_key]

            prompt = (
                f"Find one famous Notable individual and fictional character"
                f"who share the same astrology as someone born on {birthdate}. "
                f"Return JSON with keys: 'Notable individual' (name & area_of_expertice), 'fictional_charactor' (name & show/movie/anime)"
                
            )

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert in astrology, sports, anime, and famous thinkers."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )

                result = response.choices[0].message.content

                # Store result in cache
                self.match_cache[cache_key] = result
                return result

            except Exception as e:
                return {"error": f"Failed to fetch astrology matches: {str(e)}"}


        

    

