# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
import datetime

class ActionLargestMoon(Action):
    def name(self) -> Text:
        return "action_largest_moon"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # This is a mock/hard-coded response
        dispatcher.utter_message(text="The largest moon in the solar system is Ganymede, which orbits Jupiter. It’s even bigger than Mercury!")
        return []

NASA_API_KEY = "INSERT YOUR NASA API"  # store securely, e.g., in an .env file

class ActionFetchNasaApod(Action):
    def name(self) -> Text:
        return "action_fetch_nasa_apod"

    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # First, check the user's actual message.
        user_message = tracker.latest_message.get("text", "").lower()

        if "today" in user_message:
            query_date = datetime.date.today().isoformat()  # e.g. '2025-02-16'
        else:
            # Otherwise, fall back to any date slot if set
            query_date = tracker.get_slot("query_date")

            # If there's still no slot value, default to today's date
            if not query_date:
                query_date = datetime.date.today().isoformat()
        
        if query_date:
            url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={query_date}"
        else:
            url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            title = data.get("title", "No Title")
            explanation = data.get("explanation", "No description available.")
            image_url = data.get("url", "")

            msg = f"**{title}**\n{explanation[:400]}...\nSee more: {image_url}"
            dispatcher.utter_message(text=msg)
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Sorry, I couldn't fetch today's NASA image.")
            print(f"NASA APOD Error: {e}")
        
        return []

class ActionFetchNeoInfo(Action):
    def name(self) -> Text:
        return "action_fetch_neo_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # First, check the user's actual message.
        user_message = tracker.latest_message.get("text", "").lower()

        # If user typed "today", we set query_date to the real current date.
        if "today" in user_message:
            query_date = datetime.date.today().isoformat()  # e.g. '2025-02-16'
        else:
            # Otherwise, fall back to any date slot if set
            query_date = tracker.get_slot("query_date")

            # If there's still no slot value, default to today's date
            if not query_date:
                query_date = datetime.date.today().isoformat()

        url = (
            f"https://api.nasa.gov/neo/rest/v1/feed"
            f"?start_date={query_date}&end_date={query_date}&api_key={NASA_API_KEY}"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            neos = data["near_earth_objects"].get(query_date, [])
            if not neos:
                dispatcher.utter_message(text=f"No near-Earth objects found for {query_date}.")
                # Reset the slot so next time we ask for a fresh date
                return [SlotSet("query_date", None)]

            # Show the first one or a short summary:
            first_neo = neos[0]
            name = first_neo["name"]
            diameter_est = first_neo["estimated_diameter"]["meters"]["estimated_diameter_max"]
            hazard = first_neo["is_potentially_hazardous_asteroid"]

            msg = (
                f"On {query_date}, one NEObject is '{name}', diameter ~{diameter_est:.2f} m.\n"
                f"Potentially hazardous? {'Yes' if hazard else 'No'}.\n"
                "Source: NASA’s NEO API."
            )
            dispatcher.utter_message(text=msg)

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Sorry, couldn't fetch NEO info right now.")
            print(f"NASA NEO Error: {e}")

        # Reset the slot after responding, so we don't keep using the same date next time.
        return [SlotSet("query_date", None)]


class ActionFetchMarsPhotos(Action):
    def name(self) -> Text:
        return "action_fetch_mars_photos"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # Grab rover name from a slot or default to "curiosity"
        rover_name = tracker.get_slot("rover_name") or "curiosity"
        rover_name = rover_name.lower()

        # Limit the rover selection to only Curiosity or Perseverance
        if rover_name not in ["curiosity", "perseverance"]:
            dispatcher.utter_message(
                text=(
                    f"Currently, I only handle Curiosity or Perseverance. "
                    f"You asked for '{rover_name}'. Please try again."
                )
            )
            return []

        # Build the NASA URL
        url = (
            f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/latest_photos"
            f"?api_key={NASA_API_KEY}"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            latest_photos = data.get("latest_photos", [])
            if not latest_photos:
                dispatcher.utter_message(
                    text=f"I couldn't find recent photos for rover '{rover_name.title()}'."
                )
                return []

            # Return only the first photo
            first_photo = latest_photos[0]
            img_url = first_photo["img_src"]
            camera_name = first_photo["camera"]["full_name"]
            earth_date = first_photo["earth_date"]

            msg = (
                f"Here’s the latest photo from rover '{rover_name.title()}'!\n\n"
                f"Camera: {camera_name}\n"
                f"Earth Date: {earth_date}\n"
                f"Photo URL: {img_url}"
            )
            dispatcher.utter_message(text=msg)

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Sorry, couldn't fetch Mars rover photos.")
            print(f"NASA Mars Error: {e}")

        return []
