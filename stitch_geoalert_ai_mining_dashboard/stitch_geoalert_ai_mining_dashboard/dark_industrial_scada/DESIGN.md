---
name: Dark Industrial SCADA
colors:
  surface: '#0d1322'
  surface-dim: '#0d1322'
  surface-bright: '#33394a'
  surface-container-lowest: '#080e1d'
  surface-container-low: '#151b2b'
  surface-container: '#191f2f'
  surface-container-high: '#242a3a'
  surface-container-highest: '#2f3445'
  on-surface: '#dde2f8'
  on-surface-variant: '#e0c0b1'
  inverse-surface: '#dde2f8'
  inverse-on-surface: '#2a3040'
  outline: '#a78b7d'
  outline-variant: '#584237'
  surface-tint: '#ffb690'
  primary: '#ffb690'
  on-primary: '#552100'
  primary-container: '#f97316'
  on-primary-container: '#582200'
  inverse-primary: '#9d4300'
  secondary: '#7bd0ff'
  on-secondary: '#00354a'
  secondary-container: '#00a6e0'
  on-secondary-container: '#00374d'
  tertiary: '#4ae176'
  on-tertiary: '#003915'
  tertiary-container: '#00b251'
  on-tertiary-container: '#003b16'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdbca'
  primary-fixed-dim: '#ffb690'
  on-primary-fixed: '#341100'
  on-primary-fixed-variant: '#783200'
  secondary-fixed: '#c4e7ff'
  secondary-fixed-dim: '#7bd0ff'
  on-secondary-fixed: '#001e2c'
  on-secondary-fixed-variant: '#004c69'
  tertiary-fixed: '#6bff8f'
  tertiary-fixed-dim: '#4ae176'
  on-tertiary-fixed: '#002109'
  on-tertiary-fixed-variant: '#005321'
  background: '#0d1322'
  on-background: '#dde2f8'
  surface-variant: '#2f3445'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 12px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 0.75rem
  gutter-desktop: 1rem
  margin: 1rem
  margin-desktop: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

The design system reflects a mission-critical, dark industrial operations center. Built for geotechnical engineers, mining superintendents, and field safety directors, the interface translates high-velocity telemetry, seismic acoustics, and computer-vision rockfall feeds into immediate situational awareness. 

The aesthetic merges modern SCADA instrumentation with high-density geospatial interfaces:
- **Atmosphere:** Dark, utilitarian, focused, and vigilant. The UI minimizes eye strain during 12-hour shifts in dim monitoring cabins while providing stark, high-contrast callouts during hazardous events.
- **Visual Style:** Industrial Precision / Modern SCADA. It avoids decorative skeuomorphism or frivolous glass effects, prioritizing 1px technical wire-framing, strict spatial density, calibrated telemetry tickers, and unequivocal hazard signaling.
- **Sensory Response:** Zero ambiguity. Critical thresholds evoke an immediate, visceral reflex via high-chroma safety orange and warning alerts, surrounded by structured slate surfaces.

## Colors

The color palette is architected around functional optical hierarchy, environmental containment, and ISO/ANSI hazard standards.

### Canvas & Surface Architecture
- **Base Canvas (`#0B1120`):** The foundational substrate for full-screen map views, 3D point-cloud viewports, and deep-layer data canvases.
- **Sidebar & Structural Shell (`#0F172A`):** The anchor for fixed navigation rails, docked telemetry menus, and persistent header utilities.
- **Card & Module Background (`#151F32`):** The primary container for analytical widgets, sensor graphs, and data grids.
- **Elevated & Interactive Surfaces (`#1C2940`):** Modals, dropdown flyouts, active state toggles, and hovered table rows.
- **Border & Rule Definer (`#2A3850`):** Crisp 1px separations delineating dense data compartments without visual clutter.

### Signal Accents
- **Primary Accent (`#F97316` - Hazard Orange):** Active controls, active geospatial triggers, primary drill-downs, and attention-critical CTAs.
- **Secondary Accent (`#38BDF8` - Technical Blue):** Sensor telemetry paths, LiDAR point-cloud contours, vector coordinates, and system sync links.

### Operational State Matrix
- **Critical / High Risk (`#EF4444`):** Displacement thresholds breached, rockfall detected, immediate site evacuation.
- **Warning / Elevated Risk (`#F59E0B`):** Creep rate acceleration, acoustic emission burst, geofence caution.
- **Nominal / Safe (`#22C55E`):** Stable slope equilibrium, online sensors, battery calibrated.

### Typography & Content Shades
- **Primary Text (`#F1F5F9`):** High legibility for readings, metrics, coordinates, and system states.
- **Secondary Text (`#94A3B8`):** Units of measurement, metadata timestamps, column headers, and structural labels.

## Typography

The typographic system is optimized for high-density information architecture, combining clean neutral grotesques with fixed-width tabular data.

- **Primary Typeface (`Inter`):** Applied across all structural interfaces, narrative operational logs, and hierarchy headers. Tabular figures (`tnum`) must be forced across all numeric instances within Inter to prevent spatial shifting during live sensor updates.
- **Technical & Metric Subsystem (`JetBrains Mono`):** Applied strictly to GIS coordinates (Latitude/Longitude/Elevation), sensor IDs, timestamps, velocity measurements (mm/h), and status codes. Its clear character distinction (e.g., `0` vs `O`, `1` vs `l`) prevents operational misreading under crisis conditions.
- **Hierarchy Structure:** Headers are condensed and modest in scale to leave maximum viewport area for spatial mapping and telemetry charts.

## Layout & Spacing

The layout utilizes a continuous viewport model built for dynamic multi-pane arrangements (map viewport, real-time alert feed, and sensor graphs).

- **Grid Strategy:** A fluid 12-column layout grid on desktop with tight 16px (`1rem`) gutters, allowing data docks to fit along viewport edges. Mobile displays collapse into a stacked 4-column column layout with 12px (`0.75rem`) gutters.
- **Density & Padding:** Layout distances prioritize functional density. Internal panel margins use `space-md` (12px) to minimize dead pixel zones. Structural dividers use exact 1px lines rather than wide negative spaces to isolate adjacent analytical components.
- **Responsive Adaptations:**
  - **Desktop (>= 1280px):** 3-pane orchestration: fixed 64px icon utility rail, dynamic collapsible 280px navigation/asset tree, central interactive 3D/geospatial canvas, and right-docked 380px operational stream.
  - **Tablet (768px - 1279px):** Map dominates the canvas; right dock shifts to an expandable bottom drawer.
  - **Mobile (< 768px):** Full-screen tactical card views with swipeable alert panels and floating utility bottom sheets for field engineers walking benches.

## Elevation & Depth

Visual hierarchy uses tonal surface layering and precise borders rather than ambient blur shadows, mirroring technical avionics and industrial displays.

- **Surface Layering:**
  - **Level 0 (Canvas):** `#0B1120` (Underlying viewport, base map canvas).
  - **Level 1 (Docked Shells):** `#0F172A` (Sidebar rails, control bars).
  - **Level 2 (Containers):** `#151F32` (Telemetry cards, graph modules, log containers).
  - **Level 3 (Interactive Floating):** `#1C2940` (Modals, popovers, sensor detail tooltips).
- **Lineation & Borders:** All panels, cards, and docked controls feature a crisp, structural 1px outline in `#2A3850`. This creates clean boundaries between adjacent telemetry data without heavy shadows.
- **Depth Cues:** True box shadows are restricted to elevated popovers and critical alarm banners (`0 4px 20px -2px rgba(0, 0, 0, 0.65)`). When a critical alert is triggered, the affected panel replaces its static `#2A3850` border with a pulsing 1px `#EF4444` highlight.

## Shapes

The geometric silhouette combines clean industrial tooling with structured utility. 

- **Corner Radii Hierarchy:**
  - Base components (buttons, input fields, badges, tabs): `rounded-md` (8px / 0.5rem).
  - Primary modules and analytical containers (cards, map overlays, modal sheets): `rounded-lg` (12px / 0.75rem).
  - Inner items within cards (data pills, meter bars, telemetry slots): `rounded-sm` (4px / 0.25rem) to preserve concentric visual balance.
- **Form Factor:** Sharp corners are avoided to reduce visual fatigue, while excessive pill shapes are excluded from system panels to maintain an engineered, dashboard-grade profile.

## Components

### Buttons
- **Primary:** Background `#F97316`, label `#0B1120` (bold, readable contrast), border 1px solid `#EA580C`. Hover shifts to `#FB923C`.
- **Secondary / Tactical:** Background `#1C2940`, label `#F1F5F9`, border 1px solid `#2A3850`. Hover triggers background `#2A3850` and border `#38BDF8`.
- **Destructive / Emergency Stop:** Background `#EF4444`, label `#FFFFFF`, border 1px solid `#DC2626`.
- **Sizing:** Compact padding (`space-xs` vertical, `space-md` horizontal). All buttons include Lucide outline icons set at 16x16px.

### Risk & Status Badges
Badges require three points of feedback: an icon, a color indicator, and an uppercase monospaced text label.
- **Structure:** 1px solid outline, 10% opacity tinted background fill, 4px corner radius, text formatted via `label-sm`.
- **Critical Risk:** Background `rgba(239, 68, 68, 0.12)`, border `#EF4444`, text `#EF4444`, icon `AlertTriangle` (12px).
- **Warning Risk:** Background `rgba(245, 158, 11, 0.12)`, border `#F59E0B`, text `#F59E0B`, icon `AlertCircle` (12px).
- **Nominal:** Background `rgba(34, 197, 94, 0.12)`, border `#22C55E`, text `#22C55E`, icon `CheckCircle2` (12px).

### Input Fields & Selectors
- **Surface:** `#0F172A` background encased in a 1px `#2A3850` border.
- **States:** Active/focus transitions border to `#38BDF8` with a 0 0 0 1px `#38BDF8` focus ring.
- **Text:** High-contrast text `#F1F5F9` using `Inter` with placeholders in `#94A3B8`. Numeric inputs render via `JetBrains Mono`.

### Cards & Module Containers
- **Anatomy:** Header bar with 1px bottom border in `#2A3850`, widget title in `headline-md`, metadata indicator, and Lucide action icon.
- **Body:** Background `#151F32`, outer border 1px solid `#2A3850`, padding `space-md`. 

### Checkboxes & Toggle Switches
- **Checkboxes:** 16x16px boxes, `#0F172A` fill, `#2A3850` border. Checked state uses `#F97316` fill with dark checkmark.
- **Toggles:** SCADA-style track switch. Unchecked: `#1C2940` track with `#94A3B8` thumb. Checked: `#38BDF8` track with `#0B1120` thumb.

### Domain-Specific Components
- **Telemetry Vector Ticker:** Strip panel displaying real-time displacement vectors (`dX`, `dY`, `dZ`, velocity mm/h) utilizing `label-md` in `JetBrains Mono` with dynamic trend arrows (`TrendingUp`, `TrendingDown`).
- **Geofence Sector Status List:** Compact list rows with alternating `#151F32` and `#1C2940` (hovered) backgrounds, displaying sector ID, risk badge, sensor link count, and contextual action menus.