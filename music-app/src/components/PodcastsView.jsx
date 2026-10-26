import React, { useState } from 'react';
import { Podcast, Play, Download, Clock, Radio, Sparkles, Volume2, CheckCircle2, Bookmark } from 'lucide-react';
import { useAudio } from '../context/AudioContext';

const PODCAST_CATEGORIES = ['All', 'Tech & Future', 'Music & Culture', 'True Crime', 'Deep Conversations', 'Science & AI'];

const PODCAST_SHOWS = [
  { id: 'pod_1', title: 'The Sonic Architecture Podcast', host: 'AesthetiCore Originals', episodes: '42 Episodes', category: 'Music & Culture', image: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400&h=400&fit=crop' },
  { id: 'pod_2', title: 'Synthesizer Dreams', host: 'Elena Vance', episodes: '89 Episodes', category: 'Tech & Future', image: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400&h=400&fit=crop' },
  { id: 'pod_3', title: 'Future of Audio & AI', host: 'Dr. Marcus Vance', episodes: '24 Episodes', category: 'Science & AI', image: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&h=400&fit=crop' },
  { id: 'pod_4', title: 'Midnight Stories', host: 'Julian Vance', episodes: '60 Episodes', category: 'Deep Conversations', image: 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=400&h=400&fit=crop' }
];

const PODCAST_EPISODES = [
  { id: 'ep_1', title: 'Ep. 42: How Neural Networks Compose 80s Synth Harmonies', date: 'Jul 24, 2026', duration: '48 min', show: 'The Sonic Architecture Podcast', summary: 'Exploring deep learning models trained on retro analog synths and spatial reverb algorithms.', thumbnail: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300&h=300&fit=crop' },
  { id: 'ep_2', title: 'Ep. 89: The Evolution of Lossless & Spatial Audio Formats', date: 'Jul 20, 2026', duration: '54 min', show: 'Synthesizer Dreams', summary: 'A deep dive into 24-bit/192kHz resolution, binaural rendering, and high-fidelity streaming.', thumbnail: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300&h=300&fit=crop' },
  { id: 'ep_3', title: 'Ep. 24: Quantum Computing and the Future of Music Processing', date: 'Jul 15, 2026', duration: '42 min', show: 'Future of Audio & AI', summary: 'Will quantum algorithms replace traditional digital signal processors in DAWs?', thumbnail: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300&h=300&fit=crop' }
];

const PodcastsView = () => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [speed, setSpeed] = useState('1x');
  const { playTrack } = useAudio();

  const toggleSpeed = () => {
    if (speed === '1x') setSpeed('1.25x');
    else if (speed === '1.25x') setSpeed('1.5x');
    else if (speed === '1.5x') setSpeed('2x');
    else setSpeed('1x');
  };

  return (
    <div className="podcasts-view animate-fade-in">
      {/* Header Banner */}
      <div className="podcasts-hero-banner glass-card">
        <div className="podcasts-hero-text">
          <div className="podcast-badge">
            <Podcast size={14} /> EXCLUSIVE PODCASTS
          </div>
          <h1 className="podcasts-hero-title">Immersive Conversations & Audio Stories</h1>
          <p className="podcasts-hero-sub">
            Listen to top tech, music culture, science, and AI discussions with enhanced voice clarity.
          </p>
        </div>

        <div className="podcast-speed-box">
          <button className="speed-toggle-btn" onClick={toggleSpeed} title="Playback Speed">
            <Clock size={16} /> Speed: <strong>{speed}</strong>
          </button>
        </div>
      </div>

      {/* Categories Filter Pills */}
      <div className="podcast-categories-row">
        {PODCAST_CATEGORIES.map(cat => (
          <button
            key={cat}
            className={`podcast-cat-pill ${selectedCategory === cat ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Featured Shows Section */}
      <section className="podcasts-section">
        <h3 className="section-title mb-16">
          <Radio size={18} className="text-cyan" /> Featured Shows
        </h3>
        <div className="shows-grid">
          {PODCAST_SHOWS.map(show => (
            <div key={show.id} className="podcast-show-card glass-card group">
              <div className="show-img-container">
                <img src={show.image} alt={show.title} />
                <div className="show-overlay">
                  <Play size={28} fill="white" />
                </div>
              </div>
              <span className="show-cat-tag">{show.category}</span>
              <h4 className="show-title">{show.title}</h4>
              <p className="show-host">{show.host} • {show.episodes}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Latest Episodes Section */}
      <section className="podcasts-section">
        <h3 className="section-title mb-16">
          <Sparkles size={18} className="text-purple" /> Latest Episodes
        </h3>
        <div className="episodes-list">
          {PODCAST_EPISODES.map(ep => (
            <div 
              key={ep.id} 
              className="episode-card glass-card group"
              onClick={() => playTrack({
                id: ep.id,
                title: ep.title,
                artist: ep.show,
                thumbnail: ep.thumbnail
              }, [])}
            >
              <img src={ep.thumbnail} alt={ep.title} className="ep-thumb" />
              <div className="ep-content">
                <span className="ep-show-name">{ep.show}</span>
                <h4 className="ep-title">{ep.title}</h4>
                <p className="ep-summary">{ep.summary}</p>
                <div className="ep-meta">
                  <span>{ep.date}</span>
                  <span className="dot-divider">•</span>
                  <span>{ep.duration}</span>
                </div>
              </div>
              <div className="ep-actions">
                <button className="ep-play-btn glow-purple">
                  <Play size={16} fill="currentColor" /> Play
                </button>
                <button className="icon-glass-btn" title="Download Episode">
                  <Download size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default PodcastsView;
