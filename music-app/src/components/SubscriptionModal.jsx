import React, { useState } from 'react';
import { X, Crown, Check, Sparkles, Zap, ShieldCheck, HeartHandshake } from 'lucide-react';

const SubscriptionModal = ({ isOpen, onClose }) => {
  const [selectedPlan, setSelectedPlan] = useState('premium');

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop animate-fade-in" onClick={onClose}>
      <div className="subscription-modal-card glass-card animate-scale-up" onClick={e => e.stopPropagation()}>
        {/* Close Button */}
        <button className="modal-close-btn" onClick={onClose}>
          <X size={20} />
        </button>

        {/* Modal Header */}
        <div className="sub-modal-header">
          <div className="sub-crown-icon glow-purple">
            <Crown size={32} />
          </div>
          <h2 className="sub-modal-title">Elevate Your Audio Experience</h2>
          <p className="sub-modal-subtitle">
            Unlock 24-bit Lossless Spatial Audio, AI Mix Generator, Offline Downloads & Zero Ads.
          </p>
        </div>

        {/* Plans Grid */}
        <div className="plans-grid">
          {/* Plan 1: Free */}
          <div 
            className={`plan-card glass-card ${selectedPlan === 'free' ? 'active' : ''}`}
            onClick={() => setSelectedPlan('free')}
          >
            <h4 className="plan-name">Free Standard</h4>
            <div className="plan-price">$0 <span>/ month</span></div>
            <p className="plan-desc">Standard 160 kbps streaming with basic features.</p>
            <ul className="plan-checklist">
              <li><Check size={14} /> Standard 160 kbps audio</li>
              <li><Check size={14} /> Web player access</li>
              <li className="dimmed"><X size={14} /> No offline downloads</li>
              <li className="dimmed"><X size={14} /> No Hi-Res 24-bit Lossless</li>
            </ul>
          </div>

          {/* Plan 2: Premium (Featured) */}
          <div 
            className={`plan-card glass-card featured glow-purple ${selectedPlan === 'premium' ? 'active' : ''}`}
            onClick={() => setSelectedPlan('premium')}
          >
            <div className="featured-badge">MOST POPULAR</div>
            <h4 className="plan-name">Premium Individual</h4>
            <div className="plan-price">$9.99 <span>/ month</span></div>
            <p className="plan-desc">Full 320 kbps HQ audio + Unlimited AI Mix generation.</p>
            <ul className="plan-checklist">
              <li><Check size={14} color="var(--neon-emerald)" /> 320 kbps High Quality Audio</li>
              <li><Check size={14} color="var(--neon-emerald)" /> Unlimited Offline Downloads</li>
              <li><Check size={14} color="var(--neon-emerald)" /> AI Mix Generator Access</li>
              <li><Check size={14} color="var(--neon-emerald)" /> Ad-Free Streaming</li>
            </ul>
          </div>

          {/* Plan 3: Hi-Fi Lossless */}
          <div 
            className={`plan-card glass-card ${selectedPlan === 'hifi' ? 'active' : ''}`}
            onClick={() => setSelectedPlan('hifi')}
          >
            <div className="hifi-badge">AUDIO ENGINE PRO</div>
            <h4 className="plan-name">Hi-Fi Lossless Tier</h4>
            <div className="plan-price">$14.99 <span>/ month</span></div>
            <p className="plan-desc">24-bit / 192kHz Spatial Lossless + Dolby Atmos Engine.</p>
            <ul className="plan-checklist">
              <li><Check size={14} color="var(--neon-cyan)" /> 24-bit / 192kHz FLAC Lossless</li>
              <li><Check size={14} color="var(--neon-cyan)" /> Dolby Atmos Spatial Audio</li>
              <li><Check size={14} color="var(--neon-cyan)" /> Equalizer Pro & Crossfade</li>
              <li><Check size={14} color="var(--neon-cyan)" /> Early Access to New Releases</li>
            </ul>
          </div>
        </div>

        {/* Action Button */}
        <div className="sub-modal-footer">
          <button className="btn-primary sub-cta-btn glow-purple" onClick={() => {
            alert(`Selected plan: ${selectedPlan.toUpperCase()}! Plan activated.`);
            onClose();
          }}>
            <Sparkles size={18} /> Continue with {selectedPlan.toUpperCase()} Plan
          </button>
          <p className="sub-guarantee-text">Cancel anytime. 30-day money-back guarantee.</p>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionModal;
