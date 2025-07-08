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

# Routes
@api_router.get("/")
async def root():
    return {"message": "Multi-Category Movie Rating API"}

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