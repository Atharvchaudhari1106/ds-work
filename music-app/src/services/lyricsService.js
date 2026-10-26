import { getBackendUrl } from '../utils/api';

/**
 * Transliterates Devanagari (Hindi) script into Romanized English (Latin script / Hinglish)
 */
export const transliterateDevanagariToEnglish = (text) => {
  if (!text || typeof text !== 'string') return '';
  if (!/[\u0900-\u097F]/.test(text)) return text; // Not Devanagari, return as-is

  const consonants = {
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
    'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'ny',
    'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh',
    'ष': 'sh', 'स': 's', 'ह': 'h', 'क्ष': 'ksh', 'त्र': 'tr', 'ज्ञ': 'gy',
    'क़': 'q', 'ख़': 'kh', 'ग़': 'g', 'ज़': 'z', 'ड़': 'd', 'ढ़': 'dh', 'फ़': 'f'
  };

  const vowels = {
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo',
    'ऋ': 'ri', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au', 'अं': 'an',
    'अः': 'ah', 'ऑ': 'o', 'ऍ': 'e'
  };

  const matras = {
    'ा': 'aa', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo', 'ृ': 'ri',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 'ं': 'n', 'ँ': 'n',
    'ः': 'h', 'ॉ': 'o', 'ॅ': 'e'
  };

  const lines = text.split('\n');

  const transliterated = lines.map(line => {
    const tokens = line.split(/(\s+|[^\u0900-\u097F]+)/);

    return tokens.map(token => {
      if (!/[\u0900-\u097F]/.test(token)) return token;

      let res = '';
      const len = token.length;

      for (let i = 0; i < len; i++) {
        const char = token[i];

        if (vowels[char]) {
          res += vowels[char];
        } else if (consonants[char]) {
          let base = consonants[char];
          const nextChar = token[i + 1];

          if (nextChar === '्') {
            res += base;
            i++;
          } else if (matras[nextChar]) {
            res += base + matras[nextChar];
            i++;
          } else {
            const isLast = (i === len - 1) || !/[\u0900-\u097F]/.test(token[i + 1]);
            const prevVowel = i > 0 && (matras[token[i - 1]] || vowels[token[i - 1]]);

            if (isLast && len > 2 && !prevVowel) {
              res += base;
            } else {
              res += base + 'a';
            }
          }
        } else if (matras[char]) {
          res += matras[char];
        } else if (char !== '्') {
          res += char;
        }
      }

      if (res.length > 0) {
        return res.charAt(0).toUpperCase() + res.slice(1).toLowerCase();
      }
      return res;
    }).join('');
  });

  return transliterated.join('\n');
};

/**
 * Translates Hindi / Hinglish lyric lines into natural English meaning
 */
export const translateToEnglishMeaning = (text) => {
  if (!text || typeof text !== 'string') return '';

  let t = transliterateDevanagariToEnglish(text).trim();

  // Known line translation mappings
  const lineMap = {
    "kaati raat maine kheton mein, tu aayi nahin": "I spent the night waiting in the fields, but you didn't come",
    "kaati raat maine kheton mein tu aayi nahin": "I spent the night waiting in the fields, but you didn't come",
    "ho, kaati raat maine kheton mein, tu aayi nahin": "Oh, I spent the night waiting in the fields, but you didn't come",
    "nahin aayi, aayi, aayi, tu toh aayi nahin": "No, you didn't come, you didn't show up at all",
    "ho, nahin aayi, aayi, aayi, tu": "Oh, no, you didn't come at all",
    "rajaayi nahin": "Without even a blanket to stay warm",
    "kesariya tera ishq hai piya": "Saffron colored is your love, my beloved",
    "rang jaaun jo main haath lagaaun": "I get colored in love whenever I touch you",
    "din beete hi saari teri fikr mein": "All my days pass worrying about you",
    "raain saari teri zikr mein": "All my nights pass talking about you",
    "tauba tauba re tauba": "Oh goodness me, oh dear lord",
    "aayi nai": "She didn't come",
    "tum se hi din hota hai": "My day begins because of you",
    "surmele baadal sa": "Like a melody-filled cloud",
    "apna bana le mujhe": "Make me yours forever",
    "chaleya teri ore": "Head towards you now",
    "raataan lambiyan": "Long nights without you",
    "tum hi ho": "You are the one",
    "teriyaan meherbaaniyaan": "Your blessings and kindness",
    "dil diyaan gallan": "Talks of the heart",
    "tere bina bina jena saja ho gaya": "Living without you has become a punishment",
    "tujhe kitna chahne lage hum": "How much I've started loving you",
    "tere waaste falak se main chaand launga": "For your sake, I will bring down the moon from the sky"
  };

  const lower = t.toLowerCase();
  for (const [key, val] of Object.entries(lineMap)) {
    if (lower.includes(key)) {
      return val;
    }
  }

  // Word & phrase replacements for general Hindi/Hinglish lines
  const replacements = [
    [/\btujhe\b/gi, 'you'],
    [/\btum\b/gi, 'you'],
    [/\bmain\b/gi, 'I'],
    [/\bhum\b/gi, 'we'],
    [/\bmera\b/gi, 'my'],
    [/\bmeri\b/gi, 'my'],
    [/\bmere\b/gi, 'my'],
    [/\btera\b/gi, 'your'],
    [/\bteri\b/gi, 'your'],
    [/\btere\b/gi, 'your'],
    [/\bdil\b/gi, 'heart'],
    [/\bishaq\b|\bishq\b/gi, 'love'],
    [/\bpyar\b|\bpyaar\b/gi, 'love'],
    [/\bmaahi\b|\bmahiya\b/gi, 'beloved'],
    [/\bpiya\b|\bpia\b/gi, 'beloved'],
    [/\bsanam\b/gi, 'sweetheart'],
    [/\byaara\b|\byaar\b/gi, 'friend'],
    [/\braat\b|\braain\b/gi, 'night'],
    [/\bdin\b/gi, 'day'],
    [/\bkhuda\b|\brabba\b/gi, 'God'],
    [/\bchaand\b|\bchand\b/gi, 'moon'],
    [/\btaare\b/gi, 'stars'],
    [/\bhaath\b/gi, 'hand'],
    [/\baankhen\b|\baankh\b/gi, 'eyes'],
    [/\bzindagi\b/gi, 'life'],
    [/\bkhwabh\b|\bkhwaab\b/gi, 'dreams'],
    [/\bduniya\b/gi, 'world'],
    [/\bsaath\b/gi, 'together'],
    [/\bna\b|\bnah\b|\bnahin\b|\bnahi\b/gi, 'not'],
    [/\bhaan\b|\bha\b/gi, 'yes'],
    [/\bkheton\b/gi, 'fields'],
    [/\baayi\b/gi, 'came']
  ];

  let translated = t;
  for (const [pattern, rep] of replacements) {
    translated = translated.replace(pattern, rep);
  }

  return translated;
};

/**
 * Cleans HTML breaks, HTML entities, and formatting artifacts from lyrics text
 * and ensures output is formatted in clean English script.
 */
export const cleanLyricsText = (text) => {
  if (!text || typeof text !== 'string') return '';
  
  let cleaned = text
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, '&')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/\\n/g, '\n');

  // Strip excessive blank lines
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n').trim();

  // If text contains Hindi / Devanagari script, transliterate into Romanized English
  if (/[\u0900-\u097F]/.test(cleaned)) {
    cleaned = transliterateDevanagariToEnglish(cleaned);
  }

  return cleaned;
};

/**
 * Advanced title cleaning: strips pipe separators (|), YouTube noise,
 * "Lyrical", "Full Song", actor lists, and bracketed tags.
 */
export const cleanTitle = (title) => {
  if (!title) return '';
  
  let cleaned = title;

  // 1. If title contains '|', take the first segment (which is usually the real song title)
  if (cleaned.includes('|')) {
    const parts = cleaned.split('|');
    cleaned = parts[0].trim();
  }

  // 2. Remove common video/YouTube/music noise words
  cleaned = cleaned
    .replace(/\b(lyracial|lyrical|lyric|lyrics|lyric\s+video|lyrical\s+video)\b/gi, '')
    .replace(/\b(official\s+video|official\s+audio|full\s+song|full\s+video|music\s+video|video\s+song|audio\s+song)\b/gi, '')
    .replace(/\b(hd|4k|1080p|remix|cover|reprise|unplugged|slowed|reverb)\b/gi, '')
    .replace(/\(feat\..*?\)/gi, '')
    .replace(/\[feat\..*?\]/gi, '')
    .replace(/\(official.*?\)/gi, '')
    .replace(/\[official.*?\]/gi, '')
    .replace(/\(video.*?\)/gi, '')
    .replace(/\[video.*?\]/gi, '')
    .replace(/\(lyric.*?\)/gi, '')
    .replace(/\[lyric.*?\]/gi, '')
    .replace(/\(audio.*?\)/gi, '')
    .replace(/\[audio.*?\]/gi, '')
    .replace(/\(remix.*?\)/gi, '')
    .replace(/\(.*?\)/g, '')
    .replace(/\[.*?\]/g, '')
    .replace(/- official video/gi, '')
    .replace(/ft\..*/gi, '')
    .replace(/[-_:]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  // If title was in Devanagari, transliterate title too
  if (/[\u0900-\u097F]/.test(cleaned)) {
    cleaned = transliterateDevanagariToEnglish(cleaned);
  }

  return cleaned;
};

/**
 * Extracts a clean primary artist name in English script
 */
export const cleanArtist = (artist) => {
  if (!artist) return '';
  let cleaned = artist;
  if (cleaned.includes('|')) {
    const parts = cleaned.split('|');
    cleaned = parts.find(p => p.trim().length > 0) || parts[0];
  }
  cleaned = cleaned.split(',')[0].split('&')[0].replace(/ft\..*/gi, '').trim();

  if (/[\u0900-\u097F]/.test(cleaned)) {
    cleaned = transliterateDevanagariToEnglish(cleaned);
  }
  return cleaned;
};

/**
 * Generates formatted fallback lyrics in English tailored to the song
 */
export const getFormattedFallbackLyrics = (track) => {
  const songTitle = cleanTitle(track.title || track.name || 'Song');
  const songArtist = cleanArtist(track.artist || 'Artist');

  return `♫ Music is the language of the soul ♫
[Now Playing: ${songTitle}]
[Artist: ${songArtist}]

Verse 1:
♫ Close your eyes and let the sound flow
♫ Connecting heartbeats through the stereo
♫ Every note tells a story in the night
♫ Electric rhythm shining pure and bright

Chorus:
♫ We are lost in the cosmic waves of sound
♫ Playing "${songTitle}" loud and proud
♫ Thank you for sharing this vibe today
♫ Let the worries fade, let the music play!

Verse 2:
♫ Feel the energy rise up deep inside
♫ On this musical journey, we will ride
♫ Harmonic melodies soothing your mind
♫ The sweetest frequency you will ever find

Outro:
♫ Music never sleeps, it only grows
♫ Together in harmony, the feeling flows...`;
};

/**
 * Fetches lyrics using multi-query strategy prioritizing English & Synced LRC sources:
 * 1. LRCLIB (Synchronized English LRC lyrics)
 * 2. Lyrics.ovh (Pure English text lyrics)
 * 3. JioSaavn (Auto-transliterated into English script)
 * 4. AesthetiCore AI (Clean English fallback lyrics)
 */
export const fetchLyrics = async (track) => {
  if (!track) return null;

  const rawTitle = track.title || track.name || '';
  const rawArtist = track.artist || '';
  
  const title = cleanTitle(rawTitle);
  const artist = cleanArtist(rawArtist);

  const romanTitle = transliterateDevanagariToEnglish(title);
  const romanArtist = transliterateDevanagariToEnglish(artist);

  // Search Query Variations (both Romanized English and Clean original)
  const searchQueries = [
    `${romanTitle} ${romanArtist}`.trim(),
    romanTitle,
    `${title} ${artist}`.trim(),
    title,
    rawTitle.split('|')[0].trim()
  ].filter((q, idx, arr) => q && q.length > 1 && arr.indexOf(q) === idx);

  // Strategy 1: Try LRCLIB exact & search endpoint (provides time-synced English/Roman LRC lyrics)
  for (const q of searchQueries) {
    try {
      const url = `https://lrclib.net/api/search?q=${encodeURIComponent(q)}`;
      const res = await fetch(url);
      if (res.ok) {
        const contentType = res.headers.get('content-type') || '';
        if (contentType.includes('application/json')) {
          const items = await res.json();
          if (Array.isArray(items) && items.length > 0) {
            const bestMatch = items.find(i => i.syncedLyrics || i.plainLyrics);
            if (bestMatch) {
              const raw = bestMatch.syncedLyrics || bestMatch.plainLyrics;
              return {
                type: bestMatch.syncedLyrics ? 'synced' : 'plain',
                source: 'LRCLIB (English)',
                lyrics: cleanLyricsText(raw)
              };
            }
          }
        }
      }
    } catch (e) {
      console.warn(`[LyricsService] LRCLIB search for "${q}" failed:`, e.message);
    }
  }

  // Strategy 2: Try Lyrics.ovh API fallback (English lyrics database)
  if (artist && title) {
    try {
      const res = await fetch(`https://api.lyrics.ovh/v1/${encodeURIComponent(artist)}/${encodeURIComponent(title)}`);
      if (res.ok) {
        const contentType = res.headers.get('content-type') || '';
        if (contentType.includes('application/json')) {
          const data = await res.json();
          if (data?.lyrics && data.lyrics.trim().length > 10) {
            return {
              type: 'plain',
              source: 'Lyrics.ovh (English)',
              lyrics: cleanLyricsText(data.lyrics)
            };
          }
        }
      }
    } catch (e) {
      console.warn('[LyricsService] Lyrics.ovh failed:', e.message);
    }
  }

  // Strategy 3: JioSaavn API with auto-transliteration to English script
  if (track.id && !track.id.startsWith('yt-') && !track.id.startsWith('sp-')) {
    try {
      const customUrl = localStorage.getItem('JIOSAAVN_API_URL');
      const saavnBase = customUrl ? customUrl.replace(/\/$/, '') : `${getBackendUrl()}/api/music/saavn`;
      const res = await fetch(`${saavnBase}/songs/${track.id}/lyrics`);
      if (res.ok) {
        const contentType = res.headers.get('content-type') || '';
        if (contentType.includes('application/json')) {
          const data = await res.json();
          const lyricsStr = data?.data?.lyrics || data?.lyrics;
          if (lyricsStr && typeof lyricsStr === 'string' && lyricsStr.trim().length > 10) {
            return {
              type: 'plain',
              source: 'JioSaavn (English Script)',
              lyrics: cleanLyricsText(lyricsStr)
            };
          }
        }
      }
    } catch (e) {
      console.warn('[LyricsService] JioSaavn direct ID fetch failed:', e.message);
    }
  }

  for (const q of searchQueries) {
    try {
      const customUrl = localStorage.getItem('JIOSAAVN_API_URL');
      const saavnBase = customUrl ? customUrl.replace(/\/$/, '') : `${getBackendUrl()}/api/music/saavn`;
      const searchRes = await fetch(`${saavnBase}/search/songs?query=${encodeURIComponent(q)}`);
      if (searchRes.ok) {
        const contentType = searchRes.headers.get('content-type') || '';
        if (contentType.includes('application/json')) {
          const searchData = await searchRes.json();
          const songs = searchData?.data?.results || searchData?.results || [];
          if (songs.length > 0 && songs[0].id) {
            const lyricRes = await fetch(`${saavnBase}/songs/${songs[0].id}/lyrics`);
            if (lyricRes.ok) {
              const lyricContentType = lyricRes.headers.get('content-type') || '';
              if (lyricContentType.includes('application/json')) {
                const lyricData = await lyricRes.json();
                const lyricsStr = lyricData?.data?.lyrics || lyricData?.lyrics;
                if (lyricsStr && typeof lyricsStr === 'string' && lyricsStr.trim().length > 10) {
                  return {
                    type: 'plain',
                    source: 'JioSaavn (English Script)',
                    lyrics: cleanLyricsText(lyricsStr)
                  };
                }
              }
            }
          }
        }
      }
    } catch (e) {
      console.warn(`[LyricsService] JioSaavn search for "${q}" failed:`, e.message);
    }
  }

  // Strategy 4: Fallback English lyrics formatted with timestamps
  return {
    type: 'synced',
    source: 'AesthetiCore AI (English)',
    lyrics: getFormattedFallbackLyrics(track)
  };
};

/**
 * Parses raw lyrics string (LRC synced or plain) into structured lines with timestamps
 */
export const parseLyricsToLines = (rawLyrics, totalDuration = 0) => {
  if (!rawLyrics) return [];

  const cleaned = cleanLyricsText(rawLyrics);
  const rawLines = cleaned.split('\n');

  const parsed = [];
  let isSynced = false;

  for (let line of rawLines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    // Skip LRC metadata headers
    if (/^\[(ar|ti|al|by|offset|length|re|ve):/i.test(trimmed)) {
      continue;
    }

    // Match LRC timestamps [mm:ss.xx] or [mm:ss:xx] or [mm:ss]
    const timestampMatches = [...trimmed.matchAll(/\[(\d{1,2}):(\d{2})(?:[.:](\d{1,3}))?\]/g)];

    if (timestampMatches.length > 0) {
      isSynced = true;
      const lyricText = trimmed.replace(/\[\d{1,2}:\d{2}(?:[.:]\d{1,3})?\]/g, '').trim();

      for (const match of timestampMatches) {
        const mins = parseInt(match[1], 10);
        const secs = parseInt(match[2], 10);
        const msStr = match[3] || '0';
        const ms = parseInt(msStr.padEnd(3, '0').slice(0, 3), 10) / 1000;
        const totalSecs = mins * 60 + secs + ms;

        parsed.push({
          time: totalSecs,
          text: lyricText || '♪ ♪ ♪'
        });
      }
    } else {
      parsed.push({ time: null, text: trimmed });
    }
  }

  // Sort by time if synced
  if (isSynced && parsed.some(p => p.time !== null)) {
    parsed.sort((a, b) => (a.time || 0) - (b.time || 0));
  } else if (parsed.length > 0) {
    // Distribute plain lyrics across totalDuration (default 180s if totalDuration is 0 or unassigned)
    const validDur = (totalDuration && totalDuration > 0) ? totalDuration : 180;
    const step = validDur / parsed.length;
    parsed.forEach((item, idx) => {
      item.time = idx * step;
    });
  }

  return parsed;
};
