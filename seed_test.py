#!/usr/bin/env python3
import requests
import json
import unittest
import os
import sys
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

class SeedDataTest(unittest.TestCase):
    """Test suite for the Seed Data functionality"""

    def setUp(self):
        """Set up test data"""
        # Clear the database before testing seed functionality
        self.clear_database()
    
    def clear_database(self):
        """Helper method to clear the database"""
        # Get all movies
        response = requests.get(f"{API_URL}/movies")
        if response.status_code == 200:
            movies = response.json()
            # Delete each movie
            for movie in movies:
                movie_id = movie["id"]
                delete_response = requests.delete(f"{API_URL}/movies/{movie_id}")
                if delete_response.status_code != 200:
                    print(f"Warning: Failed to delete movie {movie_id}")
        else:
            print(f"Warning: Failed to get movies for cleanup, status: {response.status_code}")

    def test_01_empty_database_state(self):
        """Test that the database is empty before seeding"""
        response = requests.get(f"{API_URL}/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0, "Database should be empty before seeding")
        print("✅ Empty database state test passed")

    def test_02_seed_endpoint(self):
        """Test the seed endpoint"""
        response = requests.post(f"{API_URL}/seed")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("Successfully seeded database with 12 movies and TV shows", data["message"])
        print("✅ Seed endpoint test passed")

    def test_03_seed_content_count(self):
        """Test that the seed endpoint populates the database with 12 items"""
        # Get all movies after seeding
        response = requests.get(f"{API_URL}/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 12, "Database should contain 12 items after seeding")
        print("✅ Seed content count test passed")

    def test_04_seed_content_platforms(self):
        """Test that the seed data includes content from Netflix and Amazon Prime Video"""
        response = requests.get(f"{API_URL}/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Count items by platform
        platforms = {}
        for item in data:
            platform = item["streaming_platform"]
            platforms[platform] = platforms.get(platform, 0) + 1
        
        # Verify Netflix and Amazon Prime Video content
        self.assertIn("Netflix", platforms, "Seed data should include Netflix content")
        self.assertIn("Amazon Prime Video", platforms, "Seed data should include Amazon Prime Video content")
        self.assertEqual(platforms["Netflix"], 6, "Should have 6 Netflix items")
        self.assertEqual(platforms["Amazon Prime Video"], 6, "Should have 6 Amazon Prime Video items")
        print("✅ Seed content platforms test passed")

    def test_05_seed_content_types(self):
        """Test that the seed data includes both movies and TV shows"""
        response = requests.get(f"{API_URL}/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Count items by content type
        content_types = {}
        for item in data:
            content_type = item["content_type"]
            content_types[content_type] = content_types.get(content_type, 0) + 1
        
        # Verify movies and TV shows
        self.assertIn("movie", content_types, "Seed data should include movies")
        self.assertIn("tv_series", content_types, "Seed data should include TV series")
        self.assertEqual(content_types["movie"], 6, "Should have 6 movies")
        self.assertEqual(content_types["tv_series"], 6, "Should have 6 TV series")
        print("✅ Seed content types test passed")

    def test_06_seed_specific_content(self):
        """Test that the seed data includes specific popular content"""
        response = requests.get(f"{API_URL}/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Create a list of titles
        titles = [item["title"] for item in data]
        
        # Verify Netflix movies
        self.assertIn("The Irishman", titles, "Seed data should include The Irishman")
        self.assertIn("Roma", titles, "Seed data should include Roma")
        self.assertIn("Extraction", titles, "Seed data should include Extraction")
        
        # Verify Netflix TV shows
        self.assertIn("Stranger Things", titles, "Seed data should include Stranger Things")
        self.assertIn("The Crown", titles, "Seed data should include The Crown")
        self.assertIn("Squid Game", titles, "Seed data should include Squid Game")
        
        # Verify Amazon Prime movies
        self.assertIn("The Tomorrow War", titles, "Seed data should include The Tomorrow War")
        self.assertIn("Sound of Metal", titles, "Seed data should include Sound of Metal")
        self.assertIn("The Big Sick", titles, "Seed data should include The Big Sick")
        
        # Verify Amazon Prime TV shows
        self.assertIn("The Boys", titles, "Seed data should include The Boys")
        self.assertIn("The Marvelous Mrs. Maisel", titles, "Seed data should include The Marvelous Mrs. Maisel")
        self.assertIn("Invincible", titles, "Seed data should include Invincible")
        
        print("✅ Seed specific content test passed")

    def test_07_seed_rating_categories(self):
        """Test that all 7 rating categories are properly filled for each item"""
        response = requests.get(f"{API_URL}/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check each item has all 7 rating categories
        for item in data:
            ratings = item["ratings"]
            self.assertIn("story", ratings)
            self.assertIn("acting", ratings)
            self.assertIn("direction", ratings)
            self.assertIn("music_sound", ratings)
            self.assertIn("cinematography", ratings)
            self.assertIn("action_stunts", ratings)
            self.assertIn("emotional_impact", ratings)
            
            # Verify all ratings are within valid range (0-10)
            for category, rating in ratings.items():
                self.assertGreaterEqual(rating, 0, f"{category} rating should be >= 0")
                self.assertLessEqual(rating, 10, f"{category} rating should be <= 10")
        
        print("✅ Seed rating categories test passed")

    def test_08_seed_overall_rating_calculation(self):
        """Test that overall ratings are calculated correctly"""
        response = requests.get(f"{API_URL}/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check each item's overall rating
        for item in data:
            ratings = item["ratings"]
            # Calculate expected overall rating
            expected_overall = sum(ratings.values()) / 7
            expected_overall = round(expected_overall, 1)
            # Verify overall rating
            self.assertEqual(item["overall_rating"], expected_overall, 
                            f"Overall rating for {item['title']} should be {expected_overall}")
        
        print("✅ Seed overall rating calculation test passed")

    def test_09_seed_idempotence(self):
        """Test that calling the seed endpoint multiple times doesn't duplicate data"""
        # Call seed endpoint again
        response = requests.post(f"{API_URL}/seed")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("Database already contains", data["message"])
        
        # Verify count is still 12
        response = requests.get(f"{API_URL}/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 12, "Database should still contain 12 items after second seed call")
        
        print("✅ Seed idempotence test passed")

    def test_10_filter_by_platform(self):
        """Test filtering seeded content by platform"""
        # Test Netflix filter
        response = requests.get(f"{API_URL}/movies?platform=Netflix")
        self.assertEqual(response.status_code, 200)
        netflix_data = response.json()
        self.assertEqual(len(netflix_data), 6, "Should have 6 Netflix items")
        
        # Test Amazon Prime Video filter
        response = requests.get(f"{API_URL}/movies?platform=Amazon%20Prime%20Video")
        self.assertEqual(response.status_code, 200)
        amazon_data = response.json()
        self.assertEqual(len(amazon_data), 6, "Should have 6 Amazon Prime Video items")
        
        print("✅ Filter by platform test passed")

    def test_11_filter_by_content_type(self):
        """Test filtering seeded content by content type"""
        # Test movie filter
        response = requests.get(f"{API_URL}/movies?content_type=movie")
        self.assertEqual(response.status_code, 200)
        movie_data = response.json()
        self.assertEqual(len(movie_data), 6, "Should have 6 movies")
        
        # Test TV series filter
        response = requests.get(f"{API_URL}/movies?content_type=tv_series")
        self.assertEqual(response.status_code, 200)
        tv_data = response.json()
        self.assertEqual(len(tv_data), 6, "Should have 6 TV series")
        
        print("✅ Filter by content type test passed")

    def test_12_combined_filters(self):
        """Test combining platform and content type filters"""
        # Test Netflix movies
        response = requests.get(f"{API_URL}/movies?platform=Netflix&content_type=movie")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3, "Should have 3 Netflix movies")
        
        # Test Netflix TV series
        response = requests.get(f"{API_URL}/movies?platform=Netflix&content_type=tv_series")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3, "Should have 3 Netflix TV series")
        
        # Test Amazon Prime movies
        response = requests.get(f"{API_URL}/movies?platform=Amazon%20Prime%20Video&content_type=movie")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3, "Should have 3 Amazon Prime movies")
        
        # Test Amazon Prime TV series
        response = requests.get(f"{API_URL}/movies?platform=Amazon%20Prime%20Video&content_type=tv_series")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3, "Should have 3 Amazon Prime TV series")
        
        print("✅ Combined filters test passed")

if __name__ == "__main__":
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)