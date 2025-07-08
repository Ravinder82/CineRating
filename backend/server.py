from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uuid
from datetime import datetime
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enums
class ContentType(str, Enum):
    MOVIE = "movie"
    TV_SERIES = "tv_series"

class StreamingPlatform(str, Enum):
    NETFLIX = "Netflix"
    AMAZON_PRIME = "Amazon Prime Video"
    HOTSTAR = "Disney+ Hotstar"
    HULU = "Hulu"
    HBO_MAX = "HBO Max"
    APPLE_TV = "Apple TV+"
    PARAMOUNT = "Paramount+"
    YOUTUBE = "YouTube"
    OTHER = "Other"

# Models
class RatingCategories(BaseModel):
    story: float = Field(..., ge=0, le=10, description="Story rating (0-10)")
    acting: float = Field(..., ge=0, le=10, description="Acting rating (0-10)")
    direction: float = Field(..., ge=0, le=10, description="Direction rating (0-10)")
    music_sound: float = Field(..., ge=0, le=10, description="Music & Sound rating (0-10)")
    cinematography: float = Field(..., ge=0, le=10, description="Cinematography rating (0-10)")
    action_stunts: float = Field(..., ge=0, le=10, description="Action & Stunts rating (0-10)")
    emotional_impact: float = Field(..., ge=0, le=10, description="Emotional Impact rating (0-10)")

class MovieTVShow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, max_length=200)
    content_type: ContentType
    year: int = Field(..., ge=1900, le=2030)
    genre: str = Field(..., min_length=1, max_length=100)
    streaming_platform: StreamingPlatform
    description: Optional[str] = Field(None, max_length=1000)
    ratings: RatingCategories
    overall_rating: float = Field(..., ge=0, le=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MovieTVShowCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content_type: ContentType
    year: int = Field(..., ge=1900, le=2030)
    genre: str = Field(..., min_length=1, max_length=100)
    streaming_platform: StreamingPlatform
    description: Optional[str] = Field(None, max_length=1000)
    ratings: RatingCategories

class MovieTVShowUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content_type: Optional[ContentType] = None
    year: Optional[int] = Field(None, ge=1900, le=2030)
    genre: Optional[str] = Field(None, min_length=1, max_length=100)
    streaming_platform: Optional[StreamingPlatform] = None
    description: Optional[str] = Field(None, max_length=1000)
    ratings: Optional[RatingCategories] = None

# Helper function to calculate overall rating
def calculate_overall_rating(ratings: RatingCategories) -> float:
    """Calculate overall rating as average of all category ratings"""
    total = (ratings.story + ratings.acting + ratings.direction + 
             ratings.music_sound + ratings.cinematography + 
             ratings.action_stunts + ratings.emotional_impact)
    return round(total / 7, 1)

# Seed Data - Popular Movies and TV Shows
SEED_DATA = [
    # Netflix Movies
    {
        "title": "The Irishman",
        "content_type": "movie",
        "year": 2019,
        "genre": "Crime/Drama",
        "streaming_platform": "Netflix",
        "description": "A truck driver becomes a hitman and gets involved with the mob, spanning decades of American history.",
        "ratings": {
            "story": 8.5,
            "acting": 9.2,
            "direction": 9.0,
            "music_sound": 7.8,
            "cinematography": 8.7,
            "action_stunts": 7.5,
            "emotional_impact": 8.9
        }
    },
    {
        "title": "Roma",
        "content_type": "movie",
        "year": 2018,
        "genre": "Drama",
        "streaming_platform": "Netflix",
        "description": "A year in the life of a middle-class family's maid in Mexico City in the early 1970s.",
        "ratings": {
            "story": 8.8,
            "acting": 8.9,
            "direction": 9.5,
            "music_sound": 8.2,
            "cinematography": 9.8,
            "action_stunts": 6.0,
            "emotional_impact": 9.3
        }
    },
    {
        "title": "Extraction",
        "content_type": "movie",
        "year": 2020,
        "genre": "Action/Thriller",
        "streaming_platform": "Netflix",
        "description": "A black-market mercenary has nothing to lose when his skills are solicited to rescue the kidnapped son of an imprisoned international crime lord.",
        "ratings": {
            "story": 7.2,
            "acting": 8.1,
            "direction": 8.3,
            "music_sound": 8.0,
            "cinematography": 8.8,
            "action_stunts": 9.5,
            "emotional_impact": 7.8
        }
    },
    # Netflix TV Series
    {
        "title": "Stranger Things",
        "content_type": "tv_series",
        "year": 2016,
        "genre": "Sci-Fi/Horror",
        "streaming_platform": "Netflix",
        "description": "When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces, and one strange little girl.",
        "ratings": {
            "story": 9.1,
            "acting": 8.7,
            "direction": 8.9,
            "music_sound": 9.3,
            "cinematography": 8.6,
            "action_stunts": 8.2,
            "emotional_impact": 8.8
        }
    },
    {
        "title": "The Crown",
        "content_type": "tv_series",
        "year": 2016,
        "genre": "Historical Drama",
        "streaming_platform": "Netflix",
        "description": "Follows the political rivalries and romance of Queen Elizabeth II's reign and the events that shaped the second half of the twentieth century.",
        "ratings": {
            "story": 9.0,
            "acting": 9.4,
            "direction": 9.2,
            "music_sound": 8.5,
            "cinematography": 9.6,
            "action_stunts": 6.5,
            "emotional_impact": 8.7
        }
    },
    {
        "title": "Squid Game",
        "content_type": "tv_series",
        "year": 2021,
        "genre": "Thriller/Drama",
        "streaming_platform": "Netflix",
        "description": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games for a tempting prize, but the stakes are deadly.",
        "ratings": {
            "story": 9.3,
            "acting": 8.9,
            "direction": 9.1,
            "music_sound": 8.4,
            "cinematography": 8.8,
            "action_stunts": 8.6,
            "emotional_impact": 9.5
        }
    },
    # Amazon Prime Video Movies
    {
        "title": "The Tomorrow War",
        "content_type": "movie",
        "year": 2021,
        "genre": "Action/Sci-Fi",
        "streaming_platform": "Amazon Prime Video",
        "description": "A family man is drafted to fight in a future war where the fate of humanity relies on his ability to confront the past.",
        "ratings": {
            "story": 7.5,
            "acting": 7.8,
            "direction": 7.9,
            "music_sound": 8.2,
            "cinematography": 8.5,
            "action_stunts": 9.0,
            "emotional_impact": 7.6
        }
    },
    {
        "title": "Sound of Metal",
        "content_type": "movie",
        "year": 2019,
        "genre": "Drama",
        "streaming_platform": "Amazon Prime Video",
        "description": "A heavy-metal drummer's life is thrown into freefall when he begins to lose his hearing.",
        "ratings": {
            "story": 8.6,
            "acting": 9.1,
            "direction": 8.8,
            "music_sound": 9.7,
            "cinematography": 8.3,
            "action_stunts": 6.0,
            "emotional_impact": 9.2
        }
    },
    {
        "title": "The Big Sick",
        "content_type": "movie",
        "year": 2017,
        "genre": "Comedy/Drama",
        "streaming_platform": "Amazon Prime Video",
        "description": "Pakistan-born comedian Kumail Nanjiani and grad student Emily Gardner fall in love but struggle as their cultures clash.",
        "ratings": {
            "story": 8.7,
            "acting": 8.9,
            "direction": 8.4,
            "music_sound": 7.8,
            "cinematography": 7.9,
            "action_stunts": 6.2,
            "emotional_impact": 8.8
        }
    },
    # Amazon Prime Video TV Series
    {
        "title": "The Boys",
        "content_type": "tv_series",
        "year": 2019,
        "genre": "Superhero/Dark Comedy",
        "streaming_platform": "Amazon Prime Video",
        "description": "A group of vigilantes set out to take down corrupt superheroes who abuse their superpowers.",
        "ratings": {
            "story": 9.2,
            "acting": 8.8,
            "direction": 8.9,
            "music_sound": 8.3,
            "cinematography": 8.7,
            "action_stunts": 9.4,
            "emotional_impact": 8.6
        }
    },
    {
        "title": "The Marvelous Mrs. Maisel",
        "content_type": "tv_series",
        "year": 2017,
        "genre": "Comedy/Drama",
        "streaming_platform": "Amazon Prime Video",
        "description": "A housewife in 1958 decides to become a stand-up comic after her husband leaves her.",
        "ratings": {
            "story": 8.8,
            "acting": 9.3,
            "direction": 9.0,
            "music_sound": 8.7,
            "cinematography": 9.2,
            "action_stunts": 6.0,
            "emotional_impact": 8.5
        }
    },
    {
        "title": "Invincible",
        "content_type": "tv_series",
        "year": 2021,
        "genre": "Animated/Superhero",
        "streaming_platform": "Amazon Prime Video",
        "description": "An adult animated series based on the Skybound/Image comic about a teenager whose father is the most powerful superhero on the planet.",
        "ratings": {
            "story": 9.0,
            "acting": 8.9,
            "direction": 9.1,
            "music_sound": 8.4,
            "cinematography": 8.8,
            "action_stunts": 9.3,
            "emotional_impact": 9.1
        }
    }
]

async def seed_database():
    """Seed the database with popular movies and TV shows"""
    try:
        # Check if data already exists
        existing_count = await db.movies.count_documents({})
        if existing_count > 0:
            return {"message": f"Database already contains {existing_count} movies"}
        
        # Add seed data
        for item in SEED_DATA:
            # Calculate overall rating
            overall_rating = calculate_overall_rating(RatingCategories(**item['ratings']))
            
            # Create movie object
            movie_dict = item.copy()
            movie_dict['overall_rating'] = overall_rating
            movie_obj = MovieTVShow(**movie_dict)
            
            # Insert into database
            await db.movies.insert_one(movie_obj.dict())
        
        return {"message": f"Successfully seeded database with {len(SEED_DATA)} movies and TV shows"}
    except Exception as e:
        return {"error": f"Error seeding database: {str(e)}"}

# Routes
@api_router.get("/")
async def root():
    return {"message": "Multi-Category Movie Rating API"}

@api_router.post("/seed")
async def seed_data():
    """Seed the database with popular movies and TV shows"""
    return await seed_database()

@api_router.post("/movies", response_model=MovieTVShow)
async def create_movie(movie_data: MovieTVShowCreate):
    """Create a new movie or TV show with multi-category ratings"""
    try:
        # Calculate overall rating
        overall_rating = calculate_overall_rating(movie_data.ratings)
        
        # Create movie object
        movie_dict = movie_data.dict()
        movie_dict['overall_rating'] = overall_rating
        movie_obj = MovieTVShow(**movie_dict)
        
        # Insert into database
        result = await db.movies.insert_one(movie_obj.dict())
        
        return movie_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating movie: {str(e)}")

@api_router.get("/movies", response_model=List[MovieTVShow])
async def get_movies(
    platform: Optional[StreamingPlatform] = None,
    content_type: Optional[ContentType] = None,
    limit: int = 50
):
    """Get movies/TV shows with optional filtering"""
    try:
        # Build query
        query = {}
        if platform:
            query['streaming_platform'] = platform
        if content_type:
            query['content_type'] = content_type
        
        # Get movies from database
        cursor = db.movies.find(query).limit(limit).sort("created_at", -1)
        movies = await cursor.to_list(length=limit)
        
        return [MovieTVShow(**movie) for movie in movies]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving movies: {str(e)}")

@api_router.get("/movies/{movie_id}", response_model=MovieTVShow)
async def get_movie(movie_id: str):
    """Get a specific movie by ID"""
    try:
        movie = await db.movies.find_one({"id": movie_id})
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        return MovieTVShow(**movie)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving movie: {str(e)}")

@api_router.put("/movies/{movie_id}", response_model=MovieTVShow)
async def update_movie(movie_id: str, movie_data: MovieTVShowUpdate):
    """Update a movie or TV show"""
    try:
        # Find existing movie
        existing_movie = await db.movies.find_one({"id": movie_id})
        if not existing_movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        # Prepare update data
        update_data = movie_data.dict(exclude_unset=True)
        update_data['updated_at'] = datetime.utcnow()
        
        # Recalculate overall rating if ratings were updated
        if 'ratings' in update_data:
            update_data['overall_rating'] = calculate_overall_rating(RatingCategories(**update_data['ratings']))
        
        # Update in database
        await db.movies.update_one(
            {"id": movie_id},
            {"$set": update_data}
        )
        
        # Return updated movie
        updated_movie = await db.movies.find_one({"id": movie_id})
        return MovieTVShow(**updated_movie)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating movie: {str(e)}")

@api_router.delete("/movies/{movie_id}")
async def delete_movie(movie_id: str):
    """Delete a movie or TV show"""
    try:
        result = await db.movies.delete_one({"id": movie_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        return {"message": "Movie deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting movie: {str(e)}")

@api_router.get("/platforms")
async def get_platforms():
    """Get list of available streaming platforms"""
    return [platform.value for platform in StreamingPlatform]

@api_router.get("/stats")
async def get_stats():
    """Get statistics about the movie database"""
    try:
        total_movies = await db.movies.count_documents({"content_type": "movie"})
        total_tv_shows = await db.movies.count_documents({"content_type": "tv_series"})
        
        # Platform distribution
        pipeline = [
            {"$group": {"_id": "$streaming_platform", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        platform_stats = await db.movies.aggregate(pipeline).to_list(length=None)
        
        return {
            "total_movies": total_movies,
            "total_tv_shows": total_tv_shows,
            "total_content": total_movies + total_tv_shows,
            "platform_distribution": platform_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()