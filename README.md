# 🇮🇹 Segneri

**A personal Italian vocabulary trainer, built as a Progressive Web App — designed for your phone.**

Segneri is a self-contained Italian learning app covering **2,000+ words across 20 themed packs**, with flashcards, quizzes, games, verb conjugation practice, and spaced repetition. No accounts, no ads, no server — everything runs in the browser and all progress is stored locally on your device.

**Live app:** https://mikeatredtreelabs.github.io/segneri/

---

## 📱 Phone-First by Design

Segneri is a PWA, but it isn't a desktop web app that happens to install — it's **built for the phone in your pocket**:

- **Install to your home screen** — on iPhone, open the app in Safari, tap **Share → Add to Home Screen**. It launches fullscreen like a native app, with its own icon and no browser chrome.
- **Works offline** — a service worker caches the entire app and all vocabulary packs, so you can study on the subway, on a plane, or anywhere without a connection.
- **Touch-first UI** — flip cards with a tap, large thumb-friendly buttons, bottom-sheet settings, and layouts sized for a phone screen.
- **Speaks to you** — Italian pronunciation via the Web Speech API, ideal for listening practice on the go.
- **Your data stays on your device** — progress, streaks, and XP live in `localStorage`. Nothing is sent anywhere.

It works fine in a desktop browser, but the phone is the intended home.

## ✨ Features

### Learning Modes
- **Flashcards** — flip cards with IPA pronunciation, example sentences, and spaced repetition
- **Quiz** — 4-choice multiple choice with XP rewards
- **Spritzi** ⚡ — a fast-paced 5-choice speed game with 3 lives
- **Challenge** — type the Italian yourself, with typo tolerance (Levenshtein distance)
- **Daily Quiz** — 10 self-graded flip cards plus a bonus verb conjugation challenge card
- **Listening mode** — hear the Italian, pick the meaning
- **Sentence / cloze mode** — fill in the blank from real example sentences
- **Pronunciation practice** — listen and repeat with text-to-speech

### Verb Power
- **Full conjugation tables for 68 verbs** across multiple tenses
- Inline **Conjugate** buttons in flashcards, quizzes, and word detail views
- Daily conjugation challenge cards drawn from random tenses

### Progress & Motivation
- Spaced repetition review queue that resurfaces words as you learn
- Per-pack **mastery %** and a **weak words** list
- **XP and daily streak** tracking with confetti celebrations 🎉
- **Word of the Day**
- Dark / light theme

## 📚 Vocabulary Packs (2,005 words)

| Pack | Words | Pack | Words |
|---|---|---|---|
| 👋 Greetings & Basics | 100 | 🏥 Health & Medical | 101 |
| 🍝 At the Restaurant | 100 | 🫀 The Human Body | 101 |
| 🔢 Numbers & Time | 100 | 👗 Clothing & Fashion | 101 |
| 👨‍👩‍👧 Family & Relationships | 100 | 🛍️ Shopping & Money | 101 |
| 🚂 Getting Around | 100 | ⚽ Sports & Leisure | 100 |
| 🏠 Home & Furniture | 100 | 🎭 Arts & Culture | 100 |
| 🌿 Nature & Weather | 100 | 💻 Technology & Media | 100 |
| 🐾 Animals | 100 | 💼 Work & Business | 100 |
| ❤️ Emotions & Personality | 100 | ⚡ Everyday Verbs | 100 |
| 🎨 Describing Things | 100 | 🔥 Advanced Verbs | 101 |

## 🛠️ Tech Stack

Deliberately simple — no frameworks, no build step, no dependencies:

- **Vanilla HTML / CSS / JavaScript**
- **Service worker** (network-first for app shell, full offline caching)
- **Web Speech API** for Italian text-to-speech
- **localStorage** for all progress persistence
- **GitHub Pages** for hosting

### Project Structure

```
├── index.html        # Landing page
├── app.html          # The app shell
├── app.js            # All app logic (modes, SRS, XP, conjugations)
├── sw.js             # Service worker (offline caching)
├── manifest.json     # PWA manifest
├── pack-*.js         # 20 vocabulary packs (100+ words each)
├── whats-new.html    # Release notes
├── demo.html         # Animated, narrated feature demo
└── icon-*.png/svg    # App icons
```

Each pack file registers itself on the global scope:

```js
window.PACK_food = {
  id: "food",
  name: "At the Restaurant",
  emoji: "🍝",
  words: [
    { it: "il pane", en: "bread", cat: "noun", ipa: "/il ˈpaːne/",
      ex: "Il pane è fresco.", exEn: "The bread is fresh." },
    // ...
  ]
};
```

## 🚀 Running Locally

No build step needed — just serve the folder:

```bash
git clone https://github.com/mikeatredtreelabs/segneri.git
cd segneri
python -m http.server 8000
# open http://localhost:8000
```

> Note: service workers and the Web Speech API require `localhost` or HTTPS.

## 🔄 Updates

The service worker uses a network-first strategy for the app shell, and each release bumps the cache name to push updates to installed devices. Current version: **v2.3.0**. See [What's New](https://mikeatredtreelabs.github.io/segneri/whats-new.html) for release notes, or the [animated demo](https://mikeatredtreelabs.github.io/segneri/demo.html) for a guided tour.

## 📖 About the Name

*Segneri* is a family name — this is a personal passion project, built for the joy of learning Italian (and building the tool to do it).

---

*Buono studio!* 🇮🇹
