import React, { useState, useEffect, useCallback } from 'react';
import { getTrending, getHomeSuggestions, shuffleArray } from '../services/musicService';
import { getRecentSearchTerms } from '../services/searchHistory';
import { useAudio } from '../context/AudioContext';
import { generateMoodMixes, getTimeBasedGreeting } from '../services/aiEngine';
import { getInsight, getListeningStats } from '../services/analyticsService';
import { generateBecauseYouListened } from '../services/musicIntelligence';
import AIInsightCard from './AIInsightCard';
import TrackRow from './TrackRow';
import { Play, Heart, Sparkles, Download, Flame, Globe, Compass, Radio, Disc, Music, RefreshCw } from 'lucide-react';

const Home = ({ onOpenAIMix, onOpenInstallModal, onSelectArtist, onSelectAlbum }) => {
  const [categories, setCategories] = useState([]);
  const [featuredSong, setFeaturedSong] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [moodMixes, setMoodMixes] = useState([]);
  const [aiSections, setAiSections] = useState([]);
  const [insight, setInsight] = useState(null);
  const [stats, setStats] = useState(null);
  const [greeting, setGreeting] = useState(null);
  const { playTrack, library, addToLibrary, removeFromLibrary } = useAudio();

  useEffect(() => {
    setGreeting(getTimeBasedGreeting());
    setInsight(getInsight());
    setStats(getListeningStats());

    if (library.length >= 3) {
      setMoodMixes(generateMoodMixes(library));
    }
  }, [library]);

  useEffect(() => {
    if (library.length >= 2) {
      generateBecauseYouListened(library).then(sections => {
        setAiSections(sections);
      }).catch(err => console.warn('AI sections failed:', err));
    }
  }, [library.map(t => t.id).join(',')]);

  const fetchMusic = useCallback(async () => {
    setIsLoading(true);
    try {
      const searchTerms = getRecentSearchTerms(10);
      const allTrending = await getTrending();
      
      const newCategories = [];
      let spotlightCandidates = [];
      
      const spotifyPlaylists = JSON.parse(localStorage.getItem('spotify_playlists') || '[]');
      if (spotifyPlaylists.length > 0) {
        newCategories.push({ id: 'spotify-playlists', title: 'Spotify Playlists', tracks: spotifyPlaylists[0].tracks.slice(0, 6) });
      }

      const youtubeData = JSON.parse(localStorage.getItem('youtube_playlists') || '[]');
      if (youtubeData.length > 0) {
        newCategories.push({ id: 'yt-playlist', title: 'YouTube Playlists', tracks: youtubeData[0].tracks.slice(0, 6) });
      }
      
      // Dynamic search-based suggestions (rotates search terms & track order on every refresh)
      const dynamicCats = await getHomeSuggestions(searchTerms);
      if (dynamicCats && dynamicCats.length > 0) {
        newCategories.push(...dynamicCats);
        dynamicCats.forEach(cat => {
          if (cat.tracks && cat.tracks.length > 0) {
            spotlightCandidates.push(...cat.tracks);
          }
        });
      }

      // Shuffled Trending Section
      if (allTrending && allTrending.length > 0) {
        const shuffledTrending = shuffleArray(allTrending);
        spotlightCandidates.push(...shuffledTrending);
        newCategories.push({ 
          id: `trending-${Date.now()}`, 
          title: '🔥 Trending & Popular', 
          tracks: shuffledTrending.slice(0, 6) 
        });
      }
      
      // Select a new random Featured Spotlight Release on every refresh!
      if (spotlightCandidates.length > 0) {
        const randomFeatured = shuffleArray(spotlightCandidates)[0];
        setFeaturedSong(randomFeatured);
      }
      
      setCategories(newCategories.filter(c => c && c.tracks && c.tracks.length > 0));
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMusic();
  }, [fetchMusic]);

  const getSourceBadge = (track) => {
    if (track.source === 'youtube') return { label: 'YT', color: '#FF0000' };
    if (track.source === 'spotify') return { label: 'SP', color: '#1DB954' };
    return null;
  };

  return (
    <div className="home-view animate-fade-in">
      {/* Dynamic Animated Particles & Floating Notes Banner */}
      {featuredSong ? (
        <section className="hero-landing-section glass-card">
          <div className="hero-background-art" style={{ backgroundImage: `url(${featuredSong.thumbnail})` }} />
          <div className="hero-ambient-glow-layer" />
          
          <div className="hero-floating-notes">
            <span className="floating-note note-1">♫</span>
            <span className="floating-note note-2">♪</span>
            <span className="floating-note note-3">♬</span>
          </div>

          <div className="hero-landing-content">
            <div className="hero-tag-pill glow-purple">
              <Sparkles size={14} /> FEATURED SPOTLIGHT RELEASE
            </div>
            <h1 className="hero-landing-title">{featuredSong.title}</h1>
            <p className="hero-landing-artist">Performed by {featuredSong.artist}</p>
            <p className="hero-landing-sub">Mastered in 24-bit Lossless Spatial Audio. Stream on AesthetiCore.</p>

            <div className="hero-landing-cta-row">
              <button 
                className="btn-primary glow-purple hero-play-cta flex-align-gap"
                onClick={() => playTrack(featuredSong, [featuredSong])}
              >
                <Play size={22} fill="currentColor" /> Play Now
              </button>

              <button 
                className="btn-secondary-glass flex-align-gap"
                onClick={() => addToLibrary(featuredSong)}
              >
                <Heart size={18} /> Save to Favorites
              </button>
            </div>
          </div>
        </section>
      ) : (
        <div className="hero-skeleton glass-card animate-pulse" />
      )}

      {/* Greeting Header */}
      {greeting && (
        <div className="home-greeting-bar">
          <div>
            <h2 className="greeting-text">
              <span className="greeting-icon">{greeting.icon}</span> {greeting.greeting}
            </h2>
            <p className="greeting-subtext">{greeting.subtext}</p>
          </div>
          <button 
            className="btn-refresh-feed" 
            onClick={fetchMusic} 
            title="Refresh Recommendations"
            disabled={isLoading}
          >
            <RefreshCw size={15} className={isLoading ? "animate-spin" : ""} />
            <span>Refresh Feed</span>
          </button>
        </div>
      )}

      {isLoading ? (
        <div className="loading-state">
          <div className="pulse-loading-spinner" />
          <span>Crafting your music feed...</span>
        </div>
      ) : (
        <div className="home-content-sections">
          {/* AI Insight Card */}
          {insight && (
            <AIInsightCard insight={insight} stats={stats} onGenerateMix={onOpenAIMix} />
          )}

          {/* Mood Mixes Row */}
          {moodMixes.length > 0 && (
            <section className="home-section">
              <div className="section-header-flex">
                <h3 className="section-title">
                  <Sparkles size={18} className="text-purple" /> Mood Mixes
                </h3>
              </div>
              <div className="mood-mixes-scroll">
                {moodMixes.map(mix => (
                  <div
                    key={mix.mood}
                    className="mood-mix-card group"
                    style={{ background: mix.gradient }}
                    onClick={() => mix.tracks.length > 0 && playTrack(mix.tracks[0], mix.tracks)}
                  >
                    <span className="mood-mix-emoji">{mix.emoji}</span>
                    <h4 className="mood-mix-title">{mix.title}</h4>
                    <p className="mood-mix-count">{mix.tracks.length} tracks</p>
                    <div className="mood-mix-play">
                      <Play size={16} fill="white" />
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Featured Artists Circular Avatar Grid */}
          <section className="home-section">
            <div className="section-header-flex">
              <h3 className="section-title">
                <Globe size={18} className="text-emerald" /> Top Featured Artists
              </h3>
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
                  </div>
                  <h4 className="artist-name">{artist.name}</h4>
                  <p className="artist-listeners">{artist.listeners}</p>
                </div>
              ))}
            </div>
          </section>

          {/* Dynamic Categories */}
          {categories.map((cat, catIdx) => (
            <section key={cat.id || catIdx} className="home-section">
              <div className="section-header-flex">
                <h3 className="section-title">{cat.title}</h3>
                <span className="see-all-link">See All</span>
              </div>

              <div className="mixes-grid">
                {cat.tracks.map(song => (
                  <div key={song.id} className="mix-card glass-card group" onClick={() => playTrack(song, cat.tracks)}>
                    <div className="mix-image-container border-glow">
                      <img src={song.thumbnail} alt={song.title} />
                      <div className="mix-play-overlay">
                        <Play size={32} fill="white" className="text-white" />
                      </div>
                      {getSourceBadge(song) && (
                        <span className="yt-source-badge" style={{ background: getSourceBadge(song).color }}>
                          {getSourceBadge(song).label}
                        </span>
                      )}
                    </div>
                    <div className="mix-info">
                      <p className="mix-title">{song.title}</p>
                      <p className="mix-desc">{song.artist}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  );
};

export default Home;
