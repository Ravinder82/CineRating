import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const RatingSlider = ({ label, value, onChange, description, icon }) => (
  <div className="mb-6 p-4 bg-gray-50 rounded-xl border border-gray-200">
    <div className="flex justify-between items-center mb-2">
      <label className="text-sm font-semibold text-gray-700 flex items-center space-x-2">
        <span className="text-lg">{icon}</span>
        <span>{label}</span>
      </label>
      <div className="flex items-center space-x-2">
        <span className="text-lg font-bold text-indigo-600">{value.toFixed(1)}</span>
        <span className="text-sm text-gray-500">/10</span>
      </div>
    </div>
    <div className="relative">
      <input
        type="range"
        min="0"
        max="10"
        step="0.1"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-3 bg-gradient-to-r from-gray-300 to-gray-300 rounded-lg appearance-none cursor-pointer slider-modern"
        style={{
          background: `linear-gradient(to right, #6366f1 0%, #6366f1 ${value * 10}%, #d1d5db ${value * 10}%, #d1d5db 100%)`
        }}
      />
      <div className="flex justify-between text-xs text-gray-400 mt-1">
        <span>0</span>
        <span>5</span>
        <span>10</span>
      </div>
    </div>
    <p className="text-xs text-gray-500 mt-2 leading-relaxed">{description}</p>
  </div>
);

const MovieCard = ({ movie, onEdit, onDelete }) => {
  const categoryColors = {
    story: 'bg-gradient-to-r from-red-500 to-red-600 text-white',
    acting: 'bg-gradient-to-r from-blue-500 to-blue-600 text-white',
    direction: 'bg-gradient-to-r from-green-500 to-green-600 text-white',
    music_sound: 'bg-gradient-to-r from-purple-500 to-purple-600 text-white',
    cinematography: 'bg-gradient-to-r from-yellow-500 to-yellow-600 text-white',
    action_stunts: 'bg-gradient-to-r from-orange-500 to-orange-600 text-white',
    emotional_impact: 'bg-gradient-to-r from-pink-500 to-pink-600 text-white'
  };

  const platformColors = {
    'Netflix': 'bg-red-600 text-white',
    'Amazon Prime Video': 'bg-blue-600 text-white',
    'Disney+ Hotstar': 'bg-indigo-600 text-white',
    'HBO Max': 'bg-purple-600 text-white',
    'Apple TV+': 'bg-gray-800 text-white',
    'Hulu': 'bg-green-600 text-white',
    'Paramount+': 'bg-blue-500 text-white',
    'YouTube': 'bg-red-500 text-white',
    'Other': 'bg-gray-500 text-white'
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden group hover:scale-105">
      <div className="relative">
        <div className="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 h-32 relative">
          <div className="absolute inset-0 bg-black bg-opacity-30"></div>
          <div className="absolute top-4 right-4">
            <div className="bg-white bg-opacity-90 backdrop-blur-sm rounded-full px-3 py-1 flex items-center space-x-1">
              <span className="text-2xl font-bold text-yellow-500">⭐</span>
              <span className="text-lg font-bold text-gray-800">{movie.overall_rating}</span>
              <span className="text-sm text-gray-600">/10</span>
            </div>
          </div>
          <div className="absolute bottom-4 left-4">
            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${platformColors[movie.streaming_platform] || platformColors['Other']}`}>
              {movie.streaming_platform}
            </span>
          </div>
        </div>
        
        <div className="p-6">
          <div className="mb-4">
            <h3 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-indigo-600 transition-colors">
              {movie.title}
            </h3>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <span className="bg-gray-100 px-2 py-1 rounded-full">{movie.year}</span>
              <span>•</span>
              <span className="bg-gray-100 px-2 py-1 rounded-full">{movie.genre}</span>
              <span>•</span>
              <span className="bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full capitalize">
                {movie.content_type.replace('_', ' ')}
              </span>
            </div>
          </div>
          
          {movie.description && (
            <p className="text-gray-600 text-sm mb-4 line-clamp-2 leading-relaxed">
              {movie.description}
            </p>
          )}
          
          <div className="grid grid-cols-2 gap-2 mb-6">
            <div className={`px-3 py-2 rounded-lg text-xs font-medium ${categoryColors.story} shadow-sm`}>
              📚 Story: {movie.ratings.story}
            </div>
            <div className={`px-3 py-2 rounded-lg text-xs font-medium ${categoryColors.acting} shadow-sm`}>
              🎭 Acting: {movie.ratings.acting}
            </div>
            <div className={`px-3 py-2 rounded-lg text-xs font-medium ${categoryColors.direction} shadow-sm`}>
              🎬 Direction: {movie.ratings.direction}
            </div>
            <div className={`px-3 py-2 rounded-lg text-xs font-medium ${categoryColors.music_sound} shadow-sm`}>
              🎵 Music: {movie.ratings.music_sound}
            </div>
            <div className={`px-3 py-2 rounded-lg text-xs font-medium ${categoryColors.cinematography} shadow-sm`}>
              📸 Cinema: {movie.ratings.cinematography}
            </div>
            <div className={`px-3 py-2 rounded-lg text-xs font-medium ${categoryColors.action_stunts} shadow-sm`}>
              💥 Action: {movie.ratings.action_stunts}
            </div>
            <div className={`px-3 py-2 rounded-lg text-xs font-medium ${categoryColors.emotional_impact} shadow-sm col-span-2`}>
              💫 Emotional Impact: {movie.ratings.emotional_impact}
            </div>
          </div>
          
          <div className="flex space-x-3">
            <button
              onClick={() => onEdit(movie)}
              className="flex-1 bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-3 px-4 rounded-lg hover:from-indigo-600 hover:to-purple-700 transition-all duration-300 text-sm font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              ✏️ Edit
            </button>
            <button
              onClick={() => onDelete(movie.id)}
              className="flex-1 bg-gradient-to-r from-red-500 to-pink-600 text-white py-3 px-4 rounded-lg hover:from-red-600 hover:to-pink-700 transition-all duration-300 text-sm font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              🗑️ Delete
            </button>
          </div>
        </div>
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
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 rounded-t-2xl">
          <div className="flex justify-between items-center">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              {editingMovie ? '✏️ Edit Movie/TV Show' : '✨ Add New Movie/TV Show'}
            </h2>
            <button 
              onClick={onClose} 
              className="text-gray-400 hover:text-gray-600 transition-colors p-2 hover:bg-gray-100 rounded-full"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">🎬 Title</label>
              <input
                type="text"
                placeholder="Enter movie/TV show title"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">📺 Content Type</label>
              <select
                value={formData.content_type}
                onChange={(e) => setFormData({...formData, content_type: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
              >
                <option value="movie">Movie</option>
                <option value="tv_series">TV Series</option>
              </select>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">📅 Year</label>
              <input
                type="number"
                placeholder="Release year"
                value={formData.year}
                onChange={(e) => setFormData({...formData, year: parseInt(e.target.value)})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                min="1900"
                max="2030"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">🎭 Genre</label>
              <input
                type="text"
                placeholder="e.g., Action, Comedy, Drama"
                value={formData.genre}
                onChange={(e) => setFormData({...formData, genre: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                required
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">🎯 Streaming Platform</label>
            <select
              value={formData.streaming_platform}
              onChange={(e) => setFormData({...formData, streaming_platform: e.target.value})}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
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
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">📝 Description</label>
            <textarea
              placeholder="Brief description of the movie/TV show (optional)"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors h-24 resize-none"
            />
          </div>
          
          <div className="border-t pt-6">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              🌟 Rate Each Category (0-10)
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <RatingSlider
                label="Story"
                icon="📚"
                value={formData.ratings.story}
                onChange={(value) => updateRating('story', value)}
                description="Plot, narrative structure, and engagement level"
              />
              
              <RatingSlider
                label="Acting"
                icon="🎭"
                value={formData.ratings.acting}
                onChange={(value) => updateRating('acting', value)}
                description="Quality of performances by the cast"
              />
              
              <RatingSlider
                label="Direction"
                icon="🎬"
                value={formData.ratings.direction}
                onChange={(value) => updateRating('direction', value)}
                description="How well the director realizes the vision"
              />
              
              <RatingSlider
                label="Music & Sound"
                icon="🎵"
                value={formData.ratings.music_sound}
                onChange={(value) => updateRating('music_sound', value)}
                description="Score, soundtrack, and sound design quality"
              />
              
              <RatingSlider
                label="Cinematography"
                icon="📸"
                value={formData.ratings.cinematography}
                onChange={(value) => updateRating('cinematography', value)}
                description="Visual style, camera work, and aesthetics"
              />
              
              <RatingSlider
                label="Action & Stunts"
                icon="💥"
                value={formData.ratings.action_stunts}
                onChange={(value) => updateRating('action_stunts', value)}
                description="Quality of action sequences and stunts"
              />
            </div>
            
            <div className="mt-4">
              <RatingSlider
                label="Emotional Impact"
                icon="💫"
                value={formData.ratings.emotional_impact}
                onChange={(value) => updateRating('emotional_impact', value)}
                description="How much the content affects you emotionally"
              />
            </div>
          </div>
          
          <div className="flex space-x-4 pt-6 border-t">
            <button
              type="submit"
              className="flex-1 bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-4 px-6 rounded-lg hover:from-indigo-600 hover:to-purple-700 transition-all duration-300 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              {editingMovie ? '✅ Update Movie/TV Show' : '🚀 Add Movie/TV Show'}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-500 text-white py-4 px-6 rounded-lg hover:bg-gray-600 transition-all duration-300 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              ❌ Cancel
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
  const [seeding, setSeeding] = useState(false);

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

  const seedDatabase = async () => {
    setSeeding(true);
    try {
      const response = await axios.post(`${API}/seed`);
      console.log('Database seeded:', response.data);
      await fetchMovies(); // Refresh the movie list
    } catch (error) {
      console.error('Error seeding database:', error);
    } finally {
      setSeeding(false);
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
          
          <div className="flex gap-2">
            {movies.length === 0 && !loading && (
              <button
                onClick={seedDatabase}
                disabled={seeding}
                className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors font-medium disabled:opacity-50"
              >
                {seeding ? 'Loading Popular Content...' : 'Load Popular Movies & TV Shows'}
              </button>
            )}
            <button
              onClick={() => setShowAddForm(true)}
              className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors font-medium"
            >
              Add Movie/TV Show
            </button>
          </div>
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
            <div className="max-w-md mx-auto">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Start Rating Popular Content!</h3>
              <p className="text-gray-600 text-lg mb-6">
                Load popular movies and TV shows from Netflix and Amazon Prime Video to start rating them across 7 categories.
              </p>
              <button
                onClick={seedDatabase}
                disabled={seeding}
                className="bg-green-500 text-white px-8 py-4 rounded-lg hover:bg-green-600 transition-colors font-medium text-lg disabled:opacity-50"
              >
                {seeding ? 'Loading Popular Content...' : 'Load Popular Movies & TV Shows'}
              </button>
            </div>
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