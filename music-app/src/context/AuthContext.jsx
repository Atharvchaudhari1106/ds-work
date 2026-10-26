import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [usersList, setUsersList] = useState([]);
  const [loading, setLoading] = useState(true);

  const getSavedUsers = () => {
    try {
      const raw = localStorage.getItem('music_app_all_users');
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  };

  const updateUsersStore = (currentUser) => {
    try {
      let list = getSavedUsers();
      if (currentUser && currentUser.userId) {
        const idx = list.findIndex(u => u.userId === currentUser.userId);
        const isAdmin = currentUser.userId.toLowerCase() === 'admin';
        const userRecord = {
          id: currentUser.id || Date.now(),
          name: currentUser.name || currentUser.userId,
          userId: currentUser.userId,
          role: isAdmin ? 'Admin' : 'Premium Member',
          status: 'Active',
          lastActive: Date.now(),
          joinedAt: currentUser.joinedAt || Date.now()
        };
        if (idx >= 0) {
          list[idx] = { ...list[idx], ...userRecord };
        } else {
          list.push(userRecord);
        }
      }
      localStorage.setItem('music_app_all_users', JSON.stringify(list));
      setUsersList(list);
    } catch (e) {
      console.error('Error updating users store', e);
    }
  };

  useEffect(() => {
    let savedUser = localStorage.getItem('music_app_user');
    let parsedUser = null;
    if (!savedUser) {
      const defaultUser = { 
        id: Date.now(), 
        name: 'admin', 
        userId: 'admin',
        joinedAt: Date.now()
      };
      localStorage.setItem('music_app_user', JSON.stringify(defaultUser));
      parsedUser = defaultUser;
    } else {
      try {
        parsedUser = JSON.parse(savedUser);
      } catch (e) {
        console.error('Failed to parse saved user', e);
        localStorage.removeItem('music_app_user');
      }
    }
    setUser(parsedUser);
    updateUsersStore(parsedUser);
    setLoading(false);
  }, []);

  const login = (credentials) => {
    if (credentials.userId && credentials.password) {
      const isAdmin = credentials.userId.toLowerCase() === 'admin';
      const newUser = { 
        id: Date.now(), 
        name: credentials.userId,
        userId: credentials.userId,
        role: isAdmin ? 'Admin' : 'Premium Member',
        joinedAt: Date.now()
      };
      setUser(newUser);
      localStorage.setItem('music_app_user', JSON.stringify(newUser));
      updateUsersStore(newUser);
      return true;
    }
    return false;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('music_app_user');
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <AuthContext.Provider value={{ user, usersList, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

