# GitHub Issues Upload Script

Write-Host "🚀 Neon Society - GitHub Issues Upload Script" -ForegroundColor Cyan
Write-Host ""

# Check if gh CLI is installed
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "✅ GitHub CLI found!" -ForegroundColor Green
    
    # Issue #1
    Write-Host "Creating Issue #1: LRU History Cap..." -ForegroundColor Yellow
    gh issue create `
        --title "[P1] Implement LRU History Cap for DVR" `
        --label "performance,quick-win,priority:high" `
        --body-file ".github/issues/issue_1_lru_cap.md"
    
    # Issue #2
    Write-Host "Creating Issue #2: Diff-Based Snapshots..." -ForegroundColor Yellow
    gh issue create `
        --title "[P1] Replace Full Snapshots with Diff-Based Storage" `
        --label "performance,optimization,priority:high" `
        --body-file ".github/issues/issue_2_diff_snapshots.md"
    
    # Issue #3
    Write-Host "Creating Issue #3: Streamlit Fragments..." -ForegroundColor Yellow
    gh issue create `
        --title "[P1] Use st.experimental_fragment for Partial Reruns" `
        --label "performance,ui,priority:high" `
        --body-file ".github/issues/issue_3_fragments.md"
    
    # Issue #4
    Write-Host "Creating Issue #4: Spatial Hash Grid..." -ForegroundColor Yellow
    gh issue create `
        --title "[P2] Replace O(n²) Proximity Check with Spatial Hash" `
        --label "performance,algorithm,priority:medium" `
        --body-file ".github/issues/issue_4_spatial_grid.md"
    
    # Issue #5
    Write-Host "Creating Issue #5: Async LLM Batch..." -ForegroundColor Yellow
    gh issue create `
        --title "[P2] Batch Parallel LLM Calls for All Agents" `
        --label "performance,gemini,priority:medium" `
        --body-file ".github/issues/issue_5_async_llm.md"
    
    # Issue #6
    Write-Host "Creating Issue #6: Component Caching..." -ForegroundColor Yellow
    gh issue create `
        --title "[P2] Add st.cache_data for Stable Components" `
        --label "performance,ui,priority:medium" `
        --body-file ".github/issues/issue_6_caching.md"
    
    # Issue #7
    Write-Host "Creating Issue #7: WebSocket Backend..." -ForegroundColor Yellow
    gh issue create `
        --title "[P3] Implement FastAPI WebSocket Backend" `
        --label "architecture,backend,priority:low" `
        --body-file ".github/issues/issue_7_websocket.md"
    
    # Issue #8
    Write-Host "Creating Issue #8: React Frontend..." -ForegroundColor Yellow
    gh issue create `
        --title "[P3] Build React/Next.js Frontend with True Animations" `
        --label "architecture,frontend,priority:low" `
        --body-file ".github/issues/issue_8_react_frontend.md"
    
    # Issue #9
    Write-Host "Creating Issue #9: Neon Visual Theme..." -ForegroundColor Yellow
    gh issue create `
        --title "[P1] Implement Cyberpunk Neon Visual Theme" `
        --label "ui,design,priority:high" `
        --body-file ".github/issues/issue_9_neon_theme.md"
    
    # Issue #10
    Write-Host "Creating Issue #10: DVR Visual Feedback..." -ForegroundColor Yellow
    gh issue create `
        --title "[P2] Add Red Overlay for DVR Time Travel Mode" `
        --label "ui,feature,priority:medium" `
        --body-file ".github/issues/issue_10_dvr_feedback.md"
    
    Write-Host ""
    Write-Host "✅ All 10 Issues created successfully!" -ForegroundColor Green
    
} else {
    Write-Host "❌ GitHub CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Option 1: Install GitHub CLI" -ForegroundColor Yellow
    Write-Host "  winget install --id GitHub.cli" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Option 2: Manual Upload" -ForegroundColor Yellow
    Write-Host "  1. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/issues/new" -ForegroundColor Cyan
    Write-Host "  2. Copy content from .github/issues/issue_N_*.md files" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "All issue files are in: .github/issues/" -ForegroundColor Green
}
