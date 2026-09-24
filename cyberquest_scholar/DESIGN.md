---
name: CyberQuest Scholar
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e18'
  surface-container-low: '#171b26'
  surface-container: '#1c1f2a'
  surface-container-high: '#262a35'
  surface-container-highest: '#313540'
  on-surface: '#dfe2f1'
  on-surface-variant: '#b9cbb9'
  inverse-surface: '#dfe2f1'
  inverse-on-surface: '#2c303b'
  outline: '#849585'
  outline-variant: '#3b4b3d'
  surface-tint: '#00e479'
  primary: '#f1ffef'
  on-primary: '#003919'
  primary-container: '#00ff88'
  on-primary-container: '#007139'
  inverse-primary: '#006d37'
  secondary: '#ffb693'
  on-secondary: '#561f00'
  secondary-container: '#fe6b00'
  on-secondary-container: '#572000'
  tertiary: '#f8fbff'
  on-tertiary: '#00354a'
  tertiary-container: '#bae4ff'
  on-tertiary-container: '#00698f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#60ff99'
  primary-fixed-dim: '#00e479'
  on-primary-fixed: '#00210c'
  on-primary-fixed-variant: '#005228'
  secondary-fixed: '#ffdbcc'
  secondary-fixed-dim: '#ffb693'
  on-secondary-fixed: '#351000'
  on-secondary-fixed-variant: '#7a3000'
  tertiary-fixed: '#c4e7ff'
  tertiary-fixed-dim: '#7bd0ff'
  on-tertiary-fixed: '#001e2c'
  on-tertiary-fixed-variant: '#004c69'
  background: '#0f131d'
  on-background: '#dfe2f1'
  surface-variant: '#313540'
typography:
  display-hero:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
  display-hero-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '800'
    lineHeight: 44px
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '800'
    lineHeight: 32px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 28px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '700'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
  label-badge:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '800'
    lineHeight: 16px
  label-numeric:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '800'
    lineHeight: 18px
  label-button:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '800'
    lineHeight: 20px
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system channels an immersive, high-energy arcade and tactical HUD visual language tailored specifically for middle-school students tackling homework and study objectives. It balances the futuristic, high-stakes aesthetic of modern gaming platforms with an approachable, playful, and responsive tactile interface. The emotional goal is turning academic grind into epic questing: homework assignments become "bounties", study sessions transform into "XP raids", and streak maintenance triggers sensory visual rewards.

The aesthetic fuses **Tactile Skeuomorphic Micro-Interactions** with **Cyber/Arcade Glassmorphism**. UI elements feel chunky, punchy, and pressable, featuring thick tactile drop-shadow borders (mimicking extruded mechanical game controllers and arcade buttons) bathed in vibrant, neon-charged backlights. Dark canvas surfaces provide immersion and prevent eye fatigue during evening study blocks, while explosive pops of electric green and fiery orange provide sharp dopamine hits upon task completion.

## Colors

The palette is engineered around an immersive deep-space foundation paired with hyper-saturated luminous accents:

- **Canvas & Surfaces:**
  - Base Background: `#0b0f19` (Void Charcoal) — The primary viewport background.
  - Surface Tier 1 (Cards, Canvas Panels): `#111827` (Deep Obsidian).
  - Surface Tier 2 (Interactive Modules, Modals): `#1e293b` (Slate Bastion).
  - Surface Tier 3 (Pressed states, Inset Tracks): `#0f172a` (Trench).
- **Primary Kinetic Accent (`#00ff88` - Hyper Neon Green):**
  - Represents XP, quest clears, health recovery, progression meters, and positive validation. Emits a soft diffused aura (`rgba(0, 255, 136, 0.35)`).
- **Secondary Kinetic Accent (`#ff6b00` - Fiery Solar Orange):**
  - Represents streaks, urgent homework boss deadlines, critical multipliers, and battle-ready calls-to-action. Emits a high-heat aura (`rgba(255, 107, 0, 0.4)`).
- **Tertiary Utility (`#38bdf8` - Mana Blue):**
  - Used for subject tagging (e.g., Science/Math), informational tooltips, and neutral milestone indicators.
- **Neutrals & Typography:**
  - Headings / Active Icons: `#f8fafc` (Frost White, 100% opacity).
  - Body Text: `#cbd5e1` (Light Platinum, 85% opacity).
  - Muted Captions / Inactive Borders: `#64748b` (Armor Slate).

## Typography

Typography relies on **Plus Jakarta Sans** across all roles to synthesize geometric futuristic precision with round, approachable readability. Weights skew heavily toward Bold (`700`) and ExtraBold (`800`) to evoke classic video game title cards, arcade scores, and punchy HUD displays. 

Numerals (XP counters, countdown timers, rank tier indicators) are tuned using tabular lining properties (`font-variant-numeric: tabular-nums`) to prevent jittering during active score tallying and timer counts. Hero headings feature tight, punchy line heights that pair naturally with gamified action banners.

## Layout & Spacing

The design system operates on an 8pt base grid with a responsive fluid container system configured for handheld-first gameplay (smartphones, tablets, and lightweight student Chromebooks/laptops):

- **Mobile (< 768px):** Single column stream with fixed bottom "Controller Dock" navigation. Canvas margins sit at `1rem` with `1rem` vertical item gaps to prioritize single-thumb reachability.
- **Tablet (768px - 1024px):** 8-column layout. The viewport divides into an active "Quest Stage" (5 columns) and an "XP/Inventory Rail" (3 columns).
- **Desktop (> 1024px):** 12-column layout max-width constrained to `1280px` centered. 2-column persistent companion sidebar for guild/friend leaderboard and pet/avatar status; 7-column primary mission briefing center; 3-column upcoming schedule HUD.

Vertical rhythm enforces tactile touch target minimums of 48px across all clickable interactive zones to satisfy rapid tapping without misclicks.

## Elevation & Depth

Visual hierarchy adopts a **Tactile Neo-Arcade** elevation model rather than traditional diffuse drop shadows. Depth is communicated via directional bottom bevels and atmospheric radial glows:

- **Level 0 (Floor):** Canvas background (`#0b0f19`) featuring subtle dark hexagonal or grid-line micro-textures at 5% opacity.
- **Level 1 (Substrate Panels):** Cards and study modules use solid `#111827` framed by a 1px perimeter border of `#334155`. They feature a solid 3px bottom drop-shelf: `box-shadow: 0 4px 0 #070a11`.
- **Level 2 (Interactive Game Units):** Floating action modules, quest cards, and dialogue prompts use `#1e293b` with a crisp `0 6px 0 #0f172a` extruded bottom baseline.
- **Level 3 (Supercharged Glowing States):** Active quests, streak flame indicators, and completed levels emit concentrated dual-layer neon glows:
  - Green Aura: `box-shadow: 0 0 16px rgba(0, 255, 136, 0.4), 0 4px 0 #059669`.
  - Orange Flame Aura: `box-shadow: 0 0 16px rgba(255, 107, 0, 0.4), 0 4px 0 #c2410c`.
- **Tactile Depress Interaction:** When tapped or clicked, buttons and cards physically depress: the element shifts downwards by `3px` (`transform: translateY(3px)`) while the bottom shadow drops to `1px`, delivering mechanical feedback.

## Shapes

The shape architecture relies entirely on **Category 3 (Pill-shaped)** rounding to invoke handheld console ergonomic grips, smooth mechanical capsule keys, and friendly, kid-safe aesthetics. 

Standard interaction chips, primary push buttons, input capsules, and meter tracks utilize full capsule radii (`rounded-full` / `9999px`). Heavy dashboard modules and quest detail surfaces utilize `rounded-2xl` (`1.5rem` to `2rem`) to retain a soft, impact-resistant toy feel. Hard 90-degree corners are strictly prohibited across all functional interactive components.

## Components

### Buttons & CTAs
- **Primary Quest Button ("Claim XP", "Start Mission"):** Full pill-shape (`rounded-full`), background `#00ff88`, label in `#0b0f19` (ExtraBold). Elevated with a solid extruded baseline: `box-shadow: 0 4px 0 #059669, 0 0 20px rgba(0, 255, 136, 0.35)`. Active tap translates down 3px with shadow flattening to 1px.
- **Boss/Urgent CTA ("Turn In Homework"):** Vibrant neon orange `#ff6b00`, white text, baseline shadow: `0 4px 0 #c2410c, 0 0 20px rgba(255, 107, 0, 0.4)`.
- **Secondary / Ghost Button:** Transparent background, 2px border `#334155`, text `#f8fafc`, slight pill container with hover highlight `#1e293b`.

### Gamified Progress Bars & Level Meters
- Track: Deep inset pill `#0f172a` with inner shadow (`box-shadow: inset 0 2px 4px rgba(0,0,0,0.6)`).
- Fill: Fluid gradient from `#00ff88` to `#38bdf8` capped with a rounded edge, accompanied by an animated diagonal striped candy-stripe highlight. A radiant neon dot terminates the head of the progress bar.
- Level Pill Indicator: Positioned overlapping the left edge of the bar, displaying current level (e.g., "LVL 14") in an obsidian shield pill with a neon border.

### Quest Cards & Assignment Tiles
- Surface: `#111827`, fully rounded (`1.5rem`), outlined with a 1.5px border `#1e293b`.
- Completed State: Border shifts to `#00ff88`, background receives a subtle top-to-bottom radial glow (`rgba(0, 255, 136, 0.08)`), and assignment title takes a subtle strike-through with an animated badge burst.
- In-Progress Quest: Features a thumbnail badge, countdown pill tag, and real-time XP value indicator pill.

### Chips & Stat Badges
- XP Pill: Background `#0f172a`, border 1px solid `#00ff88`, icon (spark/crystal), text `#00ff88`, font `label-numeric`.
- Streak Pill: Background `#0f172a`, border 1px solid `#ff6b00`, icon (flame), text `#ff6b00`.
- Subject Filter Chips: Pill containers with muted borders (`#334155`), transitioning to solid `#38bdf8` with dark contrast text when selected.

### Form Inputs & Text Fields
- Container: Inset pill or `1rem` rounded capsule, background `#0b0f19`, border 2px solid `#1e293b`.
- Focus State: Border snaps to `#00ff88` with a soft electric ring `0 0 0 3px rgba(0, 255, 136, 0.2)`. Placeholder text in `#64748b`.

### Checkboxes & Quest Toggles
- Custom chunky circular checkboxes (28px diameter).
- Unchecked: Inset dark surface `#0f172a` with 2px border `#334155`.
- Checked: Spring-pop animation into solid `#00ff88` containing an obsidian bold checkmark icon, triggering micro-confetti particles on first trigger.