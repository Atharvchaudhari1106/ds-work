import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import cookieParser from 'cookie-parser';

import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

import authRoutes from './routes/auth.js';
import spotifyRoutes from './routes/spotify.js';
import youtubeRoutes from './routes/youtube.js';
import musicRoutes from './routes/music.js';
import configRoutes from './routes/config.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({
  origin: true,
  credentials: true
}));
app.use(express.json());
app.use(cookieParser());

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/spotify', spotifyRoutes);
app.use('/api/youtube', youtubeRoutes);
app.use('/api/music', musicRoutes);
app.use('/api/config', configRoutes);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'running',
    message: 'AesthetiCore Music API',
    endpoints: ['/api/spotify', '/api/youtube', '/api/auth', '/api/music']
  });
});

// Serve built frontend static files if available
const distPath = path.join(__dirname, '..', 'dist');
if (fs.existsSync(distPath)) {
  app.use(express.static(distPath));

  // Single Page Application (SPA) fallback
  app.use((req, res, next) => {
    if (req.path.startsWith('/api')) {
      return next();
    }
    res.sendFile(path.join(distPath, 'index.html'));
  });
}

// MongoDB is optional — only connect if URI is properly configured
// (Removed mandatory mongoose import to prevent crash when no DB is needed)

app.listen(PORT, '0.0.0.0', () => {
  console.log(`\n🎵 AesthetiCore Music Server running on http://localhost:${PORT}`);
  console.log(`   Spotify: ${process.env.SPOTIFY_CLIENT_ID ? '✅ Configured' : '❌ Not configured (set SPOTIFY_CLIENT_ID in .env)'}`);
  console.log(`   YouTube: ${process.env.YOUTUBE_API_KEY ? '✅ Configured' : '❌ Not configured (set YOUTUBE_API_KEY in .env)'}`);
  console.log('');
});

// Prevent Node Event Loop from exiting after startup
setInterval(() => {}, 60000);

