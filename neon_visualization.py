"""
Neon Society Advanced Visualization
Custom HTML/CSS/JS component for React-level animations
"""
import streamlit.components.v1 as components
from typing import Dict, List
import json

def render_neon_world_map(agents: Dict, map_size: int = 20, dvr_mode: bool = False, 
                          selected_agent: str = None, cell_size: int = 30) -> None:
    """
    Render advanced world map with CSS transitions and neon aesthetics
    """
    # Convert agents to JSON
    agents_data = []
    for name, agent in agents.items():
        agents_data.append({
            "name": name,
            "x": agent.x,
            "y": agent.y,
            "state": agent.state,
            "thought": agent.current_thought[:50] if agent.current_thought else "",
            "plan": agent.current_plan[:50] if agent.current_plan else ""
        })
    
    # Neon color palette
    agent_colors = {
        "Min-jun": "#ff006e",  # Hot pink
        "Seo-yeon": "#8338ec",  # Purple
        "default": "#06ffa5"     # Neon green
    }
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                background: #0a0e27;
                font-family: 'Courier New', monospace;
                overflow: hidden;
            }}
            
            .world-container {{
                position: relative;
                width: {map_size * cell_size}px;
                height: {map_size * cell_size}px;
                margin: 20px auto;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 2px solid #00d9ff;
                border-radius: 10px;
                box-shadow: 0 0 30px rgba(0, 217, 255, 0.3),
                            inset 0 0 50px rgba(0, 0, 0, 0.5);
                overflow: hidden;
            }}
            
            /* Grid overlay */
            .grid {{
                position: absolute;
                width: 100%;
                height: 100%;
                background-image: 
                    repeating-linear-gradient(0deg, transparent, transparent {cell_size-1}px, rgba(100, 150, 200, 0.1) {cell_size-1}px, rgba(100, 150, 200, 0.1) {cell_size}px),
                    repeating-linear-gradient(90deg, transparent, transparent {cell_size-1}px, rgba(100, 150, 200, 0.1) {cell_size-1}px, rgba(100, 150, 200, 0.1) {cell_size}px);
                pointer-events: none;
            }}
            
            /* Agent styling */
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
                
                box-shadow: 0 0 20px currentColor;
            }}
            
            .agent:hover {{
                transform: scale(1.3);
                z-index: 100;
            }}
            
            /* State indicators */
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
            
            /* TALKING state - bounce */
            .agent.talking::before {{
                background: #00d9ff;
                animation: bounce 1s infinite;
            }}
            
            /* THINKING state - pulse */
            .agent.thinking::before {{
                background: #8338ec;
                animation: pulse 2s infinite;
            }}
            
            /* MOVING state */
            .agent.moving::before {{
                background: #06ffa5;
                animation: spin 1s linear infinite;
            }}
            
            /* IDLE state */
            .agent.idle::before {{
                background: #666;
                opacity: 0.5;
            }}
            
            /* Selected glow */
            .agent.selected {{
                transform: scale(1.5);
                box-shadow: 0 0 40px currentColor,
                            0 0 60px currentColor;
                z-index: 200;
            }}
            
            /* Animations */
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
            
            /* DVR overlay */
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
                display: none;
            }}
            
            .dvr-overlay.active {{
                display: block;
            }}
            
            /* Tooltip */
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
    <body>
        <div class="world-container">
            <div class="grid"></div>
            <div class="dvr-overlay {'active' if dvr_mode else ''}">📼 DVR MODE - VIEWING HISTORY</div>
            <div id="agents"></div>
            <div class="tooltip" id="tooltip"></div>
        </div>
        
        <script>
            const agents = {json.dumps(agents_data)};
            const cellSize = {cell_size};
            const agentColors = {json.dumps(agent_colors)};
            const selectedAgent = {json.dumps(selected_agent)};
            
            const agentsContainer = document.getElementById('agents');
            const tooltip = document.getElementById('tooltip');
            
            function renderAgents() {{
                agentsContainer.innerHTML = '';
                
                agents.forEach(agent => {{
                    const div = document.createElement('div');
                    div.className = `agent ${{agent.state.toLowerCase()}} ${{selectedAgent === agent.name ? 'selected' : ''}}`;
                    
                    // Position mapping (logical → physical)
                    div.style.left = `${{agent.x * cellSize + 2}}px`;
                    div.style.top = `${{agent.y * cellSize + 2}}px`;
                    
                    // Color
                    const color = agentColors[agent.name] || agentColors.default;
                    div.style.backgroundColor = color;
                    div.style.color = color;
                    
                    // Initial (for smooth fade-in)
                    div.textContent = agent.name[0];
                    
                    // Hover tooltip
                    div.addEventListener('mouseenter', (e) => {{
                        tooltip.style.display = 'block';
                        tooltip.style.left = `${{e.pageX + 10}}px`;
                        tooltip.style.top = `${{e.pageY + 10}}px`;
                        tooltip.innerHTML = `
                            <strong>${{agent.name}}</strong><br>
                            State: ${{agent.state}}<br>
                            Position: (${{agent.x}}, ${{agent.y}})<br>
                            ${{agent.thought ? '💭 ' + agent.thought : ''}}
                        `;
                    }});
                    
                    div.addEventListener('mouseleave', () => {{
                        tooltip.style.display = 'none';
                    }});
                    
                    div.addEventListener('mousemove', (e) => {{
                        tooltip.style.left = `${{e.pageX + 10}}px`;
                        tooltip.style.top = `${{e.pageY + 10}}px`;
                    }});
                    
                    agentsContainer.appendChild(div);
                }});
            }}
            
            renderAgents();
        </script>
    </body>
    </html>
    """
    
    # Render in Streamlit
    components.html(html_code, height=(map_size * cell_size) + 60)
