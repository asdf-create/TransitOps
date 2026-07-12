# UI_UX.md

# TransitOps UI/UX Specification

Version: 1.0

## Design Philosophy

TransitOps should feel like a premium macOS application rather than a hackathon project.

Design inspiration:

* Apple Human Interface Guidelines
* Linear
* Raycast
* Arc Browser
* Notion
* Stripe Dashboard

The UI should communicate professionalism, speed, and clarity.

---

# Design Goals

* Native macOS feel
* Enterprise dashboard
* Smooth animations
* Minimal visual clutter
* Excellent information hierarchy
* Fast navigation
* Accessible
* Responsive
* Dark mode first

Every screen should answer:

> What is happening?
> What action should the user take next?

---

# Design Language

Overall aesthetic:

* Apple-inspired
* Modern AI dashboard
* Subtle glass effects
* Soft shadows
* Rounded corners
* High contrast
* Minimal gradients

Avoid excessive glow or cyberpunk styling.

---

# Color Palette

Primary:

Blue

Success:

Green

Warning:

Orange

Danger:

Red

Neutral:

Slate / Gray

Reserve accent colors for important actions only.

---

# Typography

Use a clean sans-serif font.

Hierarchy:

* Display
* Heading 1
* Heading 2
* Heading 3
* Body
* Caption

Avoid excessive font weights.

Maintain consistent spacing.

---

# Icons

Primary:

HugeIcons

Fallback:

Lucide

Use outlined icons by default.

Filled icons only for active navigation states.

---

# Border Radius

Small

Inputs

Buttons

Medium

Cards

Dialogs

Large

Dashboards

Maps

Avoid inconsistent corner radii.

---

# Shadows

Prefer soft shadows.

Avoid harsh drop shadows.

Glass cards should use subtle elevation.

---

# Animations

Use Framer Motion.

Animation should communicate state changes.

Never animate purely for decoration.

Target duration:

150–300 ms

Use spring animations for:

* Cards
* Drawers
* Dialogs
* Sidebar
* Map controls

---

# Navigation

Desktop layout:

```text
Sidebar
│
├── Dashboard
├── Vehicles
├── Drivers
├── Trips
├── Tracking
├── Maintenance
├── Expenses
├── Analytics
├── AI Assistant
├── Notifications
└── Settings
```

Top bar includes:

* Search
* Theme toggle
* Notifications
* User profile

---

# Dashboard

This is the showcase page.

Include:

* KPI cards
* Fleet status
* Active deliveries
* Live map
* Revenue summary
* Driver rankings
* Vehicle rankings
* AI insights
* Recent activity

The dashboard should feel alive.

---

# KPI Cards

Each card should include:

* Icon
* Metric
* Percentage change
* Small sparkline
* Hover animation

Animated counters on initial load.

---

# Data Tables

Use shadcn Data Table.

Support:

* Sorting
* Filtering
* Pagination
* Column visibility
* Search
* Bulk actions
* Sticky header

Avoid horizontal scrolling whenever possible.

---

# Forms

Use consistent spacing.

Validation:

* Inline errors
* Success indicators
* Required field markers

Disable submit while processing.

---

# Search

Global search available from every page.

Support:

* Keyboard shortcut (⌘K / Ctrl+K)
* Fuzzy search
* Quick navigation
* Quick actions

---

# Notifications

Use Sonner.

Notification types:

* Success
* Warning
* Error
* Information

Notification Center should maintain history.

---

# Sidebar

Collapsible.

Animated.

Remember previous state.

Support icons-only mode.

---

# Breadcrumbs

Show on every page except Dashboard.

Keep navigation clear.

---

# Dialogs

Use shadcn Dialog.

Support:

* Escape key
* Click outside to close
* Smooth animations

Dangerous actions require confirmation.

---

# Cards

Cards should contain:

* Title
* Optional subtitle
* Actions
* Content
* Footer (optional)

Consistent padding throughout.

---

# Empty States

Every page must have meaningful empty states.

Examples:

No vehicles.

No trips.

No maintenance.

No notifications.

Each should include:

* Illustration or icon
* Description
* Primary action

---

# Loading States

Never display blank pages.

Use:

* Skeleton loaders
* Progress indicators
* Animated placeholders

Avoid spinners whenever skeletons make sense.

---

# Maps

MapLibre GL JS.

Features:

* Live vehicle movement
* Driver markers
* Route visualization
* ETA
* Zoom controls
* Fullscreen
* Current delivery information

Movement must interpolate smoothly along roads.

---

# Customer Tracking Page

Simple and elegant.

Sections:

* Delivery status
* Live map
* ETA
* Driver information
* Vehicle information
* Delivery timeline
* Progress bar

No login required.

Read-only.

Optimized for sharing.

---

# Analytics

Use Apache ECharts.

Recommended charts:

* Line
* Bar
* Area
* Pie
* Gauge
* Heatmap
* Radar
* Sankey
* Calendar Heatmap
* Scatter
* Treemap

Every chart should support:

* Hover
* Tooltips
* Export
* Responsive resizing
* Smooth transitions

---

# AI Assistant

Dockable panel.

Support:

* Markdown
* Tables
* Code blocks
* Suggested follow-up questions

Provide quick action buttons:

* Predict delay
* Best driver
* Maintenance prediction
* Vehicle status
* Explain dashboard metric

---

# Tracking Experience

Vehicle animation should resemble Apple Maps.

Include:

* Smooth movement
* Route highlighting
* Destination marker
* Current speed
* Remaining distance
* ETA updates

Camera should optionally follow the active vehicle.

---

# Motion Guidelines

Animate:

* Sidebar
* Cards
* KPI counters
* Charts
* Tables
* Dialogs
* Drawers
* Notifications
* Tabs
* Route progress
* Vehicle movement

Do not animate every UI element simultaneously.

Maintain visual restraint.

---

# Recommended Component Libraries

Primary:

* shadcn/ui

Additional:

* shadcn Blocks
* Origin UI
* Motion Primitives
* Magic UI
* ReactBits

Use Aceternity UI only if a component cannot be reasonably recreated with the above.

Avoid mixing multiple visual styles.

---

# Recommended shadcn Components

Navigation:

* Sidebar
* Breadcrumb
* Navigation Menu
* Command
* Context Menu
* Dropdown Menu

Forms:

* Input
* Select
* Combobox
* Calendar
* Date Picker
* Checkbox
* Switch
* Radio Group
* Textarea

Layout:

* Card
* Accordion
* Tabs
* Separator
* Scroll Area
* Resizable Panels
* Collapsible

Feedback:

* Sonner
* Alert Dialog
* Progress
* Skeleton
* Hover Card
* Tooltip

Data:

* Data Table
* Badge
* Avatar
* Pagination

---

# Accessibility

Support:

* Keyboard navigation
* Visible focus states
* Proper labels
* Semantic HTML
* Screen readers where practical

Maintain sufficient color contrast.

---

# Performance

Avoid unnecessary re-renders.

Lazy-load heavy pages.

Virtualize large tables if needed.

Keep animations GPU-accelerated.

---

# UI Checklist

* [ ] Apple-inspired design language
* [ ] Dark mode
* [ ] Smooth animations
* [ ] Sidebar implemented
* [ ] Dashboard polished
* [ ] Interactive ECharts
* [ ] Live MapLibre tracking
* [ ] AI assistant panel
* [ ] Customer tracking page
* [ ] Global search
* [ ] Empty states
* [ ] Skeleton loading
* [ ] Notification center
* [ ] Responsive layout
* [ ] Consistent spacing
* [ ] HugeIcons used throughout
* [ ] Documentation updated after UI changes
