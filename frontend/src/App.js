import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const RatingSlider = ({ label, value, onChange, description }) => (
  <div className="mb-4">
    <div className="flex justify-between items-center mb-1">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      <span className="text-sm font-bold text-blue-600">{value.toFixed(1)}</span>
    </div>
    <input
      type="range"
      min="0"
      max="10"
      step="0.1"
      value={value}
      onChange={(e) => onChange(parseFloat(e.target.value))}
      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
    />
    <p className="text-xs text-gray-500 mt-1">{description}</p>
  </div>
);

const MovieCard = ({ movie, onEdit, onDelete }) => {
  const categoryColors = {
    story: 'bg-red-100 text-red-800',
    acting: 'bg-blue-100 text-blue-800',
    direction: 'bg-green-100 text-green-800',
    music_sound: 'bg-purple-100 text-purple-800',
    cinematography: 'bg-yellow-100 text-yellow-800',
    action_stunts: 'bg-orange-100 text-orange-800',
    emotional_impact: 'bg-pink-100 text-pink-800'
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-xl font-bold text-gray-800">{movie.title}</h3>
          <p className="text-sm text-gray-600">{movie.year} • {movie.genre}</p>
          <p className="text-sm text-blue-600 font-medium">{movie.streaming_platform}</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="text-2xl font-bold text-yellow-500">{movie.overall_rating}</div>
          <div className="text-sm text-gray-500">/10</div>
        </div>
      </div>
      
      {movie.description && (
        <p className="text-gray-700 text-sm mb-4 line-clamp-2">{movie.description}</p>
      )}
      
      <div className="grid grid-cols-2 gap-2 mb-4">
        <div className={`px-2 py-1 rounded text-xs ${categoryColors.story}`}>
          Story: {movie.ratings.story}
        </div>
        <div className={`px-2 py-1 rounded text-xs ${categoryColors.acting}`}>
          Acting: {movie.ratings.acting}
        </div>
        <div className={`px-2 py-1 rounded text-xs ${categoryColors.direction}`}>
          Direction: {movie.ratings.direction}
        </div>
        <div className={`px-2 py-1 rounded text-xs ${categoryColors.music_sound}`}>
          Music: {movie.ratings.music_sound}
        </div>
        <div className={`px-2 py-1 rounded text-xs ${categoryColors.cinematography}`}>
          Cinematography: {movie.ratings.cinematography}
        </div>
        <div className={`px-2 py-1 rounded text-xs ${categoryColors.action_stunts}`}>
          Action: {movie.ratings.action_stunts}
        </div>
        <div className={`px-2 py-1 rounded text-xs ${categoryColors.emotional_impact}`}>
          Emotional: {movie.ratings.emotional_impact}
        </div>
      </div>
      
      <div className="flex space-x-2">
        <button
          onClick={() => onEdit(movie)}
          className="flex-1 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors text-sm"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(movie.id)}
          className="flex-1 bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition-colors text-sm"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

const AddMovieForm = ({ onClose, onSubmit, editingMovie = null }) => {
  const [formData, setFormData] = useState({
    title: '',
    content_type: 'movie',
    year: new Date().getFullYear(),
    genre: '',
    streaming_platform: 'Netflix',
    description: '',
    ratings: {
      story: 5.0,
      acting: 5.0,
      direction: 5.0,
      music_sound: 5.0,
      cinematography: 5.0,
      action_stunts: 5.0,
      emotional_impact: 5.0
    }
  });

  useEffect(() => {
    if (editingMovie) {
      setFormData({
        title: editingMovie.title,
        content_type: editingMovie.content_type,
        year: editingMovie.year,
        genre: editingMovie.genre,
        streaming_platform: editingMovie.streaming_platform,
        description: editingMovie.description || '',
        ratings: editingMovie.ratings
      });
    }
  }, [editingMovie]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const updateRating = (category, value) => {
    setFormData(prev => ({
      ...prev,
      ratings: {
        ...prev.ratings,
        [category]: value
      }
    }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">
            {editingMovie ? 'Edit Movie/TV Show' : 'Add New Movie/TV Show'}
          </h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Title"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              className="border rounded px-3 py-2 w-full"
              required
            />
            <select
              value={formData.content_type}
              onChange={(e) => setFormData({...formData, content_type: e.target.value})}
              className="border rounded px-3 py-2 w-full"
            >
              <option value="movie">Movie</option>
              <option value="tv_series">TV Series</option>
            </select>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <input
              type="number"
              placeholder="Year"
              value={formData.year}
              onChange={(e) => setFormData({...formData, year: parseInt(e.target.value)})}
              className="border rounded px-3 py-2 w-full"
              min="1900"
              max="2030"
              required
            />
            <input
              type="text"
              placeholder="Genre"
              value={formData.genre}
              onChange={(e) => setFormData({...formData, genre: e.target.value})}
              className="border rounded px-3 py-2 w-full"
              required
            />
          </div>
          
          <select
            value={formData.streaming_platform}
            onChange={(e) => setFormData({...formData, streaming_platform: e.target.value})}
            className="border rounded px-3 py-2 w-full"
          >
            <option value="Netflix">Netflix</option>
            <option value="Amazon Prime Video">Amazon Prime Video</option>
            <option value="Disney+ Hotstar">Disney+ Hotstar</option>
            <option value="Hulu">Hulu</option>
            <option value="HBO Max">HBO Max</option>
            <option value="Apple TV+">Apple TV+</option>
            <option value="Paramount+">Paramount+</option>
            <option value="YouTube">YouTube</option>
            <option value="Other">Other</option>
          </select>
          
          <textarea
            placeholder="Description (optional)"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            className="border rounded px-3 py-2 w-full h-20 resize-none"
          />
          
          <div className="border-t pt-4">
            <h3 className="text-lg font-semibold mb-4">Rate Each Category (0-10)</h3>
            
            <RatingSlider
              label="Story"
              value={formData.ratings.story}
              onChange={(value) => updateRating('story', value)}
              description="Plot, narrative structure, and engagement level"
            />
            
            <RatingSlider
              label="Acting"
              value={formData.ratings.acting}
              onChange={(value) => updateRating('acting', value)}
              description="Quality of performances by the cast"
            />
            
            <RatingSlider
              label="Direction"
              value={formData.ratings.direction}
              onChange={(value) => updateRating('direction', value)}
              description="How well the director realizes the vision"
            />
            
            <RatingSlider
              label="Music & Sound"
              value={formData.ratings.music_sound}
              onChange={(value) => updateRating('music_sound', value)}
              description="Score, soundtrack, and sound design quality"
            />
            
            <RatingSlider
              label="Cinematography"
              value={formData.ratings.cinematography}
              onChange={(value) => updateRating('cinematography', value)}
              description="Visual style, camera work, and aesthetics"
            />
            
            <RatingSlider
              label="Action & Stunts"
              value={formData.ratings.action_stunts}
              onChange={(value) => updateRating('action_stunts', value)}
              description="Quality of action sequences and stunts"
            />
            
            <RatingSlider
              label="Emotional Impact"
              value={formData.ratings.emotional_impact}
              onChange={(value) => updateRating('emotional_impact', value)}
              description="How much the content affects you emotionally"
            />
          </div>
          
          <div className="flex space-x-4 pt-4">
            <button
              type="submit"
              className="flex-1 bg-blue-500 text-white py-3 px-6 rounded-lg hover:bg-blue-600 transition-colors font-medium"
            >
              {editingMovie ? 'Update' : 'Add'} Movie/TV Show
            </button>
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-500 text-white py-3 px-6 rounded-lg hover:bg-gray-600 transition-colors font-medium"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

function App() {
  const [movies, setMovies] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingMovie, setEditingMovie] = useState(null);
  const [filter, setFilter] = useState({ platform: '', content_type: '' });
  const [loading, setLoading] = useState(false);

  const fetchMovies = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filter.platform) params.append('platform', filter.platform);
      if (filter.content_type) params.append('content_type', filter.content_type);
      
      const response = await axios.get(`${API}/movies?${params}`);
      setMovies(response.data);
    } catch (error) {
      console.error('Error fetching movies:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMovies();
  }, [filter]);

  const handleAddMovie = async (movieData) => {
    try {
      await axios.post(`${API}/movies`, movieData);
      setShowAddForm(false);
      fetchMovies();
    } catch (error) {
      console.error('Error adding movie:', error);
    }
  };

  const handleEditMovie = async (movieData) => {
    try {
      await axios.put(`${API}/movies/${editingMovie.id}`, movieData);
      setEditingMovie(null);
      fetchMovies();
    } catch (error) {
      console.error('Error updating movie:', error);
    }
  };

  const handleDeleteMovie = async (movieId) => {
    if (window.confirm('Are you sure you want to delete this movie/TV show?')) {
      try {
        await axios.delete(`${API}/movies/${movieId}`);
        fetchMovies();
      } catch (error) {
        console.error('Error deleting movie:', error);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div 
        className="bg-cover bg-center h-96 flex items-center justify-center relative"
        style={{
          backgroundImage: `linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwyfHxtb3ZpZSUyMHRoZWF0ZXJ8ZW58MHx8fHwxNzUxOTM5MDA4fDA&ixlib=rb-4.1.0&q=85')`
        }}
      >
        <div className="text-center text-white max-w-4xl mx-auto px-4">
          <h1 className="text-5xl font-bold mb-4">CineRating</h1>
          <p className="text-xl mb-6">Rate movies and TV shows across 7 detailed categories</p>
          <p className="text-lg opacity-90">Story • Acting • Direction • Music & Sound • Cinematography • Action & Stunts • Emotional Impact</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Controls */}
        <div className="flex flex-wrap gap-4 mb-8 items-center justify-between">
          <div className="flex flex-wrap gap-4">
            <select
              value={filter.platform}
              onChange={(e) => setFilter({...filter, platform: e.target.value})}
              className="border rounded px-3 py-2"
            >
              <option value="">All Platforms</option>
              <option value="Netflix">Netflix</option>
              <option value="Amazon Prime Video">Amazon Prime Video</option>
              <option value="Disney+ Hotstar">Disney+ Hotstar</option>
              <option value="Hulu">Hulu</option>
              <option value="HBO Max">HBO Max</option>
              <option value="Apple TV+">Apple TV+</option>
              <option value="Paramount+">Paramount+</option>
              <option value="YouTube">YouTube</option>
              <option value="Other">Other</option>
            </select>
            
            <select
              value={filter.content_type}
              onChange={(e) => setFilter({...filter, content_type: e.target.value})}
              className="border rounded px-3 py-2"
            >
              <option value="">All Types</option>
              <option value="movie">Movies</option>
              <option value="tv_series">TV Series</option>
            </select>
          </div>
          
          <button
            onClick={() => setShowAddForm(true)}
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors font-medium"
          >
            Add Movie/TV Show
          </button>
        </div>

        {/* Movie Grid */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading movies...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {movies.map(movie => (
              <MovieCard
                key={movie.id}
                movie={movie}
                onEdit={setEditingMovie}
                onDelete={handleDeleteMovie}
              />
            ))}
          </div>
        )}

        {movies.length === 0 && !loading && (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">No movies found. Add your first movie to get started!</p>
          </div>
        )}
      </div>

      {/* Add/Edit Form Modal */}
      {(showAddForm || editingMovie) && (
        <AddMovieForm
          onClose={() => {
            setShowAddForm(false);
            setEditingMovie(null);
          }}
          onSubmit={editingMovie ? handleEditMovie : handleAddMovie}
          editingMovie={editingMovie}
        />
      )}
    </div>
  );
}

export default App;