import React, { useState } from 'react';
import { Play, Heart, Clock, Disc, Sparkles, Share2, Download, MoreHorizontal, Music } from 'lucide-react';
import { useAudio } from '../context/AudioContext';

const MOCK_ALBUM_TRACKS = [
  { id: 'alb_1', number: 1, title: 'Alone Again', artist: 'The Weeknd', duration: '4:10', plays: '482M' },
  { id: 'alb_2', number: 2, title: 'Too Late', artist: 'The Weeknd', duration: '3:59', plays: '390M' },
  { id: 'alb_3', number: 3, title: 'Hardest To Love', artist: 'The Weeknd', duration: '3:31', plays: '310M' },
  { id: 'alb_4', number: 4, title: 'Scared To Live', artist: 'The Weeknd', duration: '3:11', plays: '295M' },
  { id: 'alb_5', number: 5, title: 'Blinding Lights', artist: 'The Weeknd', duration: '3:20', plays: '3.8B' },
  { id: 'alb_6', number: 6, title: 'In Your Eyes', artist: 'The Weeknd', duration: '3:57', plays: '1.2B' },
  { id: 'alb_7', number: 7, title: 'Save Your Tears', artist: 'The Weeknd', duration: '3:35', plays: '2.5B' },
  { id: 'alb_8', number: 8, title: 'After Hours', artist: 'The Weeknd', duration: '6:01', plays: '890M' }
];

const AlbumDetails = ({ album, goBack }) => {
  const { playTrack, library, addToLibrary, removeFromLibrary } = useAudio();
  const [isSaved, setIsSaved] = useState(false);

  const albumData = album || {
    title: 'After Hours (Deluxe)',
    artist: 'The Weeknd',
    releaseYear: '2020',
    totalTracks: '14 Tracks',
    totalDuration: '56 min 19 sec',
    genre: 'Synthwave / R&B',
    coverUrl: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&h=600&fit=crop',
    label: 'XO / Republic Records'
  };

  return (
    <div className="album-details-view animate-fade-in">
      {/* Ambient Artwork Dynamic Lighting Background */}
      <div 
        className="album-ambient-glow"
        style={{ backgroundImage: `url(${albumData.coverUrl})` }}
      />

      {/* Header Info */}
      <div className="album-header-card glass-card">
        <div className="album-cover-wrapper border-glow">
          <img src={albumData.coverUrl} alt={albumData.title} className="album-main-cover" />
        </div>

        <div className="album-header-info">
          <span className="album-type-badge">
            <Disc size={13} /> ALBUM RELEASE
          </span>
          <h1 className="album-header-title">{albumData.title}</h1>
          
          <div className="album-artist-meta">
            <span className="album-artist-name">{albumData.artist}</span>
            <span className="dot-divider">•</span>
            <span>{albumData.releaseYear}</span>
            <span className="dot-divider">•</span>
            <span>{albumData.totalTracks}</span>
            <span className="dot-divider">•</span>
            <span>{albumData.totalDuration}</span>
          </div>

          <div className="album-cta-row">
            <button 
              className="btn-primary glow-purple flex-align-gap"
              onClick={() => playTrack({ ...MOCK_ALBUM_TRACKS[0], thumbnail: albumData.coverUrl }, MOCK_ALBUM_TRACKS.map(t => ({ ...t, thumbnail: albumData.coverUrl })))}
            >
              <Play size={18} fill="currentColor" /> Play Album
            </button>

            <button 
              className={`btn-secondary-glass ${isSaved ? 'liked' : ''}`}
              onClick={() => setIsSaved(!isSaved)}
            >
              <Heart size={18} fill={isSaved ? "var(--neon-purple)" : "none"} color={isSaved ? "var(--neon-purple)" : "currentColor"} />
              {isSaved ? 'Saved to Library' : 'Save Album'}
            </button>

            <button className="icon-glass-btn" title="Download Album">
              <Download size={18} />
            </button>
            <button className="icon-glass-btn" title="Share Album">
              <Share2 size={18} />
            </button>
          </div>
        </div>
      </div>

      {/* Tracklist Table */}
      <section className="album-tracklist-section">
        <div className="tracklist-table-header">
          <span className="col-num">#</span>
          <span className="col-title">TITLE</span>
          <span className="col-plays">PLAYS</span>
          <span className="col-dur"><Clock size={14} /></span>
        </div>

        <div className="tracklist-rows-container">
          {MOCK_ALBUM_TRACKS.map((track) => (
            <div 
              key={track.id}
              className="track-table-row glass-card group"
              onClick={() => playTrack({ ...track, thumbnail: albumData.coverUrl }, MOCK_ALBUM_TRACKS.map(t => ({ ...t, thumbnail: albumData.coverUrl })))}
            >
              <span className="track-number">{track.number}</span>
              <div className="track-title-block">
                <h4 className="track-name-text">{track.title}</h4>
                <p className="track-artist-text">{track.artist}</p>
              </div>
              <span className="track-plays-text">{track.plays}</span>
              <span className="track-dur-text">{track.duration}</span>
              <button className="track-play-hover-btn">
                <Play size={14} fill="currentColor" />
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* Album Credits & Copyright */}
      <footer className="album-footer-credits glass-card">
        <p className="credits-release-date">Released March 20, 2020</p>
        <p className="credits-label">℗ {albumData.releaseYear} {albumData.label}</p>
        <p className="credits-tech">Mastered in 24-bit / 192kHz Spatial Lossless Audio</p>
      </footer>
    </div>
  );
};

export default AlbumDetails;
