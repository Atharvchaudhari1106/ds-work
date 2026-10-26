import React from 'react';
import { User, Crown, CheckCircle2, Music, Heart, Clock, Sliders, Shield, History, Sparkles, Award } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useAudio } from '../context/AudioContext';

const UserProfileView = ({ onOpenSubscription, onOpenSettings, onOpenEqualizer }) => {
  const { user } = useAuth();
  const { library, history = [] } = useAudio();

  return (
    <div className="user-profile-view animate-fade-in">
      {/* Profile Banner */}
      <div className="profile-hero-card glass-card">
        <div className="profile-hero-left">
          <div className="profile-avatar-wrapper">
            <div className="avatar-large">
              {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
            </div>
            <span className="profile-crown-badge" title="Hi-Res Premium Member">
              <Crown size={14} fill="currentColor" color="var(--neon-purple)" />
            </span>
          </div>

          <div className="profile-details-col">
            <div className="pro-tier-pill">
              <CheckCircle2 size={13} color="var(--neon-emerald)" /> AESTHETICORE PREMIUM
            </div>
            <h1 className="profile-user-name">{user?.name || 'AesthetiCore Member'}</h1>
            <p className="profile-user-email">{user?.email || 'member@aestheticore.music'}</p>
            <p className="profile-joined-text">Member since 2026 • Hi-Fi Audio Active</p>
          </div>
        </div>

        <div className="profile-hero-actions">
          <button className="btn-primary glow-purple flex-align-gap" onClick={onOpenSubscription}>
            <Crown size={16} /> Subscription Plan
          </button>
          <button className="btn-secondary-glass flex-align-gap" onClick={onOpenSettings}>
            <Sliders size={16} /> Account Settings
          </button>
        </div>
      </div>

      {/* Listening Stats Grid */}
      <section className="profile-stats-grid">
        <div className="stat-card glass-card">
          <div className="stat-icon-wrapper text-purple">
            <Clock size={24} />
          </div>
          <div className="stat-info">
            <span className="stat-value">148.5 hrs</span>
            <span className="stat-label">Listening Time This Month</span>
          </div>
        </div>

        <div className="stat-card glass-card">
          <div className="stat-icon-wrapper text-cyan">
            <Heart size={24} />
          </div>
          <div className="stat-info">
            <span className="stat-value">{library.length} Songs</span>
            <span className="stat-label">Favorites in Library</span>
          </div>
        </div>

        <div className="stat-card glass-card">
          <div className="stat-icon-wrapper text-emerald">
            <Award size={24} />
          </div>
          <div className="stat-info">
            <span className="stat-value">Synthwave & Lofi</span>
            <span className="stat-label">Top Listening Genre</span>
          </div>
        </div>

        <div className="stat-card glass-card">
          <div className="stat-icon-wrapper text-blue">
            <Sparkles size={24} />
          </div>
          <div className="stat-info">
            <span className="stat-value">24-bit Lossless</span>
            <span className="stat-label">Audio Stream Standard</span>
          </div>
        </div>
      </section>

      {/* Favorite Artists */}
      <section className="profile-section">
        <h3 className="section-title mb-16">Top Artists You Love</h3>
        <div className="artists-scroll-row">
          {[
            { name: 'The Weeknd', plays: '482 plays', img: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300&h=300&fit=crop' },
            { name: 'Dua Lipa', plays: '390 plays', img: 'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=300&h=300&fit=crop' },
            { name: 'Kavinsky', plays: '280 plays', img: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300&h=300&fit=crop' },
            { name: 'HOME', plays: '210 plays', img: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300&h=300&fit=crop' }
          ].map((art, idx) => (
            <div key={idx} className="artist-avatar-card glass-card">
              <div className="avatar-img-container">
                <img src={art.img} alt={art.name} />
              </div>
              <h4 className="artist-name">{art.name}</h4>
              <p className="artist-listeners">{art.plays}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default UserProfileView;
