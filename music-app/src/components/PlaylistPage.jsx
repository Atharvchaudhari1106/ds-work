import React, { useState } from 'react';
import { Play, Heart, Share2, Download, Plus, Clock, ListMusic, User, MessageSquare, Sparkles } from 'lucide-react';
import { useAudio } from '../context/AudioContext';

const PlaylistPage = ({ playlist, goBack }) => {
  const { playTrack, library } = useAudio();
  const [isLiked, setIsLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(14209);

  const playlistData = playlist || {
    id: 'pl_featured',
    name: 'Cyberpunk Neon Beats',
    description: 'An immersive dark synthwave and futuristic electro voyage through glowing neon rain.',
    creator: 'AesthetiCore Editorial',
    trackCount: 38,
    duration: '2 hr 14 min',
    coverUrl: 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=600&h=600&fit=crop',
    tracks: library.length > 0 ? library : [
      { id: 'pl_t1', title: 'Midnight City', artist: 'M83', thumbnail: 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=300&h=300&fit=crop' },
      { id: 'pl_t2', title: 'Resonance', artist: 'HOME', thumbnail: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300&h=300&fit=crop' },
      { id: 'pl_t3', title: 'Nightcall', artist: 'Kavinsky', thumbnail: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300&h=300&fit=crop' },
      { id: 'pl_t4', title: 'Sunset', artist: 'The Midnight', thumbnail: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300&h=300&fit=crop' }
    ]
  };

  const handleToggleLike = () => {
    if (isLiked) {
      setIsLiked(false);
      setLikeCount(prev => prev - 1);
    } else {
      setIsLiked(true);
      setLikeCount(prev => prev + 1);
    }
  };

  return (
    <div className="playlist-page-view animate-fade-in">
      {/* Header Banner */}
      <div className="playlist-header-card glass-card">
        <div className="playlist-cover-box border-glow">
          <img src={playlistData.coverUrl} alt={playlistData.name} />
        </div>

        <div className="playlist-meta-box">
          <span className="playlist-badge">
            <Sparkles size={13} /> CURATED PLAYLIST
          </span>
          <h1 className="playlist-title">{playlistData.name}</h1>
          <p className="playlist-description">{playlistData.description}</p>

          <div className="playlist-stats-row">
            <span className="creator-text">By <strong>{playlistData.creator}</strong></span>
            <span className="dot-divider">•</span>
            <span>{likeCount.toLocaleString()} Likes</span>
            <span className="dot-divider">•</span>
            <span>{playlistData.tracks.length} Songs, {playlistData.duration}</span>
          </div>

          <div className="playlist-actions-row">
            <button 
              className="btn-primary glow-purple flex-align-gap"
              onClick={() => playlistData.tracks.length > 0 && playTrack(playlistData.tracks[0], playlistData.tracks)}
            >
              <Play size={18} fill="currentColor" /> Play Playlist
            </button>

            <button 
              className={`btn-secondary-glass ${isLiked ? 'liked' : ''}`}
              onClick={handleToggleLike}
            >
              <Heart size={18} fill={isLiked ? "var(--neon-purple)" : "none"} color={isLiked ? "var(--neon-purple)" : "currentColor"} />
              {isLiked ? 'Liked' : 'Like'}
            </button>

            <button className="icon-glass-btn" title="Download Playlist">
              <Download size={18} />
            </button>
            <button className="icon-glass-btn" title="Share">
              <Share2 size={18} />
            </button>
          </div>
        </div>
      </div>

      {/* Playlist Track List */}
      <section className="playlist-tracks-section">
        <div className="track-list-header">
          <span>#</span>
          <span>TITLE</span>
          <span>ARTIST</span>
          <span><Clock size={14} /></span>
        </div>

        <div className="playlist-tracks-container">
          {playlistData.tracks.map((track, idx) => (
            <div 
              key={track.id || idx}
              className="playlist-track-item glass-card group"
              onClick={() => playTrack(track, playlistData.tracks)}
            >
              <span className="item-idx">{idx + 1}</span>
              <div className="item-title-wrapper">
                <img src={track.thumbnail || playlistData.coverUrl} alt={track.title} className="item-thumb" />
                <h4 className="item-name">{track.title}</h4>
              </div>
              <span className="item-artist">{track.artist}</span>
              <span className="item-dur">3:45</span>
              <button className="item-play-btn">
                <Play size={14} fill="currentColor" />
              </button>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default PlaylistPage;
