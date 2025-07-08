#!/usr/bin/env python3
import requests
import json
import unittest
import os
import sys
import random
import uuid
from dotenv import load_dotenv

# Load environment variables from frontend/.env to get the backend URL
load_dotenv('/app/frontend/.env')

# Get the backend URL from environment variables
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL')
if not BACKEND_URL:
    print("Error: REACT_APP_BACKEND_URL not found in environment variables")
    sys.exit(1)

# Ensure the URL ends with /api
API_URL = f"{BACKEND_URL}/api"
print(f"Using API URL: {API_URL}")

class MovieRatingAPITest(unittest.TestCase):
    """Test suite for the Multi-Category Movie Rating API"""

    def setUp(self):
        """Set up test data"""
        # Test movie data
        self.test_movie = {
            "title": "Inception",
            "content_type": "movie",
            "year": 2010,
            "genre": "Sci-Fi",
            "streaming_platform": "Netflix",
            "description": "A thief who steals corporate secrets through the use of dream-sharing technology.",
            "ratings": {
                "story": 9.5,
                "acting": 9.0,
                "direction": 9.8,
                "music_sound": 9.2,
                "cinematography": 9.7,
                "action_stunts": 8.9,
                "emotional_impact": 8.5
            }
        }
        
        # Test TV show data
        self.test_tv_show = {
            "title": "Breaking Bad",
            "content_type": "tv_series",
            "year": 2008,
            "genre": "Drama",
            "streaming_platform": "Netflix",
            "description": "A high school chemistry teacher turned methamphetamine manufacturer.",
            "ratings": {
                "story": 9.8,
                "acting": 9.9,
                "direction": 9.5,
                "music_sound": 8.7,
                "cinematography": 9.3,
                "action_stunts": 8.0,
                "emotional_impact": 9.6
            }
        }
        
        # Edge case: minimum ratings
        self.min_ratings_movie = {
            "title": "Minimum Ratings Test",
            "content_type": "movie",
            "year": 2020,
            "genre": "Test",
            "streaming_platform": "Amazon Prime Video",
            "description": "Testing minimum ratings",
            "ratings": {
                "story": 0,
                "acting": 0,
                "direction": 0,
                "music_sound": 0,
                "cinematography": 0,
                "action_stunts": 0,
                "emotional_impact": 0
            }
        }
        
        # Edge case: maximum ratings
        self.max_ratings_movie = {
            "title": "Maximum Ratings Test",
            "content_type": "movie",
            "year": 2020,
            "genre": "Test",
            "streaming_platform": "HBO Max",
            "description": "Testing maximum ratings",
            "ratings": {
                "story": 10,
                "acting": 10,
                "direction": 10,
                "music_sound": 10,
                "cinematography": 10,
                "action_stunts": 10,
                "emotional_impact": 10
            }
        }
        
        # Store created movie IDs for cleanup
        self.created_movie_ids = []

    def tearDown(self):
        """Clean up created test data"""
        for movie_id in self.created_movie_ids:
            try:
                response = requests.delete(f"{API_URL}/movies/{movie_id}")
                print(f"Deleted test movie with ID: {movie_id}, Status: {response.status_code}")
            except Exception as e:
                print(f"Error deleting test movie {movie_id}: {str(e)}")

    def test_01_root_endpoint(self):
        """Test the root API endpoint"""
        response = requests.get(f"{API_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Multi-Category Movie Rating API")
        print("✅ Root endpoint test passed")

    def test_02_create_movie(self):
        """Test creating a new movie"""
        response = requests.post(f"{API_URL}/movies", json=self.test_movie)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify response data
        self.assertEqual(data["title"], self.test_movie["title"])
        self.assertEqual(data["content_type"], self.test_movie["content_type"])
        self.assertEqual(data["year"], self.test_movie["year"])
        self.assertEqual(data["genre"], self.test_movie["genre"])
        self.assertEqual(data["streaming_platform"], self.test_movie["streaming_platform"])
        self.assertEqual(data["description"], self.test_movie["description"])
        
        # Verify ratings
        for category in self.test_movie["ratings"]:
            self.assertEqual(data["ratings"][category], self.test_movie["ratings"][category])
        
        # Verify overall rating calculation
        expected_overall = sum(self.test_movie["ratings"].values()) / 7
        expected_overall = round(expected_overall, 1)
        self.assertEqual(data["overall_rating"], expected_overall)
        
        # Save ID for later tests and cleanup
        self.created_movie_ids.append(data["id"])
        self.test_movie_id = data["id"]
        
        print("✅ Create movie test passed")
        return data["id"]

    def test_03_create_tv_show(self):
        """Test creating a new TV show"""
        response = requests.post(f"{API_URL}/movies", json=self.test_tv_show)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify response data
        self.assertEqual(data["title"], self.test_tv_show["title"])
        self.assertEqual(data["content_type"], self.test_tv_show["content_type"])
        
        # Save ID for later tests and cleanup
        self.created_movie_ids.append(data["id"])
        self.test_tv_show_id = data["id"]
        
        print("✅ Create TV show test passed")
        return data["id"]

    def test_04_create_min_ratings(self):
        """Test creating a movie with minimum ratings (0)"""
        response = requests.post(f"{API_URL}/movies", json=self.min_ratings_movie)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify all ratings are 0
        for category, rating in data["ratings"].items():
            self.assertEqual(rating, 0)
        
        # Verify overall rating is 0
        self.assertEqual(data["overall_rating"], 0)
        
        # Save ID for cleanup
        self.created_movie_ids.append(data["id"])
        
        print("✅ Create movie with minimum ratings test passed")

    def test_05_create_max_ratings(self):
        """Test creating a movie with maximum ratings (10)"""
        response = requests.post(f"{API_URL}/movies", json=self.max_ratings_movie)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify all ratings are 10
        for category, rating in data["ratings"].items():
            self.assertEqual(rating, 10)
        
        # Verify overall rating is 10
        self.assertEqual(data["overall_rating"], 10)
        
        # Save ID for cleanup
        self.created_movie_ids.append(data["id"])
        
        print("✅ Create movie with maximum ratings test passed")

    def test_06_create_invalid_rating(self):
        """Test creating a movie with invalid rating (above 10)"""
        invalid_movie = self.test_movie.copy()
        invalid_movie["ratings"] = {
            "story": 11,  # Invalid: above 10
            "acting": 9.0,
            "direction": 9.8,
            "music_sound": 9.2,
            "cinematography": 9.7,
            "action_stunts": 8.9,
            "emotional_impact": 8.5
        }
        
        response = requests.post(f"{API_URL}/movies", json=invalid_movie)
        self.assertEqual(response.status_code, 422)  # Validation error
        
        print("✅ Create movie with invalid rating test passed")

    def test_07_get_all_movies(self):
        """Test getting all movies"""
        # First create a movie to ensure there's data
        self.test_02_create_movie()
        
        response = requests.get(f"{API_URL}/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify we got a list of movies
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        print("✅ Get all movies test passed")

    def test_08_filter_by_platform(self):
        """Test filtering movies by platform"""
        # Create movies on different platforms
        netflix_movie = self.test_movie.copy()
        netflix_movie["streaming_platform"] = "Netflix"
        
        amazon_movie = self.test_movie.copy()
        amazon_movie["title"] = "The Boys"
        amazon_movie["streaming_platform"] = "Amazon Prime Video"
        
        # Create the movies
        response1 = requests.post(f"{API_URL}/movies", json=netflix_movie)
        self.assertEqual(response1.status_code, 200)
        self.created_movie_ids.append(response1.json()["id"])
        
        response2 = requests.post(f"{API_URL}/movies", json=amazon_movie)
        self.assertEqual(response2.status_code, 200)
        self.created_movie_ids.append(response2.json()["id"])
        
        # Test filtering by Netflix
        response = requests.get(f"{API_URL}/movies?platform=Netflix")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # All returned movies should be on Netflix
        for movie in data:
            self.assertEqual(movie["streaming_platform"], "Netflix")
        
        # Test filtering by Amazon Prime
        response = requests.get(f"{API_URL}/movies?platform=Amazon%20Prime%20Video")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # All returned movies should be on Amazon Prime
        for movie in data:
            self.assertEqual(movie["streaming_platform"], "Amazon Prime Video")
        
        print("✅ Filter by platform test passed")

    def test_09_filter_by_content_type(self):
        """Test filtering by content type (movie vs TV series)"""
        # Create both a movie and TV show
        movie_id = self.test_02_create_movie()
        tv_show_id = self.test_03_create_tv_show()
        
        # Test filtering by movie
        response = requests.get(f"{API_URL}/movies?content_type=movie")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # All returned items should be movies
        for item in data:
            self.assertEqual(item["content_type"], "movie")
        
        # Test filtering by TV series
        response = requests.get(f"{API_URL}/movies?content_type=tv_series")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # All returned items should be TV series
        for item in data:
            self.assertEqual(item["content_type"], "tv_series")
        
        print("✅ Filter by content type test passed")

    def test_10_get_movie_by_id(self):
        """Test getting a specific movie by ID"""
        # First create a movie
        movie_id = self.test_02_create_movie()
        
        # Get the movie by ID
        response = requests.get(f"{API_URL}/movies/{movie_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify it's the correct movie
        self.assertEqual(data["id"], movie_id)
        self.assertEqual(data["title"], self.test_movie["title"])
        
        print("✅ Get movie by ID test passed")

    def test_11_get_nonexistent_movie(self):
        """Test getting a movie that doesn't exist"""
        fake_id = str(uuid.uuid4())
        response = requests.get(f"{API_URL}/movies/{fake_id}")
        self.assertEqual(response.status_code, 404)
        
        print("✅ Get nonexistent movie test passed")

    def test_12_update_movie(self):
        """Test updating a movie"""
        # First create a movie
        movie_id = self.test_02_create_movie()
        
        # Update data
        update_data = {
            "title": "Inception (Updated)",
            "year": 2011,
            "ratings": {
                "story": 9.0,
                "acting": 8.5,
                "direction": 9.3,
                "music_sound": 8.8,
                "cinematography": 9.2,
                "action_stunts": 8.4,
                "emotional_impact": 8.0
            }
        }
        
        # Update the movie
        response = requests.put(f"{API_URL}/movies/{movie_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify the updates
        self.assertEqual(data["title"], update_data["title"])
        self.assertEqual(data["year"], update_data["year"])
        
        # Verify ratings were updated
        for category in update_data["ratings"]:
            self.assertEqual(data["ratings"][category], update_data["ratings"][category])
        
        # Verify overall rating was recalculated
        expected_overall = sum(update_data["ratings"].values()) / 7
        expected_overall = round(expected_overall, 1)
        self.assertEqual(data["overall_rating"], expected_overall)
        
        print("✅ Update movie test passed")

    def test_13_update_nonexistent_movie(self):
        """Test updating a movie that doesn't exist"""
        fake_id = str(uuid.uuid4())
        update_data = {"title": "This movie doesn't exist"}
        
        response = requests.put(f"{API_URL}/movies/{fake_id}", json=update_data)
        self.assertEqual(response.status_code, 404)
        
        print("✅ Update nonexistent movie test passed")

    def test_14_delete_movie(self):
        """Test deleting a movie"""
        # First create a movie
        response = requests.post(f"{API_URL}/movies", json=self.test_movie)
        self.assertEqual(response.status_code, 200)
        movie_id = response.json()["id"]
        
        # Delete the movie
        response = requests.delete(f"{API_URL}/movies/{movie_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Movie deleted successfully")
        
        # Verify it's gone
        response = requests.get(f"{API_URL}/movies/{movie_id}")
        self.assertEqual(response.status_code, 404)
        
        # Remove from cleanup list since we already deleted it
        if movie_id in self.created_movie_ids:
            self.created_movie_ids.remove(movie_id)
        
        print("✅ Delete movie test passed")

    def test_15_delete_nonexistent_movie(self):
        """Test deleting a movie that doesn't exist"""
        fake_id = str(uuid.uuid4())
        response = requests.delete(f"{API_URL}/movies/{fake_id}")
        self.assertEqual(response.status_code, 404)
        
        print("✅ Delete nonexistent movie test passed")

    def test_16_get_platforms(self):
        """Test getting available streaming platforms"""
        response = requests.get(f"{API_URL}/platforms")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify we got a list of platforms
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Verify expected platforms are in the list
        expected_platforms = [
            "Netflix", "Amazon Prime Video", "Disney+ Hotstar", 
            "Hulu", "HBO Max", "Apple TV+", "Paramount+", 
            "YouTube", "Other"
        ]
        
        for platform in expected_platforms:
            self.assertIn(platform, data)
        
        print("✅ Get platforms test passed")

    def test_17_get_stats(self):
        """Test getting database statistics"""
        # First create both a movie and TV show to ensure there's data
        self.test_02_create_movie()
        self.test_03_create_tv_show()
        
        response = requests.get(f"{API_URL}/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify the stats structure
        self.assertIn("total_movies", data)
        self.assertIn("total_tv_shows", data)
        self.assertIn("total_content", data)
        self.assertIn("platform_distribution", data)
        
        # Verify the math
        self.assertEqual(data["total_content"], data["total_movies"] + data["total_tv_shows"])
        
        # Verify platform distribution
        self.assertIsInstance(data["platform_distribution"], list)
        
        print("✅ Get stats test passed")

if __name__ == "__main__":
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)