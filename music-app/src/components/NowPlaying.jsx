import React, { useState, useRef, useEffect } from 'react';
import { 
  SkipBack, Play, Pause, SkipForward, 
  Shuffle, Repeat, Heart, ChevronDown, 
  Share2, ListMusic, Music, Plus, Download, Sparkles, Quote, Sliders, Globe, ZoomIn, ZoomOut, Disc, Copy, Check, Loader2, Search, ExternalLink, RefreshCw
} from 'lucide-react';
import { useAudio } from '../context/AudioContext';
import { downloadSong, sanitizeTrackMetadata } from '../services/musicService';
import { getSmartNextTracks } from '../services/musicIntelligence';
import { fetchLyrics, parseLyricsToLines, translateToEnglishMeaning } from '../services/lyricsService';

const NowPlaying = ({ goBack, onOpenEqualizer, initialTab = 'artwork' }) => {
  const { 
    currentTrack, 
    isPlaying, 
    togglePlay, 
    playNext, 
    playPrevious,
    isShuffled,
    toggleShuffle,
    repeatMode,
    toggleRepeat,
    library,
    addToLibrary,
    removeFromLibrary,
    playTrack
  } = useAudio();

  const [playedSeconds, setPlayedSeconds] = useState(0);
  const [duration, setDuration] = useState(0);
  const [similarSongs, setSimilarSongs] = useState([]);
  const [showLyrics, setShowLyrics] = useState(initialTab === 'lyrics');
  const [vinylMode, setVinylMode] = useState(initialTab === 'vinyl');
  const [lyricsFontSize, setLyricsFontSize] = useState(22);
  const [isEnglishTranslation, setIsEnglishTranslation] = useState(false);
  const [lyricsOffset, setLyricsOffset] = useState(0);

  const [lyricsLoading, setLyricsLoading] = useState(false);
  const [lyricsSource, setLyricsSource] = useState(null);
  const [lyricsType, setLyricsType] = useState(null);
  const [rawLyricsText, setRawLyricsText] = useState('');
  const [lyricsData, setLyricsData] = useState([]);

  const [copied, setCopied] = useState(false);
  const [likeToast, setLikeToast] = useState(null);
  const lyricsContainerRef = useRef(null);

  useEffect(() => {
    if (initialTab === 'lyrics') {
      setShowLyrics(true);
      setVinylMode(false);
    } else if (initialTab === 'vinyl') {
      setVinylMode(true);
      setShowLyrics(false);
    } else if (initialTab === 'artwork') {
      setShowLyrics(false);
      setVinylMode(false);
    }
  }, [initialTab]);

  const loadLyrics = () => {
    if (!currentTrack) return;
    setLyricsLoading(true);
    setLyricsSource(null);
    setLyricsType(null);
    setRawLyricsText('');
    setLyricsData([]);
    setLyricsOffset(0);

    fetchLyrics(currentTrack)
      .then(res => {
        if (res && res.lyrics) {
          setLyricsSource(res.source);
          setLyricsType(res.type);
          setRawLyricsText(res.lyrics);
        } else {
          setRawLyricsText('');
          setLyricsData([]);
        }
      })
      .catch(err => {
        console.warn('[NowPlaying] Lyrics fetch error:', err);
        setRawLyricsText('');
        setLyricsData([]);
      })
      .finally(() => setLyricsLoading(false));
  };

  useEffect(() => {
    if (rawLyricsText) {
      const parsed = parseLyricsToLines(rawLyricsText, duration);
      setLyricsData(parsed);
    } else {
      setLyricsData([]);
    }
  }, [rawLyricsText, duration]);

  useEffect(() => {
    if (!currentTrack) return;

    getSmartNextTracks(currentTrack, library)
      .then(res => setSimilarSongs(res.slice(0, 5)))
      .catch(err => console.warn('Failed to load similar songs:', err));

    loadLyrics();
  }, [currentTrack?.id, currentTrack?.title]);

  const activeLyricIndex = lyricsData.reduce((acc, lyric, index) => {
    if (lyric.time !== null && (playedSeconds + lyricsOffset) >= lyric.time) return index;
    return acc;
  }, 0);

  useEffect(() => {
    if (showLyrics && lyricsContainerRef.current && lyricsData.length > 0) {
      const activeEl = lyricsContainerRef.current.querySelector('.np-lyrics-line.active');
      if (activeEl) {
        activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }, [activeLyricIndex, showLyrics, lyricsData.length]);

  useEffect(() => {
    const handleProgress = (e) => setPlayedSeconds(e.detail.playedSeconds);
    const handleDuration = (e) => setDuration(e.detail.duration);

    window.addEventListener('music-progress', handleProgress);
    window.addEventListener('music-duration', handleDuration);
    window.dispatchEvent(new CustomEvent('music-request-sync'));

    return () => {
      window.removeEventListener('music-progress', handleProgress);
      window.removeEventListener('music-duration', handleDuration);
    };
  }, [currentTrack?.id]);

  const formatTime = (seconds) => {
    if (isNaN(seconds) || seconds === null || seconds === undefined || seconds < 0) return '0:00';
    let s = Number(seconds);
    if (s > 86400) {
      s = s / 1000;
    }
    const hrs = Math.floor(s / 3600);
    const mins = Math.floor((s % 3600) / 60);
    const secs = Math.floor(s % 60);
    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleSeek = (e) => {
    const time = parseFloat(e.target.value);
    setPlayedSeconds(time);
    window.dispatchEvent(new CustomEvent('music-seek', { detail: { time } }));
  };

  const isLiked = currentTrack ? library.some(t => t.id === currentTrack.id) : false;

  const handleToggleLike = () => {
    if (!currentTrack) return;
    if (isLiked) {
      removeFromLibrary(currentTrack.id);
      setLikeToast("Removed from Library");
    } else {
      addToLibrary(currentTrack);
      setLikeToast("Saved to Your Library ❤️");
    }
    setTimeout(() => setLikeToast(null), 2500);
  };

  const handleCopyLyrics = () => {
    if (!lyricsData.length) return;
    const textToCopy = lyricsData.map(l => l.text).join('\n');
    navigator.clipboard.writeText(textToCopy).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const openExternalLyricsSearch = () => {
    if (!currentTrack) return;
    const query = encodeURIComponent(`${currentTrack.title} ${currentTrack.artist} lyrics`);
    window.open(`https://www.google.com/search?q=${query}`, '_blank');
  };

  if (!currentTrack) {
    return (
      <div className="np-view animate-fade-in">
        <div className="np-empty">
          <Music size={64} strokeWidth={1} />
          <h2>Nothing Playing</h2>
          <button className="np-back-btn" onClick={goBack}>
            <ChevronDown size={20} /> Go Back
          </button>
        </div>
      </div>
    );
  }

  const cleanTrack = sanitizeTrackMetadata(currentTrack);
  const progress = duration > 0 ? (playedSeconds / duration) * 100 : 0;

  return (
    <div className="np-view animate-fade-in">
      {/* Blurred Album Artwork Layer */}
      <div 
        className="np-blurred-bg" 
        style={{ backgroundImage: `url(${cleanTrack.thumbnail})` }} 
      />
      <div className="np-overlay" />

      {likeToast && (
        <div className="np-toast-notification animate-bounce-in" style={{
          position: 'fixed',
          top: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 10000,
          background: 'rgba(30, 30, 30, 0.95)',
          color: '#fff',
          padding: '10px 20px',
          borderRadius: '30px',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
          fontSize: '14px',
          fontWeight: '600',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <Sparkles size={16} color="var(--neon-purple)" />
          {likeToast}
        </div>
      )}

      <div className="np-content">
        {/* Header */}
        <div className="np-header">
          <button className="np-back-btn" onClick={goBack} title="Close Now Playing">
            <ChevronDown size={24} />
          </button>
          <div className="np-header-center">
            <span className="np-header-label">Now Playing</span>
            <span className="np-audio-badge">
              <Sparkles size={12} color="var(--neon-purple)" /> 24-bit Lossless Spatial Audio
            </span>
          </div>
          <div className="np-header-actions">
            <button className={`np-top-icon-btn ${vinylMode ? 'active' : ''}`} onClick={() => { setVinylMode(!vinylMode); if (!vinylMode) setShowLyrics(false); }} title="Toggle Vinyl Mode">
              <Disc size={20} className={vinylMode ? 'text-purple' : ''} />
            </button>
            {onOpenEqualizer && (
              <button className="np-top-icon-btn" onClick={onOpenEqualizer} title="Equalizer & Audio Engine">
                <Sliders size={20} />
              </button>
            )}
          </div>
        </div>

        {/* Mode Switcher Tabs: Artwork | Lyrics | Vinyl */}
        <div className="np-mode-tabs">
          <button 
            className={`np-mode-tab ${!showLyrics && !vinylMode ? 'active' : ''}`} 
            onClick={() => { setShowLyrics(false); setVinylMode(false); }}
          >
            <Music size={14} /> Artwork
          </button>
          <button 
            className={`np-mode-tab ${showLyrics ? 'active' : ''}`} 
            onClick={() => { setShowLyrics(true); setVinylMode(false); }}
          >
            <Quote size={14} /> Lyrics
          </button>
          <button 
            className={`np-mode-tab ${vinylMode ? 'active' : ''}`} 
            onClick={() => { setVinylMode(true); setShowLyrics(false); }}
          >
            <Disc size={14} /> Vinyl
          </button>
        </div>

        {/* Center Artwork or Vinyl Disc or Synchronized Lyrics */}
        {showLyrics ? (
          <div className="np-lyrics-wrapper glass-card">
            <div className="np-lyrics-toolbar">
              <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                <button className="lyrics-tool-btn" onClick={() => setLyricsFontSize(prev => Math.min(prev + 2, 36))} title="Zoom In Text">
                  <ZoomIn size={16} />
                </button>
                <button className="lyrics-tool-btn" onClick={() => setLyricsFontSize(prev => Math.max(prev - 2, 14))} title="Zoom Out Text">
                  <ZoomOut size={16} />
                </button>
                <button 
                  className={`lyrics-tool-btn ${isEnglishTranslation ? 'active' : ''}`} 
                  onClick={() => setIsEnglishTranslation(!isEnglishTranslation)} 
                  title="Toggle English Meaning Translation"
                >
                  <Globe size={14} /> {isEnglishTranslation ? 'English Meaning' : 'Romanized'}
                </button>
              </div>

              <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                <button className="lyrics-tool-btn" onClick={() => setLyricsOffset(prev => prev - 2)} title="Shift Sync 2 seconds earlier">
                  -2s
                </button>
                <button className="lyrics-tool-btn" onClick={() => setLyricsOffset(prev => prev + 2)} title="Shift Sync 2 seconds later">
                  +2s
                </button>
                {lyricsOffset !== 0 && (
                  <button className="lyrics-tool-btn active" onClick={() => setLyricsOffset(0)} title="Reset Sync Offset">
                    Reset ({lyricsOffset > 0 ? `+${lyricsOffset}` : lyricsOffset}s)
                  </button>
                )}
                {lyricsSource && (
                  <span className="lyrics-source-badge" style={{ fontSize: '11px', color: 'var(--neon-purple)', padding: '4px 10px', background: 'rgba(168,85,247,0.15)', borderRadius: '20px', fontWeight: 'bold' }}>
                    {lyricsType === 'synced' ? '⚡ Synced' : '📄 Text'} • {lyricsSource}
                  </span>
                )}
                {lyricsData.length > 0 && (
                  <button className="lyrics-tool-btn" onClick={handleCopyLyrics} title="Copy Lyrics">
                    {copied ? <Check size={16} color="var(--neon-emerald)" /> : <Copy size={16} />}
                  </button>
                )}
              </div>
            </div>

            <div className="np-lyrics-container" ref={lyricsContainerRef}>
              {lyricsLoading ? (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', gap: '12px', color: 'var(--text-secondary)' }}>
                  <Loader2 size={32} className="spin" color="var(--neon-purple)" />
                  <p style={{ fontSize: '14px', fontWeight: '600' }}>Fetching lyrics...</p>
                </div>
              ) : lyricsData.length > 0 ? (
                lyricsData.map((line, index) => (
                  <div
                    key={index}
                    style={{ fontSize: `${lyricsFontSize}px` }}
                    className={`np-lyrics-line ${index === activeLyricIndex ? 'active' : ''}`}
                    onClick={() => {
                      if (line.time !== null) {
                        const targetTime = Math.max(0, line.time - lyricsOffset);
                        window.dispatchEvent(new CustomEvent('music-seek', { detail: { time: targetTime } }));
                        setPlayedSeconds(targetTime);
                      }
                    }}
                    title={line.time !== null ? "Click line to seek audio to this timestamp" : ""}
                  >
                    {isEnglishTranslation ? translateToEnglishMeaning(line.text) : line.text}
                  </div>
                ))
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', gap: '14px', textAlign: 'center', padding: '20px' }}>
                  <Quote size={40} color="rgba(255,255,255,0.3)" />
                  <div>
                    <h3 style={{ fontSize: '16px', fontWeight: '700', marginBottom: '6px' }}>No Lyrics Found</h3>
                    <p style={{ fontSize: '13px', color: 'rgba(255,255,255,0.6)', maxWidth: '280px' }}>
                      We couldn't fetch synchronized lyrics for "{currentTrack.title}".
                    </p>
                  </div>
                  <div style={{ display: 'flex', gap: '10px', marginTop: '6px' }}>
                    <button 
                      onClick={loadLyrics} 
                      className="lyrics-tool-btn active"
                      style={{ padding: '8px 16px', fontSize: '12px' }}
                    >
                      <RefreshCw size={14} /> Retry Search
                    </button>
                    <button 
                      onClick={openExternalLyricsSearch} 
                      className="lyrics-tool-btn"
                      style={{ padding: '8px 16px', fontSize: '12px' }}
                    >
                      <Search size={14} /> Search Online
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : vinylMode ? (
          <div className={`np-vinyl-container ${isPlaying ? 'playing' : ''}`}>
            <div className="np-vinyl-disc glow-purple">
              <div className="np-vinyl-grooves" />
              <div className="np-vinyl-label">
                <img src={cleanTrack.thumbnail} alt={cleanTrack.title} />
                <div className="np-vinyl-center-hole" />
              </div>
            </div>
          </div>
        ) : (
          <div className="np-art-container">
            <div className={`np-art-wrapper ${isPlaying ? 'playing' : ''}`}>
              <img src={cleanTrack.thumbnail} alt={cleanTrack.title} className="np-art border-glow" />
            </div>
          </div>
        )}

        {/* Track Title & Artist */}
        <div className="np-track-info">
          <h1 className="np-title">{cleanTrack.title}</h1>
          <p className="np-artist">{cleanTrack.artist}</p>
        </div>

        {/* Live Audio Waveform Animation Bars */}
        <div className={`np-waveform-bars ${isPlaying ? 'animating' : ''}`}>
          <span className="bar bar1" />
          <span className="bar bar2" />
          <span className="bar bar3" />
          <span className="bar bar4" />
          <span className="bar bar5" />
          <span className="bar bar6" />
        </div>

        {/* Progress Bar */}
        <div className="np-progress-section">
          <div className="np-progress-bar">
            <input
              type="range"
              min="0"
              max={duration || 0}
              step="0.1"
              value={playedSeconds}
              onChange={handleSeek}
              className="np-slider"
              style={{ '--np-progress': `${progress}%` }}
            />
            <div className="np-progress-fill glow-purple-sm" style={{ width: `${progress}%` }} />
          </div>
          <div className="np-time-row">
            <span>{formatTime(playedSeconds)}</span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>

        {/* Playback Controls */}
        <div className="np-controls">
          <button className={`np-ctrl-btn ${isShuffled ? 'active' : ''}`} onClick={toggleShuffle} title="Shuffle">
            <Shuffle size={20} />
          </button>
          <button className="np-ctrl-btn" onClick={playPrevious} title="Previous">
            <SkipBack size={26} fill="currentColor" />
          </button>
          <button className="np-play-btn glow-purple" onClick={togglePlay} title={isPlaying ? "Pause" : "Play"}>
            {isPlaying ? <Pause size={32} fill="currentColor" /> : <Play size={32} fill="currentColor" style={{ marginLeft: '4px' }} />}
          </button>
          <button className="np-ctrl-btn" onClick={playNext} title="Next">
            <SkipForward size={26} fill="currentColor" />
          </button>
          <button className={`np-ctrl-btn ${repeatMode !== 'off' ? 'active' : ''}`} onClick={toggleRepeat} title="Repeat">
            <Repeat size={20} />
          </button>
        </div>

        {/* Bottom Actions Row */}
        <div className="np-actions-row">
          <button className={`np-action-btn ${isLiked ? 'liked' : ''}`} onClick={handleToggleLike} title={isLiked ? "Remove from Library" : "Add to Library"}>
            <Heart size={22} fill={isLiked ? "var(--neon-purple)" : "none"} color={isLiked ? "var(--neon-purple)" : "currentColor"} />
          </button>
          <button className="np-action-btn" onClick={() => downloadSong(currentTrack)} title="Download Track">
            <Download size={22} />
          </button>
          <button 
            className={`np-action-btn lyrics-badge-btn ${showLyrics ? 'active' : ''}`} 
            onClick={() => { setShowLyrics(!showLyrics); if (vinylMode) setVinylMode(false); }}
            title="View Song Lyrics"
          >
            <Quote size={20} />
            <span style={{ fontSize: '12px', fontWeight: '700', marginLeft: '4px' }}>Lyrics</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default NowPlaying;
