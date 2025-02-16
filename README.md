# NASA Rasa
This repository contains a Rasa-powered chatbot focused on astronomical information and interactions with NASA data. The bot offers multiple scenarios, including looking up daily astronomy photos, fetching near-Earth objects, retrieving Mars rover images, and a mock “largest moon” Q&A.

## 1. Domain & Motivation

### Domain

Astronomy & Space Exploration. The chatbot helps users explore data from NASA and learn about the solar system in a conversational way.

### Motivation
* Space exploration and astronomy is a core interest of mine.
* NASA provides public APIs that are straightforward to consume, making it ideal for demonstrating real-time data integration.
* Users can query up-to-date astronomy pictures, near-Earth object information, and Mars rover images, which keeps the chatbot content fresh.

---

## 2. Implemented Scenarios

This bot implements **four** main scenarios to demonstrate its capabilities:

1. **Astronomy Picture of the Day (APOD)**
   - Users can ask: “Show me NASA’s picture of the day.”
   - The bot calls the NASA APOD API and returns the image link and a brief explanation.

2. **Near-Earth Objects (Asteroids) Lookup**
   - Users can query: “Are there any asteroids passing near Earth today?” or provide a date.
   - The bot integrates with NASA’s NEO API to fetch details on asteroids for a given day.

3. **Mars Rover Images**
   - Users say: “Show me the latest photos from Curiosity (or Perseverance).”
   - The bot queries the NASA Mars Rover Photos API, returning a single recent photo.

4. **Mock (Largest Moon)**
   - Demonstrates a placeholder action (“What’s the largest moon in the solar system?”).
   - The bot replies with a hard-coded message about Ganymede.

These scenarios illustrate both **real-time data fetching** (NASA) and a **mock** scenario for testing or demonstration.

---

## 3. Integrated Data Sources & Rationale

1. **NASA APOD API**
   - Endpoint: `https://api.nasa.gov/planetary/apod?api_key=YOUR_KEY`
   - Rationale: Delivers fascinating daily images and explanations, perfect for showcasing a dynamic chatbot.

2. **NASA NEO (Near-Earth Objects) API**
   - Endpoint: `https://api.nasa.gov/neo/rest/v1/feed?start_date=...&end_date=...&api_key=YOUR_KEY`
   - Rationale: Real-time asteroid data is interesting and timely.

3. **NASA Mars Rover Photos**
   - Endpoint: `https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/latest_photos?api_key=YOUR_KEY`
   - Rationale: Users can see rover images from Curiosity or Perseverance in near real-time.

4. **Largest Moon (Mock Action)**
   - No external API, just a hard-coded answer.
   - Demonstrates how to simulate a task or placeholder logic in Rasa before real integration.

---

## 4. Challenges & How They Were Addressed

1. **Slot Mapping in Rasa 3.x**
   - Problem: Must provide `mappings:` for each slot in `domain.yml`.
   - Solution: Used minimal mappings like `from_text`, `from_entity`, or `custom` to satisfy Rasa validation.

2. **Intent Overlap (One-word answers)**
   - Problem: Single words like “earth” or “mars” confused the bot between NASA calls and other intents.
   - Solution: Added more training data as examples of each intent.

3. **Date Interpretation**
   - Problem: Writing e.g. 'January 7th' instead of 2025-01-07 (the ISO-format) is not always correctly interpreted by the bot.
   - Solution: More examples of what a date can look like as well as a hard-coded interpretation of 'today'.

4. **Domain & Rules Validation**
   - Problem: Rasa 3.x changed domain/rule schemas, requiring precise YAML structure.
   - Solution: Carefully separated `stories.yml` vs. `rules.yml` and used the new `slot_was_set` condition.

---

## 5. Setup & Credentials

### Clone & Install
```bash
git clone https://github.com/yourusername/nasarasa.git
```
### NASA API Keys
1. Get a free API key from https://api.nasa.gov.
2. Store it in a .env or environment variable. Example:
   ```bash
   export NASA_API_KEY="YOUR_NASA_KEY"
   ```
3. The code in actions.py references NASA_API_KEY. Alternatively, you can hard-code it.

## 6. Example runs
### 6.1 NASA Astronomy Picture of the Day
```bash
Your input -> Show me NASA’s picture
Bot -> “**Parhelia at Abisko** ... See more: https://apod.nasa.gov/apod/...” 
```
### 6.2 Near-Earth Objects
