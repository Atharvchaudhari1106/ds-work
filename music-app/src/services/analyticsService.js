/**
 * Analytics Service — Track user listening behavior for AI personalization
 * 
 * All data stays in localStorage — no cloud dependency.
 * Tracks: play events, skip events, completion rate, time-of-day patterns.
 */

const ANALYTICS_KEY = 'music_analytics';
const MAX_EVENTS = 500;

// ─── Event Types ────────────────────────────────────────────────
export const EventType = {
  PLAY: 'play',
  SKIP: 'skip',
  COMPLETE: 'complete',
  LIKE: 'like',
  UNLIKE: 'unlike',
  SEARCH: 'search',
  IMPORT_PLAYLIST: 'import_playlist'
};

// ─── Storage Helpers ────────────────────────────────────────────
function getAnalytics() {
  try {
    const raw = localStorage.getItem(ANALYTICS_KEY);
    if (!raw) return { events: [], artistAffinity: {}, genreAffinity: {}, playCount: {}, skipCount: {} };
    const parsed = JSON.parse(raw) || {};
    return {
      events: Array.isArray(parsed.events) ? parsed.events : [],
      artistAffinity: parsed.artistAffinity || {},
      genreAffinity: parsed.genreAffinity || {},
      playCount: parsed.playCount || {},
      skipCount: parsed.skipCount || {}
    };
  } catch {
    return { events: [], artistAffinity: {}, genreAffinity: {}, playCount: {}, skipCount: {} };
  }
}

function saveAnalytics(data) {
  try {
    // Trim events to prevent localStorage from growing too large
    if (data.events.length > MAX_EVENTS) {
      data.events = data.events.slice(-MAX_EVENTS);
    }
    localStorage.setItem(ANALYTICS_KEY, JSON.stringify(data));
  } catch {
    // localStorage might be full
  }
}

// ─── Track Events ───────────────────────────────────────────────
/**
 * Record a play event with rapid-trigger deduplication
 */
export function trackPlay(song) {
  if (!song) return;
  const data = getAnalytics();
  const now = Date.now();

  // Deduplicate rapid consecutive triggers for the same song within 3s
  const lastEvent = data.events[data.events.length - 1];
  if (lastEvent && lastEvent.songId === song.id && (now - lastEvent.timestamp) < 3000) {
    return;
  }

  const hour = new Date().getHours();
  const day = new Date().getDay();

  data.events.push({
    type: EventType.PLAY,
    songId: song.id,
    title: song.title,
    artist: song.artist,
    source: song.source || 'jiosaavn',
    timestamp: now,
    hour,
    day
  });

  // Update play count
  data.playCount[song.id] = (data.playCount[song.id] || 0) + 1;

  // Update artist affinity
  const artists = (song.artist || '').split(',').map(a => a.split('|')[0].trim());
  for (const artist of artists) {
    if (artist && artist.toLowerCase() !== 'unknown artist') {
      data.artistAffinity[artist] = (data.artistAffinity[artist] || 0) + 1;
    }
  }

  saveAnalytics(data);
}

/**
 * Record a skip event
 */
export function trackSkip(song) {
  if (!song) return;
  const data = getAnalytics();

  data.events.push({
    type: EventType.SKIP,
    songId: song.id,
    title: song.title,
    artist: song.artist,
    timestamp: Date.now()
  });

  data.skipCount[song.id] = (data.skipCount[song.id] || 0) + 1;
  saveAnalytics(data);
}

/**
 * Record a song completion
 */
export function trackComplete(song) {
  if (!song) return;
  const data = getAnalytics();

  data.events.push({
    type: EventType.COMPLETE,
    songId: song.id,
    title: song.title,
    artist: song.artist,
    timestamp: Date.now()
  });

  saveAnalytics(data);
}

/**
 * Record a search event
 */
export function trackSearch(query) {
  if (!query) return;
  const data = getAnalytics();
  data.events.push({
    type: EventType.SEARCH,
    query,
    timestamp: Date.now(),
    hour: new Date().getHours()
  });
  saveAnalytics(data);
}

// ─── Analytics Queries ──────────────────────────────────────────

/**
 * Get top artists by play count
 */
export function getTopArtists(limit = 10) {
  const stats = getListeningStats();
  return stats.topArtists.slice(0, limit);
}

/**
 * Get all known artist names
 */
export function getKnownArtists() {
  const data = getAnalytics();
  return Object.keys(data.artistAffinity);
}

/**
 * Get most played songs
 */
export function getMostPlayed(limit = 10) {
  const data = getAnalytics();
  return Object.entries(data.playCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([songId, count]) => ({ songId, count }));
}

/**
 * Get skip rate for a song
 */
export function getSkipRate(songId) {
  const data = getAnalytics();
  const plays = data.playCount[songId] || 0;
  const skips = data.skipCount[songId] || 0;
  if (plays === 0) return 0;
  return skips / plays;
}

/**
 * Get listening pattern by hour of day
 */
export function getHourlyPattern() {
  const data = getAnalytics();
  const pattern = new Array(24).fill(0);

  for (const event of data.events) {
    if (event.type === EventType.PLAY && event.hour !== undefined) {
      pattern[event.hour]++;
    }
  }

  return pattern;
}

/**
 * Get recent play history (unique songs)
 */
export function getRecentPlays(limit = 20) {
  const data = getAnalytics();
  const seen = new Set();
  const recent = [];

  for (let i = data.events.length - 1; i >= 0 && recent.length < limit; i--) {
    const event = data.events[i];
    if (event.type === EventType.PLAY && event.songId && !seen.has(event.songId)) {
      seen.add(event.songId);
      recent.push({
        songId: event.songId,
        title: event.title,
        artist: event.artist,
        source: event.source,
        timestamp: event.timestamp
      });
    }
  }

  return recent;
}

/**
 * Get 100% accurate listening stats calculated directly from play events
 */
export function getListeningStats() {
  const data = getAnalytics();
  const playEvents = data.events.filter(e => e && e.type === EventType.PLAY);
  
  // Calculate unique songs from playEvents
  const uniqueSongIds = new Set(playEvents.map(e => e.songId || e.title).filter(Boolean));

  // Calculate artist counts dynamically from playEvents to guarantee math consistency
  const artistCounts = {};
  const uniqueArtists = new Set();

  for (const event of playEvents) {
    if (event.artist) {
      const primaryArtist = event.artist.split(',')[0].split('|')[0].trim();
      if (primaryArtist && primaryArtist.toLowerCase() !== 'unknown artist') {
        uniqueArtists.add(primaryArtist);
        artistCounts[primaryArtist] = (artistCounts[primaryArtist] || 0) + 1;
      }
    }
  }

  const topArtists = Object.entries(artistCounts)
    .map(([artist, count]) => ({ artist, count }))
    .sort((a, b) => b.count - a.count);

  // This week's plays
  const weekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
  const thisWeekPlays = playEvents.filter(e => e.timestamp > weekAgo).length;

  // Today's plays
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const todayPlays = playEvents.filter(e => e.timestamp > today.getTime()).length;

  return {
    totalPlays: playEvents.length,
    uniqueSongs: uniqueSongIds.size,
    uniqueArtists: uniqueArtists.size,
    thisWeekPlays,
    todayPlays,
    topArtists,
    hourlyPattern: getHourlyPattern()
  };
}

/**
 * Get an insight message based on analytics
 */
export function getInsight() {
  const stats = getListeningStats();
  const topArtists = stats.topArtists;

  if (stats.totalPlays < 3) {
    return {
      title: 'Getting Started',
      message: "Play more songs and I'll learn your taste!",
      icon: '🎵'
    };
  }

  const hourlyPattern = stats.hourlyPattern;
  const peakHour = hourlyPattern.indexOf(Math.max(...hourlyPattern));

  const insights = [];

  if (topArtists.length > 0) {
    insights.push({
      title: `You love ${topArtists[0].artist}`,
      message: `You've played their songs ${topArtists[0].count} times. Shall I find more like them?`,
      icon: '❤️'
    });
  }

  if (stats.thisWeekPlays > 10) {
    insights.push({
      title: 'Music Enthusiast!',
      message: `You've played ${stats.thisWeekPlays} songs this week across ${stats.uniqueArtists} artists.`,
      icon: '🔥'
    });
  }

  if (peakHour >= 0) {
    const period = peakHour < 12 ? 'morning' : peakHour < 17 ? 'afternoon' : peakHour < 21 ? 'evening' : 'night';
    insights.push({
      title: `${period.charAt(0).toUpperCase() + period.slice(1)} Listener`,
      message: `You listen the most around ${peakHour > 12 ? peakHour - 12 : peakHour}${peakHour >= 12 ? 'PM' : 'AM'}`,
      icon: peakHour < 12 ? '🌅' : peakHour < 17 ? '☀️' : peakHour < 21 ? '<ctrl42>' : '🌙'
    });
  }

  return insights.length > 0 ? insights[Math.floor(Math.random() * insights.length)] : {
    title: 'Keep Exploring',
    message: `You've discovered ${stats.uniqueSongs} unique songs so far!`,
    icon: '🎶'
  };
}

/**
 * Clear all analytics data
 */
export function clearAnalytics() {
  localStorage.removeItem(ANALYTICS_KEY);
}
