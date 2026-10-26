import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { LogIn, UserPlus, Lock, User } from 'lucide-react';

import logo from '../assets/logo.png';

const AuthModal = () => {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    
    if (userId.trim().length < 3) {
      setError('User ID must be at least 3 characters');
      return;
    }
    if (password.trim().length < 4) {
      setError('Password must be at least 4 characters');
      return;
    }

    const success = login({ userId, password });
    if (!success) {
      setError('Invalid login credentials');
    }
  };

  return (
    <div className="auth-modal-overlay">
      <div className="auth-modal animate-fade-in">
        <div className="auth-header">
          <div className="auth-logo">
            <img src={logo} alt="AesthetiCore" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
          </div>
          <h2>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
          <p>{isLogin ? 'Login to continue to AesthetiCore Music' : 'Start your musical journey today'}</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <User className="input-icon" size={20} />
            <input
              type="text"
              placeholder="User ID"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <Lock className="input-icon" size={20} />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          {error && <div className="auth-error">{error}</div>}
          
          <button type="submit" className="auth-submit-btn">
            {isLogin ? 'Login' : 'Sign Up'}
          </button>
        </form>

        <div className="auth-footer">
          <p onClick={() => setIsLogin(!isLogin)} className="toggle-auth">
            {isLogin ? "Don't have an account? Sign Up" : 'Already have an account? Login'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthModal;

