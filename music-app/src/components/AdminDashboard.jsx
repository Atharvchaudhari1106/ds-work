import React, { useState, useEffect, useMemo } from 'react';
import {
  LayoutDashboard, Users, Music, BarChart3, Settings, TrendingUp,
  Play, SkipForward, Heart, Clock, ArrowUpRight, ArrowDownRight,
  Disc, Headphones, Radio, Mic2, Globe, Shield, Zap, Activity,
  Eye, Download, Trash2, Search, Filter, ChevronDown, ChevronRight,
  RefreshCw, Bell, AlertTriangle, CheckCircle, XCircle, MoreVertical,
  Volume2, ListMusic, Star, Calendar, Sun, Moon, Sunset, Sunrise,
  UserCheck, UserX, Crown, TrendingDown, PieChart, ArrowLeft, X
} from 'lucide-react';
import { useAudio } from '../context/AudioContext';
import { useAuth } from '../context/AuthContext';
import {
  getListeningStats, getRecentPlays, getMostPlayed,
  getHourlyPattern, getTopArtists, clearAnalytics
} from '../services/analyticsService';
import '../admin-dashboard.css';

// ─── Mini Chart Components ──────────────────────────────────────

const SparklineChart = ({ data, color = '#8B5CF6', height = 40 }) => {
  if (!data || data.length === 0) return null;
  const max = Math.max(...data, 1);
  const points = data.map((v, i) => {
    const x = (i / (data.length - 1)) * 100;
    const y = height - (v / max) * height;
    return `${x},${y}`;
  }).join(' ');
  
  return (
    <svg viewBox={`0 0 100 ${height}`} className="sparkline-svg" preserveAspectRatio="none">
      <defs>
        <linearGradient id={`grad-${color.replace('#','')}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.3" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      <polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        vectorEffect="non-scaling-stroke"
      />
      <polygon
        points={`0,${height} ${points} 100,${height}`}
        fill={`url(#grad-${color.replace('#','')})`}
      />
    </svg>
  );
};

const BarChart = ({ data, labels, color = '#8B5CF6', height = 120 }) => {
  if (!data || data.length === 0) return null;
  const max = Math.max(...data, 1);
  const barWidth = 100 / data.length;

  return (
    <svg viewBox={`0 0 100 ${height}`} className="bar-chart-svg" preserveAspectRatio="none">
      {data.map((v, i) => {
        const barH = (v / max) * (height - 20);
        const x = i * barWidth + barWidth * 0.15;
        const w = barWidth * 0.7;
        const y = height - barH;
        const isActive = v === Math.max(...data);
        return (
          <g key={i}>
            <rect
              x={x}
              y={y}
              width={w}
              height={barH}
              rx="2"
              fill={isActive ? color : `${color}66`}
              className="bar-rect"
            />
            {labels && labels[i] && (
              <text
                x={x + w / 2}
                y={height - 2}
                textAnchor="middle"
                fill="var(--text-subdued)"
                fontSize="3.5"
                fontFamily="Outfit"
              >
                {labels[i]}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
};

const DonutChart = ({ segments, size = 100 }) => {
  const total = segments.reduce((s, seg) => s + seg.value, 0) || 1;
  let cumulative = 0;
  const radius = 35;
  const circumference = 2 * Math.PI * radius;

  return (
    <svg viewBox="0 0 100 100" width={size} height={size} className="donut-chart">
      {segments.map((seg, i) => {
        const pct = seg.value / total;
        const dashArray = `${pct * circumference} ${circumference}`;
        const dashOffset = -cumulative * circumference;
        cumulative += pct;
        return (
          <circle
            key={i}
            cx="50" cy="50" r={radius}
            fill="none"
            stroke={seg.color}
            strokeWidth="8"
            strokeDasharray={dashArray}
            strokeDashoffset={dashOffset}
            strokeLinecap="round"
            className="donut-segment"
            style={{ transformOrigin: 'center', transform: 'rotate(-90deg)' }}
          />
        );
      })}
      <text x="50" y="48" textAnchor="middle" fill="var(--text-bright)" fontSize="14" fontWeight="700" fontFamily="Outfit">
        {total}
      </text>
      <text x="50" y="60" textAnchor="middle" fill="var(--text-subdued)" fontSize="5" fontFamily="Outfit">
        total
      </text>
    </svg>
  );
};

// ─── Helper Functions ───────────────────────────────────────────

function formatTimeAgo(timestamp) {
  if (!timestamp) return 'Recently';
  const diff = Date.now() - timestamp;
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}

function getTimeOfDay() {
  const hour = new Date().getHours();
  if (hour < 6) return { label: 'Night', icon: Moon, color: '#6366F1' };
  if (hour < 12) return { label: 'Morning', icon: Sunrise, color: '#F59E0B' };
  if (hour < 17) return { label: 'Afternoon', icon: Sun, color: '#EF4444' };
  if (hour < 21) return { label: 'Evening', icon: Sunset, color: '#EC4899' };
  return { label: 'Night', icon: Moon, color: '#6366F1' };
}

// ─── Admin Dashboard Component ──────────────────────────────────

const AdminDashboard = ({ goBack }) => {
  const { library, playlists, queue, currentTrack } = useAudio();
  const { user, usersList = [] } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [searchQuery, setSearchQuery] = useState('');
  const [refreshKey, setRefreshKey] = useState(0);
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const [liveTime, setLiveTime] = useState(new Date());

  // Live clock
  useEffect(() => {
    const timer = setInterval(() => setLiveTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Analytics data
  const stats = useMemo(() => getListeningStats(), [refreshKey]);
  const recentPlays = useMemo(() => getRecentPlays(20), [refreshKey]);
  const mostPlayed = useMemo(() => getMostPlayed(10), [refreshKey]);
  const hourlyData = useMemo(() => getHourlyPattern(), [refreshKey]);
  const topArtists = useMemo(() => getTopArtists(8), [refreshKey]);

  const timeOfDay = getTimeOfDay();
  const TimeIcon = timeOfDay.icon;

  // Generate weekly trend data (simulated from hourly pattern)
  const weeklyTrend = useMemo(() => {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    return days.map((day, i) => ({
      day,
      plays: Math.max(1, Math.floor(stats.totalPlays / 7 + (Math.random() - 0.5) * stats.totalPlays / 10))
    }));
  }, [stats.totalPlays, refreshKey]);

  // Source distribution
  const sourceDistribution = useMemo(() => {
    const sources = {};
    library.forEach(track => {
      const src = track.source || 'jiosaavn';
      sources[src] = (sources[src] || 0) + 1;
    });
    return Object.entries(sources).map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value,
      color: name === 'youtube' ? '#FF0000' : name === 'spotify' ? '#1DB954' : '#8B5CF6'
    }));
  }, [library]);

  // System health metrics
  const systemHealth = useMemo(() => {
    const storageUsed = JSON.stringify(localStorage).length;
    const maxStorage = 5 * 1024 * 1024; // 5MB typical
    return {
      storagePercent: Math.min(100, (storageUsed / maxStorage) * 100),
      storageUsed: (storageUsed / 1024).toFixed(1),
      totalTracks: library.length,
      totalPlaylists: playlists.length,
      queueLength: queue.length,
      isPlaying: !!currentTrack
    };
  }, [library, playlists, queue, currentTrack, refreshKey]);

  // Filter library based on search
  const filteredLibrary = useMemo(() => {
    if (!searchQuery) return library;
    const q = searchQuery.toLowerCase();
    return library.filter(t =>
      (t.title || '').toLowerCase().includes(q) ||
      (t.artist || '').toLowerCase().includes(q)
    );
  }, [library, searchQuery]);

  const handleRefresh = () => {
    setRefreshKey(k => k + 1);
  };

  const handleClearAnalytics = () => {
    clearAnalytics();
    setShowClearConfirm(false);
    setRefreshKey(k => k + 1);
  };

  const hourLabels = Array.from({ length: 24 }, (_, i) => {
    if (i % 4 === 0) return `${i === 0 ? '12' : i > 12 ? i - 12 : i}${i >= 12 ? 'p' : 'a'}`;
    return '';
  });

  // Tab definitions
  const tabs = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'content', label: 'Content', icon: Music },
    { id: 'users', label: 'Users', icon: Users },
    { id: 'system', label: 'System', icon: Settings },
  ];

  return (
    <div className="admin-dashboard">
      {/* Header */}
      <div className="admin-header">
        <div className="admin-header-left">
          <button className="admin-back-btn" onClick={goBack} title="Back">
            <ArrowLeft size={20} />
          </button>
          <div className="admin-title-group">
            <h1 className="admin-title">
              <Shield size={22} className="admin-shield-icon" />
              Admin Dashboard
            </h1>
            <span className="admin-subtitle">AesthetiCore Control Center</span>
          </div>
        </div>
        <div className="admin-header-right">
          <div className="admin-live-clock">
            <TimeIcon size={16} style={{ color: timeOfDay.color }} />
            <span>{liveTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</span>
          </div>
          <button className="admin-refresh-btn" onClick={handleRefresh} title="Refresh Data">
            <RefreshCw size={16} />
          </button>
          <div className="admin-status-badge">
            <span className="status-dot live"></span>
            Live
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="admin-tabs">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              className={`admin-tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <Icon size={16} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <div className="admin-content">
        {activeTab === 'overview' && (
          <div className="admin-tab-content animate-admin-in">
            {/* KPI Cards */}
            <div className="admin-kpi-grid">
              <div className="kpi-card kpi-purple">
                <div className="kpi-icon-wrap">
                  <Play size={20} />
                </div>
                <div className="kpi-info">
                  <span className="kpi-value">{stats.totalPlays.toLocaleString()}</span>
                  <span className="kpi-label">Total Plays</span>
                </div>
                <div className="kpi-trend up">
                  <ArrowUpRight size={14} />
                  <span>{stats.todayPlays} today</span>
                </div>
              </div>

              <div className="kpi-card kpi-blue">
                <div className="kpi-icon-wrap">
                  <Music size={20} />
                </div>
                <div className="kpi-info">
                  <span className="kpi-value">{stats.uniqueSongs.toLocaleString()}</span>
                  <span className="kpi-label">Unique Songs</span>
                </div>
                <div className="kpi-trend up">
                  <Disc size={14} />
                  <span>In library</span>
                </div>
              </div>

              <div className="kpi-card kpi-cyan">
                <div className="kpi-icon-wrap">
                  <Headphones size={20} />
                </div>
                <div className="kpi-info">
                  <span className="kpi-value">{stats.uniqueArtists.toLocaleString()}</span>
                  <span className="kpi-label">Artists Discovered</span>
                </div>
                <div className="kpi-trend up">
                  <TrendingUp size={14} />
                  <span>Growing</span>
                </div>
              </div>

              <div className="kpi-card kpi-emerald">
                <div className="kpi-icon-wrap">
                  <TrendingUp size={20} />
                </div>
                <div className="kpi-info">
                  <span className="kpi-value">{stats.thisWeekPlays.toLocaleString()}</span>
                  <span className="kpi-label">This Week</span>
                </div>
                <div className="kpi-trend up">
                  <Zap size={14} />
                  <span>Active</span>
                </div>
              </div>
            </div>

            {/* Charts Row */}
            <div className="admin-charts-row">
              {/* Listening Activity */}
              <div className="admin-card admin-card-lg">
                <div className="admin-card-header">
                  <div className="card-title-group">
                    <Activity size={18} className="card-icon" />
                    <h3>Listening Activity</h3>
                  </div>
                  <span className="card-badge">24h</span>
                </div>
                <div className="chart-container">
                  <BarChart
                    data={hourlyData}
                    labels={hourLabels}
                    color="#8B5CF6"
                    height={120}
                  />
                </div>
                <div className="chart-footer">
                  <span className="chart-footnote">
                    Peak: {hourlyData.indexOf(Math.max(...hourlyData))}:00 ({Math.max(...hourlyData)} plays)
                  </span>
                </div>
              </div>

              {/* Source Distribution */}
              <div className="admin-card admin-card-sm">
                <div className="admin-card-header">
                  <div className="card-title-group">
                    <PieChart size={18} className="card-icon" />
                    <h3>Sources</h3>
                  </div>
                </div>
                <div className="donut-container">
                  <DonutChart
                    segments={sourceDistribution.length > 0 ? sourceDistribution : [{ value: 1, color: '#333' }]}
                    size={120}
                  />
                </div>
                <div className="source-legend">
                  {sourceDistribution.map((src, i) => (
                    <div key={i} className="legend-item">
                      <span className="legend-dot" style={{ background: src.color }}></span>
                      <span className="legend-label">{src.name}</span>
                      <span className="legend-value">{src.value}</span>
                    </div>
                  ))}
                  {sourceDistribution.length === 0 && (
                    <div className="legend-item">
                      <span className="legend-label" style={{ color: 'var(--text-subdued)' }}>No data yet</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Bottom Row */}
            <div className="admin-bottom-row">
              {/* Top Artists */}
              <div className="admin-card">
                <div className="admin-card-header">
                  <div className="card-title-group">
                    <Star size={18} className="card-icon" />
                    <h3>Top Artists</h3>
                  </div>
                </div>
                <div className="top-artists-list">
                  {topArtists.length === 0 && (
                    <div className="empty-state-mini">
                      <Mic2 size={24} />
                      <p>Play songs to discover your top artists</p>
                    </div>
                  )}
                  {topArtists.slice(0, 6).map((artist, i) => (
                    <div key={i} className="top-artist-row">
                      <span className="artist-rank">#{i + 1}</span>
                      <div className="artist-avatar-sm">
                        {artist.artist.charAt(0).toUpperCase()}
                      </div>
                      <div className="artist-info-col">
                        <span className="artist-name-text">{artist.artist}</span>
                        <span className="artist-plays-text">{artist.count} plays</span>
                      </div>
                      <div className="artist-bar-wrap">
                        <div
                          className="artist-bar-fill"
                          style={{ width: `${(artist.count / (topArtists[0]?.count || 1)) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recent Activity Feed */}
              <div className="admin-card">
                <div className="admin-card-header">
                  <div className="card-title-group">
                    <Clock size={18} className="card-icon" />
                    <h3>Recent Activity</h3>
                  </div>
                  <span className="card-badge">{recentPlays.length}</span>
                </div>
                <div className="activity-feed">
                  {recentPlays.length === 0 && (
                    <div className="empty-state-mini">
                      <Radio size={24} />
                      <p>No recent plays yet</p>
                    </div>
                  )}
                  {recentPlays.slice(0, 8).map((play, i) => (
                    <div key={i} className="activity-item">
                      <div className="activity-icon-wrap">
                        <Play size={12} />
                      </div>
                      <div className="activity-info">
                        <span className="activity-title">{play.title}</span>
                        <span className="activity-meta">{play.artist} • {play.source}</span>
                      </div>
                      <span className="activity-time">{formatTimeAgo(play.timestamp)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="admin-tab-content animate-admin-in">
            {/* Deep Analytics */}
            <div className="admin-section-header">
              <h2><BarChart3 size={20} /> Deep Analytics</h2>
              <p>Detailed listening behavior and engagement metrics</p>
            </div>

            {/* Weekly Trend */}
            <div className="admin-card admin-card-full">
              <div className="admin-card-header">
                <div className="card-title-group">
                  <TrendingUp size={18} className="card-icon" />
                  <h3>Weekly Play Trend</h3>
                </div>
                <span className="card-badge">7 days</span>
              </div>
              <div className="weekly-trend-chart">
                {weeklyTrend.map((day, i) => (
                  <div key={i} className="trend-day-col">
                    <div className="trend-bar-wrapper">
                      <div
                        className="trend-bar"
                        style={{
                          height: `${(day.plays / Math.max(...weeklyTrend.map(d => d.plays), 1)) * 100}%`
                        }}
                      >
                        <span className="trend-bar-value">{day.plays}</span>
                      </div>
                    </div>
                    <span className="trend-day-label">{day.day}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Hourly Heatmap */}
            <div className="admin-card admin-card-full">
              <div className="admin-card-header">
                <div className="card-title-group">
                  <Clock size={18} className="card-icon" />
                  <h3>Hourly Listening Heatmap</h3>
                </div>
              </div>
              <div className="heatmap-grid">
                {hourlyData.map((count, hour) => {
                  const maxH = Math.max(...hourlyData, 1);
                  const intensity = count / maxH;
                  return (
                    <div
                      key={hour}
                      className="heatmap-cell"
                      style={{
                        background: `rgba(139, 92, 246, ${Math.max(0.08, intensity * 0.9)})`,
                        borderColor: intensity > 0.6 ? 'rgba(139, 92, 246, 0.5)' : 'transparent'
                      }}
                      title={`${hour}:00 — ${count} plays`}
                    >
                      <span className="heatmap-hour">{hour}</span>
                      <span className="heatmap-count">{count}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Most Played Songs */}
            <div className="admin-card admin-card-full">
              <div className="admin-card-header">
                <div className="card-title-group">
                  <Volume2 size={18} className="card-icon" />
                  <h3>Most Played Songs</h3>
                </div>
                <span className="card-badge">Top {mostPlayed.length}</span>
              </div>
              <div className="most-played-list">
                {mostPlayed.length === 0 && (
                  <div className="empty-state-mini">
                    <Disc size={28} />
                    <p>Play more songs to see your most played tracks</p>
                  </div>
                )}
                {mostPlayed.map((item, i) => {
                  const track = library.find(t => t.id === item.songId);
                  return (
                    <div key={i} className="most-played-row">
                      <span className="mp-rank">{i + 1}</span>
                      <div className="mp-thumb">
                        {track?.thumbnail ? (
                          <img src={track.thumbnail} alt="" />
                        ) : (
                          <Music size={16} />
                        )}
                      </div>
                      <div className="mp-info">
                        <span className="mp-title">{track?.title || item.songId}</span>
                        <span className="mp-artist">{track?.artist || 'Unknown'}</span>
                      </div>
                      <div className="mp-count-bar">
                        <div
                          className="mp-count-fill"
                          style={{ width: `${(item.count / (mostPlayed[0]?.count || 1)) * 100}%` }}
                        ></div>
                      </div>
                      <span className="mp-count-num">{item.count}×</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'content' && (
          <div className="admin-tab-content animate-admin-in">
            <div className="admin-section-header">
              <h2><Music size={20} /> Content Management</h2>
              <p>Manage your library tracks and playlists</p>
            </div>

            {/* Content Stats */}
            <div className="content-stats-row">
              <div className="content-stat-card">
                <Music size={24} />
                <div>
                  <span className="cs-value">{library.length}</span>
                  <span className="cs-label">Library Tracks</span>
                </div>
              </div>
              <div className="content-stat-card">
                <ListMusic size={24} />
                <div>
                  <span className="cs-value">{playlists.length}</span>
                  <span className="cs-label">Playlists</span>
                </div>
              </div>
              <div className="content-stat-card">
                <Volume2 size={24} />
                <div>
                  <span className="cs-value">{queue.length}</span>
                  <span className="cs-label">Queue Items</span>
                </div>
              </div>
            </div>

            {/* Search Bar */}
            <div className="admin-search-bar">
              <Search size={16} />
              <input
                type="text"
                placeholder="Search library tracks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <button className="search-clear-btn" onClick={() => setSearchQuery('')}>
                  <X size={14} />
                </button>
              )}
            </div>

            {/* Library Table */}
            <div className="admin-card admin-card-full">
              <div className="admin-card-header">
                <div className="card-title-group">
                  <ListMusic size={18} className="card-icon" />
                  <h3>Library ({filteredLibrary.length} tracks)</h3>
                </div>
              </div>
              <div className="admin-table-wrap">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Cover</th>
                      <th>Title</th>
                      <th>Artist</th>
                      <th>Source</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredLibrary.length === 0 && (
                      <tr>
                        <td colSpan="5" className="table-empty">
                          {searchQuery ? 'No tracks match your search' : 'Library is empty — start exploring music!'}
                        </td>
                      </tr>
                    )}
                    {filteredLibrary.slice(0, 50).map((track, i) => (
                      <tr key={track.id || i}>
                        <td className="table-num">{i + 1}</td>
                        <td>
                          <div className="table-thumb">
                            {track.thumbnail ? (
                              <img src={track.thumbnail} alt="" />
                            ) : (
                              <Music size={14} />
                            )}
                          </div>
                        </td>
                        <td className="table-title">{track.title || 'Untitled'}</td>
                        <td className="table-artist">{track.artist || 'Unknown'}</td>
                        <td>
                          <span className={`source-badge source-${(track.source || 'jiosaavn').toLowerCase()}`}>
                            {(track.source || 'JioSaavn').charAt(0).toUpperCase() + (track.source || 'JioSaavn').slice(1)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Playlists */}
            <div className="admin-card admin-card-full">
              <div className="admin-card-header">
                <div className="card-title-group">
                  <ListMusic size={18} className="card-icon" />
                  <h3>Playlists ({playlists.length})</h3>
                </div>
              </div>
              <div className="playlists-grid">
                {playlists.length === 0 && (
                  <div className="empty-state-mini" style={{ gridColumn: '1 / -1' }}>
                    <ListMusic size={28} />
                    <p>No playlists created yet</p>
                  </div>
                )}
                {playlists.map((pl, i) => (
                  <div key={pl.id} className="playlist-admin-card">
                    <div className="pac-cover">
                      {pl.thumbnail ? (
                        <img src={pl.thumbnail} alt="" />
                      ) : (
                        <ListMusic size={24} />
                      )}
                    </div>
                    <div className="pac-info">
                      <span className="pac-name">{pl.name}</span>
                      <span className="pac-tracks">{pl.tracks?.length || 0} tracks</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'users' && (
          <div className="admin-tab-content animate-admin-in">
            <div className="admin-section-header">
              <h2><Users size={20} /> User Accounts & Management</h2>
              <p>View active user profile, session details, and registered account statistics</p>
            </div>

            <div className="user-admin-grid">
              {/* Current Active User Card */}
              <div className="admin-card user-profile-card">
                <div className="user-profile-header">
                  <div className="user-admin-avatar">
                    <Crown size={20} className="crown-icon" />
                    <span>{(user?.name || user?.userId || 'A').charAt(0).toUpperCase()}</span>
                  </div>
                  <div className="user-admin-meta">
                    <h3>{user?.name || user?.userId || 'AesthetiCore User'}</h3>
                    <span className="user-role-badge">
                      <Shield size={12} /> {user?.role || (user?.userId?.toLowerCase() === 'admin' ? 'Admin' : 'Premium Member')}
                    </span>
                  </div>
                </div>
                <div className="user-detail-list">
                  <div className="user-detail-row">
                    <span className="ud-label">User ID</span>
                    <span className="ud-value">{user?.userId || 'admin'}</span>
                  </div>
                  <div className="user-detail-row">
                    <span className="ud-label">Status</span>
                    <span className="ud-value">
                      <span className="status-dot live"></span> Active Now
                    </span>
                  </div>
                  <div className="user-detail-row">
                    <span className="ud-label">Session</span>
                    <span className="ud-value">Current Session</span>
                  </div>
                  <div className="user-detail-row">
                    <span className="ud-label">Storage Used</span>
                    <span className="ud-value">{systemHealth.storageUsed} KB</span>
                  </div>
                  <div className="user-detail-row">
                    <span className="ud-label">Library</span>
                    <span className="ud-value">{library.length} tracks</span>
                  </div>
                  <div className="user-detail-row">
                    <span className="ud-label">Playlists</span>
                    <span className="ud-value">{playlists.length}</span>
                  </div>
                  <div className="user-detail-row">
                    <span className="ud-label">Total Plays</span>
                    <span className="ud-value">{stats.totalPlays}</span>
                  </div>
                </div>
              </div>

              {/* Engagement Summary */}
              <div className="admin-card user-engagement-card">
                <div className="admin-card-header">
                  <div className="card-title-group">
                    <Activity size={18} className="card-icon" />
                    <h3>Engagement Summary</h3>
                  </div>
                </div>
                <div className="engagement-metrics">
                  <div className="engagement-metric">
                    <div className="em-circle" style={{ '--pct': `${Math.min(100, stats.totalPlays)}%`, '--color': '#8B5CF6' }}>
                      <span>{stats.totalPlays}</span>
                    </div>
                    <span className="em-label">Plays</span>
                  </div>
                  <div className="engagement-metric">
                    <div className="em-circle" style={{ '--pct': `${Math.min(100, stats.uniqueSongs * 2)}%`, '--color': '#3B82F6' }}>
                      <span>{stats.uniqueSongs}</span>
                    </div>
                    <span className="em-label">Songs</span>
                  </div>
                  <div className="engagement-metric">
                    <div className="em-circle" style={{ '--pct': `${Math.min(100, stats.uniqueArtists * 5)}%`, '--color': '#06B6D4' }}>
                      <span>{stats.uniqueArtists}</span>
                    </div>
                    <span className="em-label">Artists</span>
                  </div>
                  <div className="engagement-metric">
                    <div className="em-circle" style={{ '--pct': `${Math.min(100, stats.thisWeekPlays * 3)}%`, '--color': '#10B981' }}>
                      <span>{stats.thisWeekPlays}</span>
                    </div>
                    <span className="em-label">This Week</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Registered Users Directory */}
            <div className="admin-card admin-card-full">
              <div className="admin-card-header">
                <div className="card-title-group">
                  <UserCheck size={18} className="card-icon" />
                  <h3>Registered Account Directory ({usersList.length || 1})</h3>
                </div>
                <span className="card-badge">System Users</span>
              </div>
              <div className="admin-table-wrap">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>User</th>
                      <th>Role</th>
                      <th>Status</th>
                      <th>Last Active</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(usersList.length > 0 ? usersList : [
                      {
                        userId: user?.userId || 'admin',
                        name: user?.name || user?.userId || 'admin',
                        role: user?.userId?.toLowerCase() === 'admin' ? 'Admin' : 'Premium Member',
                        status: 'Active',
                        lastActive: Date.now()
                      }
                    ]).map((u, i) => (
                      <tr key={u.userId || i}>
                        <td className="table-num">{i + 1}</td>
                        <td className="table-title">
                          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <div className="artist-avatar-sm" style={{ width: '28px', height: '28px', fontSize: '0.75rem' }}>
                              {(u.name || u.userId || 'U').charAt(0).toUpperCase()}
                            </div>
                            <span>{u.name || u.userId}</span>
                          </div>
                        </td>
                        <td>
                          <span className="user-role-badge" style={{ fontSize: '0.7rem', padding: '2px 8px' }}>
                            <Shield size={10} /> {u.role || (u.userId?.toLowerCase() === 'admin' ? 'Admin' : 'Premium Member')}
                          </span>
                        </td>
                        <td>
                          <span className="ud-value" style={{ fontSize: '0.78rem' }}>
                            <span className="status-dot live"></span> Active
                          </span>
                        </td>
                        <td className="table-artist" style={{ fontSize: '0.78rem' }}>
                          {formatTimeAgo(u.lastActive)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'system' && (
          <div className="admin-tab-content animate-admin-in">
            <div className="admin-section-header">
              <h2><Settings size={20} /> System Health</h2>
              <p>Monitor storage, performance, and data integrity</p>
            </div>

            <div className="system-grid">
              {/* Storage Card */}
              <div className="admin-card system-card">
                <div className="admin-card-header">
                  <div className="card-title-group">
                    <Download size={18} className="card-icon" />
                    <h3>Local Storage</h3>
                  </div>
                  <span className={`system-status-badge ${systemHealth.storagePercent > 80 ? 'warning' : 'healthy'}`}>
                    {systemHealth.storagePercent > 80 ? (
                      <><AlertTriangle size={12} /> Warning</>
                    ) : (
                      <><CheckCircle size={12} /> Healthy</>
                    )}
                  </span>
                </div>
                <div className="storage-meter">
                  <div className="storage-bar-bg">
                    <div
                      className="storage-bar-fill"
                      style={{
                        width: `${systemHealth.storagePercent}%`,
                        background: systemHealth.storagePercent > 80
                          ? 'linear-gradient(90deg, #F59E0B, #EF4444)'
                          : 'linear-gradient(90deg, #8B5CF6, #3B82F6)'
                      }}
                    ></div>
                  </div>
                  <div className="storage-labels">
                    <span>{systemHealth.storageUsed} KB used</span>
                    <span>~5 MB limit</span>
                  </div>
                </div>
              </div>

              {/* Status Cards */}
              <div className="admin-card system-card">
                <div className="admin-card-header">
                  <div className="card-title-group">
                    <Activity size={18} className="card-icon" />
                    <h3>Runtime Status</h3>
                  </div>
                  <span className="system-status-badge healthy">
                    <CheckCircle size={12} /> Online
                  </span>
                </div>
                <div className="system-status-list">
                  <div className="status-row">
                    <span className="sr-label">App State</span>
                    <span className="sr-value">
                      <span className="status-dot live"></span> Running
                    </span>
                  </div>
                  <div className="status-row">
                    <span className="sr-label">Now Playing</span>
                    <span className="sr-value">
                      {currentTrack ? (
                        <><span className="status-dot live"></span> {currentTrack.title?.substring(0, 20)}...</>
                      ) : (
                        <><span className="status-dot idle"></span> Idle</>
                      )}
                    </span>
                  </div>
                  <div className="status-row">
                    <span className="sr-label">Queue</span>
                    <span className="sr-value">{queue.length} tracks</span>
                  </div>
                  <div className="status-row">
                    <span className="sr-label">Library Size</span>
                    <span className="sr-value">{library.length} tracks</span>
                  </div>
                  <div className="status-row">
                    <span className="sr-label">Playlists</span>
                    <span className="sr-value">{playlists.length}</span>
                  </div>
                </div>
              </div>

              {/* Danger Zone */}
              <div className="admin-card system-card danger-zone-card">
                <div className="admin-card-header">
                  <div className="card-title-group">
                    <AlertTriangle size={18} className="card-icon danger-icon" />
                    <h3>Danger Zone</h3>
                  </div>
                </div>
                <div className="danger-zone-content">
                  <p className="danger-desc">
                    Clear all analytics and listening history data. This action cannot be undone.
                  </p>
                  {!showClearConfirm ? (
                    <button className="danger-btn" onClick={() => setShowClearConfirm(true)}>
                      <Trash2 size={16} />
                      Clear Analytics Data
                    </button>
                  ) : (
                    <div className="danger-confirm">
                      <p>Are you sure? This will permanently delete all listening data.</p>
                      <div className="danger-confirm-actions">
                        <button className="danger-btn-confirm" onClick={handleClearAnalytics}>
                          <Trash2 size={14} /> Yes, Clear Everything
                        </button>
                        <button className="danger-btn-cancel" onClick={() => setShowClearConfirm(false)}>
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
