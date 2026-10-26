import React, { useState } from 'react';
import { X, Sliders, Volume2, Sparkles, Check, RefreshCw } from 'lucide-react';

const PRESETS = {
  flat: [0, 0, 0, 0, 0],
  bass: [8, 6, 2, 0, -2],
  vocal: [-2, 2, 6, 4, 1],
  electronic: [6, 4, -1, 3, 6],
  rock: [5, 3, -1, 4, 6],
  acoustic: [3, 2, 1, 4, 3]
};

const EqualizerModal = ({ isOpen, onClose }) => {
  const [activePreset, setActivePreset] = useState('bass');
  const [bands, setBands] = useState(PRESETS.bass);
  const [dolbyAtmos, setDolbyAtmos] = useState(true);
  const [crossfade, setCrossfade] = useState(4);
  const [gapless, setGapless] = useState(true);

  if (!isOpen) return null;

  const handlePresetSelect = (key) => {
    setActivePreset(key);
    setBands(PRESETS[key]);
  };

  const handleBandChange = (idx, value) => {
    const nextBands = [...bands];
    nextBands[idx] = parseFloat(value);
    setBands(nextBands);
    setActivePreset('custom');
  };

  const bandLabels = ['60 Hz', '230 Hz', '910 Hz', '3.6 kHz', '14 kHz'];

  return (
    <div className="modal-backdrop animate-fade-in" onClick={onClose}>
      <div className="equalizer-modal-card glass-card animate-scale-up" onClick={e => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>
          <X size={20} />
        </button>

        <div className="eq-modal-header">
          <div className="eq-icon-wrapper text-purple">
            <Sliders size={26} />
          </div>
          <div>
            <h2 className="eq-title">Audio Experience & Equalizer Pro</h2>
            <p className="eq-sub">Tune frequency response, crossfade, and Dolby Atmos Spatial Audio.</p>
          </div>
        </div>

        {/* Presets Row */}
        <div className="eq-presets-section">
          <span className="eq-section-label">PRESETS</span>
          <div className="eq-presets-pills">
            {Object.keys(PRESETS).map(pKey => (
              <button
                key={pKey}
                className={`eq-preset-pill ${activePreset === pKey ? 'active' : ''}`}
                onClick={() => handlePresetSelect(pKey)}
              >
                {pKey.toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        {/* 5-Band Visual Sliders */}
        <div className="eq-bands-container glass-card">
          {bands.map((gain, idx) => (
            <div key={idx} className="eq-band-col">
              <span className="gain-val-label">{gain > 0 ? `+${gain}` : gain} dB</span>
              <input
                type="range"
                min="-12"
                max="12"
                step="0.5"
                value={gain}
                onChange={e => handleBandChange(idx, e.target.value)}
                className="eq-vertical-slider"
              />
              <span className="band-freq-label">{bandLabels[idx]}</span>
            </div>
          ))}
        </div>

        {/* Spatial Audio & Audio Engine Switches */}
        <div className="eq-controls-group">
          <div className="eq-switch-row glass-card">
            <div>
              <h4 className="switch-title flex-align-gap">
                <Sparkles size={16} color="var(--neon-purple)" /> Dolby Atmos Spatial Audio
              </h4>
              <p className="switch-desc">360-degree immersive soundstage simulation.</p>
            </div>
            <label className="toggle-switch">
              <input type="checkbox" checked={dolbyAtmos} onChange={e => setDolbyAtmos(e.target.checked)} />
              <span className="slider-round" />
            </label>
          </div>

          <div className="eq-switch-row glass-card">
            <div>
              <h4 className="switch-title">Gapless Playback</h4>
              <p className="switch-desc">Seamless transitions between live album tracks.</p>
            </div>
            <label className="toggle-switch">
              <input type="checkbox" checked={gapless} onChange={e => setGapless(e.target.checked)} />
              <span className="slider-round" />
            </label>
          </div>

          <div className="eq-slider-row glass-card">
            <div className="row-header-flex">
              <span className="switch-title">Crossfade Songs</span>
              <span className="val-text">{crossfade} seconds</span>
            </div>
            <input
              type="range"
              min="0"
              max="12"
              step="1"
              value={crossfade}
              onChange={e => setCrossfade(parseInt(e.target.value))}
              className="eq-horizontal-slider"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default EqualizerModal;
