## 🎯 Problem

Current visualization lacks the "cyberpunk neon" aesthetic that makes Neon Society immersive.

**Missing Elements:**

- Dark space background
- Neon glow effects
- Glassmorphism UI
- Agent-specific colors
- State-based animations

## ✅ Solution

Implement comprehensive visual theme following Neon Society design specification.

**Visual Identity:**

```
Dark Background (#0a0e27) + Neon Accents (Cyan/Purple/Pink)
+ Glassmorphism (backdrop-filter: blur)
+ Glow Effects (box-shadow)
+ Smooth Animations (CSS keyframes)
```

## 🔧 Implementation

**File:** `neon_visualization.py`

Update HTML/CSS in custom component:

```python
def render_neon_world_map(...):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* === NEON THEME === */

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                background: #0a0e27;  /* Deep space */
                font-family: 'Courier New', monospace;
                overflow: hidden;
            }}

            /* World Container */
            .world-container {{
                position: relative;
                width: {map_size * cell_size}px;
                height: {map_size * cell_size}px;
                margin: 20px auto;

                /* Gradient background */
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);

                /* Neon border */
                border: 2px solid #00d9ff;
                border-radius: 10px;

                /* Glow effect */
                box-shadow:
                    0 0 30px rgba(0, 217, 255, 0.3),
                    inset 0 0 50px rgba(0, 0, 0, 0.5);

                overflow: hidden;
            }}

            /* Grid Overlay */
            .grid {{
                position: absolute;
                width: 100%;
                height: 100%;
                background-image:
                    repeating-linear-gradient(
                        0deg,
                        transparent,
                        transparent {cell_size-1}px,
                        rgba(100, 150, 200, 0.1) {cell_size-1}px,
                        rgba(100, 150, 200, 0.1) {cell_size}px
                    ),
                    repeating-linear-gradient(
                        90deg,
                        transparent,
                        transparent {cell_size-1}px,
                        rgba(100, 150, 200, 0.1) {cell_size-1}px,
                        rgba(100, 150, 200, 0.1) {cell_size}px
                    );
                pointer-events: none;
            }}

            /* Agent Styling */
            .agent {{
                position: absolute;
                width: {cell_size - 4}px;
                height: {cell_size - 4}px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 10px;
                font-weight: bold;
                color: white;
                cursor: pointer;

                /* ULTRA SMOOTH TRANSITIONS */
                transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);

                /* Neon glow */
                box-shadow: 0 0 20px currentColor;
            }}

            .agent:hover {{
                transform: scale(1.3);
                z-index: 100;
            }}

            /* Agent Colors */
            .agent.min-jun {{
                background-color: #ff006e;
                color: #ff006e;
            }}

            .agent.seo-yeon {{
                background-color: #8338ec;
                color: #8338ec;
            }}

            .agent.default {{
                background-color: #06ffa5;
                color: #06ffa5;
            }}

            /* State Indicators */
            .agent::before {{
                content: '';
                position: absolute;
                top: -8px;
                right: -8px;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                border: 2px solid #0a0e27;
            }}

            /* TALKING - Bounce */
            .agent.talking::before {{
                background: #00d9ff;
                animation: bounce 1s infinite;
            }}

            /* THINKING - Pulse */
            .agent.thinking::before {{
                background: #8338ec;
                animation: pulse 2s infinite;
            }}

            /* MOVING - Spin */
            .agent.moving::before {{
                background: #06ffa5;
                animation: spin 1s linear infinite;
            }}

            /* IDLE - Static */
            .agent.idle::before {{
                background: #666;
                opacity: 0.5;
            }}

            /* Selected Glow */
            .agent.selected {{
                transform: scale(1.5);
                box-shadow:
                    0 0 40px currentColor,
                    0 0 60px currentColor;
                z-index: 200;
            }}

            /* === ANIMATIONS === */

            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-5px); }}
            }}

            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.3; }}
            }}

            @keyframes spin {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}

            /* DVR Overlay */
            .dvr-overlay {{
                position: absolute;
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 0, 0, 0.8);
                color: white;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: bold;
                backdrop-filter: blur(10px);
                animation: pulse 1.5s infinite;
                z-index: 1000;
                display: {'block' if dvr_mode else 'none'};
            }}

            /* Tooltip (Glassmorphism) */
            .tooltip {{
                position: absolute;
                background: rgba(10, 14, 39, 0.95);
                color: #00d9ff;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #00d9ff;
                font-size: 11px;
                pointer-events: none;
                z-index: 500;
                display: none;
                backdrop-filter: blur(5px);
            }}
        </style>
    </head>
    ...
    """
```

**File:** `neon_app.py` - Streamlit Base Theme

```python
st.markdown("""
<style>
    /* Global Dark Theme */
    .stApp {
        background-color: #0a0e27;
        color: #e0e0e0;
    }

    /* Agent Cards */
    .agent-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d1b4e 100%);
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #00d9ff;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
    }

    /* Stat Boxes */
    .stat-box {
        background-color: #1a1a2e;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #f72585;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
</style>
""", unsafe_allow_html=True)
```

## ✔️ Acceptance Criteria

- [ ] All 4 state animations work (bounce, pulse, spin, static)
- [ ] Agent colors distinct and neon-styled
- [ ] Grid overlay visible but subtle
- [ ] Glow effects perform well (no lag)
- [ ] Matches Neon Society mockups
- [ ] Dark mode optimized (no white flashes)

## 🎨 Color Palette

```python
AGENT_COLORS = {
    "Min-jun": "#ff006e",     # Hot Pink
    "Seo-yeon": "#8338ec",    # Purple
    "Default": "#06ffa5",     # Neon Green
    "Grid": "rgba(100, 150, 200, 0.1)",
    "Border": "#00d9ff",      # Cyan
}
```

## 📊 Visual Checklist

- [ ] Dark background (#0a0e27)
- [ ] Neon borders (Cyan #00d9ff)
- [ ] Box-shadow glows
- [ ] Backdrop-filter: blur (glassmorphism)
- [ ] Smooth transitions (0.5s ease-in-out)
- [ ] State-based keyframe animations
- [ ] Gradient backgrounds

## ⏱️ Estimate

**3-4 hours**

## 🏷️ Labels

`ui`, `design`, `priority:high`, `visual`
