/**
 * Music Intelligence — Smart queue management & recommendation orchestration
 * 
 * Combines AI Engine + Analytics to provide:
 *   - Smart auto-queue when current queue ends
 *   - "Because you listened to X" discovery
 *   - Context-aware next-track selection
 */

import { buildUserProfile, getSmartRecommendations, detectMood, classifyByMood } from './aiEngine';
import { getRecentPlays, getTopArtists, getSkipRate } from './analyticsService';
import { searchMusic, shuffleArray } from './musicService';
import { getRecentSearchTerms } from './searchHistory';

/**
 * Get smart next-track recommendations when the queue is exhausted or populating.
 * Uses a combination of:
 *   1. User's recent search queries & affinity
 *   2. Current track artist & title similarity
 *   3. Current track mood continuity & AI listening profile
 * 
 * @param {Object} currentTrack - The currently playing track
 * @param {Array} library - User's liked songs
 * @param {Array} currentQueue - Current playback queue (to avoid duplicates)
 * @returns {Promise<Array>} Recommended tracks
 */
export async function getSmartNextTracks(currentTrack, library = [], currentQueue = []) {
  if (!currentTrack) return [];

  const results = [];
  const queueIds = new Set(currentQueue.map(t => t.id));
  const currentMood = detectMood(currentTrack);

  // 1. Search for tracks matching User's Recent Search History
  try {
    const recentSearches = getRecentSearchTerms(6);
    if (recentSearches && recentSearches.length > 0) {
      const sampledTerms = shuffleArray(recentSearches).slice(0, 3);
      for (const term of sampledTerms) {
        const searchResults = await searchMusic(term);
        const filtered = searchResults
          .filter(s => s.streamUrl && !queueIds.has(s.id) && s.id !== currentTrack.id)
          .filter(s => getSkipRate(s.id) < 0.7);
        
        if (filtered.length > 0) {
          const shuffled = shuffleArray(filtered).slice(0, 3);
          results.push(...shuffled);
        }
      }
    }
  } catch (err) {
    console.warn('[MusicIntelligence] User search next-track query failed:', err.message);
  }

  // 2. Search for similar songs by the same primary artist
  try {
    const mainArtist = (currentTrack.artist || '').split(',')[0].trim();
    if (mainArtist) {
      const artistSongs = await searchMusic(mainArtist);
      const filtered = artistSongs
        .filter(s => s.streamUrl && !queueIds.has(s.id) && s.id !== currentTrack.id && !results.find(r => r.id === s.id))
        .filter(s => getSkipRate(s.id) < 0.7);
      results.push(...shuffleArray(filtered).slice(0, 4));
    }
  } catch (err) {
    console.warn('[MusicIntelligence] Artist search failed:', err.message);
  }

  // 3. Search by track title to find similar/related songs
  try {
    const titleWords = currentTrack.title
      .replace(/\(.*?\)/g, '')
      .replace(/\[.*?\]/g, '')
      .split(/\s+/)
      .filter(w => w.length > 2)
      .slice(0, 3)
      .join(' ');
    
    if (titleWords) {
      const similar = await searchMusic(titleWords);
      const newSongs = similar
        .filter(s => s.streamUrl && !queueIds.has(s.id) && s.id !== currentTrack.id && !results.find(r => r.id === s.id))
        .slice(0, 3);
      results.push(...newSongs);
    }
  } catch (err) {
    console.warn('[MusicIntelligence] Title search failed:', err.message);
  }

  // 4. If we have library, use AI mood recommendations
  if (library.length > 3) {
    const recentPlays = getRecentPlays(10).map(rp => ({
      id: rp.songId,
      title: rp.title,
      artist: rp.artist
    }));
    const profile = buildUserProfile(library, recentPlays);

    try {
      const moodQuery = currentMood.mood === 'happy' ? 'bollywood hits' :
                         currentMood.mood === 'sad' ? 'emotional songs' :
                         currentMood.mood === 'energetic' ? 'party songs' :
                         currentMood.mood === 'romantic' ? 'love songs' :
                         currentMood.mood === 'chill' ? 'chill music' : 'top songs';
      
      const moodSongs = await searchMusic(moodQuery);
      const scored = getSmartRecommendations(
        moodSongs.filter(s => s.streamUrl),
        profile,
        [...queueIds, currentTrack.id],
        5
      );
      results.push(...scored);
    } catch (err) {
      console.warn('[MusicIntelligence] Mood search failed:', err.message);
    }
  }

  // Deduplicate results
  const seen = new Set();
  const deduped = results.filter(r => {
    if (seen.has(r.id) || queueIds.has(r.id)) return false;
    seen.add(r.id);
    return true;
  });

  return shuffleArray(deduped).slice(0, 10);
}

/**
 * Generate "Because you listened to X" sections for the home page
 * 
 * @param {Array} library - User's liked songs
 * @returns {Promise<Array>} Array of { title, tracks, basedOn } sections
 */
export async function generateBecauseYouListened(library = []) {
  if (library.length < 2) return [];

  const topArtists = getTopArtists(3);
  const sections = [];

  for (const { artist } of topArtists) {
    try {
      const results = await searchMusic(artist);
      const libraryIds = new Set(library.map(t => t.id));
      const newSongs = results
        .filter(s => s.streamUrl && !libraryIds.has(s.id))
        .filter(s => {
          const lower = s.title.toLowerCase();
          return !['instrumental', 'karaoke', 'ringtone', 'bgm'].some(kw => lower.includes(kw));
        })
        .slice(0, 6);

      if (newSongs.length >= 3) {
        sections.push({
          id: `because-${artist}`,
          title: `Because you like ${artist}`,
          tracks: newSongs,
          basedOn: artist
        });
      }
    } catch (err) {
      console.warn(`[MusicIntelligence] Failed to get recs for ${artist}:`, err.message);
    }
  }

  return sections;
}

/**
 * Auto-organize library songs into smart playlists by mood
 * @param {Array} library - User's liked songs
 * @returns {Array} Smart playlists: { name, mood, emoji, gradient, tracks }
 */
export function autoOrganizeLibrary(library) {
  if (!library || library.length < 4) return [];

  const classified = classifyByMood(library);
  const playlists = [];

  const moodNames = {
    happy: { name: 'Good Vibes', emoji: '☀️' },
    sad: { name: 'In My Feels', emoji: '🌧️' },
    energetic: { name: 'Pump It Up', emoji: '⚡' },
    chill: { name: 'Chill Zone', emoji: '🌊' },
    romantic: { name: 'Love Songs', emoji: '💕' },
    dark: { name: 'After Dark', emoji: '🌑' }
  };

  for (const [mood, tracks] of Object.entries(classified)) {
    if (tracks.length >= 2) {
      const config = moodNames[mood] || { name: mood, emoji: '🎵' };
      playlists.push({
        id: `ai-${mood}-${Date.now()}`,
        name: `${config.emoji} ${config.name}`,
        mood,
        tracks,
        isAIGenerated: true,
        createdAt: new Date().toISOString()
      });
    }
  }

  return playlists.sort((a, b) => b.tracks.length - a.tracks.length);
}
