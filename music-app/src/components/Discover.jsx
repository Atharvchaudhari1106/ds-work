import React, { useState, useEffect } from 'react';
import { Play, Sparkles, TrendingUp, Radio, Flame, Disc, Globe, Compass, Music, Heart } from 'lucide-react';
import { getTrending } from '../services/musicService';
import { useAudio } from '../context/AudioContext';

const GENRES = [
  { id: 'synthwave', name: 'Synthwave & Cyber', gradient: 'linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)', icon: '⚡' },
  { id: 'lofi', name: 'Chill Lofi Beats', gradient: 'linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%)', icon: '☕' },
  { id: 'pop', name: 'Global Top Pop', gradient: 'linear-gradient(135deg, #F59E0B 0%, #EF4444 100%)', icon: '🔥' },
  { id: 'hiphop', name: 'Hip Hop & Trap', gradient: 'linear-gradient(135deg, #10B981 0%, #3B82F6 100%)', icon: '🎤' },
  { id: 'edm', name: 'Electronic & Dance', gradient: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)', icon: '🎧' },
  { id: 'rock', name: 'Alt Rock & Indie', gradient: 'linear-gradient(135deg, #D97706 0%, #B45309 100%)', icon: '🎸' },
  { id: 'ambient', name: 'Deep Space Ambient', gradient: 'linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%)', icon: '🌌' },
  { id: 'rnb', name: 'Neo Soul & R&B', gradient: 'linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%)', icon: '🎷' },
];

const Discover = ({ onSelectArtist, onSelectAlbum }) => {
  const [trendingTracks, setTrendingTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const { playTrack, library, addToLibrary, removeFromLibrary } = useAudio();

  useEffect(() => {
    getTrending()
      .then(tracks => {
        setTrendingTracks(tracks || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch trending:', err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="discover-view animate-fade-in">
      {/* Top Banner */}
      <div className="discover-hero-banner glass-card">
        <div className="hero-banner-content">
          <div className="discover-badge">
            <Compass size={14} /> EXPLORE WORLD SOUNDS
          </div>
          <h1 className="discover-hero-title">Discover Tomorrow's Music Today</h1>
          <p className="discover-hero-subtitle">
            Curated soundscapes, trending global charts, and personalized sonic journeys.
          </p>
        </div>
        <div className="discover-hero-floating-elements">
          <div className="floating-glow-orb purple" />
          <div className="floating-glow-orb blue" />
        </div>
      </div>

      {/* Genre Collections Grid */}
      <section className="discover-section">
        <div className="section-header">
          <h3 className="section-title">
            <Sparkles size={20} className="text-purple" /> Explore Genres & Moods
          </h3>
          <span className="section-sub">Handcrafted sonic universes</span>
        </div>

        <div className="genres-grid">
          {GENRES.map((genre) => (
            <div
              key={genre.id}
              className="genre-card group"
              style={{ background: genre.gradient }}
            >
              <div className="genre-card-overlay" />
              <span className="genre-emoji">{genre.icon}</span>
              <h4 className="genre-name">{genre.name}</h4>
              <div className="genre-play-badge">
                <Play size={16} fill="white" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Global Top Charts */}
      <section className="discover-section">
        <div className="section-header">
          <h3 className="section-title">
            <TrendingUp size={20} className="text-cyan" /> Global Top Charts
          </h3>
          <span className="section-sub">Most streamed tracks right now</span>
        </div>

        {loading ? (
          <div className="loading-state">
            <div className="pulse-loading-spinner" />
            <span>Fetching Global Charts...</span>
          </div>
        ) : (
          <div className="top-charts-list">
            {trendingTracks.slice(0, 6).map((track, idx) => {
              const isLiked = library.some(t => t.id === track.id);
              return (
                <div
                  key={track.id || idx}
                  className="chart-row-card glass-card group"
                  onClick={() => playTrack(track, trendingTracks)}
                >
                  <span className={`chart-rank rank-${idx + 1}`}>#{idx + 1}</span>
                  <img
                    src={track.thumbnail}
                    alt={track.title}
                    className="chart-track-thumb"
                  />
                  <div className="chart-track-info">
                    <h4 className="chart-track-title">{track.title}</h4>
                    <p className="chart-track-artist">{track.artist}</p>
                  </div>

                  <div className="chart-row-actions">
                    <button
                      className="action-circle-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        isLiked ? removeFromLibrary(track.id) : addToLibrary(track);
                      }}
                    >
                      <Heart size={16} fill={isLiked ? "var(--neon-purple)" : "none"} color={isLiked ? "var(--neon-purple)" : "currentColor"} />
                    </button>
                    <button className="play-circle-sm">
                      <Play size={14} fill="currentColor" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* Featured Artists Showcase */}
      <section className="discover-section">
        <div className="section-header">
          <h3 className="section-title">
            <Globe size={20} className="text-emerald" /> Top Trending Artists
          </h3>
          <span className="section-sub">Creators shaping the future of sound</span>
        </div>

        <div className="artists-scroll-row">
          {[
            { id: '1', name: 'The Weeknd', listeners: '108M monthly', img: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400&h=400&fit=crop' },
            { id: '2', name: 'Dua Lipa', listeners: '76M monthly', img: 'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=400&h=400&fit=crop' },
            { id: '3', name: 'Drake', listeners: '84M monthly', img: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=400&fit=crop' },
            { id: '4', name: 'Billie Eilish', listeners: '92M monthly', img: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&h=400&fit=crop' },
            { id: '5', name: 'Travis Scott', listeners: '65M monthly', img: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400&h=400&fit=crop' }
          ].map(artist => (
            <div 
              key={artist.id} 
              className="artist-avatar-card glass-card"
              onClick={() => onSelectArtist && onSelectArtist(artist)}
            >
              <div className="avatar-img-container">
                <img src={artist.img} alt={artist.name} />
                <div className="verified-badge-dot" title="Verified Artist">✓</div>
              </div>
              <h4 className="artist-name">{artist.name}</h4>
              <p className="artist-listeners">{artist.listeners}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Discover;
