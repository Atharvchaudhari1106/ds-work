import React from 'react';
import { 
  Home, Compass, Search, Library, Heart, ListMusic, 
  Podcast, Radio, Download, Settings, User, Sparkles, 
  Plus, LogOut, Disc, Music2, TvMinimalPlay, Crown, X, Shield
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useAudio } from '../context/AudioContext';
import logo from '../assets/logo.png';

const Sidebar = ({ 
  setView, 
  activeView, 
  onClose,
  onOpenSettings, 
  onOpenAIMix, 
  onOpenInstallModal,
  onOpenSubscription
}) => {
  const { logout, user } = useAuth();
  const { createPlaylist, library, playlists, currentTrack } = useAudio();

  const handleCreatePlaylist = () => {
    const name = window.prompt("Enter playlist name:");
    if (name) {
      createPlaylist(name);
    }
  };

  const navItems = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'discover', label: 'Discover', icon: Compass },
    { id: 'search', label: 'Search', icon: Search },
    { id: 'library', label: 'Your Library', icon: Library },
    { id: 'favorites', label: 'Favorites', icon: Heart },
    ...(currentTrack ? [{ id: 'nowplaying', label: 'Now Playing', icon: Disc }] : []),
    { id: 'podcasts', label: 'Podcasts', icon: Podcast },
    { id: 'downloads', label: 'Downloads', icon: Download },
    { id: 'profile', label: 'Profile', icon: User },
  ];

  return (
    <aside className="sidebar floating-glass-sidebar">
      {/* App Logo Header */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-content" onClick={() => setView('home')}>
          <div className="logo-glow-wrapper">
            <img src={logo} alt="AesthetiCore Logo" className="logo-img" />
          </div>
          <div className="logo-text">
            <span className="app-title">AesthetiCore</span>
            <span className="app-badge">PRO</span>
          </div>
        </div>
        {onClose && (
          <button 
            type="button" 
            className="sidebar-close-btn" 
            onClick={onClose} 
            title="Close Menu"
            aria-label="Close menu"
          >
            <X size={20} />
          </button>
        )}
      </div>

      {/* Main Navigation Items */}
      <div className="sidebar-scrollable">
        {/* Streaming Imports & AI Mix */}
        <div className="sidebar-nav-group">
          <span className="group-label">STUDIO & SOURCES</span>
          <button
            className="sidebar-nav-item ai-mix-item glow-purple-sm"
            onClick={onOpenAIMix}
          >
            <div className="nav-icon-box ai-icon-box">
              <Sparkles size={18} />
            </div>
            <span className="nav-label">AI Mix Generator</span>
          </button>

          <button
            className={`sidebar-nav-item ${activeView === 'spotify' ? 'active' : ''}`}
            onClick={() => setView('spotify')}
          >
            <div className="nav-icon-box">
              <Music2 size={18} color="#1DB954" />
            </div>
            <span className="nav-label">Spotify Stream</span>
          </button>

          <button
            className={`sidebar-nav-item ${activeView === 'youtube' ? 'active' : ''}`}
            onClick={() => setView('youtube')}
          >
            <div className="nav-icon-box">
              <TvMinimalPlay size={18} color="#FF0000" />
            </div>
            <span className="nav-label">YouTube Stream</span>
          </button>

          <button
            className={`sidebar-nav-item ${activeView === 'admin' ? 'active' : ''}`}
            onClick={() => setView('admin')}
          >
            <div className="nav-icon-box">
              <Shield size={18} color="var(--neon-purple)" />
            </div>
            <span className="nav-label">Admin Dashboard</span>
          </button>
        </div>

        {/* User Playlists */}
        <div className="sidebar-nav-group">
          <div className="group-header-flex">
            <span className="group-label">PLAYLISTS</span>
            <button className="icon-add-btn" onClick={handleCreatePlaylist} title="Create Playlist">
              <Plus size={16} />
            </button>
          </div>
          <div className="user-playlists-list">
            {playlists.length === 0 ? (
              <p className="empty-playlists-hint">No custom playlists yet</p>
            ) : (
              playlists.map((pl) => (
                <button
                  key={pl.id}
                  className={`playlist-item-btn ${activeView === 'playlist' ? 'active' : ''}`}
                  onClick={() => setView('library')}
                >
                  <ListMusic size={16} className="pl-icon" />
                  <span className="pl-name">{pl.name}</span>
                </button>
              ))
            )}
          </div>
        </div>

        {/* App Install Banner */}
        <div className="sidebar-install-box">
          <button className="sidebar-install-btn" onClick={onOpenInstallModal}>
            <Download size={16} />
            <span>Install Desktop/Mobile App</span>
          </button>
        </div>
      </div>

      {/* Sidebar Footer with Settings & Profile */}
      <div className="sidebar-footer-card">
        <div className="footer-user-row" onClick={() => setView('profile')}>
          <div className="user-avatar-sm">
            {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
          </div>
          <div className="user-meta-sm">
            <span className="user-name-text">{user?.name || 'AesthetiCore User'}</span>
            <span className="user-status-text">Premium Audio</span>
          </div>
        </div>

        <div className="footer-actions-row">
          <button className="footer-icon-btn" onClick={onOpenSubscription} title="Subscription Tier">
            <Crown size={18} color="var(--neon-purple)" />
          </button>
          <button className="footer-icon-btn" onClick={onOpenSettings} title="Settings">
            <Settings size={18} />
          </button>
          <button className="footer-icon-btn danger" onClick={logout} title="Log Out">
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
