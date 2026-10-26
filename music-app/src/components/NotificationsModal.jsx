import React from 'react';
import { X, Bell, Music2, Sparkles, Crown, CheckCircle2 } from 'lucide-react';

const NOTIFICATIONS = [
  { id: '1', title: 'New Release from The Weeknd', desc: 'Album "After Hours (Deluxe)" is now available in 24-bit Lossless Audio.', time: '10 min ago', type: 'release', unread: true },
  { id: '2', title: 'Weekly AI Mix Generated', desc: 'Your personalized Cyberpunk & Synthwave Mix for Friday is ready to stream.', time: '2 hours ago', type: 'ai', unread: true },
  { id: '3', title: 'Hi-Fi Dolby Atmos Active', desc: 'Your account is verified for 360 Spatial Audio playback on compatible devices.', time: '1 day ago', type: 'system', unread: false }
];

const NotificationsModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop animate-fade-in" onClick={onClose}>
      <div className="notifications-modal-card glass-card animate-scale-up" onClick={e => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>
          <X size={20} />
        </button>

        <div className="notif-header">
          <Bell size={22} className="text-purple" />
          <h3 className="notif-title">Notifications & Updates</h3>
        </div>

        <div className="notif-list">
          {NOTIFICATIONS.map(n => (
            <div key={n.id} className={`notif-item-card glass-card ${n.unread ? 'unread' : ''}`}>
              <div className="notif-icon-box">
                {n.type === 'release' && <Music2 size={18} color="var(--neon-purple)" />}
                {n.type === 'ai' && <Sparkles size={18} color="var(--neon-cyan)" />}
                {n.type === 'system' && <CheckCircle2 size={18} color="var(--neon-emerald)" />}
              </div>
              <div className="notif-content-col">
                <h4 className="notif-item-title">{n.title}</h4>
                <p className="notif-item-desc">{n.desc}</p>
                <span className="notif-item-time">{n.time}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default NotificationsModal;
