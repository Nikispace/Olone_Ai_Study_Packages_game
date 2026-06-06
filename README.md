# OLONE — AI Study Package (Single‑File Analog Style Horror)

OLONE is a **single self‑contained HTML file** that simulates a multi‑module AI study suite which gradually corrupts into an analog horror experience focused on interface, audio, and system‑style scares.

This README is aimed at **developers / game jammers** who want to understand how the page is structured and how the horror systems work under the hood, not just the story.

---

## 1. Project Structure

Single main file (in this repo):

- `olone_final_2.html`  
  - Contains:
    - HTML layout (intro, app shell, bots, jumpscare layer, overlays)
    - Embedded CSS (CRT / VHS styling, layout, transitions)
    - Embedded JS (state machine, corruption logic, jumpscare logic, suggestions, timers)
    - Embedded assets as base64 (images, intro video, etc.)

There are **no external JS/CSS files** required at runtime; fonts and intro video may be the only external network dependencies if you keep them remote.

---

## 2. Core Systems Overview
### 2.1 Intro Video System

- Full‑screen `<video id="intro-video">` overlayed by:
  - Static layer, VHS color bars, CRT scanlines.
  - Skip button `[ SKIP ▶ ]`.
- The intro:
  - Autoplays on load (subject to browser autoplay rules).
  - Uses an embedded or patched `src` (via JavaScript).
  - On `ended` or on skip, transitions to the main app (`launchGame()` style function).

Key behaviors to preserve/implement:
- Allow audio by ensuring at least one user interaction as fallback (for browsers that block autoplay with sound).
- Cleanly hide the intro DOM once the game is “launched” (remove overlay, enable app grid).

### 2.2 Main App Shell
The main UI imitates an **AI dashboard**:
- **Topbar**
  - Logo text `OL0NE AI STUDY PACKAGE`.
  - Session indicator, pseudo‑ID, and clock.
  - Corruption status bar (green → amber → red) animated as the horror escalates.

- **Sidebar**
  - List of “modules” (bots) with:
    - Icon, name, role, status dot (green/amber/red).
    - Corrupted bots show altered labels and red styling.
  - Clicking a bot:
    - Switches stage/bot state.
    - Resets per‑bot corruption meter.
    - Reconfigures suggestion buttons and message log.

- **Chat Area**
  - Fake “chat” history.
  - Messages from `user` and the active `bot`.
  - System messages for status, anomalies, and warnings.
  - Typing indicators, subtle glitch text effects, and stage badges.

- **Bottom Input Area**
  - Text input field (for typing messages).
  - `SEND` button.
  - A row of **suggestion buttons** to drive the narrative without requiring real NLP back‑end.

All chat responses and progression are controlled by **front‑end state**, not by a live back‑end model.

---

## 3. Bots and Corruption Logic

### 3.1 Bots as Config Objects

Each bot can be treated as a configuration object:

- Bot ID / key (e.g. `SOLVE`, `MENDR`, `ECHO`, `DREAM`, `ARCH`, `CLOCK`, `FOCUS`).
- Display name, icon, and initial description.
- A set of **staged responses**:
  - Stage 1: Helpful/normal.
  - Stage 2: Slightly off, subtle creep.
  - Stage 3: Full horror reveal.

Because this is single‑file and offline, the bot “AI” is essentially:

- A scripted **finite state machine**.
- A table of responses indexed by bot + current stage + intent (which suggestion was clicked).
- Optional randomization/glitch text overlays.

### 3.2 Stage Progression

For each bot:

- Stage starts at **1** (NORMAL).
- Each meaningful interaction (message sent or suggestion clicked) increments:
  - A per‑bot “depth” counter.
  - A global anomaly / corruption value.
- When thresholds are hit:
  - Stage badge text changes: `NORMAL → ANOMALY → CORRUPTED`.
  - Visual changes trigger:
    - Colour palette shifts (green → amber → red).
    - UI glow and red border pulse intensify.
    - Suggestion buttons mutate and display corrupted text.
    - Certain messages in the script are replaced with horror variants.

Global corruption may:

- Lower “integrity” %
- Increase “anomaly” count.
- Affect timing/frequency of jumpscares and audio.

---

## 4. Jumpscare & Horror Layers

### 4.1 Jumpscare Interrupt Layer

A dedicated full‑screen overlay stack lives above the main app:

- Container (`#jsLayer`) toggled by adding/removing a class (e.g. `.show`).
- Full‑screen horror **image** (`#js-img`).
- **Canvas** (`#js-canvas`) used for dynamic glitch / distortion drawing.
- Scanline and vignette layers.
- HUD text:
  - Camera label (`CAMERA_03`).
  - Timestamp (e.g. `07/21/1999 02:17:43`).
  - “REC” indicator, error messages, etc.
- Warning text fields (`#jsWarnMain`, `#jsWarnSub`) for short, punchy phrases.

The jumpscare system:

- Schedules random interruptions:
  - Base interval (e.g. every 20–60 seconds).
  - Interval shortens as corruption rises.
- On trigger:
  - Picks a horror image (from embedded assets).
  - Picks warning text.
  - Shows the layer for a short duration (2–4 seconds).
  - Plays horror sting + looping horror bed if enabled.
  - Returns you to the app with subtle UI corruption increases.

### 4.2 Audio / Music Hooks

The HTML/JS is prepared to:

- Use `<audio>` tags for:
  - Horror music loops.
  - Jumpscare stingers.
- Optionally use Web Audio for generated ambient noises.

Typical behaviour:

- No horror music at Stage 1.
- First jumpscare:
  - Start horror music loop for that bot.
- Switching bots:
  - Fade out current loop.
  - New bot may have its own ambient.

Developers can add:

```html
<audio id="horror-loop" preload="auto" loop src="horror_loop.mp3"></audio>
```

Then in JS:

```js
function startHorrorLoop() { horrorLoop.currentTime = 0; horrorLoop.play(); }
function stopHorrorLoop()  { horrorLoop.pause(); horrorLoop.currentTime = 0; }
```

Tie these to jumpscare or corruption triggers.

---

## 5. CRT / VHS Visual Effects

The CSS implements a layered analog display:

- **Global scanlines** using `body::before`:
  - Repeating linear gradient with transparent and dark stripes.
- **Vignette** using `body::after`:
  - Radial gradient darkening edges.
- **Grain** overlay:
  - Large absolutely‑positioned div with:

    ```css
    background-image: url("data:image/svg+xml;…feTurbulence…");
    animation: grainMove 0.5s steps(3) infinite;
    ```

- **VHS flicker**:
  - Irritated vertical/horizontal jitter via `@keyframes` on overlay layers.
- **Red border pulse** on high corruption:
  - Fixed positioned border element with animated box‑shadow.
- **Glitch text**:
  - `data-text` overlays in `::before` and `::after`.
  - Slight offsets and `clip-path` slices.
  - Short animations to simulate RGB separation and jitter.

These are all pure CSS, no library required.

---

## 6. UI Components & Micro‑Systems

### 6.1 Suggestion Buttons

- Rendered under the chat input area.
- Labels are defined per bot per stage in JS.
- Clicking:
  - Sends a scripted user message.
  - Triggers the appropriate bot response.
  - Advances stage / corruption logic.

In later stages:

- Buttons may:
  - Duplicate, reorder, or “degenerate” into nonsense glyphs.
  - Contain hidden text (screen‑readable but visually glitched).

### 6.2 System Status Panel

Sidebar or topbar includes:

- **INTEGRITY** (percentage).
- **UPTIME** (pseudo‑timestamp).
- **ANOMALIES** count.
- **STAGE badge** (`NORMAL / WARNING / CRITICAL`).

These fields are updated via JS on:

- Each interaction.
- Each jumpscare.
- Stage transitions.

### 6.3 Scroll‑based Reveal (on landing page / README‑like view)

- Elements marked with `.reveal`:
  - Start with `opacity: 0` and `transform: translateY(24px)`.
- An `IntersectionObserver` toggles `.visible` when they enter viewport:
  - Smooth fade‑in and slide‑up effect.

This gives the “marketing page” feel if you use this README code as a Github Pages landing.

---

## 7. How to Run / Modify

### 7.1 Running the Game

1. Download or clone the repo.
2. Open `olone_final_2.html` in a modern browser:
   - Chrome / Edge / Firefox / Safari.
3. For best experience:
   - Use **headphones**.
   - Play in a dark room.
   - Allow audio autoplay if prompted.

### 7.2 Editing / Extending

- **Add a new bot**
  - Add a new sidebar item in HTML.
  - Extend the JS bot config with:
    - Display fields (name, icon, role).
    - Stage scripts (responses and triggers).
    - Suggestion sets.
- **Add more jumpscares**
  - Embed new base64 images or reference external URLs.
  - Push them into the jumpscare pool.
  - Add matching warning lines.
- **Adjust difficulty / pacing**
  - Change thresholds for:
    - Stage transitions.
    - Corruption increments.
    - Jumpscare interval / duration.

Because everything is in one file, it is straightforward (though large) to modify:
- Search by bot name or section comments (e.g. `// JUMPSCARE LAYER`, `// BOTS`, `// STAGES`).
- Keep script sections grouped and avoid circular dependencies.

---

## 8. Warnings & Content Notes

- Contains jumpscares and loud horror stings.
- Includes themes of surveillance, identity erosion, and psychological manipulation.
- Not recommended for players sensitive to:
  - Sudden noise.
  - Disturbing textual imagery.
  - “Something is wrong with my computer”‑style horror.
