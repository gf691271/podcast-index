import csv
import os
from dotenv import load_dotenv
import podcastindex
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()

# Initialize the podcast index
config = {"api_key": os.getenv("API_KEY"), "api_secret": os.getenv("API_SECRET")}
index = podcastindex.init(config)

# Define the search terms and the output CSV file
search_terms = ["汽车", "electric car", "electric vehicle"]  # replace with your search terms
output_file = "data/file.csv"  # replace with the path to your CSV file

# Prepare the data for the CSV file
data = []

# Iterate over the search terms
for search_term in search_terms:
    # Search for podcasts
    result = index.search(search_term)

    # Iterate over the podcasts
    for podcast in tqdm(result["feeds"], desc=f"Processing podcasts for {search_term}"):
        # Get the episodes of the podcast
        episodes = index.episodesByFeedId(podcast["id"], max_results=1000)

        # Iterate over the episodes
        for episode in tqdm(
            episodes["items"], desc=f"Processing episodes for {podcast['title']}"
        ):
            # if episode time is > 2022.7.1
            if episode["datePublished"] > 1656633600:
                # Add the episode data to the list
                data.append(
                    {
                        "search_term": search_term,
                        "podcast_id": podcast["id"],
                        "podcast_title": podcast["title"],
                        "episode_id": episode["id"],
                        "episode_time": episode["datePublishedPretty"],
                        "episode_timestamp": episode["datePublished"],
                        "episode_title": episode["title"],
                        "episode_description": episode["description"],
                        "audio_url": episode["enclosureUrl"],
                        "audio_type": episode["enclosureType"],
                        "audio_transcript": episode["transcriptUrl"],
                        "feed_language": episode["feedLanguage"],
                    }
                )

# Write the data to the CSV file
with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

print(f"Saved search results to {output_file}")
