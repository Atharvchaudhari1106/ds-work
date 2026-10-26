import React, { useState, useEffect, useCallback } from 'react';
import { Search as SearchIcon, Mic, Sparkles, Flame, Clock, X, Play, Heart } from 'lucide-react';
import { performAISmartSearch } from '../services/smartAISearchEngine';
import { getRecentSearchTerms, addSearchTerm } from '../services/searchHistory';
import { useAudio } from '../context/AudioContext';

const SEARCH_GENRE_CARDS = [
  { title: 'Synthwave & Cyber', color: 'linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%)', query: 'Synthwave' },
  { title: 'Chill Lofi Beats', color: 'linear-gradient(135deg, #06B6D4 0%, #10B981 100%)', query: 'Lofi Beats' },
  { title: 'Pop Explosions', color: 'linear-gradient(135deg, #EC4899 0%, #F59E0B 100%)', query: 'Pop Hits' },
  { title: 'Hip Hop Classics', color: 'linear-gradient(135deg, #10B981 0%, #6366F1 100%)', query: 'Hip Hop' },
  { title: 'Electronic & Dance', color: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)', query: 'Electronic Dance' },
  { title: 'Rock & Alternative', color: 'linear-gradient(135deg, #EF4444 0%, #B45309 100%)', query: 'Rock Alternative' }
];

const TRENDING_SEARCHES = ['The Weeknd', 'Synthwave 80s', 'Lofi Girl Study Beats', 'Dua Lipa Houdini', 'Metro Boomin', 'Spatial Audio Classics'];

const Search = ({ initialQuery = '' }) => {
  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [recentTerms, setRecentTerms] = useState([]);
  const [showVoiceModal, setShowVoiceModal] = useState(false);
  const [voiceListening, setVoiceListening] = useState(false);
  const [aiNotice, setAiNotice] = useState(null);
  const [originalQuery, setOriginalQuery] = useState('');
  const [correctedQuery, setCorrectedQuery] = useState('');
  const { playTrack } = useAudio();

  const handleSearch = useCallback(async (searchTerm) => {
    const term = searchTerm !== undefined ? searchTerm : query;
    if (!term || !term.trim()) {
      setResults([]);
      setAiNotice(null);
      return;
    }

    setIsSearching(true);
    addSearchTerm(term);
    setRecentTerms(getRecentSearchTerms(6));

    try {
      const searchData = await performAISmartSearch(term);
      setResults(searchData.tracks || []);
      setAiNotice(searchData.aiNotice);
      setOriginalQuery(searchData.originalQuery);
      setCorrectedQuery(searchData.correctedQuery);
    } catch (err) {
      console.error('Search error:', err);
    } finally {
      setIsSearching(false);
    }
  }, [query]);

  useEffect(() => {
    setRecentTerms(getRecentSearchTerms(6));
  }, []);

  // Handle initialQuery when coming from TopNav or navigation
  useEffect(() => {
    if (initialQuery && initialQuery.trim()) {
      setQuery(initialQuery);
      handleSearch(initialQuery);
    }
  }, [initialQuery, handleSearch]);

  // Live debounced search as user types
  useEffect(() => {
    if (!query || !query.trim()) {
      setResults([]);
      setAiNotice(null);
      return;
    }

    const timer = setTimeout(() => {
      handleSearch(query);
    }, 450);

    return () => clearTimeout(timer);
  }, [query, handleSearch]);

  const startVoiceSearch = () => {
    setShowVoiceModal(true);
    setVoiceListening(true);

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.lang = 'en-US';
      recognition.start();

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setQuery(transcript);
        setVoiceListening(false);
        setShowVoiceModal(false);
        handleSearch(transcript);
      };

      recognition.onerror = () => {
        setVoiceListening(false);
      };
    } else {
      setTimeout(() => {
        const simulated = 'The Weeknd Blinding Lights';
        setQuery(simulated);
        setVoiceListening(false);
        setShowVoiceModal(false);
        handleSearch(simulated);
      }, 2000);
    }
  };

  return (
    <div className="search-view animate-fade-in">
      {/* Search Field Header */}
      <div className="search-header-container glass-card">
        <form onSubmit={(e) => { e.preventDefault(); handleSearch(); }} className="search-input-wrapper">
          <SearchIcon size={22} className="search-leading-icon" />
          <input
            type="text"
            placeholder="Search tracks, artists, albums, or genres..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="main-search-input"
            autoFocus
          />
          {query && (
            <button type="button" className="clear-btn" onClick={() => { setQuery(''); setResults([]); setAiNotice(null); }}>
              <X size={16} />
            </button>
          )}
          <button type="button" className="voice-mic-btn glow-purple" title="Voice Search" onClick={startVoiceSearch}>
            <Mic size={18} />
          </button>
        </form>

        {/* Trending Searches Tags */}
        <div className="trending-tags-row">
          <span className="trending-label">
            <Flame size={14} className="text-purple" /> Trending:
          </span>
          {TRENDING_SEARCHES.map(tag => (
            <button key={tag} className="tag-pill" onClick={() => handleSearch(tag)}>
              {tag}
            </button>
          ))}
        </div>
      </div>

      {/* Voice Search Modal */}
      {showVoiceModal && (
        <div className="modal-backdrop animate-fade-in" onClick={() => setShowVoiceModal(false)}>
          <div className="voice-modal-card glass-card animate-scale-up" onClick={e => e.stopPropagation()}>
            <button className="modal-close-btn" onClick={() => setShowVoiceModal(false)}>
              <X size={20} />
            </button>
            <div className="voice-pulse-ring glow-purple">
              <Mic size={36} color="white" />
            </div>
            <h3 className="voice-title">Listening...</h3>
            <p className="voice-sub">Speak the artist, track, or song title now.</p>
          </div>
        </div>
      )}

      {/* Search Results OR Browse Genres */}
      {isSearching ? (
        <div className="loading-state">
          <div className="pulse-loading-spinner" />
          <span>Searching Hi-Res Music Network...</span>
        </div>
      ) : results.length > 0 ? (
        <section className="search-results-section">
          <h3 className="section-title mb-16">Search Results for "{correctedQuery || query}"</h3>

          {aiNotice && (
            <div className="ai-search-correction-badge glass-card border-glow" style={{
              padding: '12px 20px',
              borderRadius: '12px',
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              background: 'rgba(139, 92, 246, 0.12)',
              border: '1px solid rgba(139, 92, 246, 0.3)',
              fontSize: '13px',
              color: 'var(--text-base)'
            }}>
              <Sparkles size={16} style={{ color: '#8B5CF6' }} />
              <span><strong>AI Auto-Correction:</strong> Showing results for <strong>"{correctedQuery}"</strong> (searched: <em>"{originalQuery}"</em>)</span>
            </div>
          )}
          <div className="mixes-grid">
            {results.map(track => (
              <div key={track.id} className="mix-card glass-card group" onClick={() => playTrack(track, results)}>
                <div className="mix-image-container border-glow">
                  <img src={track.thumbnail} alt={track.title} />
                  <div className="mix-play-overlay">
                    <Play size={32} fill="white" />
                  </div>
                </div>
                <div className="mix-info">
                  <p className="mix-title">{track.title}</p>
                  <p className="mix-desc">{track.artist}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      ) : (
        <div className="browse-genres-wrapper">
          {/* Recently Searched Terms */}
          {recentTerms.length > 0 && (
            <section className="recent-searches-section">
              <h4 className="section-subtitle">
                <Clock size={16} /> Recent Searches
              </h4>
              <div className="recent-tags-flex">
                {recentTerms.map((term, i) => (
                  <button key={i} className="recent-tag-btn" onClick={() => handleSearch(term)}>
                    {term}
                  </button>
                ))}
              </div>
            </section>
          )}

          {/* Genre Grid */}
          <section className="search-genres-section">
            <h3 className="section-title mb-16">
              <Sparkles size={18} className="text-purple" /> Browse All Genres
            </h3>
            <div className="search-genres-grid">
              {SEARCH_GENRE_CARDS.map(g => (
                <div
                  key={g.title}
                  className="search-genre-card group"
                  style={{ background: g.color }}
                  onClick={() => handleSearch(g.query)}
                >
                  <h4 className="search-genre-title">{g.title}</h4>
                  <div className="search-genre-play">
                    <Play size={18} fill="white" />
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  );
};

export default Search;
