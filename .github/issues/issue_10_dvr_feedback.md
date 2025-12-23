## 🎯 Problem

Users cannot easily tell when they're viewing past history vs live simulation.

**UX Issue:**

- DVR mode has no visual feedback
- Slider looks like normal control
- Risk of confusion (thinking past is present)

## ✅ Solution

Add prominent red overlay with pulsing animation when DVR mode is active.

**Visual Design:**

```
┌────────────────────────────────────┐
│  📼 DVR MODE - VIEWING HISTORY     │ ← Red banner, pulsing
│                                    │
│    [===●=======] Tick 47          │ ← Timeline scrubber
│                                    │
│    ┌──────────────────┐           │
│    │   World Map      │           │
│    └──────────────────┘           │
└────────────────────────────────────┘
```

## 🔧 Implementation

**File:** `neon_visualization.py`

```python
def render_neon_world_map(..., dvr_mode: bool = False):
    html_code = f"""
    <style>
        /* DVR Overlay */
        .dvr-overlay {{
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);

            /* Red warning style */
            background: rgba(255, 0, 0, 0.8);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;

            /* Glassmorphism */
            backdrop-filter: blur(10px);

            /* Pulse animation */
            animation: pulse 1.5s infinite;

            z-index: 1000;
            display: {'block' if dvr_mode else 'none'};

            /* VCR aesthetic */
            font-family: 'Courier New', monospace;
            letter-spacing: 2px;
        }}

        @keyframes pulse {{
            0%, 100% {{
                opacity: 1;
                box-shadow: 0 0 20px rgba(255, 0, 0, 0.8);
            }}
            50% {{
                opacity: 0.7;
                box-shadow: 0 0 40px rgba(255, 0, 0, 1);
            }}
        }}

        /* Scanline effect (optional) */
        .dvr-overlay::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 0, 0, 0.1),
                rgba(0, 0, 0, 0.1) 1px,
                transparent 1px,
                transparent 2px
            );
            pointer-events: none;
        }}
    </style>

    <div class="world-container">
        <!-- DVR Overlay -->
        <div class="dvr-overlay">
            📼 DVR MODE - VIEWING HISTORY
        </div>

        <!-- Rest of map -->
        ...
    </div>
    """
```

**File:** `neon_app.py` - DVR Controls

```python
# DVR Timeline Section
if st.session_state.dvr_mode and st.session_state.history:
    st.markdown("### ⏪ Time Travel")

    # Warning banner
    st.error("📼 DVR Mode Active - Viewing Historical State")

    # Timeline scrubber
    col1, col2 = st.columns([4, 1])

    with col1:
        selected_tick = st.slider(
            "Timeline",
            min_value=0,
            max_value=len(st.session_state.history) - 1,
            value=len(st.session_state.history) - 1,
            format="Tick %d"
        )

    with col2:
        if st.button("🔴 Exit DVR"):
            st.session_state.dvr_mode = False
            st.rerun()

    # Tick info
    historical_world = st.session_state.history[selected_tick]
    st.info(f"⏰ Viewing Tick #{historical_world.tick} (History)")

    # Visual separator
    st.markdown("---")
```

**Enhanced Slider Styling:**

```python
st.markdown("""
<style>
    /* DVR Slider - Red theme */
    div[data-testid="stSlider"] {
        background: rgba(255, 0, 0, 0.1);
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #ff0000;
    }

    div[data-testid="stSlider"] label {
        color: #ff6b6b !important;
        font-weight: bold;
    }

    /* Timeline track */
    div[data-testid="stSlider"] [role="slider"] {
        background: linear-gradient(90deg, #ff0000 0%, #ff6b6b 100%);
    }
</style>
""", unsafe_allow_html=True)
```

## ✔️ Acceptance Criteria

- [ ] Red banner visible when DVR active
- [ ] Pulse animation smooth (1.5s cycle)
- [ ] Banner disappears when exiting DVR
- [ ] Timeline scrubber styled distinctly
- [ ] "Exit DVR" button prominent
- [ ] No overlap with other UI elements
- [ ] Works on mobile (responsive)

## 🎨 Visual Elements

**Red Overlay:**

- Background: `rgba(255, 0, 0, 0.8)`
- Text: White, bold, Courier New
- Animation: Pulsing box-shadow
- Z-index: 1000 (top layer)

**Timeline**:

- Red slider track
- Tick markers every 10 ticks
- Current tick highlighted

**Exit Button:**

- Red background
- White text with icon (🔴)
- Hover effect: Brighter red

## 📊 Interactive Demo

```
LIVE MODE:              DVR MODE:
┌─────────────┐        ┌─────────────────────────┐
│ World Map   │        │ 📼 DVR MODE ← pulsing  │
│             │   →    │ [===●====] Tick 47      │
│ [agents]    │        │ World Map (frozen)      │
│             │        │ [agents at tick 47]     │
│ ▶️ Running  │        │ 🔴 Exit DVR             │
└─────────────┘        └─────────────────────────┘
```

## ⏱️ Estimate

**2-3 hours**

## 🏷️ Labels

`ui`, `feature`, `priority:medium`, `dvr`
