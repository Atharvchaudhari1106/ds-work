/**
 * Smart AI Search Engine — LLM & Fuzzy Intelligence for Music Search
 * 
 * Features:
 *   - Auto-corrects misspelled query strings (e.g. "arijit sing" -> "Arijit Singh")
 *   - Case-insensitive & symbol normalization
 *   - Phonetic & Transliteration mapping (e.g. "tum se hy" -> "Tum Se Hi")
 *   - Fuzzy Levenshtein distance matching over music database
 *   - Merges & ranks search results across endpoints (JioSaavn + YouTube)
 */

import { searchMusic } from './musicService';

// ─── Direct Typo & Transliteration AI Dictionary ────────────────
const LLM_QUERY_DICTIONARY = {
  // Artists
  'arijit sing': 'Arijit Singh',
  'arijiet singh': 'Arijit Singh',
  'arjit singh': 'Arijit Singh',
  'arijit': 'Arijit Singh',
  'taylor swft': 'Taylor Swift',
  'tailor swift': 'Taylor Swift',
  'taylor swif': 'Taylor Swift',
  'the weeknd': 'The Weeknd',
  'the weekend': 'The Weeknd',
  'weeknd': 'The Weeknd',
  'diljit dosangh': 'Diljit Dosanjh',
  'diljit dosanj': 'Diljit Dosanjh',
  'karan aujlaa': 'Karan Aujla',
  'karan ujla': 'Karan Aujla',
  'ap dhilon': 'AP Dhillon',
  'ap dillon': 'AP Dhillon',
  'ap dhillon': 'AP Dhillon',
  'dua leepa': 'Dua Lipa',
  'dua lipa': 'Dua Lipa',
  'billie elish': 'Billie Eilish',
  'billi eilish': 'Billie Eilish',
  'billie eilish': 'Billie Eilish',
  'travis scot': 'Travis Scott',
  'traviss scott': 'Travis Scott',
  'shreya ghosal': 'Shreya Ghoshal',
  'shreya gosal': 'Shreya Ghoshal',
  'post malon': 'Post Malone',
  'ed sheran': 'Ed Sheeran',
  'ed shiran': 'Ed Sheeran',
  'sidhu moosewala': 'Sidhu Moose Wala',
  'sidhu moose wala': 'Sidhu Moose Wala',
  'atif aslam': 'Atif Aslam',
  'atif aslamm': 'Atif Aslam',
  'badshah': 'Badshah',
  'badshahh': 'Badshah',
  'yo yo honey singh': 'Yo Yo Honey Singh',
  'honey singh': 'Yo Yo Honey Singh',
  'prateek kuhad': 'Prateek Kuhad',
  'anuv jain': 'Anuv Jain',

  // Songs
  'blinding lites': 'Blinding Lights',
  'blnding lights': 'Blinding Lights',
  'tum se hy': 'Tum Se Hi',
  'tumse hi': 'Tum Se Hi',
  'tum se he': 'Tum Se Hi',
  'channa merey': 'Channa Mereya',
  'channa meria': 'Channa Mereya',
  'kesariiya': 'Kesariya',
  'kesariya': 'Kesariya',
  'pasuri': 'Pasoori',
  'pasoori': 'Pasoori',
  'kahani sunoo': 'Kahani Suno',
  'kahani suno': 'Kahani Suno',
  'mi amor': 'Mi Amor',
  'cheques': 'Cheques',
  'checks': 'Cheques',
  'softly': 'Softly',
  'heeriye': 'Heeriye',
  'heriye': 'Heeriye',
  'jawan': 'Jawan',
  'animal': 'Animal',
  'kabir singh': 'Kabir Singh',
  'saibo': 'Saibo',
  'saybo': 'Saibo',
  'raatan lambiyan': 'Raatan Lambiyan',
  'ratan lambiyan': 'Raatan Lambiyan',
  'shayad': 'Shayad',
  'shayat': 'Shayad',
  'apna bana le': 'Apna Bana Le',
  'apna banale': 'Apna Bana Le',
  'chaleya': 'Chaleya',
  'chaliya': 'Chaleya',
  'satranga': 'Satranga',
  'o maahi': 'O Maahi',
  'o mahi': 'O Maahi'
};

// ─── Known Entity Master List for Fuzzy Matching ───────────────
const MASTER_MUSIC_ENTITIES = [
  'Arijit Singh', 'Taylor Swift', 'The Weeknd', 'Diljit Dosanjh', 'Karan Aujla',
  'AP Dhillon', 'Dua Lipa', 'Billie Eilish', 'Travis Scott', 'Drake', 'Shreya Ghoshal',
  'Post Malone', 'Ed Sheeran', 'Sidhu Moose Wala', 'Atif Aslam', 'Badshah',
  'Yo Yo Honey Singh', 'Prateek Kuhad', 'Anuv Jain', 'Pritam', 'AR Rahman',
  'Blinding Lights', 'Tum Se Hi', 'Channa Mereya', 'Kesariya', 'Pasoori',
  'Kahani Suno', 'Mi Amor', 'Cheques', 'Softly', 'Heeriye', 'Jawan', 'Animal',
  'Kabir Singh', 'Saibo', 'Raatan Lambiyan', 'Shayad', 'Apna Bana Le', 'Chaleya',
  'Satranga', 'O Maahi', 'Synthwave', 'Lofi Beats', 'Pop Hits', 'Hip Hop', 'Bollywood Hits'
];

// ─── Levenshtein Distance Calculator ────────────────────────────
function calculateLevenshtein(a, b) {
  const matrix = [];
  const aLen = a.length;
  const bLen = b.length;
  if (aLen === 0) return bLen;
  if (bLen === 0) return aLen;
  for (let i = 0; i <= bLen; i++) matrix[i] = [i];
  for (let j = 0; j <= aLen; j++) matrix[0][j] = j;
  for (let i = 1; i <= bLen; i++) {
    for (let j = 1; j <= aLen; j++) {
      const cost = b.charAt(i - 1) === a.charAt(j - 1) ? 0 : 1;
      matrix[i][j] = Math.min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost);
    }
  }
  return matrix[bLen][aLen];
}

/**
 * Clean & Normalize user input query string
 * Strips punctuation, extra spaces, and converts to lowercase
 */
export function normalizeQuery(query) {
  if (!query) return '';
  return query
    .toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * AI Query Corrector — Fix typos, casing, and misspellings
 * Returns { queryToSearch, isCorrected, originalQuery, matchedEntity }
 */
export function processAIQueryCorrection(userQuery) {
  if (!userQuery || typeof userQuery !== 'string') {
    return { queryToSearch: '', isCorrected: false, originalQuery: '' };
  }

  const rawTrimmed = userQuery.trim();
  const normalized = normalizeQuery(rawTrimmed);

  if (!normalized) {
    return { queryToSearch: rawTrimmed, isCorrected: false, originalQuery: rawTrimmed };
  }

  // 1. Direct LLM dictionary match
  if (LLM_QUERY_DICTIONARY[normalized]) {
    const corrected = LLM_QUERY_DICTIONARY[normalized];
    return {
      queryToSearch: corrected,
      isCorrected: corrected.toLowerCase() !== normalized,
      originalQuery: rawTrimmed,
      matchedEntity: corrected
    };
  }

  // 2. Fuzzy Levenshtein Distance Matching against master entities
  let bestEntity = null;
  let minDistance = Infinity;

  for (const entity of MASTER_MUSIC_ENTITIES) {
    const entityNorm = normalizeQuery(entity);
    
    // Direct match
    if (entityNorm === normalized) {
      return {
        queryToSearch: entity,
        isCorrected: entity.toLowerCase() !== rawTrimmed.toLowerCase(),
        originalQuery: rawTrimmed,
        matchedEntity: entity
      };
    }

    const dist = calculateLevenshtein(normalized, entityNorm);
    const maxAllowedDist = Math.max(1, Math.floor(entityNorm.length * 0.35)); // 35% tolerance threshold

    if (dist < minDistance && dist <= maxAllowedDist) {
      minDistance = dist;
      bestEntity = entity;
    }
  }

  if (bestEntity && minDistance <= 3) {
    return {
      queryToSearch: bestEntity,
      isCorrected: true,
      originalQuery: rawTrimmed,
      matchedEntity: bestEntity
    };
  }

  // 3. Token-level partial matching
  const words = normalized.split(/\s+/);
  if (words.length === 1 && words[0].length >= 4) {
    const singleWord = words[0];
    for (const entity of MASTER_MUSIC_ENTITIES) {
      const entityWords = normalizeQuery(entity).split(/\s+/);
      for (const ew of entityWords) {
        if (ew.length >= 4) {
          const d = calculateLevenshtein(singleWord, ew);
          if (d === 1 || (d === 2 && ew.length >= 6)) {
            return {
              queryToSearch: entity,
              isCorrected: true,
              originalQuery: rawTrimmed,
              matchedEntity: entity
            };
          }
        }
      }
    }
  }

  return {
    queryToSearch: rawTrimmed,
    isCorrected: false,
    originalQuery: rawTrimmed
  };
}

/**
 * Execute LLM-Powered Smart Search
 * Returns { tracks, isCorrected, correctedQuery, originalQuery, aiNotice }
 */
export async function performAISmartSearch(userQuery) {
  const correction = processAIQueryCorrection(userQuery);
  const targetQuery = correction.queryToSearch || userQuery;

  try {
    let tracks = await searchMusic(targetQuery);

    // If corrected query gave less than 3 results, fallback to original query search
    if (tracks.length < 3 && correction.isCorrected && correction.originalQuery !== targetQuery) {
      const fallbackTracks = await searchMusic(correction.originalQuery);
      const seen = new Set(tracks.map(t => t.id));
      for (const ft of fallbackTracks) {
        if (!seen.has(ft.id)) {
          tracks.push(ft);
          seen.add(ft.id);
        }
      }
    }

    return {
      tracks: tracks || [],
      isCorrected: correction.isCorrected,
      correctedQuery: targetQuery,
      originalQuery: correction.originalQuery,
      aiNotice: correction.isCorrected ? `✨ AI Corrected: Showing results for "${targetQuery}"` : null
    };
  } catch (err) {
    console.error('[AISmartSearch] Search error:', err);
    return {
      tracks: [],
      isCorrected: false,
      correctedQuery: targetQuery,
      originalQuery: userQuery,
      aiNotice: null
    };
  }
}
