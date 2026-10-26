import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import TopNav from './components/TopNav';
import Home from './components/Home';
import Discover from './components/Discover';
import Search from './components/Search';
import Library from './components/Library';
import ArtistProfile from './components/ArtistProfile';
import AlbumDetails from './components/AlbumDetails';
import PlaylistPage from './components/PlaylistPage';
import PodcastsView from './components/PodcastsView';
import UserProfileView from './components/UserProfileView';
import NowPlaying from './components/NowPlaying';
import PlayerBar from './components/PlayerBar';
import AuthModal from './components/AuthModal';
import BottomNav from './components/BottomNav';
import SpotifyView from './components/SpotifyView';
import YoutubeView from './components/YoutubeView';
import SpotifyCallback from './components/SpotifyCallback';
import SettingsModal from './components/SettingsModal';
import AIMixModal from './components/AIMixModal';
import InstallModal from './components/InstallModal';
import EqualizerModal from './components/EqualizerModal';
import SubscriptionModal from './components/SubscriptionModal';
import NotificationsModal from './components/NotificationsModal';
import SplashScreen from './components/SplashScreen';
import AdminDashboard from './components/AdminDashboard';
import { useAuth } from './context/AuthContext';
import { useAudio } from './context/AudioContext';
import { applyTheme } from './utils/theme';

function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [activeView, setActiveView] = useState('home');
  const [prevView, setPrevView] = useState('home');
  const [selectedArtist, setSelectedArtist] = useState(null);
  const [selectedAlbum, setSelectedAlbum] = useState(null);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [activeSearchQuery, setActiveSearchQuery] = useState('');

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isAIMixOpen, setIsAIMixOpen] = useState(false);
  const [isInstallOpen, setIsInstallOpen] = useState(false);
  const [isEqualizerOpen, setIsEqualizerOpen] = useState(false);
  const [isSubscriptionOpen, setIsSubscriptionOpen] = useState(false);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);

  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isIOS, setIsIOS] = useState(false);
  const [isStandalone, setIsStandalone] = useState(false);
  const { user } = useAuth();
  const { currentTrack } = useAudio();

  useEffect(() => {
    const savedTheme = localStorage.getItem('AESTHETICORE_THEME') || 'default';
    applyTheme(savedTheme);
  }, []);

  const [nowPlayingTab, setNowPlayingTab] = useState('artwork');

  useEffect(() => {
    const handleOpenNowPlaying = (e) => {
      if (e?.detail?.tab) {
        setNowPlayingTab(e.detail.tab);
      } else {
        setNowPlayingTab('artwork');
      }
      handleSetView('nowplaying');
    };
    window.addEventListener('open-now-playing', handleOpenNowPlaying);
    return () => window.removeEventListener('open-now-playing', handleOpenNowPlaying);
  }, [activeView]);

  useEffect(() => {
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };

    const isIOSDevice = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    setIsIOS(isIOSDevice);
    
    const isStandaloneMode = window.matchMedia('(display-mode: standalone)').matches;
    setIsStandalone(isStandaloneMode);

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  const handleInstallClick = () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
          console.log('User accepted install prompt');
        }
        setDeferredPrompt(null);
      });
    } else if (isIOS) {
      alert("📱 Install AesthetiCore:\n\n1. Tap 'Share' icon at the bottom.\n2. Tap 'Add to Home Screen'.");
    } else {
      alert("📱 Install AesthetiCore:\n\n1. Tap browser menu (three dots).\n2. Tap 'Install App' or 'Add to Home Screen'.");
    }
  };

  const showInstallButton = (deferredPrompt || isIOS || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) && !isStandalone;

  const handleSetView = (view) => {
    console.log(`[App] Navigating from "${activeView}" to "${view}"`);
    if (view !== activeView) {
      setPrevView(activeView);
      setActiveView(view);
    }
  };

  const handleSelectArtist = (artistData) => {
    setSelectedArtist(artistData);
    handleSetView('artist');
  };

  const handleSelectAlbum = (albumData) => {
    setSelectedAlbum(albumData);
    handleSetView('album');
  };

  if (showSplash) {
    return <SplashScreen onFinish={() => setShowSplash(false)} />;
  }

  if (!user) {
    return <AuthModal />;
  }

  const renderView = () => {
    switch (activeView) {
      case 'home': 
        return (
          <Home 
            onOpenAIMix={() => setIsAIMixOpen(true)} 
            onOpenInstallModal={() => setIsInstallOpen(true)} 
            onSelectArtist={handleSelectArtist}
            onSelectAlbum={handleSelectAlbum}
          />
        );
      case 'discover':
        return (
          <Discover 
            onSelectArtist={handleSelectArtist}
            onSelectAlbum={handleSelectAlbum}
          />
        );
      case 'search': 
        return <Search initialQuery={activeSearchQuery} />;
      case 'library': 
      case 'favorites':
      case 'downloads':
        return (
          <Library 
            setView={handleSetView} 
            onOpenSettings={() => setIsSettingsOpen(true)} 
            onInstall={handleInstallClick}
            showInstallButton={showInstallButton}
            onOpenAIMix={() => setIsAIMixOpen(true)}
            initialFilter={activeView === 'favorites' ? 'favorites' : activeView === 'downloads' ? 'downloads' : 'all'}
          />
        );
      case 'artist':
        return <ArtistProfile artist={selectedArtist} goBack={() => handleSetView(prevView)} />;
      case 'album':
        return <AlbumDetails album={selectedAlbum} goBack={() => handleSetView(prevView)} />;
      case 'playlist':
        return <PlaylistPage playlist={selectedPlaylist} goBack={() => handleSetView(prevView)} />;
      case 'podcasts':
        return <PodcastsView />;
      case 'profile':
        return (
          <UserProfileView 
            onOpenSubscription={() => setIsSubscriptionOpen(true)}
            onOpenSettings={() => setIsSettingsOpen(true)}
            onOpenEqualizer={() => setIsEqualizerOpen(true)}
          />
        );
      case 'spotify': return <SpotifyView />;
      case 'youtube': return <YoutubeView />;
      case 'spotify-callback': return <SpotifyCallback />;
      case 'admin': return <AdminDashboard goBack={() => handleSetView(prevView)} />;
      case 'nowplaying': 
        return (
          <NowPlaying 
            goBack={() => handleSetView(prevView)} 
            onOpenEqualizer={() => setIsEqualizerOpen(true)}
            initialTab={nowPlayingTab}
          />
        );
      default: 
        return (
          <Home 
            onOpenAIMix={() => setIsAIMixOpen(true)} 
            onOpenInstallModal={() => setIsInstallOpen(true)} 
            onSelectArtist={handleSelectArtist}
            onSelectAlbum={handleSelectAlbum}
          />
        );
    }
  };

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);
  const isNowPlaying = activeView === 'nowplaying';

  return (
    <div className={`app-container ${isNowPlaying ? 'np-mode' : ''} ${currentTrack ? 'has-player' : ''}`}>
      <div 
        className={`sidebar-overlay ${isSidebarOpen ? 'active' : ''}`} 
        onClick={() => setIsSidebarOpen(false)} 
      />
      <div className={`sidebar-wrapper ${isSidebarOpen ? 'active' : ''}`}>
        <Sidebar 
          setView={(view) => {
            handleSetView(view);
            setIsSidebarOpen(false);
          }} 
          activeView={activeView} 
          onClose={() => setIsSidebarOpen(false)}
          onOpenSettings={() => setIsSettingsOpen(true)}
          onInstall={handleInstallClick}
          showInstallButton={showInstallButton}
          onOpenAIMix={() => setIsAIMixOpen(true)}
          onOpenInstallModal={() => setIsInstallOpen(true)}
          onOpenSubscription={() => setIsSubscriptionOpen(true)}
        />
      </div>
      
      <main className="main-content">
        {!isNowPlaying && (
          <TopNav 
            activeView={activeView} 
            setView={handleSetView}
            toggleSidebar={toggleSidebar}
            onOpenSettings={() => setIsSettingsOpen(true)}
            onOpenEqualizer={() => setIsEqualizerOpen(true)}
            onOpenNotifications={() => setIsNotificationsOpen(true)}
            onOpenSubscription={() => setIsSubscriptionOpen(true)}
            onSearchQueryChange={(q) => setActiveSearchQuery(q)}
          />
        )}
        <div className="content-overflow-wrapper">
          <div key={activeView} className="animate-fade-in">
            {renderView()}
          </div>
        </div>
      </main>

      <div className="player-wrapper" style={isNowPlaying || !currentTrack ? { display: 'none' } : {}}>
        <PlayerBar onOpenNowPlaying={(tab) => {
          setNowPlayingTab(tab || 'artwork');
          handleSetView('nowplaying');
        }} />
      </div>

      {!isNowPlaying && (
        <BottomNav 
          activeView={activeView} 
          setView={handleSetView} 
          toggleSidebar={toggleSidebar} 
        />
      )}

      <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
      <AIMixModal isOpen={isAIMixOpen} onClose={() => setIsAIMixOpen(false)} />
      <InstallModal isOpen={isInstallOpen} onClose={() => setIsInstallOpen(false)} onInstallPrompt={handleInstallClick} hasPrompt={!!deferredPrompt} />
      <EqualizerModal isOpen={isEqualizerOpen} onClose={() => setIsEqualizerOpen(false)} />
      <SubscriptionModal isOpen={isSubscriptionOpen} onClose={() => setIsSubscriptionOpen(false)} />
      <NotificationsModal isOpen={isNotificationsOpen} onClose={() => setIsNotificationsOpen(false)} />
    </div>
  );
}

export default App;
