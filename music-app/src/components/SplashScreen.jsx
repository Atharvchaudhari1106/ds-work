import React, { useEffect, useState } from 'react';
import { Sparkles, Music2 } from 'lucide-react';
import logo from '../assets/logo.png';

const SplashScreen = ({ onFinish }) => {
  const [fade, setFade] = useState(false);

  useEffect(() => {
    const timer1 = setTimeout(() => setFade(true), 1600);
    const timer2 = setTimeout(() => onFinish(), 2100);
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, [onFinish]);

  return (
    <div className={`splash-screen-container ${fade ? 'fade-out' : ''}`}>
      <div className="splash-background-glow" />
      <div className="splash-content-box animate-scale-up">
        <div className="splash-logo-wrapper glow-purple">
          <img src={logo} alt="AesthetiCore Logo" className="splash-logo-img" />
        </div>
        <h1 className="splash-title">AesthetiCore</h1>
        <p className="splash-subtitle">
          <Sparkles size={14} className="text-cyan" /> ULTRA LOSSLESS MUSIC PLATFORM
        </p>

        <div className="splash-progress-bar">
          <div className="splash-progress-fill" />
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;
