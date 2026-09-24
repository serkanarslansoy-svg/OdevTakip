---
name: Vibrant Quest Studio
colors:
  surface: '#fdf7ff'
  surface-dim: '#dfd6f1'
  surface-bright: '#fdf7ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f8f1ff'
  surface-container: '#f3eaff'
  surface-container-high: '#eee4ff'
  surface-container-highest: '#e8def9'
  on-surface: '#1e192c'
  on-surface-variant: '#484456'
  inverse-surface: '#332d42'
  inverse-on-surface: '#f5eeff'
  outline: '#797488'
  outline-variant: '#cac3d9'
  surface-tint: '#642cf7'
  primary: '#5300e7'
  on-primary: '#ffffff'
  primary-container: '#6c38ff'
  on-primary-container: '#e9e0ff'
  inverse-primary: '#cbbeff'
  secondary: '#994700'
  on-secondary: '#ffffff'
  secondary-container: '#fb7800'
  on-secondary-container: '#592600'
  tertiary: '#005569'
  on-tertiary: '#ffffff'
  tertiary-container: '#006f88'
  on-tertiary-container: '#baecff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e7deff'
  primary-fixed-dim: '#cbbeff'
  on-primary-fixed: '#1e0060'
  on-primary-fixed-variant: '#4c00d3'
  secondary-fixed: '#ffdbc8'
  secondary-fixed-dim: '#ffb68b'
  on-secondary-fixed: '#321200'
  on-secondary-fixed-variant: '#753400'
  tertiary-fixed: '#b6ebff'
  tertiary-fixed-dim: '#47d6ff'
  on-tertiary-fixed: '#001f28'
  on-tertiary-fixed-variant: '#004e60'
  background: '#fdf7ff'
  on-background: '#1e192c'
  surface-variant: '#e8def9'
typography:
  display-hero:
    fontFamily: Plus Jakarta Sans
    fontSize: 44px
    fontWeight: '800'
    lineHeight: 52px
    letterSpacing: -0.03em
  display-hero-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 28px
    letterSpacing: -0.01em
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
    fontWeight: '500'
    lineHeight: 16px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 18px
    letterSpacing: 0.02em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.03em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 10px
    fontWeight: '800'
    lineHeight: 12px
    letterSpacing: 0.05em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-sm: 0.75rem
  margin: 1.25rem
  margin-sm: 1rem
  margin-lg: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system is engineered for middle-school learners navigating daily homework, study streaks, and exam prep. The personality balances energetic gamification with functional academic clarity: it feels rewarding, encouraging, and punchy, never sterile or overwhelming. 

The aesthetic is **Tactile Neo-Pop**: hyper-saturated accents, playful pill-shaped geometry, tactile micro-elevations (subtle pushable depth mimicking arcade tokens), and high contrast for rapid legibility during hurried morning checks or late-evening study sprints. The visual tone transforms school tasks from chores into dynamic mini-quests without infantilizing 10–14 year olds.

## Colors

The palette establishes an electric visual rhythm using an anchor of punchy royal violet, flanked by high-velocity secondary and tertiary beacons.

- **Primary (`#6C38FF` - Electric Violet):** Drives primary navigation, core CTAs, level-up milestones, and active quest markers.
- **Secondary (`#FF7A00` - Neon Blaze):** Reserved for urgent deadlines, XP multipliers, flame streaks, and hot-action states. Pair with bright lemon yellow (`#FFD600`) for celebratory badges and bonus alerts.
- **Tertiary (`#00D2FF` - Cyber Azure):** Fuels subject categorization (STEM/Math), completed task tokens, and progress bars.
- **Neutral (`#1A1528` - Deep Ink Violet):** Replaces pure black with an ink-infused midnight violet for text and dark-accent surfaces, preserving high contrast (WCAG AAA against white) while harmonizing with saturated overlays.
- **Surface & Canvas:** Base canvas is crisp cloud white (`#FAFAFD`) with layered card surfaces in pure white (`#FFFFFF`) and softly tinted violet-slate tints (`#F0EDFF`) for secondary structural panels.

## Typography

Plus Jakarta Sans is utilized across all tiers to deliver geometric precision paired with warm, friendly curves. 

- Large numerals (streaks, countdown timers, points) rely on `display-hero` with an ultra-bold weight (800) to reinforce game metrics.
- Headlines maintain tight negative tracking to prevent sprawling strings in multi-word Turkish academic titles (e.g., "Fen Bilimleri Ödevi").
- Body copy sits at medium weight (500) to withstand active handheld viewing on medium-spec smartphones without degradation or thinning.
- Badges and mini-counters exploit uppercase `label-sm` with widened letter-spacing for crisp rendering inside compact pill chips.

## Layout & Spacing

The layout is built upon an 8pt rhythmic grid optimized for thumb-reach ergonomics on mobile viewport devices (360px to 430px wide).

- **Mobile (Default):** Single-column fluid stream with `1.25rem` (20px) outer canvas margins and `1rem` (16px) element gaps. Interactive cards stretch edge-to-edge within safety boundaries to maximize touch surface areas.
- **Tablet / Large Mobile Foldables:** Adapts to a 4-to-6 column fluid grid with `2rem` outer padding, splitting views into side-by-side homework streams and sticky schedule/streak dashboards.
- Spacing inside gamified widgets uses `space-md` for standard card padding and `space-sm` for inline metadata clusters (e.g., badge + subject tag + due date).

## Elevation & Depth

Visual hierarchy uses a blend of **Tactile Layering** and **Tinted Ambient Shadows** to evoke interactive physical game tiles:

- **Level 0 (Canvas):** Flat base `#FAFAFD`.
- **Level 1 (Default Task Cards & Containers):** Pure white `#FFFFFF` surface accompanied by a soft, directional ambient drop shadow: `0 8px 24px -4px rgba(108, 56, 255, 0.08)`. Subtle 1.5px border in `#ECE8FC` to retain definition on bright outdoor screens.
- **Level 2 (Active/Selected & Interactive Cards):** Enhanced colored under-glow matching the card's accent. Violet cards cast `0 12px 28px -6px rgba(108, 56, 255, 0.28)`; streak cards cast `0 12px 28px -6px rgba(255, 122, 0, 0.3)`.
- **Level 3 (Modals, XP Level-Up Dialogs, Overlays):** Deep tinted shadow: `0 20px 40px -8px rgba(26, 21, 40, 0.25)` over a 12px frosted glass backdrop (`rgba(26, 21, 40, 0.45)` with `backdrop-filter: blur(12px)`).
- **Physical "Press" Effect:** High-priority cards and buttons feature a 3px tactile bottom offset that compresses down to 0px on active tap (`transform: translateY(3px)`).

## Shapes

This design system implements **Pill-shaped (Level 3)** roundedness to maintain an inviting, tactile, and non-intimidating interface.

- **Badges, XP Tags, Streak Trackers:** Fully rounded pill shapes (`border-radius: 9999px`).
- **Cards & Quest Blocks:** `rounded-lg` (2rem / 32px) or `rounded-xl` (3rem / 48px on modal sheets), softening rectangular edges and giving task containers an approachable toy-like feel.
- **Interactive Checkpoints:** Perfectly circular checkboxes and status discs that transform via scale animation upon completion.

## Components

### Buttons
- **Primary Action (Quest Complete / Submit):** Pill-shaped, full-bleed gradient from Electric Violet (`#6C38FF`) to vibrant violet (`#8B5CF6`). Crisp bold typography (`label-lg`), with a 3D bottom bevel (`box-shadow: 0 4px 0 #4B1EE0`). On press, shifts down by 4px with zero shadow.
- **Secondary (Streak Booster / Bonus):** Neon Blaze (`#FF7A00`) with a darker amber offset bevel (`#CC5A00`).
- **Ghost/Tertiary:** High-contrast outline with 2px solid `#ECE8FC`, tinted violet text, and transparent background.

### Chips & Pill Badges
- **XP / Streak Indicators:** Neon Blaze background with ink-violet text or white bold numeric text, flanked by mini vector icons (flame, lightning, star).
- **Subject Chips:** Micro-pills using 12% tinted alpha backgrounds of the subject color (e.g., Azure for Math, Violet for Turkish, Green for Science) paired with solid 100% saturation text for high contrast.

### Task & Homework Cards
- Layered white card container with 24px inner padding.
- Left edge features a 6px thick vertical status stripe indicating proximity to deadline (Green: >3 days, Yellow: tomorrow, Red/Orange: today).
- Embedded progress bar: 8px tall rounded pill track with an animated neon gradient fill indicating steps completed (e.g., "3/5 Test Çözüldü").

### Gamified Checkboxes
- 28x28px circular tap targets. Unchecked state is a 2px bordered circle (`#D5CFF8`). Checked state bursts with a scale spring animation into solid Cyber Azure (`#00D2FF`) with a bold white checkmark and trailing micro-confetti particle effect.

### Achievement & Exam Countdown Cards
- High-contrast celebration tiles utilizing dark-accent violet backgrounds (`#1A1528`) populated with glowing neon yellow/orange countdown typography, radial ambient glows, and floating 3D badge icons.

### Input Fields
- Generous 56px height for easy finger input. Surface is tinted white (`#F8F7FD`) with a subtle 1.5px border in `#E3DFFC`. On focus, transitions to an Electric Violet border with an accompanying 4px violet aura ring (`rgba(108, 56, 255, 0.15)`).