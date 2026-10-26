import React, { useState } from 'react';
import { Play, Heart, CheckCircle2, UserPlus, Shuffle, Music, Disc, Ticket, ShoppingBag, Info, Share2, Sparkles } from 'lucide-react';
import { useAudio } from '../context/AudioContext';

const MOCK_POPULAR_TRACKS = [
  { id: 'ap_1', title: 'Blinding Lights', artist: 'The Weeknd', album: 'After Hours', duration: '3:20', streams: '3.8B', thumbnail: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300&h=300&fit=crop' },
  { id: 'ap_2', title: 'Starboy', artist: 'The Weeknd', album: 'Starboy', duration: '3:50', streams: '2.9B', thumbnail: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300&h=300&fit=crop' },
  { id: 'ap_3', title: 'Save Your Tears', artist: 'The Weeknd', album: 'After Hours', duration: '3:35', streams: '2.5B', thumbnail: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300&h=300&fit=crop' },
  { id: 'ap_4', title: 'Die For You', artist: 'The Weeknd', album: 'Starboy', duration: '4:20', streams: '1.8B', thumbnail: 'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=300&h=300&fit=crop' },
  { id: 'ap_5', title: 'The Hills', artist: 'The Weeknd', album: 'Beauty Behind The Madness', duration: '4:02', streams: '2.1B', thumbnail: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300&h=300&fit=crop' }
];

const ArtistProfile = ({ artist, goBack }) => {
  const [isFollowing, setIsFollowing] = useState(false);
  const [activeTab, setActiveTab] = useState('popular');
  const { playTrack } = useAudio();

  const artistData = artist || {
    name: 'The Weeknd',
    listeners: '108,492,103 monthly listeners',
    verified: true,
    bannerUrl: 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=1200&h=400&fit=crop',
    avatarUrl: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400&h=400&fit=crop',
    bio: 'Abel Makkonen Tesfaye, known professionally as The Weeknd, is a Canadian singer-songwriter and record producer. Renowned for his sonic versatility and dark lyricism.'
  };

  return (
    <div className="artist-profile-view animate-fade-in">
      {/* Hero Banner */}
      <div className="artist-hero-banner" style={{ backgroundImage: `url(${artistData.bannerUrl})` }}>
        <div className="artist-banner-overlay" />
        <div className="artist-hero-content">
          <div className="artist-avatar-wrapper">
            <img src={artistData.avatarUrl} alt={artistData.name} className="artist-avatar-img" />
            <span className="artist-verified-badge" title="Verified Artist">
              <CheckCircle2 size={16} fill="var(--neon-emerald)" color="black" />
            </span>
          </div>

          <div className="artist-meta-info">
            <div className="verified-tag">
              <Sparkles size={12} color="var(--neon-cyan)" /> Verified Artist
            </div>
            <h1 className="artist-main-name">{artistData.name}</h1>
            <p className="artist-listeners-count">{artistData.listeners || '108M monthly listeners'}</p>

            <div className="artist-cta-buttons">
              <button 
                className="btn-primary flex-align-gap glow-purple"
                onClick={() => playTrack(MOCK_POPULAR_TRACKS[0], MOCK_POPULAR_TRACKS)}
              >
                <Play size={18} fill="currentColor" /> Play Discography
              </button>
              <button 
                className={`btn-secondary-glass ${isFollowing ? 'following' : ''}`}
                onClick={() => setIsFollowing(!isFollowing)}
              >
                <UserPlus size={16} /> {isFollowing ? 'Following' : 'Follow'}
              </button>
              <button className="icon-glass-btn" title="Share Artist Profile">
                <Share2 size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Profile Navigation Tabs */}
      <div className="artist-tabs-header glass-card">
        <button 
          className={`artist-tab-btn ${activeTab === 'popular' ? 'active' : ''}`}
          onClick={() => setActiveTab('popular')}
        >
          <Music size={16} /> Popular Tracks
        </button>
        <button 
          className={`artist-tab-btn ${activeTab === 'albums' ? 'active' : ''}`}
          onClick={() => setActiveTab('albums')}
        >
          <Disc size={16} /> Albums
        </button>
        <button 
          className={`artist-tab-btn ${activeTab === 'concerts' ? 'active' : ''}`}
          onClick={() => setActiveTab('concerts')}
        >
          <Ticket size={16} /> Tour Dates
        </button>
        <button 
          className={`artist-tab-btn ${activeTab === 'about' ? 'active' : ''}`}
          onClick={() => setActiveTab('about')}
        >
          <Info size={16} /> About
        </button>
      </div>

      {/* Tab Content */}
      <div className="artist-tab-content">
        {activeTab === 'popular' && (
          <section className="artist-tracks-section">
            <h3 className="section-title mb-16">Top 5 Popular Tracks</h3>
            <div className="tracks-list-container">
              {MOCK_POPULAR_TRACKS.map((track, idx) => (
                <div 
                  key={track.id}
                  className="artist-track-row glass-card group"
                  onClick={() => playTrack(track, MOCK_POPULAR_TRACKS)}
                >
                  <span className="track-idx">{idx + 1}</span>
                  <img src={track.thumbnail} alt={track.title} className="track-thumb-sm" />
                  <div className="track-details-col">
                    <h4 className="track-title">{track.title}</h4>
                    <p className="track-album-name">{track.album}</p>
                  </div>
                  <span className="track-streams-count">{track.streams} plays</span>
                  <span className="track-duration">{track.duration}</span>
                  <button className="play-row-btn">
                    <Play size={14} fill="currentColor" />
                  </button>
                </div>
              ))}
            </div>
          </section>
        )}

        {activeTab === 'albums' && (
          <section className="artist-albums-section">
            <h3 className="section-title mb-16">Albums & EPs</h3>
            <div className="albums-grid">
              {[
                { title: 'After Hours', year: '2020', tracks: '14 Songs', cover: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&h=400&fit=crop' },
                { title: 'Dawn FM', year: '2022', tracks: '16 Songs', cover: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400&h=400&fit=crop' },
                { title: 'Starboy', year: '2016', tracks: '18 Songs', cover: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400&h=400&fit=crop' },
                { title: 'Beauty Behind The Madness', year: '2015', tracks: '14 Songs', cover: 'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=400&h=400&fit=crop' }
              ].map((album, i) => (
                <div key={i} className="album-card glass-card group">
                  <div className="album-cover-box">
                    <img src={album.cover} alt={album.title} />
                    <div className="album-hover-overlay">
                      <Play size={28} fill="white" />
                    </div>
                  </div>
                  <h4 className="album-title">{album.title}</h4>
                  <p className="album-meta">{album.year} • {album.tracks}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        {activeTab === 'concerts' && (
          <section className="artist-concerts-section">
            <h3 className="section-title mb-16">Upcoming After Hours Til Dawn World Tour</h3>
            <div className="concerts-list">
              {[
                { date: 'OCT 14', city: 'London, UK', venue: 'Wembley Stadium', status: 'Selling Fast' },
                { date: 'OCT 18', city: 'Paris, France', venue: 'Stade de France', status: 'Sold Out' },
                { date: 'OCT 24', city: 'Tokyo, Japan', venue: 'Tokyo Dome', status: 'Tickets Available' },
              ].map((c, i) => (
                <div key={i} className="concert-row glass-card">
                  <div className="concert-date-badge">{c.date}</div>
                  <div className="concert-info">
                    <h4 className="concert-city">{c.city}</h4>
                    <p className="concert-venue">{c.venue}</p>
                  </div>
                  <span className="concert-status">{c.status}</span>
                  <button className="btn-secondary-sm">Get Tickets</button>
                </div>
              ))}
            </div>
          </section>
        )}

        {activeTab === 'about' && (
          <section className="artist-about-section glass-card">
            <h3 className="section-title">Biography</h3>
            <p className="artist-bio-text">{artistData.bio}</p>
          </section>
        )}
      </div>
    </div>
  );
};

export default ArtistProfile;
