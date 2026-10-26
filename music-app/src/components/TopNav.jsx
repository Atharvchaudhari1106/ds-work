import React, { useState, useRef, useEffect } from 'react';
import { 
  Search, Bell, Sliders, Mic, Sparkles, User, LogOut, Settings, 
  Crown, CheckCircle2, ChevronRight, Music, Radio, Home, Compass, 
  Library, Heart, Podcast, Download, Disc, Menu
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useAudio } from '../context/AudioContext';

const TopNav = ({ 
  activeView, 
  setView, 
  toggleSidebar,
  onOpenSettings, 
  onOpenEqualizer, 
  onOpenNotifications, 
  onOpenSubscription, 
  unreadNotificationsCount = 2,
  onOpenVoiceSearch,
  onSearchQueryChange
}) => {
  const { user, logout } = useAuth();
  const { currentTrack } = useAudio();
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearchFocused, setIsSearchFocused] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(e.target)) {
        setShowProfileMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      if (onSearchQueryChange) {
        onSearchQueryChange(searchQuery.trim());
      }
      setView('search');
    }
  };

  const getTitleForView = () => {
    switch (activeView) {
      case 'home': return 'Home';
      case 'discover': return 'Discover';
      case 'search': return 'Search';
      case 'library': return 'Your Library';
      case 'favorites': return 'Favorites';
      case 'downloads': return 'Offline Downloads';
      case 'podcasts': return 'Podcasts & Shows';
      case 'profile': return 'User Profile';
      case 'artist': return 'Artist Spotlight';
      case 'album': return 'Album Overview';
      case 'playlist': return 'Playlist Details';
      case 'spotify': return 'Spotify Import';
      case 'youtube': return 'YouTube Import';
      case 'nowplaying': return 'Now Playing';
      default: return 'AesthetiCore';
    }
  };

  const mainNavItems = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'discover', label: 'Discover', icon: Compass },
    { id: 'search', label: 'Search', icon: Search },
    { id: 'library', label: 'Library', icon: Library },
    ...(currentTrack ? [{ id: 'nowplaying', label: 'Now Playing', icon: Disc }] : []),
    { id: 'podcasts', label: 'Podcasts', icon: Podcast },
    { id: 'downloads', label: 'Downloads', icon: Download },
  ];

  return (
    <header className="top-nav-bar glass-nav">
      {/* Left: View Title & Top Horizontal Navigation Links */}
      <div className="top-nav-left">
        {toggleSidebar && (
          <button 
            type="button"
            className="mobile-menu-toggle-btn" 
            onClick={toggleSidebar} 
            aria-label="Open navigation menu"
            title="Menu"
          >
            <Menu size={20} />
          </button>
        )}
        <div className="view-indicator">
          <span className="view-indicator-dot"></span>
          <h2 className="view-title">{getTitleForView()}</h2>
        </div>

        {/* Main Navigation Items moved from Sidebar to Top Bar */}
        <nav className="top-nav-menu-bar" aria-label="Top Bar Navigation">
          {mainNavItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                className={`top-menu-item ${isActive ? 'active' : ''}`}
                onClick={() => setView(item.id)}
                title={item.label}
                type="button"
              >
                <Icon size={15} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Right: Audio Quality, Equalizer, Notifications, Subscription & User Profile */}
      <div className="top-nav-right">
        {/* Hi-Res Audio Indicator */}
        <div className="audio-badge-pill" title="Hi-Res Lossless Audio Active">
          <Sparkles size={13} className="sparkle-icon" />
          <span>24-bit Hi-Res</span>
        </div>

        {/* Equalizer Button */}
        <button 
          className="nav-icon-btn equalizer-nav-btn" 
          title="Audio Equalizer & FX"
          onClick={onOpenEqualizer}
        >
          <Sliders size={18} />
        </button>

        {/* Notifications Button */}
        <button 
          className="nav-icon-btn notification-nav-btn" 
          title="Notifications"
          onClick={onOpenNotifications}
        >
          <Bell size={18} />
          {unreadNotificationsCount > 0 && (
            <span className="notification-badge">{unreadNotificationsCount}</span>
          )}
        </button>

        {/* Premium Subscription Badge */}
        <button 
          className="premium-pill-btn glow-purple" 
          onClick={onOpenSubscription}
          title="Manage Subscription"
        >
          <Crown size={14} />
          <span>PREMIUM</span>
        </button>

        {/* User Avatar Menu */}
        <div className="user-menu-wrapper" ref={profileMenuRef}>
          <button 
            className="user-avatar-btn" 
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            title={user?.name || 'User'}
          >
            <div className="avatar-glow-ring">
              <div className="avatar-img-placeholder">
                {user?.name ? user.name.charAt(0).toUpperCase() : <User size={18} />}
              </div>
            </div>
          </button>

          {showProfileMenu && (
            <div className="user-dropdown-menu glass-card animate-scale-up">
              <div className="user-menu-header" onClick={() => { setView('profile'); setShowProfileMenu(false); }}>
                <div className="menu-avatar">
                  {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
                </div>
                <div className="menu-user-details">
                  <div className="menu-user-name">{user?.name || 'AesthetiCore User'}</div>
                  <div className="menu-user-tier">
                    <CheckCircle2 size={12} color="var(--neon-emerald)" /> Premium Member
                  </div>
                </div>
              </div>
              <div className="dropdown-divider" />
              <button className="dropdown-menu-item" onClick={() => { setView('profile'); setShowProfileMenu(false); }}>
                <User size={16} /> Profile Dashboard
              </button>
              <button className="dropdown-menu-item" onClick={() => { onOpenSubscription(); setShowProfileMenu(false); }}>
                <Crown size={16} color="var(--neon-purple)" /> Subscription Plan
              </button>
              <button className="dropdown-menu-item" onClick={() => { onOpenEqualizer(); setShowProfileMenu(false); }}>
                <Sliders size={16} /> Audio & Equalizer
              </button>
              <button className="dropdown-menu-item" onClick={() => { onOpenSettings(); setShowProfileMenu(false); }}>
                <Settings size={16} /> App Settings
              </button>
              <div className="dropdown-divider" />
              <button className="dropdown-menu-item logout" onClick={() => { logout(); setShowProfileMenu(false); }}>
                <LogOut size={16} /> Log Out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default TopNav;
