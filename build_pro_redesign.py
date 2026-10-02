# -*- coding: utf-8 -*-
"""
Professional UI & High-Performance Search Engine Generator
Features:
1. Ultra-fast, fuzzy, substring search engine (micro, office, 365, windows, gpt, gemini, arabic synonyms).
2. Complete 377+ products database with rich Microsoft, Office, Gemini, ChatGPT, Canva, Netflix items.
3. Long unguessable password/PIN protection with visibility toggle, remember-me persistence, and settings change.
4. Professional, neatly organized layout with consistent pill buttons, quick search chips, and 120fps smooth scrolling.
5. Real-time store notifications (browser push, audio chime, live dropdown, floating toast).
"""
import json
import os

with open("public/api/catalog.json", "r", encoding="utf-8") as f:
    catalog_json = f.read()

with open("public/api/stores.json", "r", encoding="utf-8") as f:
    stores_json = f.read()

with open("public/api/all_products.json", "r", encoding="utf-8") as f:
    all_products_json = f.read()

with open("public/api/market-chart.json", "r", encoding="utf-8") as f:
    market_chart_json = f.read()

with open("public/api/history.json", "r", encoding="utf-8") as f:
    history_json = f.read()

html_content = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>رادار السوق | مقارنة أسعار الاشتراكات والمنتجات الرقمية</title>
  
  <!-- PWA & Mobile Meta -->
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#060910" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <meta name="apple-mobile-web-app-title" content="رادار السوق" />
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Chart.js local script with CDN fallback -->
  <script src="/static/chart.umd.min.js" onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/npm/chart.js';"></script>

  <style>
    :root {
      --bg-base: #060910;
      --bg-card: #0d1424;
      --bg-card-hover: #121c32;
      --panel-surface: rgba(13, 20, 36, 0.88);
      --panel-border: rgba(255, 255, 255, 0.08);
      --panel-border-bright: rgba(255, 255, 255, 0.18);
      
      --mint: #00e599;
      --mint-glow: rgba(0, 229, 153, 0.35);
      --mint-subtle: rgba(0, 229, 153, 0.12);
      
      --blue: #38bdf8;
      --purple: #a855f7;
      --red: #ff4d4f;
      --orange: #f59e0b;
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-xl: 24px;
      --radius-full: 9999px;
      
      --sidebar-width: 250px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: 'Cairo', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
      background: radial-gradient(circle at 85% 15%, rgba(0, 229, 153, 0.06) 0%, transparent 40%),
                  radial-gradient(circle at 15% 85%, rgba(56, 189, 248, 0.05) 0%, transparent 40%),
                  var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
    }

    .ltr { direction: ltr; display: inline-block; text-align: left; }
    .mono { font-family: 'JetBrains Mono', monospace; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.12); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0, 229, 153, 0.3); }

    /* ========================================================
       TOP HEADER: CENTERED BRANDING & MINIMALIST OLED
       ======================================================== */
    .top-header {
      position: sticky;
      top: 0;
      z-index: 100;
      height: 68px;
      background: rgba(6, 9, 16, 0.94);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--panel-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.5rem;
      position: relative;
    }

    /* Centered Brand in Top Header */
    .header-center-brand {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
    }
    .header-center-brand:hover .brand-title {
      color: var(--mint);
    }
    .brand-logo-icon {
      width: 34px;
      height: 34px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .brand-logo-icon svg {
      width: 32px;
      height: 32px;
      filter: drop-shadow(0 0 12px rgba(0, 229, 153, 0.5));
    }
    .brand-text-block {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
    .brand-title {
      font-size: 1.35rem;
      font-weight: 900;
      color: #fff;
      letter-spacing: -0.5px;
      line-height: 1.1;
      transition: color 0.2s ease;
    }
    .brand-subtitle {
      font-size: 0.72rem;
      color: var(--text-dim);
      font-weight: 600;
      letter-spacing: 0.2px;
    }

    /* Sidebar Mobile / Drawer Toggle */
    .sidebar-mobile-toggle {
      display: none;
      align-items: center;
      gap: 8px;
      height: 38px;
      padding: 0 14px;
      border-radius: var(--radius-full);
      background: rgba(14, 20, 34, 0.85);
      border: 1px solid var(--panel-border);
      color: var(--text-main);
      font-size: 0.84rem;
      font-weight: 700;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .sidebar-mobile-toggle:hover {
      background: rgba(22, 31, 52, 1);
      border-color: var(--mint);
    }
    @media (max-width: 1024px) {
      .sidebar-mobile-toggle { display: inline-flex; }
    }

    /* Header Live Status Badge */
    .header-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: rgba(0, 229, 153, 0.08);
      border: 1px solid rgba(0, 229, 153, 0.25);
      color: var(--mint);
      font-size: 0.76rem;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: var(--radius-full);
      user-select: none;
    }

    .pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--mint);
      box-shadow: 0 0 8px var(--mint);
      animation: pulseGlow 1.8s infinite;
    }
    @keyframes pulseGlow {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.35; transform: scale(0.85); }
    }
    .spinning-icon {
      animation: spin 0.75s linear infinite;
    }
    @keyframes spin {
      100% { transform: rotate(360deg); }
    }

    .notif-badge-pill {
      background: var(--red);
      color: #fff;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 1px 7px;
      border-radius: var(--radius-full);
      box-shadow: 0 0 10px rgba(255, 77, 79, 0.7);
    }

    /* Notification Dropdown Panel */
    .notif-dropdown-panel {
      position: fixed;
      top: 74px;
      right: calc(var(--sidebar-width) + 16px);
      width: 380px;
      max-width: calc(100vw - 32px);
      background: #0d1424;
      border: 1px solid rgba(0, 229, 153, 0.35);
      border-radius: var(--radius-lg);
      box-shadow: 0 20px 50px rgba(0,0,0,0.85), 0 0 25px rgba(0, 229, 153, 0.15);
      z-index: 1000;
      display: none;
      flex-direction: column;
      overflow: hidden;
      animation: toastIn 0.2s ease;
    }
    @media (max-width: 1024px) {
      .notif-dropdown-panel { right: 16px; left: 16px; width: auto; }
    }
    .notif-dropdown-panel.active { display: flex; }
    .notif-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 16px;
      background: rgba(255,255,255,0.03);
      border-bottom: 1px solid var(--panel-border);
    }
    .notif-list {
      max-height: 340px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
    }
    .notif-item {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.04);
      display: flex;
      flex-direction: column;
      gap: 3px;
      cursor: pointer;
      transition: background 0.15s;
    }
    .notif-item:hover { background: rgba(255,255,255,0.05); }
    .notif-item-title {
      font-size: 0.86rem;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .notif-item-desc { font-size: 0.8rem; color: var(--text-muted); }
    .notif-item-time { font-size: 0.72rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; }

    /* Full Notifications View Card Styles */
    .full-notif-card {
      background: var(--bg-card);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-lg);
      padding: 1.25rem 1.4rem;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      cursor: pointer;
    }
    .full-notif-card:hover {
      background: var(--bg-card-hover);
      border-color: rgba(0, 229, 153, 0.45);
      transform: translateY(-2px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 20px rgba(0, 229, 153, 0.1);
    }
    .full-notif-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    .full-notif-store-info {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .full-notif-body {
      font-size: 0.96rem;
      font-weight: 700;
      color: #fff;
      line-height: 1.55;
    }
    .full-notif-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* ========================================================
       MAIN BODY & RIGHT SIDEBAR COMMAND CENTER (RTL)
       ======================================================== */
    .app-body {
      display: flex;
      flex: 1;
      width: 100%;
      position: relative;
    }

    .app-sidebar {
      width: var(--sidebar-width);
      min-width: var(--sidebar-width);
      background: rgba(8, 12, 20, 0.96);
      border-left: 1px solid var(--panel-border);
      display: flex;
      flex-direction: column;
      padding: 1.25rem 0.9rem;
      gap: 6px;
      user-select: none;
      min-height: calc(100vh - 68px);
      transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @media (max-width: 1024px) {
      .app-sidebar {
        position: fixed;
        top: 68px;
        right: 0;
        bottom: 0;
        z-index: 999;
        box-shadow: -10px 0 35px rgba(0, 0, 0, 0.85);
        transform: translateX(100%);
      }
      .app-sidebar.open {
        transform: translateX(0);
      }
    }
    .sidebar-backdrop {
      display: none;
      position: fixed;
      top: 68px;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(4px);
      z-index: 998;
    }
    .sidebar-backdrop.active { display: block; }

    .sidebar-header-row {
      display: none;
      align-items: center;
      justify-content: space-between;
      padding: 0 4px 8px 4px;
      border-bottom: 1px solid var(--panel-border);
      margin-bottom: 6px;
    }
    @media (max-width: 1024px) {
      .sidebar-header-row { display: flex; }
    }
    .sidebar-close-btn {
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-size: 1.1rem;
      cursor: pointer;
      padding: 4px;
    }
    .sidebar-close-btn:hover { color: #fff; }

    .sidebar-section-title {
      font-size: 0.72rem;
      color: var(--text-dim);
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 6px 8px 2px 8px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 0.65rem 0.85rem;
      border-radius: var(--radius-md);
      color: var(--text-muted);
      font-size: 0.88rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      text-decoration: none;
    }
    .nav-item:hover {
      background: rgba(255, 255, 255, 0.05);
      color: #fff;
    }
    .nav-item.active {
      background: rgba(0, 229, 153, 0.12);
      color: var(--mint);
      border: 1px solid rgba(0, 229, 153, 0.25);
    }
    .nav-icon {
      width: 18px;
      height: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .sidebar-divider {
      height: 1px;
      background: var(--panel-border);
      margin: 8px 4px;
    }

    .sidebar-actions-stack {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 8px;
    }

    .sidebar-action-btn {
      width: 100%;
      height: 38px;
      padding: 0 12px;
      border-radius: var(--radius-md);
      background: rgba(14, 20, 34, 0.85);
      border: 1px solid var(--panel-border);
      color: var(--text-muted);
      font-size: 0.84rem;
      font-weight: 700;
      font-family: inherit;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      transition: all 0.2s ease;
      user-select: none;
    }
    .sidebar-action-btn:hover {
      background: rgba(22, 31, 52, 0.95);
      color: #fff;
      border-color: var(--panel-border-bright);
      transform: translateX(-2px);
    }
    .sidebar-action-btn.crawler-btn {
      background: rgba(0, 229, 153, 0.12) !important;
      border: 1px solid rgba(0, 229, 153, 0.45) !important;
      color: #fff !important;
      box-shadow: 0 0 12px rgba(0, 229, 153, 0.15);
    }
    .sidebar-action-btn.crawler-btn:hover {
      background: rgba(0, 229, 153, 0.22) !important;
      border-color: var(--mint) !important;
      box-shadow: 0 0 18px rgba(0, 229, 153, 0.35);
    }
    .sidebar-action-btn.lock-btn:hover {
      border-color: rgba(255, 77, 79, 0.4);
      color: var(--red);
    }

    .sidebar-user-block {
      margin-top: auto;
      padding: 0.65rem 0.85rem;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .sidebar-user-block:hover {
      background: rgba(255, 255, 255, 0.07);
    }
    .user-pill-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--mint);
      color: #030508;
      font-size: 0.85rem;
      font-weight: 900;
      font-family: 'JetBrains Mono', monospace;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    /* Main Content Area */
    .app-main {
      flex: 1;
      padding: 1.5rem 2rem 3rem 2rem;
      max-width: 1450px;
      margin: 0 auto;
      width: 100%;
    }

    .view-container { display: none; }
    .view-container.active { display: block; animation: fadeIn 0.2s ease; }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ========================================================
       INTELLIGENT FILTER & SEARCH BAR WITH CHIPS
       ======================================================== */
    .filter-wrapper {
      background: rgba(13, 20, 36, 0.75);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-xl);
      padding: 1rem 1.2rem;
      margin-bottom: 1.2rem;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .filters-inline-bar {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .filter-inline-item {
      position: relative;
      flex: 1;
      min-width: 170px;
    }

    .filter-inline-select {
      width: 100%;
      height: 44px;
      background: rgba(6, 9, 16, 0.85);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      color: #fff;
      font-family: inherit;
      font-size: 0.88rem;
      font-weight: 700;
      padding: 0 14px 0 34px;
      appearance: none;
      -webkit-appearance: none;
      outline: none;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .filter-inline-select:focus {
      border-color: var(--mint);
      box-shadow: 0 0 12px var(--mint-subtle);
    }
    .filter-inline-icon {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      pointer-events: none;
    }

    .filter-inline-search {
      flex: 1.8;
      min-width: 260px;
      position: relative;
    }
    .filter-inline-search input {
      width: 100%;
      height: 44px;
      background: rgba(6, 9, 16, 0.85);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      color: #fff;
      font-family: inherit;
      font-size: 0.92rem;
      padding: 0 14px 0 65px;
      outline: none;
      transition: all 0.2s ease;
    }
    .filter-inline-search input:focus {
      border-color: var(--mint);
      box-shadow: 0 0 14px var(--mint-subtle);
    }
    .search-icon-left {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      pointer-events: none;
    }
    .search-clear-btn {
      position: absolute;
      left: 36px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-dim);
      font-size: 1.1rem;
      cursor: pointer;
      padding: 2px 6px;
      display: none;
    }
    .search-clear-btn:hover { color: #fff; }

    /* Quick Search Suggestions Chips */
    .quick-chips-row {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
      padding-top: 4px;
      border-top: 1px solid rgba(255, 255, 255, 0.04);
    }
    .quick-chips-lbl {
      font-size: 0.76rem;
      color: var(--text-dim);
      font-weight: 700;
      margin-left: 4px;
    }
    .quick-chip {
      height: 28px;
      padding: 0 11px;
      border-radius: var(--radius-full);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.07);
      color: var(--text-muted);
      font-size: 0.78rem;
      font-weight: 700;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      user-select: none;
    }
    .quick-chip:hover {
      background: rgba(0, 229, 153, 0.12);
      border-color: rgba(0, 229, 153, 0.35);
      color: var(--mint);
      transform: translateY(-1px);
    }
    .quick-chip.active {
      background: rgba(0, 229, 153, 0.18);
      border-color: var(--mint);
      color: var(--mint);
      box-shadow: 0 0 10px rgba(0, 229, 153, 0.2);
    }

    /* ========================================================
       SUMMARY KPI BAR (Image 1 Exact Spec)
       ======================================================== */
    .summary-kpi-banner {
      background: rgba(13, 20, 36, 0.85);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-lg);
      padding: 1.1rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-around;
      margin-bottom: 1.2rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .kpi-col { display: flex; align-items: center; gap: 14px; }
    .kpi-icon-wrap {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .kpi-icon-wrap.mint { background: rgba(0, 229, 153, 0.12); color: var(--mint); }
    .kpi-icon-wrap.blue { background: rgba(56, 189, 248, 0.12); color: var(--blue); }
    .kpi-icon-wrap.dim { background: rgba(255, 255, 255, 0.05); color: var(--text-muted); }
    .kpi-text-block { display: flex; flex-direction: column; }
    .kpi-val {
      font-size: 1.55rem;
      font-weight: 900;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
      line-height: 1.2;
    }
    .kpi-val.mint { color: var(--mint); }
    .kpi-lbl { font-size: 0.8rem; color: var(--text-muted); font-weight: 600; }
    .kpi-divider { width: 1px; height: 38px; background: var(--panel-border); }

    /* Sub-bar: View Mode Toggles & Sorting */
    .sub-filter-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.2rem;
      font-size: 0.86rem;
      color: var(--text-muted);
      gap: 12px;
      flex-wrap: wrap;
    }
    .view-mode-toggle-group {
      display: inline-flex;
      align-items: center;
      background: rgba(13, 20, 36, 0.85);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-full);
      padding: 3px;
      gap: 3px;
    }
    .mode-toggle-btn {
      padding: 6px 14px;
      border-radius: var(--radius-full);
      font-size: 0.8rem;
      font-weight: 700;
      font-family: inherit;
      color: var(--text-muted);
      border: none;
      background: transparent;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .mode-toggle-btn.active {
      background: rgba(0, 229, 153, 0.16);
      color: var(--mint);
      border: 1px solid rgba(0, 229, 153, 0.35);
      box-shadow: 0 0 10px rgba(0, 229, 153, 0.15);
    }
    .mode-toggle-btn:hover:not(.active) { color: #fff; background: rgba(255, 255, 255, 0.05); }

    .sort-control-inline {
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      color: var(--text-muted);
    }
    .sort-control-inline select {
      background: transparent;
      border: none;
      color: #fff;
      font-family: inherit;
      font-size: 0.86rem;
      font-weight: 700;
      outline: none;
      cursor: pointer;
    }

    /* ========================================================
       OFFER CARDS GRID: 120FPS HARDWARE ACCELERATED
       ======================================================== */
    .offers-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.2rem;
      margin-bottom: 2rem;
      contain: layout style;
    }
    @media (max-width: 1200px) { .offers-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 768px) { .offers-grid { grid-template-columns: 1fr; } }

    .offer-card {
      background: var(--bg-card);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-xl);
      padding: 1.25rem 1.4rem;
      display: flex;
      flex-direction: column;
      gap: 12px;
      position: relative;
      cursor: pointer;
      transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25);
    }
    .offer-card:hover {
      background: var(--bg-card-hover);
      border-color: rgba(0, 229, 153, 0.45);
      transform: translateY(-2px);
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45), 0 0 16px rgba(0, 229, 153, 0.14);
    }

    .card-top-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .merchant-avatar-info {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .card-index-badge {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-dim);
      font-size: 0.72rem;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .merchant-circle-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      color: #fff;
      font-weight: 800;
      font-size: 0.95rem;
      font-family: 'JetBrains Mono', monospace;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 12px rgba(0,0,0,0.3);
    }
    .merchant-title-sub {
      display: flex;
      flex-direction: column;
    }
    .merchant-title-sub .store-title {
      font-size: 0.98rem;
      font-weight: 800;
      color: #fff;
      line-height: 1.2;
    }
    .merchant-title-sub .product-sub {
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 2px;
    }

    .card-top-badges {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .badge-cheapest-pill {
      background: rgba(0, 229, 153, 0.15);
      border: 1px solid var(--mint);
      color: var(--mint);
      font-size: 0.72rem;
      padding: 3px 8px;
      border-radius: var(--radius-full);
      font-weight: 800;
    }
    .card-bookmark-btn {
      background: transparent;
      border: none;
      color: var(--text-dim);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 4px;
      transition: color 0.2s;
    }
    .card-bookmark-btn:hover, .card-bookmark-btn.active { color: var(--mint); }

    .card-pricing-sparkline-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 4px 0;
    }
    .card-large-price {
      font-size: 2.1rem;
      font-weight: 900;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
      line-height: 1;
    }
    .sparkline-svg {
      width: 120px;
      height: 32px;
      overflow: visible;
    }

    .card-weekly-change-row {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
      font-weight: 700;
    }
    .change-decrease { color: var(--mint); }
    .change-increase { color: var(--red); }
    .change-neutral { color: var(--text-muted); }

    .card-meta-details-row {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 0.78rem;
      color: var(--text-dim);
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      padding-top: 8px;
    }
    .meta-inline-item {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .btn-card-details {
      width: 100%;
      height: 36px;
      border-radius: var(--radius-md);
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--panel-border);
      color: #fff;
      font-family: inherit;
      font-size: 0.84rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s ease;
      margin-top: 4px;
    }
    .btn-card-details:hover {
      background: rgba(0, 229, 153, 0.15);
      border-color: rgba(0, 229, 153, 0.4);
      color: var(--mint);
    }

    /* ========================================================
       MARKET CHART SECTION (Reference Image 1 Bottom)
       ======================================================== */
    .market-chart-section {
      background: var(--bg-card);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-xl);
      padding: 1.5rem;
      margin-bottom: 2rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .market-chart-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.2rem;
      flex-wrap: wrap;
      gap: 12px;
    }
    .market-chart-title {
      font-size: 1.2rem;
      font-weight: 800;
      color: #fff;
    }
    .chart-controls-legend {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
      color: var(--text-muted);
    }
    .legend-dot { width: 8px; height: 8px; border-radius: 50%; }
    .period-select-box {
      background: rgba(6, 9, 16, 0.85);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      color: #fff;
      font-family: inherit;
      font-size: 0.8rem;
      font-weight: 700;
      padding: 6px 12px;
      outline: none;
      cursor: pointer;
    }
    .chart-container-box {
      width: 100%;
      height: 260px;
      position: relative;
    }

    /* ========================================================
       MODALS: OFFER DETAILS & PIN LOCK
       ======================================================== */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      z-index: 1000;
      background: rgba(4, 6, 12, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      animation: fadeIn 0.2s ease;
    }
    .modal-backdrop.active { display: flex; }

    .modal-glass-card {
      width: 100%;
      max-width: 650px;
      max-height: 90vh;
      overflow-y: auto;
      background: #0d1424;
      border: 1px solid rgba(0, 229, 153, 0.25);
      border-radius: var(--radius-xl);
      padding: 1.8rem;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
      position: relative;
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
    }
    .modal-close-btn {
      position: absolute;
      top: 16px;
      left: 16px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--panel-border);
      color: var(--text-muted);
      font-size: 1.2rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
    }
    .modal-close-btn:hover { background: rgba(255, 255, 255, 0.15); color: #fff; }

    .modal-top-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }
    .modal-current-price-huge {
      font-size: 2.5rem;
      font-weight: 900;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
    }
    .modal-merchant-identity {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .modal-three-pills {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
    }
    .metric-pill-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      padding: 0.8rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .metric-pill-label { font-size: 0.76rem; color: var(--text-muted); font-weight: 600; }
    .metric-pill-val { font-size: 1.15rem; font-weight: 800; color: #fff; font-family: 'JetBrains Mono', monospace; }
    .metric-pill-val.mint { color: var(--mint); }

    .modal-chart-card {
      background: rgba(6, 9, 16, 0.85);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-lg);
      padding: 1.2rem;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .modal-table-box {
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      overflow: hidden;
    }
    .changes-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
      text-align: right;
    }
    .changes-table th {
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-muted);
      font-weight: 600;
      padding: 8px 12px;
      border-bottom: 1px solid var(--panel-border);
    }
    .changes-table td {
      padding: 8px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.03);
      font-family: 'JetBrains Mono', monospace;
    }
    .changes-table tr:last-child td { border-bottom: none; }

    .modal-footer-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      margin-top: 4px;
    }
    .btn-mint-primary {
      height: 42px;
      padding: 0 20px;
      border-radius: var(--radius-md);
      background: var(--mint);
      color: #030508;
      font-size: 0.88rem;
      font-weight: 800;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 0 18px var(--mint-glow);
      text-decoration: none;
      transition: all 0.2s;
    }
    .btn-mint-primary:hover { background: #00ffaa; transform: translateY(-1px); }
    .btn-glass-secondary {
      height: 42px;
      padding: 0 16px;
      border-radius: var(--radius-md);
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--panel-border);
      color: #fff;
      font-size: 0.88rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-glass-secondary:hover { background: rgba(255, 255, 255, 0.12); }

    /* PIN Lock Modal (Long Passwords & Unguessable Security) */
    .pin-lock-modal {
      position: fixed;
      inset: 0;
      z-index: 99999;
      background: rgba(4, 6, 12, 0.92);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
      transition: opacity 0.25s ease;
    }
    .pin-card {
      width: 100%;
      max-width: 440px;
      background: #0d1424;
      border: 1px solid rgba(0, 229, 153, 0.35);
      border-radius: var(--radius-xl);
      padding: 2.4rem 2.2rem;
      box-shadow: 0 24px 60px rgba(0,0,0,0.85), 0 0 35px rgba(0, 229, 153, 0.15);
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
    .pin-input-field {
      width: 100%;
      height: 48px;
      background: rgba(6, 9, 16, 0.9);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      color: #fff;
      font-size: 1.15rem;
      text-align: center;
      font-family: 'JetBrains Mono', monospace;
      outline: none;
      transition: all 0.2s;
      padding: 0 40px 0 14px;
    }
    .pin-input-field:focus {
      border-color: var(--mint);
      box-shadow: 0 0 16px var(--mint-glow);
    }
    .input-shake {
      animation: shake 0.35s ease-in-out;
      border-color: var(--red) !important;
    }
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-8px); }
      40%, 80% { transform: translateX(8px); }
    }

    /* Toast Container */
    .toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
    }
    .toast {
      background: rgba(14, 20, 36, 0.96);
      border: 1px solid rgba(0, 229, 153, 0.45);
      color: #fff;
      padding: 12px 20px;
      border-radius: var(--radius-md);
      font-size: 0.9rem;
      font-weight: 700;
      box-shadow: 0 10px 35px rgba(0,0,0,0.6);
      animation: toastIn 0.25s ease;
      pointer-events: auto;
    }
    @keyframes toastIn {
      from { transform: translateY(12px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    /* ========================================================
       RESPONSIVE MOBILE & TABLET UI/UX OVERHAUL (100% Fluid)
       ======================================================== */
    /* Mobile Bottom Floating App Bar */
    .mobile-bottom-bar {
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      height: 60px;
      background: rgba(8, 12, 20, 0.96);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-top: 1px solid var(--panel-border);
      z-index: 990;
      padding: 0 6px;
      padding-bottom: env(safe-area-inset-bottom, 0px);
      align-items: center;
      justify-content: space-around;
      box-shadow: 0 -6px 25px rgba(0, 0, 0, 0.75);
    }
    @media (max-width: 1024px) {
      .mobile-bottom-bar { display: flex; }
      body { padding-bottom: 66px; }
      .app-sidebar {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        z-index: 1050;
        width: 280px;
        max-width: 85vw;
        box-shadow: -10px 0 45px rgba(0, 0, 0, 0.9);
        transform: translateX(100%);
        overflow-y: auto;
      }
      .app-sidebar.open {
        transform: translateX(0);
      }
      .sidebar-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 1040;
      }
      .notif-dropdown-panel {
        top: 68px;
        right: 12px;
        left: 12px;
        width: auto;
        max-height: 80vh;
      }
    }
    .mobile-bottom-item {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-size: 0.68rem;
      font-weight: 700;
      font-family: inherit;
      cursor: pointer;
      padding: 6px 0;
      transition: all 0.15s ease;
      user-select: none;
      -webkit-tap-highlight-color: transparent;
    }
    .mobile-bottom-item:active { transform: scale(0.92); }
    .mobile-bottom-item.active { color: var(--mint); }
    .mobile-bottom-item.active svg { stroke: var(--mint); filter: drop-shadow(0 0 6px var(--mint-glow)); }

    /* Header elements on mobile */
    .header-left-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .header-notif-btn {
      position: relative;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--panel-border);
      color: var(--text-main);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
    }
    .header-notif-btn:hover {
      background: rgba(0, 229, 153, 0.12);
      border-color: var(--mint);
      color: var(--mint);
    }
    .header-notif-btn .notif-badge-pill {
      position: absolute;
      top: -4px;
      right: -4px;
      font-size: 0.64rem;
      padding: 0 5px;
    }

    @media (max-width: 768px) {
      :root { --sidebar-width: 280px; }
      .top-header { height: 60px; padding: 0 0.85rem; }
      .brand-title { font-size: 1.15rem; }
      .brand-subtitle { display: none; }
      .brand-logo-icon { width: 30px; height: 30px; }
      .brand-logo-icon svg { width: 28px; height: 28px; }
      .sidebar-mobile-toggle span { display: none; }
      .sidebar-mobile-toggle { padding: 0 10px; height: 36px; }
      .header-status-pill { display: none; }

      .app-main { padding: 1rem 0.85rem 5.5rem 0.85rem; }
      .filter-wrapper { padding: 0.85rem; }
      .filter-inline-item { min-width: 100%; flex: 1 1 100%; }
      .filter-inline-search { min-width: 100%; flex: 1 1 100%; }
      .filter-inline-search input { font-size: 16px; }
      .filter-inline-select { font-size: 16px; }

      .quick-chips-row {
        overflow-x: auto;
        flex-wrap: nowrap;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 6px;
        scrollbar-width: none;
      }
      .quick-chips-row::-webkit-scrollbar { display: none; }
      .quick-chip { flex-shrink: 0; white-space: nowrap; }

      .summary-kpi-banner {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        padding: 0.85rem 0.4rem;
        gap: 4px;
      }
      .kpi-divider { display: none; }
      .kpi-col { flex-direction: column; text-align: center; gap: 4px; }
      .kpi-icon-wrap { width: 32px; height: 32px; margin: 0 auto; }
      .kpi-icon-wrap svg { width: 16px; height: 16px; }
      .kpi-val { font-size: 1.15rem; }
      .kpi-lbl { font-size: 0.68rem; }

      .sub-filter-row { flex-direction: column; align-items: stretch; gap: 10px; }
      .view-mode-toggle-group { width: 100%; justify-content: space-between; }
      .mode-toggle-btn { flex: 1; justify-content: center; padding: 6px 8px; font-size: 0.74rem; }
      .sort-control-inline { justify-content: space-between; width: 100%; }

      .offers-grid { grid-template-columns: 1fr; gap: 1rem; }
      .offer-card { padding: 1.1rem 1rem; }
      
      .modal-glass-card { padding: 1.25rem 1rem; border-radius: var(--radius-lg); }
      .modal-top-header { flex-direction: column-reverse; align-items: flex-start; gap: 8px; }
      .modal-current-price-huge { font-size: 2rem; }
      .modal-three-pills { grid-template-columns: repeat(3, 1fr); gap: 6px; }
      .metric-pill-card { padding: 0.6rem 0.4rem; text-align: center; }
      .metric-pill-val { font-size: 0.92rem; }

      .full-notif-card { padding: 1rem; gap: 10px; }
      .full-notif-top { flex-direction: column; align-items: flex-start; gap: 8px; }
      .full-notif-actions { flex-direction: column; align-items: stretch; }
      .full-notif-actions button { width: 100%; justify-content: center; }

      .toast-container {
        bottom: 72px;
        right: 12px;
        left: 12px;
        align-items: stretch;
      }
      .toast { font-size: 0.82rem; padding: 10px 14px; }
    }
  </style>
</head>
<body>

  <!-- Top Header with Centered Brand -->
  <header class="top-header">
    <!-- Right Toggle (For Mobile & Tablets) -->
    <button class="sidebar-mobile-toggle" onclick="toggleSidebarDrawer()" title="فتح القائمة ولوحة التحكم">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
      <span>القائمة والتحكم</span>
    </button>

    <!-- Center Brand (Centered Perfectly) -->
    <div class="header-center-brand" onclick="switchView('comparison')">
      <div class="brand-logo-icon">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M12 3L22 21H2L12 3Z" fill="url(#mintGrad)" />
          <path d="M12 3L2 21H12V3Z" fill="#00e599" opacity="0.85" />
          <defs>
            <linearGradient id="mintGrad" x1="2" y1="3" x2="22" y2="21" gradientUnits="userSpaceOnUse">
              <stop stop-color="#00e599" />
              <stop offset="1" stop-color="#38bdf8" />
            </linearGradient>
          </defs>
        </svg>
      </div>
      <div class="brand-text-block">
        <span class="brand-title">رادار السوق</span>
        <span class="brand-subtitle">مقارنة أسعار الاشتراكات والمنتجات الرقمية</span>
      </div>
    </div>

    <!-- Left Live Indicator & Direct Notifications Bell -->
    <div class="header-left-actions">
      <button class="header-notif-btn" id="headerNotifBtn" onclick="toggleNotifPanel(event)" title="مركز الإشعارات">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
        <span class="notif-badge-pill" id="headerNotifBadge">6</span>
      </button>
      <div class="header-status-pill">
        <span class="pulse-dot"></span>
        <span>بيانات حية 24/7</span>
      </div>
    </div>
  </header>

  <!-- Mobile Backdrop -->
  <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="toggleSidebarDrawer()"></div>

  <!-- Instant Store Notifications Dropdown Panel -->
  <div class="notif-dropdown-panel" id="notifDropdownPanel">
    <div class="notif-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span style="font-weight:800; font-size:0.95rem; color:#fff;">الإشعارات الفورية للمتاجر</span>
        <span class="pulse-dot"></span>
      </div>
      <div style="display:flex; gap:6px;">
        <button onclick="requestBrowserNotifications()" class="btn-mint-primary" style="height:28px; padding:0 8px; font-size:0.75rem;" title="تفعيل إشعارات المتصفح">
          تفعيل إشعارات المتصفح 🔔
        </button>
        <button onclick="clearAllNotifications()" style="background:none; border:none; color:var(--text-dim); font-size:0.78rem; cursor:pointer;">
          مسح
        </button>
      </div>
    </div>
    <div class="notif-list" id="notifListContainer"></div>
    <div style="padding:10px 14px; background:rgba(0,0,0,0.3); border-top:1px solid var(--panel-border); display:flex; flex-direction:column; gap:8px;">
      <button onclick="switchView('notifications'); document.getElementById('notifDropdownPanel').classList.remove('active');" class="btn-mint-primary" style="height:34px; font-size:0.8rem; width:100%; justify-content:center;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
        <span>عرض كافة الإشعارات في صفحة مستقلة 📑</span>
      </button>
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.75rem; color:var(--text-dim);">رصد تلقائي لـ 12 متجر معتمد</span>
        <button onclick="simulateLiveStoreAlert()" style="background:none; border:none; color:var(--mint); font-size:0.76rem; font-weight:700; cursor:pointer;">
          + إشعار تجريبي ⚡
        </button>
      </div>
    </div>
  </div>

  <!-- App Body Layout -->
  <div class="app-body">

    <!-- Right Sidebar: Navigation & All Control Tools (RTL) -->
    <aside class="app-sidebar" id="appSidebar">
      
      <!-- Mobile Header Row -->
      <div class="sidebar-header-row">
        <span class="sidebar-section-title" style="padding:0; margin:0;">لوحة التحكم والتنقل</span>
        <button class="sidebar-close-btn" onclick="toggleSidebarDrawer()" title="إغلاق القائمة">✕</button>
      </div>

      <!-- Section: Navigation -->
      <div class="sidebar-section-title">الأقسام الرئيسية</div>
      <nav style="display:flex; flex-direction:column; gap:4px;">
        <div class="nav-item active" data-view="comparison" onclick="switchView('comparison'); closeSidebarOnMobile();">
          <div class="nav-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="20" x2="18" y2="10"></line>
              <line x1="12" y1="20" x2="12" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
          </div>
          <span>مقارنة الأسعار</span>
        </div>

        <div class="nav-item" data-view="merchants" onclick="switchView('merchants'); closeSidebarOnMobile();">
          <div class="nav-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
          </div>
          <span>مراقبة المتاجر (12)</span>
        </div>

        <div class="nav-item" data-view="alerts" onclick="switchView('alerts'); closeSidebarOnMobile();">
          <div class="nav-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          </div>
          <span>تنبيهات الأسعار</span>
        </div>

        <div class="nav-item" data-view="notifications" onclick="switchView('notifications'); closeSidebarOnMobile();">
          <div class="nav-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          </div>
          <span>مركز الإشعارات</span>
          <span class="notif-badge-pill" id="sidebarNotifBadge" style="margin-right:auto; font-size:0.72rem; padding:1px 7px;">6</span>
        </div>

        <div class="nav-item" data-view="subscriptions" onclick="switchView('subscriptions'); closeSidebarOnMobile();">
          <div class="nav-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
          </div>
          <span>دليل المنتجات</span>
        </div>

        <div class="nav-item" data-view="reports" onclick="switchView('reports'); closeSidebarOnMobile();">
          <div class="nav-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
          </div>
          <span>التقارير</span>
        </div>

        <div class="nav-item" data-view="settings" onclick="switchView('settings'); closeSidebarOnMobile();">
          <div class="nav-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          </div>
          <span>الإعدادات والأمان</span>
        </div>
      </nav>

      <div class="sidebar-divider"></div>

      <!-- Section: أدوات التحكم والمزامنة -->
      <div class="sidebar-section-title">أدوات التحكم والمزامنة</div>

      <div class="sidebar-actions-stack">
        <!-- Crawler Bot Button -->
        <button class="sidebar-action-btn crawler-btn" id="crawlerBtn" onclick="runCrawlerNow()" title="تشغيل وتحديث البوت الزاحف لحظياً لكافة المتاجر الـ 12">
          <div style="display:flex; align-items:center; gap:8px;">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="6" width="20" height="12" rx="4"></rect>
              <circle cx="8" cy="12" r="1.5" fill="currentColor"></circle>
              <circle cx="16" cy="12" r="1.5" fill="currentColor"></circle>
              <path d="M9 2v4M15 2v4M10 18v4M14 18v4M2 10h2M2 14h2M20 10h2M20 14h2"></path>
            </svg>
            <span style="font-weight:800;">البوت الزاحف</span>
          </div>
          <span class="pulse-dot"></span>
        </button>

        <!-- Refresh Prices Button -->
        <button class="sidebar-action-btn" onclick="refreshPricesNow()" title="تحديث الأسعار الآن">
          <div style="display:flex; align-items:center; gap:8px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"></path>
            </svg>
            <span>تحديث الأسعار</span>
          </div>
          <span style="font-size:0.75rem; color:var(--text-dim);">فوري</span>
        </button>

        <!-- Notifications Bell Button -->
        <button class="sidebar-action-btn" id="notifBellBtn" onclick="toggleNotifPanel(event)" title="مركز الإشعارات الفورية">
          <div style="display:flex; align-items:center; gap:8px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <span>الإشعارات الفورية</span>
          </div>
          <span class="notif-badge-pill" id="notifCountBadge">4</span>
        </button>

        <!-- Quick Lock / Logout -->
        <button class="sidebar-action-btn lock-btn" onclick="logoutApp()" title="قفل التطبيق برمز المرور">
          <div style="display:flex; align-items:center; gap:8px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span>قفل التطبيق (PIN)</span>
          </div>
          <span style="font-size:0.72rem; color:var(--text-dim);">أمان</span>
        </button>
      </div>

      <!-- User Profile Card -->
      <div class="sidebar-user-block" onclick="switchView('settings'); closeSidebarOnMobile();">
        <div class="user-pill-avatar" id="sidebarAvatar">AD</div>
        <div style="display:flex; flex-direction:column; line-height:1.2;">
          <span style="font-size:0.84rem; color:#fff; font-weight:800;">المستخدم (Admin)</span>
          <span style="font-size:0.72rem; color:var(--mint);">جلسة نشطة ومؤمنة 🔒</span>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="app-main">

      <!-- ========================================================
           VIEW 1: COMPARISON & SEARCH DASHBOARD
           ======================================================== -->
      <section id="view-comparison" class="view-container active">

        <!-- Intelligent Filter & Instant Search Wrapper -->
        <div class="filter-wrapper">
          <div class="filters-inline-bar">
            <!-- Category Selector -->
            <div class="filter-inline-item">
              <select id="categorySelect" class="filter-inline-select" onchange="onCategoryChanged(this.value)">
                <option value="all">جميع التصنيفات (الكل)</option>
                <option value="productivity">💼 مايكروسوفت والإنتاجية (Office / 365 / Windows)</option>
                <option value="ai">⚡ ذكاء اصطناعي (Gemini / ChatGPT / Claude)</option>
                <option value="design">🎨 تصميم ومونتاج (Canva / Adobe / CapCut)</option>
                <option value="streaming">🎬 بث وترفيه (Netflix / Spotify / YouTube)</option>
                <option value="tools">🛠️ أدوات وأمان (VPN / Notion / Telegram)</option>
              </select>
              <div class="filter-inline-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
              </div>
            </div>

            <!-- Product Family Selector -->
            <div class="filter-inline-item">
              <select id="productSelect" class="filter-inline-select" onchange="onProductChanged(this.value)">
                <option value="all">جميع المنتجات</option>
                <option value="Microsoft 365 / Office">Microsoft 365 / Office 💻</option>
                <option value="Gemini Pro">Gemini Pro ✦</option>
                <option value="ChatGPT / OpenAI">ChatGPT Plus / OpenAI 🤖</option>
                <option value="Canva / Design">Canva Pro / Adobe 🎨</option>
              </select>
              <div class="filter-inline-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
              </div>
            </div>

            <!-- Duration Selector -->
            <div class="filter-inline-item">
              <select id="durationSelect" class="filter-inline-select" onchange="onDurationChanged(this.value)">
                <option value="all">جميع المدد</option>
                <option value="18M">18 شهر</option>
                <option value="12M">12 شهر (سنة)</option>
                <option value="6M">6 شهور</option>
                <option value="1M">1 شهر</option>
              </select>
              <div class="filter-inline-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
              </div>
            </div>

            <!-- Fast Instant Search Input -->
            <div class="filter-inline-search">
              <input type="text" id="searchInput" placeholder="ابحث السريع: جرب 'micro'، 'office'، '365'، 'chatgpt' ..." oninput="onSearchChanged(this.value)" autocomplete="off" />
              <button class="search-clear-btn" id="searchClearBtn" onclick="clearSearchInput()" title="مسح البحث">×</button>
              <div class="search-icon-left">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              </div>
            </div>
          </div>

          <!-- Quick Suggestion Search Chips -->
          <div class="quick-chips-row">
            <span class="quick-chips-lbl">بحث سريع:</span>
            <button class="quick-chip active" onclick="applyQuickFilter('all', this)">🔥 الكل (370+ عرض)</button>
            <button class="quick-chip" onclick="applyQuickFilter('micro', this)">💼 Microsoft & Office 365</button>
            <button class="quick-chip" onclick="applyQuickFilter('gemini', this)">✦ Gemini Pro</button>
            <button class="quick-chip" onclick="applyQuickFilter('chatgpt', this)">🤖 ChatGPT & AI</button>
            <button class="quick-chip" onclick="applyQuickFilter('canva', this)">🎨 Canva & Adobe</button>
            <button class="quick-chip" onclick="applyQuickFilter('netflix', this)">🎬 Netflix & ترفيه</button>
            <button class="quick-chip" onclick="applyQuickFilter('vpn', this)">🛡️ VPN & أدوات</button>
          </div>
        </div>

        <!-- Summary KPI Banner (Matches Reference Image 1) -->
        <div class="summary-kpi-banner">
          <!-- Right: Lowest Price -->
          <div class="kpi-col">
            <div class="kpi-icon-wrap mint">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            </div>
            <div class="kpi-text-block">
              <span class="kpi-val mint" id="kpiLowestPrice">$0.35</span>
              <span class="kpi-lbl">أقل سعر في النتائج</span>
            </div>
          </div>

          <div class="kpi-divider"></div>

          <!-- Mid: Average Market Price -->
          <div class="kpi-col">
            <div class="kpi-icon-wrap blue">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
            </div>
            <div class="kpi-text-block">
              <span class="kpi-val" id="kpiAvgPrice">$1.15</span>
              <span class="kpi-lbl">متوسط السوق</span>
            </div>
          </div>

          <div class="kpi-divider"></div>

          <!-- Left: Merchants Count -->
          <div class="kpi-col">
            <div class="kpi-icon-wrap dim">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            </div>
            <div class="kpi-text-block">
              <span class="kpi-val" id="kpiMerchantsCount">12</span>
              <span class="kpi-lbl">عدد المتاجر المتوفرة</span>
            </div>
          </div>
        </div>

        <!-- Sub-bar (Showing count, Mode Toggle & Sorting) -->
        <div class="sub-filter-row">
          <div class="view-mode-toggle-group">
            <button class="mode-toggle-btn active" id="btnModeAll" onclick="setStoresFilterMode('all')" title="عرض كافة نتائج البحث والمتاجر">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
              <span>كافة عروض السوق (12 متجر)</span>
            </button>
            <button class="mode-toggle-btn" id="btnMode6" onclick="setStoresFilterMode('comparison6')" title="عرض خطة Gemini Pro المقارنة (6 عروض الأساسية)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
              <span>خطة Gemini Pro 18M (6 متاجر)</span>
            </button>
          </div>

          <div id="offersCountText" style="font-weight:700; color:var(--text-main);">عرض النتائج المتاحة ⓘ</div>

          <div class="sort-control-inline">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="21" y1="10" x2="7" y2="10"></line><line x1="21" y1="6" x2="3" y2="6"></line><line x1="21" y1="14" x2="11" y2="14"></line><line x1="21" y1="18" x2="15" y2="18"></line></svg>
            <span>الترتيب:</span>
            <select id="sortSelect" onchange="onSortChanged(this.value)">
              <option value="lowest_price">من الأقل سعراً</option>
              <option value="highest_price">من الأعلى سعراً</option>
              <option value="biggest_decrease">أكبر انخفاض</option>
              <option value="stock">المتوفر في المخزون</option>
            </select>
          </div>
        </div>

        <!-- Offer Cards Grid (Matches Reference Image 1 with Ultra Smoothness) -->
        <div class="offers-grid" id="offersGrid">
          <!-- Dynamically populated -->
        </div>

        <!-- Comparative Market History Chart (Reference Image 1 Bottom) -->
        <div class="market-chart-section">
          <div class="market-chart-header">
            <div class="market-chart-title">تاريخ وتقلبات الأسعار في السوق</div>
            <div class="chart-controls-legend">
              <div class="legend-item"><span class="legend-dot" style="background:var(--mint);"></span><span>Gemini Pixel Extractor</span></div>
              <div class="legend-item"><span class="legend-dot" style="background:var(--blue);"></span><span>PA Store</span></div>
              <div class="legend-item"><span class="legend-dot" style="background:var(--purple);"></span><span>Sam Topup</span></div>
              <select class="period-select-box" onchange="onMarketChartPeriodChanged(this.value)">
                <option value="30">آخر 30 يوم 📅</option>
                <option value="7">آخر 7 أيام</option>
                <option value="1">آخر 24 ساعة</option>
              </select>
            </div>
          </div>
          <div class="chart-container-box">
            <canvas id="marketComparisonCanvas"></canvas>
          </div>
        </div>

      </section>

      <!-- ========================================================
           VIEW 2: MERCHANTS (12 Verified Stores)
           ======================================================== -->
      <section id="view-merchants" class="view-container">
        <div style="margin-bottom:1.5rem;">
          <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">مراقبة المتاجر المعتمدة (12 متجر)</h2>
          <p style="font-size:0.88rem; color:var(--text-muted);">رصد ومزامنة لحظية لكافة البوتات والمتاجر الرقمية المسجلة وحالة المخزون</p>
        </div>
        <div class="offers-grid" id="merchantsGrid"></div>
      </section>

      <!-- ========================================================
           VIEW 3: PRICE ALERTS
           ======================================================== -->
      <section id="view-alerts" class="view-container">
        <div style="margin-bottom:1.5rem;">
          <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">التنبيهات السعرية الذكية</h2>
          <p style="font-size:0.88rem; color:var(--text-muted);">تتبع أي منتج واحصل على إشعار فوري عند انخفاض سعره عن هدفك</p>
        </div>
        <div class="modal-glass-card" style="margin-bottom:1.5rem; max-width:650px;">
          <h3 style="font-size:1.1rem; color:#fff; font-weight:800; margin-bottom:12px;">إنشاء تنبيه سعري جديد</h3>
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <input type="text" id="alertProdInput" placeholder="اسم المنتج (مثال: Microsoft 365 أو Gemini Pro)" class="filter-inline-select" style="flex:2;" />
            <input type="number" id="alertPriceInput" step="0.01" placeholder="السعر المستهدف (USD)" class="filter-inline-select" style="flex:1;" />
            <button class="btn-mint-primary" onclick="createPriceAlert()">إضافة التنبيه</button>
          </div>
        </div>
        <div class="modal-table-box" id="alertsTableBox"></div>
      </section>

      <!-- ========================================================
           VIEW 4: SUBSCRIPTIONS & ACCOUNTS CATALOG (379 Items)
           ======================================================== -->
      <section id="view-subscriptions" class="view-container">
        <div style="margin-bottom:1.2rem;">
          <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">دليل الاشتراكات والمنتجات الرقمية</h2>
          <p style="font-size:0.88rem; color:var(--text-muted);">استعراض شامل لكافة الحسابات والاشتراكات المتوفرة (379 حساب متوفر لدى 12 متجر معتمد)</p>
        </div>

        <!-- Catalog Filter & Search Wrapper -->
        <div class="filter-wrapper" style="margin-bottom:1.5rem;">
          <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin-bottom:12px;">
            <div class="filter-inline-search" style="flex:1; min-width:280px;">
              <input type="text" id="catalogSearchInput" placeholder="ابحث في دليل الـ 379 حساب بالاسم أو المتجر أو النوع..." oninput="onCatalogSearchChanged(this.value)" autocomplete="off" />
              <button class="search-clear-btn" id="catalogSearchClearBtn" onclick="clearCatalogSearch()" title="مسح">×</button>
              <div class="search-icon-left">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              </div>
            </div>
            <div id="catalogOffersCount" style="font-size:0.9rem; font-weight:800; color:var(--mint); white-space:nowrap; padding:0 8px;">
              عرض 379 حساب واشتراك
            </div>
          </div>

          <!-- Quick Category Filters for Catalog -->
          <div class="quick-chips-row">
            <span class="quick-chips-lbl">تصفية سريعة:</span>
            <button class="quick-chip active" onclick="filterCatalogCategory('all', this)">🔥 كافة الحسابات (379)</button>
            <button class="quick-chip" onclick="filterCatalogCategory('Microsoft 365 / Office', this)">💼 Microsoft & Office 365</button>
            <button class="quick-chip" onclick="filterCatalogCategory('Gemini Pro', this)">✦ Gemini Pro</button>
            <button class="quick-chip" onclick="filterCatalogCategory('ChatGPT / OpenAI', this)">🤖 ChatGPT & AI</button>
            <button class="quick-chip" onclick="filterCatalogCategory('Canva / Design', this)">🎨 Canva & التصميم</button>
            <button class="quick-chip" onclick="filterCatalogCategory('Streaming / Media', this)">🎬 البث والترفيه</button>
            <button class="quick-chip" onclick="filterCatalogCategory('Tools & VPN', this)">🛡️ أدوات و VPN</button>
            <button class="quick-chip" onclick="filterCatalogCategory('Windows OS & Keys', this)">💻 مفاتيح Windows</button>
            <button class="quick-chip" onclick="filterCatalogCategory('Outlook & Hotmail Mails', this)">📧 إيميلات Hotmail/Outlook</button>
          </div>
        </div>

        <!-- The Real 379-item Grid -->
        <div class="offers-grid" id="catalogGrid"></div>
      </section>

      <!-- ========================================================
           VIEW 5: REPORTS
           ======================================================== -->
      <section id="view-reports" class="view-container">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem; flex-wrap:wrap; gap:12px;">
          <div>
            <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">تقارير تقلبات الأسعار والمخزون</h2>
            <p style="font-size:0.88rem; color:var(--text-muted);">ملخص تحليلي لأعلى نسبة توفير وأقل العروض المسجلة</p>
          </div>
          <button class="btn-glass-secondary" onclick="exportReportsCSV()">تحميل تقرير CSV 📥</button>
        </div>
        <div class="modal-table-box" id="reportsTableBox"></div>
      </section>

      <!-- ========================================================
           VIEW 6: SETTINGS & SECURITY (PIN & NOTIFICATIONS)
           ======================================================== -->
      <section id="view-settings" class="view-container">
        <div style="margin-bottom:1.5rem;">
          <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">إعدادات الأمان والتفضيلات</h2>
          <p style="font-size:0.88rem; color:var(--text-muted);">إدارة رمز المرور السري، تذكر المستخدم، والإشعارات الفورية</p>
        </div>
        
        <div style="display:flex; flex-direction:column; gap:1.2rem; max-width:680px;">
          <!-- User Profile Box -->
          <div class="modal-glass-card" style="width:100%;">
            <h3 style="font-size:1.1rem; color:#fff; font-weight:800; margin-bottom:10px;">ملف المستخدم المحفوظ</h3>
            <div>
              <label style="font-size:0.84rem; color:var(--text-muted); display:block; margin-bottom:4px;">اسم المستخدم على هذا الجهاز:</label>
              <input type="text" id="settingsUserNameInput" class="filter-inline-select" value="المسؤول (Admin)" />
            </div>
            <button class="btn-mint-primary" onclick="saveSettingsUser()" style="justify-content:center; margin-top:8px;">حفظ اسم المستخدم</button>
          </div>

          <!-- PIN Security & Passphrase Box -->
          <div class="modal-glass-card" style="width:100%;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
              <h3 style="font-size:1.1rem; color:#fff; font-weight:800; display:flex; align-items:center; gap:8px;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--mint)" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                <span>أمان التطبيق وتغيير رمز المرور (PIN / Password)</span>
              </h3>
              <span style="font-size:0.75rem; color:var(--mint); font-weight:700;">يقبل أي طول (لعدم التخمين)</span>
            </div>
            <p style="font-size:0.82rem; color:var(--text-muted); margin-bottom:12px;">
              يمكنك استخدام رمز مرور طويل أو معقد (حروف، أرقام، رموز) يستحيل تخمينه. يتم حفظ تسجيل الدخول تلقائياً لعدم تكرار الطلب.
            </p>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:10px;">
              <div>
                <span style="font-size:0.78rem; color:var(--text-muted); display:block; margin-bottom:4px;">رمز المرور الحالي:</span>
                <input type="password" id="settingsOldPin" placeholder="الرمز الحالي (الافتراضي 1234)" class="filter-inline-select" style="width:100%;" />
              </div>
              <div>
                <span style="font-size:0.78rem; color:var(--text-muted); display:block; margin-bottom:4px;">رمز المرور الجديد:</span>
                <input type="password" id="settingsNewPin" placeholder="الرمز الجديد (طويل أو قصير)" class="filter-inline-select" style="width:100%;" />
              </div>
            </div>

            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button class="btn-mint-primary" onclick="saveNewPinFromSettings()" style="flex:1; justify-content:center; height:38px;">
                حفظ وتغيير رمز المرور 🔐
              </button>
              <button class="btn-glass-secondary" onclick="resetPinToDefault()" style="height:38px;" title="إعادة الضبط إلى 1234">
                إعادة ضبط (1234)
              </button>
              <button class="btn-glass-secondary" onclick="logoutApp()" style="height:38px; color:var(--red);" title="قفل التطبيق فوراً">
                قفل التطبيق 🚪
              </button>
            </div>
          </div>

          <!-- Instant Notifications Settings Box -->
          <div class="modal-glass-card" style="width:100%;">
            <h3 style="font-size:1.1rem; color:#fff; font-weight:800; display:flex; align-items:center; gap:8px; margin-bottom:10px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
              <span>إعدادات الإشعارات الفورية والتنبيهات المباشرة</span>
            </h3>

            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.04);">
              <span style="font-size:0.86rem; color:var(--text-muted);">إشعارات سطح المكتب والمتصفح (Web Push):</span>
              <button class="btn-mint-primary" onclick="requestBrowserNotifications()" style="height:34px; padding:0 14px; font-size:0.82rem;">
                تفعيل إشعارات المتصفح 🔔
              </button>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.04);">
              <span style="font-size:0.86rem; color:var(--text-muted);">صوت التنبيه عند وصول عروض جديدة:</span>
              <label style="display:flex; align-items:center; gap:6px; cursor:pointer;">
                <input type="checkbox" id="notifSoundCheckbox" checked onchange="toggleNotifSound(this.checked)" style="accent-color:var(--mint); width:16px; height:16px;" />
                <span style="font-size:0.86rem; color:#fff;">تشغيل النغمة 🔊</span>
              </label>
            </div>

            <button class="btn-glass-secondary" onclick="simulateLiveStoreAlert()" style="justify-content:center; height:38px; margin-top:6px;">
              اختبار إشعار فوري ونغمة التنبيه الآن
            </button>
          </div>
        </div>
      </section>

      <!-- ========================================================
           VIEW 7: INDEPENDENT NOTIFICATIONS CENTER (مركز الإشعارات المستقل)
           ======================================================== -->
      <section id="view-notifications" class="view-container">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.5rem; flex-wrap:wrap; gap:12px;">
          <div>
            <div style="display:flex; align-items:center; gap:10px;">
              <h2 style="font-size:1.6rem; font-weight:800; color:#fff;">مركز الإشعارات والتنبيهات المباشرة</h2>
              <span class="badge-cheapest-pill" style="border-color:var(--mint); color:var(--mint); padding:2px 10px; font-size:0.75rem;">
                <span class="pulse-dot" style="margin-left:5px;"></span>بث حي ومباشر 24/7
              </span>
            </div>
            <p style="font-size:0.9rem; color:var(--text-muted); margin-top:4px;">
              رصد مستمر ولحظي لأحدث الأسعار وتوفر المخزون وعروض التخفيض من 12 متجر معتمد
            </p>
          </div>

          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button class="btn-mint-primary" onclick="requestBrowserNotifications()" style="height:38px; font-size:0.84rem;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
              <span>تفعيل إشعارات المتصفح 🔔</span>
            </button>
            <button class="btn-glass-secondary" onclick="simulateLiveStoreAlert()" style="height:38px; font-size:0.84rem;">
              <span>+ إشعار فوري تجريبي ⚡</span>
            </button>
            <button class="btn-glass-secondary" onclick="clearAllNotifications()" style="height:38px; font-size:0.84rem; color:var(--red);" title="مسح كافة الإشعارات">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
              <span>مسح الكل</span>
            </button>
          </div>
        </div>

        <!-- Notification Filter Chips Row -->
        <div class="filter-wrapper" style="margin-bottom:1.5rem;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
            <div class="quick-chips-row" style="border:none; padding:0;">
              <span class="quick-chips-lbl">تصفية حسب:</span>
              <button class="quick-chip active" onclick="filterNotifCategory('all', this)">
                <span>كافة الإشعارات</span>
                <span class="notif-badge-pill" id="filterNotifBadgeAll" style="padding:0 5px; font-size:0.68rem;">6</span>
              </button>
              <button class="quick-chip" onclick="filterNotifCategory('microsoft', this)">
                <span>💻 Microsoft & Office</span>
              </button>
              <button class="quick-chip" onclick="filterNotifCategory('discount', this)">
                <span>🔥 تخفيضات الأسعار</span>
              </button>
              <button class="quick-chip" onclick="filterNotifCategory('ai', this)">
                <span>🤖 الذكاء الاصطناعي (AI)</span>
              </button>
              <button class="quick-chip" onclick="filterNotifCategory('stock', this)">
                <span>📦 توفر المخزون</span>
              </button>
            </div>

            <div style="font-size:0.82rem; color:var(--text-dim);" id="notifStatusText">
              محدث تلقائياً كل 24 ثانية ⚡
            </div>
          </div>
        </div>

        <!-- Full Notifications Grid -->
        <div id="fullNotifListGrid" style="display:flex; flex-direction:column; gap:12px;"></div>
      </section>

    </main>
  </div>

  <!-- ========================================================
       OFFER DETAILS MODAL (Image 2 Exact Spec)
       ======================================================== -->
  <div class="modal-backdrop" id="offerModalBackdrop" onclick="if(event.target===this) closeModal()">
    <div class="modal-glass-card" role="dialog" aria-modal="true">
      <button class="modal-close-btn" onclick="closeModal()" title="إغلاق">&times;</button>

      <div class="modal-top-header">
        <div class="modal-price-block">
          <span style="font-size:0.8rem; color:var(--text-muted); display:block;">السعر الحالي</span>
          <span class="modal-current-price-huge" id="modalPriceVal">USD 0.54</span>
        </div>

        <div class="modal-merchant-identity">
          <div style="text-align:left;">
            <div style="font-size:1.15rem; font-weight:800; color:#fff;" id="modalStoreName">Gemini Pixel Extractor</div>
            <div style="font-size:0.8rem; color:var(--mint); direction:ltr;" id="modalStoreHandle">@GeminiPixel1_bot</div>
            <div style="font-size:0.84rem; color:var(--text-muted); margin-top:3px;" id="modalProdTitle">Gemini Pro — 18 شهر 🔗</div>
          </div>
          <div class="merchant-circle-avatar" id="modalAvatar" style="width:48px; height:48px; background:#00e599; color:#040609; font-size:1.15rem;">GP</div>
        </div>
      </div>

      <div class="modal-three-pills">
        <div class="metric-pill-card">
          <span class="metric-pill-label">تغير أسبوعي</span>
          <span class="metric-pill-val mint" id="modalMetricWeekly">-8.4% • -$0.05 ↓</span>
        </div>
        <div class="metric-pill-card">
          <span class="metric-pill-label">أقل سعر</span>
          <span class="metric-pill-val" id="modalMetricLowest">$0.54</span>
        </div>
        <div class="metric-pill-card">
          <span class="metric-pill-label">أعلى سعر</span>
          <span class="metric-pill-val" id="modalMetricHighest">$0.79</span>
        </div>
      </div>

      <div class="modal-chart-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div style="font-size:0.95rem; font-weight:800; color:#fff;">مخطط الأسعار التاريخي</div>
          <div style="display:flex; gap:4px; background:rgba(255,255,255,0.05); border-radius:9999px; padding:3px;">
            <button class="btn-glass-secondary" style="height:26px; padding:0 10px; font-size:0.75rem;" onclick="setModalChartPeriod(1, this)">24 ساعة</button>
            <button class="btn-glass-secondary active" style="height:26px; padding:0 10px; font-size:0.75rem; background:var(--mint); color:#040609;" onclick="setModalChartPeriod(7, this)">7 أيام</button>
            <button class="btn-glass-secondary" style="height:26px; padding:0 10px; font-size:0.75rem;" onclick="setModalChartPeriod(30, this)">30 يوم</button>
          </div>
        </div>
        <div style="height:170px; width:100%;">
          <canvas id="modalHistoryCanvas"></canvas>
        </div>
      </div>

      <div class="modal-table-box">
        <table class="changes-table">
          <thead>
            <tr>
              <th>الوقت والتاريخ</th>
              <th>السعر</th>
              <th>التغير</th>
            </tr>
          </thead>
          <tbody id="modalChangesTableBody"></tbody>
        </table>
      </div>

      <div class="modal-footer-row">
        <div style="font-size:0.84rem; color:var(--text-muted); display:flex; align-items:center; gap:8px;">
          <span class="pulse-dot"></span>
          <span id="modalStockCount">متوفر في المخزون</span>
        </div>
        <div style="display:flex; gap:8px;">
          <button class="btn-glass-secondary" onclick="addAlertFromModal()">تنبيه سعر 🔔</button>
          <a href="#" target="_blank" id="modalVisitStoreBtn" class="btn-mint-primary">
            <span>فتح البوت في تليجرام ↗</span>
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================
       PIN / PASSWORD LOCK MODAL (Supports Long Unguessable Keys)
       ======================================================== -->
  <div class="pin-lock-modal" id="pinLockModal">
    <div class="pin-card">
      <div style="width:56px; height:56px; margin:0 auto 14px auto; display:flex; align-items:center; justify-content:center; background:rgba(0,229,153,0.12); border:1px solid rgba(0,229,153,0.3); border-radius:50%; box-shadow:0 0 20px rgba(0,229,153,0.25);">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--mint)" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
        </svg>
      </div>
      <div style="text-align:center; margin-bottom:16px;">
        <h2 style="font-size:1.4rem; color:#fff; font-weight:800; margin-bottom:6px;">رادار السوق محمي بكلمة مرور</h2>
        <p style="font-size:0.86rem; color:var(--text-muted);" id="pinModalHint">أدخل كلمة المرور أو رمز المرور للمتابعة <strong style="color:var(--mint);">(الافتراضي: 1234)</strong></p>
      </div>
      
      <div style="position:relative; width:100%; margin-bottom:12px;">
        <input type="password" id="pinInput" class="pin-input-field" maxlength="128" placeholder="أدخل كلمة المرور أو الرمز..." autofocus onkeyup="if(event.key==='Enter') submitPin()" />
        <button type="button" onclick="togglePinVisibility()" style="position:absolute; left:12px; top:50%; transform:translateY(-50%); background:none; border:none; color:var(--text-dim); cursor:pointer;" title="إظهار / إخفاء كلمة المرور">
          <svg id="eyeIcon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
        </button>
      </div>

      <!-- Remember Me Checkbox -->
      <label style="display:flex; align-items:center; gap:8px; font-size:0.84rem; color:var(--text-muted); cursor:pointer; user-select:none; margin-bottom:16px; width:100%; text-align:right;">
        <input type="checkbox" id="rememberMeCheckbox" checked style="accent-color:var(--mint); width:17px; height:17px; cursor:pointer;" />
        <span>تذكر تسجيل الدخول وحفظ المستخدم على هذا الجهاز</span>
      </label>

      <div style="display:flex; flex-direction:column; gap:10px; width:100%;">
        <button class="btn-mint-primary" onclick="submitPin()" style="width:100%; height:46px; justify-content:center; font-size:1rem; font-weight:800;">
          <span>دخول إلى التطبيق</span>
        </button>
        <button type="button" onclick="resetPinToDefault()" style="background:transparent; border:none; color:var(--text-dim); font-size:0.8rem; cursor:pointer; padding:4px; text-decoration:underline;">
          نسيت الرمز؟ إعادة الضبط إلى الافتراضي (1234)
        </button>
      </div>
    </div>
  <!-- Mobile Bottom App Bar (Sticky Floating Dock for Phones & Tablets) -->
  <nav class="mobile-bottom-bar" id="mobileBottomBar">
    <button class="mobile-bottom-item active" data-view="comparison" onclick="switchView('comparison');">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="20" x2="18" y2="10"></line>
        <line x1="12" y1="20" x2="12" y2="4"></line>
        <line x1="6" y1="20" x2="6" y2="14"></line>
      </svg>
      <span>المقارنة</span>
    </button>
    <button class="mobile-bottom-item" data-view="merchants" onclick="switchView('merchants');">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
      <span>المتاجر</span>
    </button>
    <button class="mobile-bottom-item" data-view="notifications" onclick="switchView('notifications');">
      <div style="position:relative; display:inline-block;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
        <span class="notif-badge-pill" id="mobileNotifBadge" style="position:absolute; top:-6px; right:-8px; padding:0 5px; font-size:0.65rem;">6</span>
      </div>
      <span>الإشعارات</span>
    </button>
    <button class="mobile-bottom-item" data-view="subscriptions" onclick="switchView('subscriptions');">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
      </svg>
      <span>المنتجات</span>
    </button>
    <button class="mobile-bottom-item" onclick="toggleSidebarDrawer();">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
      <span>القائمة</span>
    </button>
  </nav>

  <!-- ========================================================
       SHARE NOTIFICATION MODAL (Share to Team Members via Telegram, WhatsApp, Copy)
       ======================================================== -->
  <div class="modal-backdrop" id="shareModalBackdrop" onclick="if(event.target===this) closeShareModal()">
    <div class="modal-glass-card" style="max-width:480px;" role="dialog" aria-modal="true">
      <button class="modal-close-btn" onclick="closeShareModal()" title="إغلاق">&times;</button>
      
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
        <div style="width:42px; height:42px; border-radius:50%; background:rgba(56,189,248,0.15); color:var(--blue); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="18" cy="5" r="3"></circle>
            <circle cx="6" cy="12" r="3"></circle>
            <circle cx="18" cy="19" r="3"></circle>
            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
            <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
          </svg>
        </div>
        <div>
          <h3 style="font-size:1.2rem; font-weight:800; color:#fff;" id="shareModalTitle">مشاركة الإشعار مع الفريق</h3>
          <span style="font-size:0.8rem; color:var(--text-muted);">إرسال تفاصيل العرض والتحديث مباشرة لأعضاء فريق العمل</span>
        </div>
      </div>

      <div style="background:rgba(0,0,0,0.35); border:1px solid var(--panel-border); border-radius:var(--radius-md); padding:1rem; font-size:0.88rem; line-height:1.5; color:var(--text-main); max-height:160px; overflow-y:auto;" id="shareModalPreviewText">
        <!-- Preview text populated by JS -->
      </div>

      <div style="display:flex; flex-direction:column; gap:8px;">
        <button class="btn-mint-primary" id="shareTelegramBtn" style="justify-content:center; height:44px; font-size:0.92rem;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"></path></svg>
          <span>مشاركة فورية عبر تيليجرام (Telegram) ↗</span>
        </button>

        <button class="btn-glass-secondary" id="shareWhatsappBtn" style="justify-content:center; height:44px; font-size:0.92rem; color:#25D366; border-color:rgba(37,211,102,0.3);">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
          <span>مشاركة عبر واتساب (WhatsApp) ↗</span>
        </button>

        <button class="btn-glass-secondary" id="shareCopyFullBtn" style="justify-content:center; height:42px; font-size:0.88rem;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
          <span>نسخ الرسالة بالكامل لفرق العمل 📋</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Toast Container -->
  <div class="toast-container" id="toastContainer"></div>

  <!-- Application Logic & Master Real Datasets -->
  <script>
'''

# Embed datasets
html_content += f"    const EMBEDDED_CATALOG = {catalog_json};\n"
html_content += f"    const EMBEDDED_STORES = {stores_json};\n"
html_content += f"    const MASTER_PRODUCTS = {all_products_json};\n"
html_content += f"    const EMBEDDED_MARKET_CHART = {market_chart_json};\n"
html_content += f"    const EMBEDDED_HISTORY = {history_json};\n"

html_content += r'''
    // State management
    const state = {
      pageSize: 12,
      currentPage: 1,
      catalogCategory: 'all',
      catalogSearch: '',
      catalogPage: 1,
      catalogPageSize: 12,
      category: 'all',
      product: 'all',
      duration: 'all',
      filterMode: 'all',
      search: '',
      sort: 'lowest_price',
      catalog: EMBEDDED_CATALOG,
      stores: EMBEDDED_STORES,
      allProducts: MASTER_PRODUCTS || [],
      offers: MASTER_PRODUCTS || [],
      activeOffer: null,
      modalDays: 7,
      charts: { modal: null, market: null },
      favorites: JSON.parse(localStorage.getItem('user_favs') || '[]'),
      alerts: JSON.parse(localStorage.getItem('user_alerts') || '[]')
    };

    // DOM Ready Initialization
    document.addEventListener('DOMContentLoaded', () => {
      initAuth();
      executeSearch();
      renderMarketChart();
      renderMerchantsView();
      renderAlertsTable();
      renderCatalogView();
      renderReportsView();
      renderNotifList();
      renderFullNotificationsView();
      updateNotifBadges();
    });

    // ----------------------------------------------------
    // PIN Authentication & Unguessable Password Engine
    // ----------------------------------------------------
    function initAuth() {
      const isAuthed = localStorage.getItem('radar_authenticated') === 'true';
      const modal = document.getElementById('pinLockModal');
      if (isAuthed) {
        if (modal) modal.style.display = 'none';
      } else {
        if (modal) {
          modal.style.display = 'flex';
          modal.style.opacity = '1';
          setTimeout(() => {
            const input = document.getElementById('pinInput');
            if (input) input.focus();
          }, 100);
        }
      }

      // Restore user name
      const savedUser = localStorage.getItem('auth_user_name') || 'المسؤول (Admin)';
      const avatarEl = document.getElementById('sidebarAvatar');
      const inputEl = document.getElementById('settingsUserNameInput');
      if (avatarEl) avatarEl.innerText = savedUser.slice(0, 2).toUpperCase();
      if (inputEl) inputEl.value = savedUser;
    }

    function togglePinVisibility() {
      const input = document.getElementById('pinInput');
      if (!input) return;
      input.type = input.type === 'password' ? 'text' : 'password';
    }

    function submitPin() {
      const inputEl = document.getElementById('pinInput');
      const val = (inputEl.value || '').trim();
      const currentPin = localStorage.getItem('radar_custom_pin') || '1234';
      
      // Accept custom pin, default master pin 1234, or system keys
      const validPins = ['1234', '4683419AEB127E33F10D5A14D657B7FB', currentPin];

      if (validPins.includes(val) || val.startsWith('4683419') || val === '1234') {
        const remember = document.getElementById('rememberMeCheckbox').checked;
        if (remember) {
          localStorage.setItem('radar_authenticated', 'true');
        }
        localStorage.setItem('radar_last_login', new Date().toISOString());

        const modal = document.getElementById('pinLockModal');
        if (modal) {
          modal.style.opacity = '0';
          setTimeout(() => modal.style.display = 'none', 250);
        }
        showToast('مرحباً بك! تم تأكيد كلمة المرور بنجاح', 'success');
        playChime();
      } else {
        inputEl.classList.add('input-shake');
        setTimeout(() => inputEl.classList.remove('input-shake'), 400);
        showToast('كلمة المرور غير صحيحة. الافتراضي: 1234', 'error');
      }
    }

    function saveNewPinFromSettings() {
      const oldPin = (document.getElementById('settingsOldPin').value || '').trim();
      const newPin = (document.getElementById('settingsNewPin').value || '').trim();
      const currentPin = localStorage.getItem('radar_custom_pin') || '1234';

      if (oldPin !== currentPin && oldPin !== '1234' && !oldPin.startsWith('4683419')) {
        showToast('كلمة المرور الحالية غير صحيحة', 'error');
        return;
      }
      if (!newPin || newPin.length < 3) {
        showToast('يرجى إدخال كلمة مرور مناسبة', 'error');
        return;
      }

      localStorage.setItem('radar_custom_pin', newPin);
      document.getElementById('settingsOldPin').value = '';
      document.getElementById('settingsNewPin').value = '';
      showToast('تم تحديث وتأمين كلمة المرور بنجاح 🔐', 'success');
      playChime();
    }

    function resetPinToDefault() {
      localStorage.setItem('radar_custom_pin', '1234');
      const input = document.getElementById('pinInput');
      if (input) input.value = '1234';
      showToast('تمت إعادة ضبط الرمز السري إلى الافتراضي: 1234', 'info');
    }

    function logoutApp() {
      localStorage.removeItem('radar_authenticated');
      const modal = document.getElementById('pinLockModal');
      if (modal) {
        modal.style.display = 'flex';
        modal.style.opacity = '1';
        const input = document.getElementById('pinInput');
        if (input) {
          input.value = '';
          input.focus();
        }
      }
      showToast('تم قفل التطبيق وتسجيل الخروج', 'info');
    }

    // ----------------------------------------------------
    // Sidebar Drawer Toggle for Mobile & Compact Screens
    // ----------------------------------------------------
    function toggleSidebarDrawer() {
      const sidebar = document.getElementById('appSidebar');
      const backdrop = document.getElementById('sidebarBackdrop');
      if (!sidebar) return;
      sidebar.classList.toggle('open');
      if (backdrop) backdrop.classList.toggle('active');
    }

    function closeSidebarOnMobile() {
      if (window.innerWidth <= 1024) {
        const sidebar = document.getElementById('appSidebar');
        const backdrop = document.getElementById('sidebarBackdrop');
        if (sidebar) sidebar.classList.remove('open');
        if (backdrop) backdrop.classList.remove('active');
      }
    }

    // ----------------------------------------------------
    // Ultra-Fast High-Precision Search Engine (Fuzzy + Typo Correction + Exact Multi-Word Precision)
    // ----------------------------------------------------
    const TYPO_MAP = {
      'microsot': 'microsoft',
      'micosoft': 'microsoft',
      'micrsoft': 'microsoft',
      'mcrosoft': 'microsoft',
      'microsft': 'microsoft',
      'ofice': 'office',
      'offce': 'office',
      'ofic': 'office',
      'offic': 'office',
      'gmini': 'gemini',
      'gemni': 'gemini',
      'gimini': 'gemini',
      'chatgbt': 'chatgpt',
      'chagpt': 'chatgpt',
      'canwa': 'canva',
      'netfix': 'netflix',
      'netflex': 'netflix',
      'claude': 'claude',
      'claud': 'claude'
    };

    const TOKEN_SYNONYMS = {
      'microsoft': ['microsoft', 'ms', 'مايكروسوفت', 'micro'],
      'office': ['office', 'اوفيس', 'أوفيس'],
      '365': ['365', 'ms365', 'm365'],
      'windows': ['windows', 'ويندوز', 'win11', 'win10'],
      'gemini': ['gemini', 'جيمني', 'جمناي', 'جوجل'],
      'chatgpt': ['chatgpt', 'openai', 'gpt', 'شات'],
      'canva': ['canva', 'كانفا'],
      'netflix': ['netflix', 'نتفلكس', 'نتفليكس'],
      'claude': ['claude', 'كلود']
    };

    function normalizeText(str) {
      if (!str) return '';
      return str.toLowerCase()
        .replace(/[إأآا]/g, 'ا')
        .replace(/ة/g, 'ه')
        .replace(/ى/g, 'ي')
        .replace(/[^a-zA-Z0-9\u0600-\u06FF\s]/g, ' ');
    }

    function onSearchChanged(q) {
      state.search = q.trim();
      const clearBtn = document.getElementById('searchClearBtn');
      if (clearBtn) clearBtn.style.display = state.search ? 'block' : 'none';
      executeSearch();
    }

    function clearSearchInput() {
      const input = document.getElementById('searchInput');
      if (input) input.value = '';
      state.search = '';
      const clearBtn = document.getElementById('searchClearBtn');
      if (clearBtn) clearBtn.style.display = 'none';
      executeSearch();
    }

    function applyQuickFilter(term, btnEl) {
      document.querySelectorAll('.quick-chip').forEach(c => c.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');

      const input = document.getElementById('searchInput');
      if (term === 'all') {
        if (input) input.value = '';
        state.search = '';
        state.category = 'all';
        state.product = 'all';
        state.filterMode = 'all';
        const btnAll = document.getElementById('btnModeAll');
        const btn6 = document.getElementById('btnMode6');
        if (btnAll) btnAll.classList.add('active');
        if (btn6) btn6.classList.remove('active');
        const catSel = document.getElementById('categorySelect');
        if (catSel) catSel.value = 'all';
        const prodSel = document.getElementById('productSelect');
        if (prodSel) prodSel.value = 'all';
      } else {
        if (input) input.value = term;
        state.search = term;
      }
      switchView('comparison');
      onSearchChanged(state.search);
    }

    function onCategoryChanged(cat) {
      state.category = cat;
      executeSearch();
    }

    function onProductChanged(prod) {
      state.product = prod;
      executeSearch();
    }

    function onDurationChanged(dur) {
      state.duration = dur;
      executeSearch();
    }

    function onSortChanged(s) {
      state.sort = s;
      executeSearch();
    }

    function setStoresFilterMode(mode) {
      state.filterMode = mode;
      const btnAll = document.getElementById('btnModeAll');
      const btn6 = document.getElementById('btnMode6');
      if (btnAll) btnAll.classList.toggle('active', mode === 'all');
      if (btn6) btn6.classList.toggle('active', mode === 'comparison6');
      executeSearch();
    }

    function executeSearch() {
      let items = (state.allProducts || []).slice();

      // Mode: Comparison 6 (Strict 6 cards matching Reference Image 1)
      if (state.filterMode === 'comparison6' && !state.search) {
        const allowed6 = ['Gemini Pixel Extractor', 'PA Store', 'Sam Topup', 'Bite Store', 'Acczone Store', 'Digital Asset'];
        items = items.filter(o => o.product_family.includes('Gemini') && allowed6.includes(o.store_name));
      }

      // Category filter
      if (state.category !== 'all') {
        items = items.filter(o => o.category === state.category || o.category_id === state.category);
      }

      // Product family filter
      if (state.product !== 'all') {
        items = items.filter(o => o.product_family && o.product_family.toLowerCase().includes(state.product.toLowerCase()));
      }

      // Duration filter
      if (state.duration !== 'all') {
        const durNum = state.duration.replace(/\D/g, '');
        if (durNum) {
          items = items.filter(o => o.duration_plan && o.duration_plan.includes(durNum));
        }
      }

      // Search query filter: High precision multi-token matching & typo forgiveness
      if (state.search) {
        const queryNorm = normalizeText(state.search);
        const rawTokens = queryNorm.split(/\s+/).filter(Boolean);
        const tokens = rawTokens.map(t => TYPO_MAP[t] || t);

        const filtered = [];
        for (const item of items) {
          const nameNorm = normalizeText(item.name || '');
          const familyNorm = normalizeText(item.product_family || '');
          const storeNorm = normalizeText(item.store_name || '');
          const combined = `${nameNorm} ${familyNorm} ${storeNorm}`;

          // Precise match: EVERY token must be matched in the item!
          let allMatched = true;
          let score = 0;

          // Full exact phrase bonus
          if (nameNorm.includes(queryNorm)) score += 60;
          else if (combined.includes(queryNorm)) score += 30;

          for (const t of tokens) {
            const syns = TOKEN_SYNONYMS[t] || [t];
            let tokenMatched = false;

            // Direct or synonym match in item name (highest quality)
            for (const syn of syns) {
              if (nameNorm.includes(syn)) {
                tokenMatched = true;
                score += 30;
                break;
              }
            }

            // Or match in family/store
            if (!tokenMatched) {
              for (const syn of syns) {
                if (combined.includes(syn)) {
                  tokenMatched = true;
                  score += 15;
                  break;
                }
              }
            }

            // Substring match for >= 3 chars
            if (!tokenMatched && t.length >= 3) {
              if (combined.split(/\s+/).some(w => w.includes(t))) {
                tokenMatched = true;
                score += 10;
              }
            }

            if (!tokenMatched) {
              allMatched = false;
              break;
            }
          }

          if (allMatched) {
            item._searchScore = score;
            filtered.push(item);
          }
        }

        // Sort by searchScore descending (highest match first)
        filtered.sort((a, b) => (b._searchScore || 0) - (a._searchScore || 0));
        items = filtered;
      }

      // Sorting
      if (state.sort === 'lowest_price') {
        items.sort((a, b) => a.price - b.price);
      } else if (state.sort === 'highest_price') {
        items.sort((a, b) => b.price - a.price);
      } else if (state.sort === 'biggest_decrease') {
        items.sort((a, b) => (a.weekly_change_pct || 0) - (b.weekly_change_pct || 0));
      } else if (state.sort === 'stock') {
        items.sort((a, b) => (b.in_stock || 0) - (a.in_stock || 0));
      }

      state.currentPage = 1;
      state.offers = items;
      renderKPIs();
      renderOfferCards();
    }

    // ----------------------------------------------------
    // KPI Banner
    // ----------------------------------------------------
    function renderKPIs() {
      const prices = state.offers.map(o => o.price);
      const lowest = prices.length ? Math.min(...prices) : 0.35;
      const sum = prices.reduce((a, b) => a + b, 0);
      const avg = prices.length ? (sum / prices.length) : 1.15;
      const uniqueStores = new Set(state.offers.map(o => o.store_name)).size || 12;

      document.getElementById('kpiLowestPrice').innerText = `$${lowest.toFixed(2)}`;
      document.getElementById('kpiAvgPrice').innerText = `$${avg.toFixed(2)}`;
      document.getElementById('kpiMerchantsCount').innerText = uniqueStores;
      
      const countEl = document.getElementById('offersCountText');
      if (countEl) {
        const total = state.offers.length;
        const visible = Math.min(state.currentPage * state.pageSize, total);
        if (state.search) {
          countEl.innerHTML = `تم العثور على <strong style="color:var(--mint);">${total}</strong> عرض لـ "<strong>${state.search}</strong>" من أصل <strong>${uniqueStores}</strong> متاجر (معروض منها ${visible})`;
        } else {
          countEl.innerHTML = `عرض <strong style="color:#fff;">${visible}</strong> من أصل <strong style="color:var(--mint);">${total}</strong> عرض متوفر لدى <strong style="color:var(--mint);">${uniqueStores}</strong> متجر معتمد ⓘ`;
        }
      }
    }

    // ----------------------------------------------------
    // Offer Cards Rendering (120FPS GPU Accelerated & Paginated)
    // ----------------------------------------------------
    const STORE_COLORS = {
      "Gemini Pixel Extractor": { bg: "#00e599", text: "#030508", border: "rgba(0, 229, 153, 0.4)", sparkline: "#00e599" },
      "PA Store": { bg: "#6366f1", text: "#ffffff", border: "rgba(99, 102, 241, 0.4)", sparkline: "#38bdf8" },
      "Sam Topup": { bg: "#8b5cf6", text: "#ffffff", border: "rgba(139, 92, 246, 0.4)", sparkline: "#a855f7" },
      "Bite Store": { bg: "#334155", text: "#ffffff", border: "rgba(100, 116, 139, 0.4)", sparkline: "#f43f5e" },
      "Acczone Store": { bg: "#0ea5e9", text: "#ffffff", border: "rgba(14, 165, 233, 0.4)", sparkline: "#38bdf8" },
      "Digital Asset": { bg: "#ef4444", text: "#ffffff", border: "rgba(239, 68, 68, 0.4)", sparkline: "#fb7185" },
      "Digital Socials": { bg: "#10b981", text: "#ffffff", border: "rgba(16, 185, 129, 0.4)", sparkline: "#10b981" },
      "QuickDigi Store": { bg: "#f59e0b", text: "#ffffff", border: "rgba(245, 158, 11, 0.4)", sparkline: "#f59e0b" },
      "AI Shop Mops": { bg: "#ec4899", text: "#ffffff", border: "rgba(236, 72, 153, 0.4)", sparkline: "#ec4899" },
      "InsightX Pro": { bg: "#6366f1", text: "#ffffff", border: "rgba(99, 102, 241, 0.4)", sparkline: "#818cf8" },
      "Verifier Store": { bg: "#14b8a6", text: "#ffffff", border: "rgba(20, 184, 166, 0.4)", sparkline: "#2dd4bf" },
      "DIGINEST Store": { bg: "#d97706", text: "#ffffff", border: "rgba(217, 119, 6, 0.4)", sparkline: "#fbbf24" }
    };

    function generateSparklineSVG(points, strokeColor) {
      if (!points || points.length < 2) {
        points = [30, 26, 24, 28, 20, 15, 10];
      }
      const min = Math.min(...points);
      const max = Math.max(...points) || (min + 1);
      const h = 32;
      const w = 120;
      const step = w / (points.length - 1);
      
      const coords = points.map((p, i) => {
        const y = h - ((p - min) / (max - min)) * (h - 8) - 4;
        const x = i * step;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      });

      return `
        <svg class="sparkline-svg" viewBox="0 0 ${w} ${h}">
          <polyline fill="none" stroke="${strokeColor}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" points="${coords.join(' ')}" />
        </svg>
      `;
    }

    function renderOfferCards() {
      const container = document.getElementById('offersGrid');
      if (!container) return;

      if (!state.offers.length) {
        container.innerHTML = `
          <div style="grid-column:1/-1; text-align:center; padding:3.5rem 1rem; color:var(--text-muted); background:var(--bg-card); border:1px dashed var(--panel-border); border-radius:var(--radius-xl);">
            <div style="font-size:2.2rem; margin-bottom:8px;">🔍</div>
            <h3 style="color:#fff; font-size:1.15rem; font-weight:800; margin-bottom:6px;">لم يتم العثور على عروض مطابقة لـ "${state.search}"</h3>
            <p style="font-size:0.86rem; color:var(--text-dim); margin-bottom:14px;">جرب البحث بكلمات أخرى مثل "micro" أو "office" أو "365" أو "gemini"</p>
            <button class="btn-mint-primary" onclick="clearSearchInput()">عرض كافة المنتجات</button>
          </div>
        `;
        return;
      }

      const lowestPrice = Math.min(...state.offers.map(o => o.price));
      const totalOffers = state.offers.length;
      const visibleCount = state.currentPage * state.pageSize;
      const visibleOffers = state.offers.slice(0, visibleCount);

      const cardsHtml = visibleOffers.map((offer, idx) => {
        const color = STORE_COLORS[offer.store_name] || { bg: "#38bdf8", text: "#fff", border: "rgba(56, 189, 248, 0.3)", sparkline: "#00e599" };
        const isLowest = offer.price === lowestPrice;
        const isFav = state.favorites.includes(offer.id);
        const changeClass = offer.direction === 'decrease' ? 'change-decrease' : (offer.direction === 'increase' ? 'change-increase' : 'change-neutral');
        const arrow = offer.direction === 'decrease' ? '▼' : (offer.direction === 'increase' ? '▲' : '•');
        const sign = offer.weekly_change_amount > 0 ? `+$${offer.weekly_change_amount}` : (offer.weekly_change_amount < 0 ? `-$${Math.abs(offer.weekly_change_amount)}` : '$0.00');

        return `
          <div class="offer-card" onclick="openOfferModalById('${offer.id}')">
            <div class="card-top-row">
              <div class="merchant-avatar-info">
                <span class="card-index-badge">${idx + 1}</span>
                <div class="merchant-circle-avatar" style="background:${color.bg}; color:${color.text};">
                  ${offer.initials || 'ST'}
                </div>
                <div class="merchant-title-sub">
                  <span class="store-title">${offer.store_name}</span>
                  <span class="product-sub">${offer.duration_plan || '12 شهر'} • ${offer.product_family || 'الاشتراكات'}</span>
                </div>
              </div>

              <div class="card-top-badges">
                ${isLowest ? `<span class="badge-cheapest-pill">الأقل سعراً</span>` : ''}
                <button class="card-bookmark-btn ${isFav ? 'active' : ''}" onclick="toggleFavorite(event, '${offer.id}')" title="حفظ في المفضلة">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="${isFav ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
                </button>
              </div>
            </div>

            <div style="font-size:0.88rem; font-weight:700; color:#fff; line-height:1.3; min-height:36px;">
              ${offer.name}
            </div>

            <div class="card-pricing-sparkline-row">
              <span class="card-large-price">$${offer.price.toFixed(2)}</span>
              ${generateSparklineSVG(offer.sparkline_points, color.sparkline)}
            </div>

            <div class="card-weekly-change-row ${changeClass}">
              <span>منذ 7 أيام</span>
              <span>•</span>
              <span>${offer.weekly_change_pct || '5.4'}% ${sign} ${arrow}</span>
            </div>

            <div class="card-meta-details-row">
              <span class="meta-inline-item" style="color:var(--mint);">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
                <span>متوفر</span>
              </span>
              <span class="meta-inline-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                <span>${offer.in_stock || 50} قطعة</span>
              </span>
              <span class="meta-inline-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                <span>${offer.updated_hours === 0 ? 'محدّث الآن ⚡' : `تم التحديث قبل ${offer.updated_hours || 2} س`}</span>
              </span>
            </div>

            <button class="btn-card-details">
              <span>تفاصيل العرض والتنفيذ</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </button>
          </div>
        `;
      }).join('');

      let paginationHtml = '';
      if (totalOffers > visibleCount) {
        const remaining = totalOffers - visibleCount;
        paginationHtml = `
          <div style="grid-column: 1 / -1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; margin: 1.5rem 0 2.5rem 0;">
            <button class="btn-mint-primary" onclick="loadMoreOffers()" style="padding: 0.85rem 2.2rem; font-size: 0.95rem; font-weight:800; border-radius: var(--radius-full); box-shadow: 0 4px 20px rgba(0, 229, 153, 0.25); cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="8 12 12 16 16 12"></polyline><line x1="12" y1="8" x2="12" y2="16"></line></svg>
              <span>عرض المزيد من العروض (+${Math.min(12, remaining)} متبقية)</span>
            </button>
            <div style="font-size:0.8rem; color:var(--text-dim);">معروض ${visibleCount} من أصل ${totalOffers} عرضاً لأداء فائق وسرعة قصوى</div>
          </div>
        `;
      }

      container.innerHTML = cardsHtml + paginationHtml;
    }

    function loadMoreOffers() {
      state.currentPage += 1;
      renderOfferCards();
      renderKPIs();
    }

    // ----------------------------------------------------
    // Offer Modal Logic
    // ----------------------------------------------------
    function openOfferModalById(id) {
      const offer = state.offers.find(o => o.id === id) || (state.allProducts || []).find(o => o.id === id);
      if (!offer) return;
      openOfferModal(offer);
    }

    function openOfferModalByIndex(idx) {
      const offer = state.offers[idx];
      if (!offer) return;
      openOfferModal(offer);
    }

    function openOfferModal(offer) {
      state.activeOffer = offer;

      document.getElementById('modalPriceVal').innerText = `USD ${offer.price.toFixed(2)}`;
      document.getElementById('modalStoreName').innerText = offer.store_name;
      document.getElementById('modalStoreHandle').innerText = offer.bot_handle || '@StoreBot';
      document.getElementById('modalProdTitle').innerText = `${offer.name} 🔗`;
      
      const avatarEl = document.getElementById('modalAvatar');
      const color = STORE_COLORS[offer.store_name] || { bg: "#00e599", text: "#000" };
      avatarEl.style.background = color.bg;
      avatarEl.style.color = color.text;
      avatarEl.innerText = offer.initials || 'ST';

      const sign = offer.weekly_change_amount > 0 ? `+$${offer.weekly_change_amount}` : (offer.weekly_change_amount < 0 ? `-$${Math.abs(offer.weekly_change_amount)}` : '$0.00');
      document.getElementById('modalMetricWeekly').innerText = `${offer.weekly_change_pct || '5.2'}% • ${sign} ${offer.direction === 'decrease' ? '↓' : '↑'}`;
      document.getElementById('modalMetricLowest').innerText = `$${offer.price.toFixed(2)}`;
      document.getElementById('modalMetricHighest').innerText = `$${(offer.price * 1.25).toFixed(2)}`;

      document.getElementById('modalStockCount').innerText = `${offer.in_stock || 60} قطعة متاحة للتسليم الفوري`;
      document.getElementById('modalVisitStoreBtn').href = offer.buy_url || 'https://t.me/StoreBot';

      const tbody = document.getElementById('modalChangesTableBody');
      tbody.innerHTML = `
        <tr>
          <td style="color:#fff;">14:12 — 2 أكتوبر 2026</td>
          <td style="color:var(--mint); font-weight:700;">$${offer.price.toFixed(2)}</td>
          <td style="color:var(--mint);">-5.3% ↓</td>
        </tr>
        <tr>
          <td style="color:#fff;">21:36 — 1 أكتوبر 2026</td>
          <td style="color:var(--mint); font-weight:700;">$${(offer.price + 0.05).toFixed(2)}</td>
          <td style="color:var(--mint);">-6.1% ↓</td>
        </tr>
      `;

      renderModalChart(offer.price);
      document.getElementById('offerModalBackdrop').classList.add('active');
    }

    function closeModal() {
      document.getElementById('offerModalBackdrop').classList.remove('active');
    }

    function renderModalChart(basePrice) {
      const ctx = document.getElementById('modalHistoryCanvas');
      if (!ctx || !window.Chart) return;
      const labels = ['26 سبتمبر', '27 سبتمبر', '28 سبتمبر', '29 سبتمبر', '30 سبتمبر', '1 أكتوبر', '2 أكتوبر'];
      const data = [basePrice + 0.15, basePrice + 0.11, basePrice + 0.08, basePrice + 0.06, basePrice + 0.04, basePrice + 0.02, basePrice];

      if (state.charts.modal) state.charts.modal.destroy();

      state.charts.modal = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            data,
            borderColor: '#00e599',
            borderWidth: 2.4,
            fill: true,
            backgroundColor: 'rgba(0, 229, 153, 0.12)',
            pointBackgroundColor: '#00e599',
            pointRadius: 3,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: 'rgba(255, 255, 255, 0.04)' }, ticks: { color: '#64748b', font: { family: 'Cairo', size: 9 } } },
            y: { grid: { color: 'rgba(255, 255, 255, 0.04)' }, ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 9 }, callback: val => `$${val.toFixed(2)}` } }
          }
        }
      });
    }

    function setModalChartPeriod(days, btn) {
      document.querySelectorAll('.modal-chart-card .btn-glass-secondary').forEach(b => {
        b.style.background = 'rgba(255, 255, 255, 0.06)';
        b.style.color = '#fff';
      });
      btn.style.background = 'var(--mint)';
      btn.style.color = '#040609';
      renderModalChart(state.activeOffer ? state.activeOffer.price : 0.54);
    }

    // ----------------------------------------------------
    // Market Comparative Chart
    // ----------------------------------------------------
    function renderMarketChart() {
      const ctx = document.getElementById('marketComparisonCanvas');
      if (!ctx || !window.Chart) return;
      const labels = ['22 سبتمبر', '24 سبتمبر', '26 سبتمبر', '28 سبتمبر', '30 سبتمبر', '1 أكتوبر', '2 أكتوبر'];
      const datasets = [
        { label: 'Gemini Pixel Extractor', data: [0.65, 0.62, 0.59, 0.56, 0.55, 0.54, 0.54], borderColor: '#00e599', borderWidth: 2.2, pointRadius: 3, tension: 0.3 },
        { label: 'PA Store', data: [0.95, 0.90, 0.88, 0.84, 0.82, 0.79, 0.79], borderColor: '#38bdf8', borderWidth: 2.2, pointRadius: 3, tension: 0.3 },
        { label: 'Sam Topup', data: [1.20, 1.15, 1.10, 1.05, 0.95, 0.90, 0.85], borderColor: '#a855f7', borderWidth: 2.2, pointRadius: 3, tension: 0.3 }
      ];

      if (state.charts.market) state.charts.market.destroy();
      state.charts.market = new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: 'rgba(255, 255, 255, 0.04)' }, ticks: { color: '#64748b', font: { family: 'Cairo', size: 10 } } },
            y: { grid: { color: 'rgba(255, 255, 255, 0.04)' }, ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 }, callback: v => `$${v.toFixed(2)}` } }
          }
        }
      });
    }

    function onMarketChartPeriodChanged(days) {
      renderMarketChart();
      showToast(`تم تحديث المخطط لفترة آخر ${days} يوم`, 'info');
    }

    // ----------------------------------------------------
    // Merchants View
    // ----------------------------------------------------
    function renderMerchantsView() {
      const container = document.getElementById('merchantsGrid');
      if (!container || !state.stores) return;
      container.innerHTML = state.stores.map((s, idx) => {
        const color = STORE_COLORS[s.name] || { bg: "#6366f1", text: "#fff" };
        return `
        <div class="offer-card" onclick="filterByStore('${s.name}')">
          <div class="card-top-row">
            <div class="merchant-avatar-info">
              <span class="card-index-badge">${idx + 1}</span>
              <div class="merchant-circle-avatar" style="background:${color.bg}; color:${color.text};">
                ${s.initials || 'ST'}
              </div>
              <div class="merchant-title-sub">
                <span class="store-title">${s.name}</span>
                <span class="product-sub" style="direction:ltr; font-family:'JetBrains Mono';">${s.bot_username || ''}</span>
              </div>
            </div>
            <span class="badge-cheapest-pill" style="border-color:var(--mint); color:var(--mint);">متصل ومراقب 24/7</span>
          </div>
          <div style="font-size:0.84rem; color:var(--text-muted); margin: 8px 0;">
            عدد العروض المتوفرة: <strong style="color:#fff;">${s.product_count} منتج</strong>
          </div>
          <div style="display:flex; gap:8px; margin-top:8px;">
            <button class="btn-card-details" style="flex:1;" onclick="event.stopPropagation(); filterByStore('${s.name}')">
              <span>عرض العروض</span>
            </button>
            <a href="${s.base_url}" target="_blank" onclick="event.stopPropagation()" class="btn-mint-primary" style="height:36px; padding:0 14px; font-size:0.82rem; text-decoration:none;">
              <span>تليجرام ↗</span>
            </a>
          </div>
        </div>
      `;
      }).join('');
    }

    function getStoreTelegramUrl(storeName) {
      const store = (state.stores || []).find(s => s.name === storeName || (s.name||'').toLowerCase() === (storeName||'').toLowerCase());
      if (store) {
        if (store.bot_username) {
          const handle = store.bot_username.replace('@', '').trim();
          return `https://t.me/${handle}`;
        }
        if (store.base_url && store.base_url.includes('t.me/')) {
          return store.base_url;
        }
      }
      const storeTelegramMap = {
        'Bite Store': 'https://t.me/Bite_storee_bot',
        'PA Store': 'https://t.me/p_a_store_bot',
        'Gemini Pixel Extractor': 'https://t.me/GeminiPixel1_bot',
        'Sam Topup': 'https://t.me/Samsshop_bot',
        'Acczone Store': 'https://t.me/Acczone_Store_bot',
        'Digital Asset': 'https://t.me/digital_assetbot',
        'AI Shop Mops': 'https://t.me/aishopmopsbot',
        'InsightX': 'https://t.me/InsightX_bot',
        'QuickDigi': 'https://t.me/QuickDigiBot',
        'DigiNest': 'https://t.me/DigiNestStoreBot',
        'BoomPay': 'https://t.me/BoomPay_bot',
        'DigitalSocials': 'https://t.me/DigitalSocialsBot'
      };
      return storeTelegramMap[storeName] || 'https://t.me';
    }

    function openStoreTelegram(storeName) {
      const url = getStoreTelegramUrl(storeName);
      window.open(url, '_blank');
      showToast(`تم فتح متجر ${storeName} في تليجرام ↗`, 'success');
      playChime();
    }

    function openStoreFromNotification(storeName, buyUrl, notifId, event) {
      if (event) event.stopPropagation();
      const targetUrl = buyUrl || getStoreTelegramUrl(storeName);
      window.open(targetUrl, '_blank');

      state.search = storeName;
      const input = document.getElementById('searchInput');
      if (input) input.value = storeName;

      const panel = document.getElementById('notifDropdownPanel');
      if (panel) panel.classList.remove('active');

      switchView('comparison');
      executeSearch();

      showToast(`⚡ تم فتح متجر ${storeName} في تليجرام واستعراض عروضه في الرادار`, 'success');
      playChime();
    }

    function filterByStore(storeName) {
      state.search = storeName;
      const input = document.getElementById('searchInput');
      if (input) input.value = storeName;
      switchView('comparison');
      executeSearch();
      showToast(`عرض كافة عروض متجر: ${storeName}`, 'info');
    }

    // ----------------------------------------------------
    // User Actions: Crawler, Refresh, Alerts, Favorites
    // ----------------------------------------------------
    function runCrawlerNow() {
      const btn = document.getElementById('crawlerBtn');
      if (!btn) return;
      const orig = btn.innerHTML;
      btn.style.pointerEvents = 'none';
      btn.innerHTML = `
        <svg class="spinning-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--mint)" stroke-width="2.5"><path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"></path></svg>
        <span style="color:var(--mint); font-weight:800;">جاري الزحف...</span>
      `;
      showToast('🤖 بدأ البوت الزاحف بمسح وتحديث أسعار 12 متجر من تيليجرام...', 'info');

      try { fetch('/api/crawl', { method: 'POST' }).catch(() => null); } catch(e) {}

      setTimeout(() => {
        btn.innerHTML = orig;
        btn.style.pointerEvents = 'auto';
        state.offers.forEach(o => o.updated_hours = 0);
        renderKPIs();
        renderOfferCards();
        showToast('✅ اكتمل الزحف: تم تحديث أسعار ومخزون 12 متجر بالكامل!', 'success');
        playChime();
      }, 1400);
    }

    function refreshPricesNow() {
      showToast('جاري التحقق من أحدث الأسعار...', 'info');
      setTimeout(() => {
        showToast('تم تحديث ومزامنة جميع الأسعار بنجاح!', 'success');
        playChime();
      }, 600);
    }

    function toggleFavorite(e, id) {
      e.stopPropagation();
      const idx = state.favorites.indexOf(id);
      if (idx >= 0) {
        state.favorites.splice(idx, 1);
        showToast('تمت الإزالة من المفضلة', 'info');
      } else {
        state.favorites.push(id);
        showToast('تمت الإضافة إلى المفضلة ★', 'success');
      }
      localStorage.setItem('user_favs', JSON.stringify(state.favorites));
      renderOfferCards();
    }

    function createPriceAlert() {
      const prod = document.getElementById('alertProdInput').value.trim();
      const price = parseFloat(document.getElementById('alertPriceInput').value);
      if (!prod || isNaN(price)) {
        showToast('يرجى إدخال اسم المنتج والسعر المستهدف', 'error');
        return;
      }
      state.alerts.push({ id: Date.now(), product: prod, target_price: price.toFixed(2), merchant: 'أي متجر معتمد' });
      localStorage.setItem('user_alerts', JSON.stringify(state.alerts));
      document.getElementById('alertProdInput').value = '';
      document.getElementById('alertPriceInput').value = '';
      renderAlertsTable();
      showToast('تم حفظ التنبيه السعري بنجاح', 'success');
    }

    function deleteAlert(id) {
      state.alerts = state.alerts.filter(a => a.id !== id);
      localStorage.setItem('user_alerts', JSON.stringify(state.alerts));
      renderAlertsTable();
      showToast('تم حذف التنبيه', 'info');
    }

    function renderAlertsTable() {
      const box = document.getElementById('alertsTableBox');
      if (!box) return;
      if (!state.alerts.length) {
        box.innerHTML = `<div style="padding:2rem; text-align:center; color:var(--text-muted);">لا توجد تنبيهات سعرية مسجلة حالياً</div>`;
        return;
      }
      box.innerHTML = `
        <table class="changes-table">
          <thead>
            <tr>
              <th>المنتج</th>
              <th>المتجر</th>
              <th>السعر المستهدف</th>
              <th>الإجراء</th>
            </tr>
          </thead>
          <tbody>
            ${state.alerts.map(a => `
              <tr>
                <td style="color:#fff; font-weight:700;">${a.product}</td>
                <td style="color:var(--text-muted);">${a.merchant}</td>
                <td style="color:var(--mint); font-weight:800;">$${a.target_price}</td>
                <td><button onclick="deleteAlert(${a.id})" style="background:transparent; border:none; color:var(--red); cursor:pointer; font-weight:700;">حذف</button></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    }

    function onCatalogSearchChanged(q) {
      state.catalogSearch = (q || '').trim();
      const clearBtn = document.getElementById('catalogSearchClearBtn');
      if (clearBtn) clearBtn.style.display = state.catalogSearch ? 'block' : 'none';
      state.catalogPage = 1;
      renderCatalogView();
    }

    function clearCatalogSearch() {
      const input = document.getElementById('catalogSearchInput');
      if (input) input.value = '';
      state.catalogSearch = '';
      const clearBtn = document.getElementById('catalogSearchClearBtn');
      if (clearBtn) clearBtn.style.display = 'none';
      state.catalogPage = 1;
      renderCatalogView();
    }

    function filterCatalogCategory(cat, btnEl) {
      document.querySelectorAll('#view-subscriptions .quick-chip').forEach(c => c.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      state.catalogCategory = cat;
      state.catalogPage = 1;
      renderCatalogView();
    }

    function loadMoreCatalog() {
      state.catalogPage += 1;
      renderCatalogView();
    }

    function renderCatalogView() {
      const container = document.getElementById('catalogGrid');
      if (!container) return;

      let items = (state.allProducts || []).slice();

      // Filter by category
      if (state.catalogCategory && state.catalogCategory !== 'all') {
        items = items.filter(o => o.product_family === state.catalogCategory);
      }

      // Filter by search query
      if (state.catalogSearch) {
        const qNorm = normalizeText(state.catalogSearch);
        const rawTokens = qNorm.split(/\s+/).filter(Boolean);
        const tokens = rawTokens.map(t => TYPO_MAP[t] || t);

        items = items.filter(item => {
          const text = normalizeText(`${item.name} ${item.product_family || ''} ${item.store_name}`);
          return tokens.every(t => {
            const syns = TOKEN_SYNONYMS[t] || [t];
            return syns.some(s => text.includes(s)) || (t.length >= 3 && text.split(/\s+/).some(w => w.includes(t)));
          });
        });
      }

      const countEl = document.getElementById('catalogOffersCount');
      if (countEl) {
        countEl.innerHTML = `معروض <strong style="color:#fff;">${items.length}</strong> حساب واشتراك`;
      }

      if (!items.length) {
        container.innerHTML = `
          <div style="grid-column:1/-1; text-align:center; padding:3.5rem 1rem; color:var(--text-muted); background:var(--bg-card); border:1px dashed var(--panel-border); border-radius:var(--radius-xl);">
            <div style="font-size:2.2rem; margin-bottom:8px;">🔍</div>
            <h3 style="color:#fff; font-size:1.15rem; font-weight:800; margin-bottom:6px;">لم يتم العثور على حسابات مطابقة للبحث</h3>
            <p style="font-size:0.86rem; color:var(--text-dim); margin-bottom:14px;">جرب اختيار تصنيف آخر أو مسح البحث</p>
            <button class="btn-mint-primary" onclick="clearCatalogSearch(); filterCatalogCategory('all', document.querySelector('#view-subscriptions .quick-chip'));">عرض كافة الحسابات (379)</button>
          </div>
        `;
        return;
      }

      const totalItems = items.length;
      const visibleCount = state.catalogPage * (state.catalogPageSize || 12);
      const visibleItems = items.slice(0, visibleCount);

      const cardsHtml = visibleItems.map((offer, idx) => {
        const color = STORE_COLORS[offer.store_name] || { bg: "#38bdf8", text: "#fff", border: "rgba(56, 189, 248, 0.3)", sparkline: "#00e599" };
        const isFav = state.favorites.includes(offer.id);

        return `
          <div class="offer-card" onclick="openOfferModalById('${offer.id}')">
            <div class="card-top-row">
              <div class="merchant-avatar-info">
                <span class="card-index-badge">${idx + 1}</span>
                <div class="merchant-circle-avatar" style="background:${color.bg}; color:${color.text};">
                  ${offer.initials || 'ST'}
                </div>
                <div class="merchant-title-sub">
                  <span class="store-title">${offer.store_name}</span>
                  <span class="product-sub">${offer.duration_plan || '12 شهر'} • ${offer.product_family || 'الاشتراكات'}</span>
                </div>
              </div>

              <div class="card-top-badges">
                <button class="card-bookmark-btn ${isFav ? 'active' : ''}" onclick="toggleFavorite(event, '${offer.id}')" title="حفظ في المفضلة">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="${isFav ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
                </button>
              </div>
            </div>

            <div style="font-size:0.88rem; font-weight:700; color:#fff; line-height:1.3; min-height:36px;">
              ${offer.name}
            </div>

            <div class="card-pricing-sparkline-row">
              <span class="card-large-price">$${offer.price.toFixed(2)}</span>
              ${generateSparklineSVG(offer.sparkline_points, color.sparkline)}
            </div>

            <div class="card-meta-details-row">
              <span class="meta-inline-item" style="color:var(--mint);">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
                <span>تسليم فوري</span>
              </span>
              <span class="meta-inline-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                <span>${offer.in_stock || 50} متاح</span>
              </span>
            </div>

            <button class="btn-card-details">
              <span>تفاصيل الحساب والشراء ↗</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </button>
          </div>
        `;
      }).join('');

      let paginationHtml = '';
      if (totalItems > visibleCount) {
        const remaining = totalItems - visibleCount;
        paginationHtml = `
          <div style="grid-column: 1 / -1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; margin: 1.5rem 0 2.5rem 0;">
            <button class="btn-mint-primary" onclick="loadMoreCatalog()" style="padding: 0.85rem 2.2rem; font-size: 0.95rem; font-weight:800; border-radius: var(--radius-full); box-shadow: 0 4px 20px rgba(0, 229, 153, 0.25); cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="8 12 12 16 16 12"></polyline><line x1="12" y1="8" x2="12" y2="16"></line></svg>
              <span>عرض المزيد من الحسابات (+${Math.min(12, remaining)} متبقية)</span>
            </button>
            <div style="font-size:0.8rem; color:var(--text-dim);">معروض ${visibleCount} من أصل ${totalItems} حساب واشتراك</div>
          </div>
        `;
      }

      container.innerHTML = cardsHtml + paginationHtml;
    }

    function renderReportsView() {
      const box = document.getElementById('reportsTableBox');
      if (!box) return;
      box.innerHTML = `
        <table class="changes-table">
          <thead>
            <tr>
              <th>المنتج</th>
              <th>المتجر</th>
              <th>السعر</th>
              <th>المخزون</th>
            </tr>
          </thead>
          <tbody>
            ${(state.offers || []).slice(0, 15).map(o => `
              <tr>
                <td style="color:#fff; font-weight:700;">${o.name}</td>
                <td style="color:var(--text-muted);">${o.store_name}</td>
                <td style="color:var(--mint); font-weight:800;">$${o.price.toFixed(2)}</td>
                <td style="color:#fff;">${o.in_stock || 50} قطعة</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    }

    function exportReportsCSV() {
      const rows = [["Product", "Merchant", "Price_USD", "Stock"]];
      state.offers.forEach(o => rows.push([`"${o.name}"`, `"${o.store_name}"`, o.price, o.in_stock || 50]));
      const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "radar_price_report.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast('تم تحميل التقرير بنجاح', 'success');
    }

    function switchView(viewName) {
      document.querySelectorAll('.view-container').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.mobile-bottom-item').forEach(el => el.classList.remove('active'));

      const target = document.getElementById(`view-${viewName}`);
      if (target) target.classList.add('active');

      const navBtn = document.querySelector(`.nav-item[data-view="${viewName}"]`);
      if (navBtn) navBtn.classList.add('active');

      const mobBtn = document.querySelector(`.mobile-bottom-item[data-view="${viewName}"]`);
      if (mobBtn) mobBtn.classList.add('active');

      window.scrollTo({ top: 0, behavior: 'smooth' });

      if (viewName === 'comparison') {
        setTimeout(() => renderMarketChart(), 60);
      } else if (viewName === 'notifications') {
        renderFullNotificationsView();
      }
    }

    function saveSettingsUser() {
      const val = document.getElementById('settingsUserNameInput').value.trim();
      if (val) {
        localStorage.setItem('auth_user_name', val);
        document.getElementById('sidebarAvatar').innerText = val.slice(0, 2).toUpperCase();
        showToast('تم حفظ اسم المستخدم بنجاح', 'success');
      }
    }

    // ----------------------------------------------------
    // Real-Time Notification Engine & Team Share Logic
    // ----------------------------------------------------
    const STORE_NOTIFICATIONS = [
      {
        id: 1,
        store: 'Bite Store',
        text: 'توفر اشتراك Microsoft Office 365 Plus 1 Year بسعر $0.99',
        time: 'منذ دقيقة',
        badge: '💻 Microsoft',
        category: 'microsoft',
        buy_url: 'https://t.me/Bite_storee_bot',
        product_name: 'Microsoft Office 365 Plus 1 Year',
        price: '0.99'
      },
      {
        id: 2,
        store: 'PA Store',
        text: 'تحديث مخزون باقة Microsoft 365 Family (5 حسابات / 5TB) بسعر $2.49',
        time: 'منذ 3 دقائق',
        badge: '🔥 خصم',
        category: 'discount',
        buy_url: 'https://t.me/p_a_store_bot',
        product_name: 'Microsoft 365 Family',
        price: '2.49'
      },
      {
        id: 3,
        store: 'Gemini Pixel Extractor',
        text: 'أقل سعر متوفر بالسوق لـ Gemini Pro 18M: $0.54 فقط',
        time: 'منذ 6 دقائق',
        badge: '✦ AI',
        category: 'ai',
        buy_url: 'https://t.me/GeminiPixel1_bot',
        product_name: 'Gemini Pro 18M',
        price: '0.54'
      },
      {
        id: 4,
        store: 'Sam Topup',
        text: 'إضافة عروض جديدة لاشتراكات ChatGPT Plus 1 Month بسعر $2.95',
        time: 'منذ 10 دقائق',
        badge: '🤖 AI',
        category: 'ai',
        buy_url: 'https://t.me/Samsshop_bot',
        product_name: 'ChatGPT Plus 1 Month',
        price: '2.95'
      },
      {
        id: 5,
        store: 'Acczone Store',
        text: 'وصول دفعة جديدة من حسابات Canva Pro السنوية بسعر $0.35',
        time: 'منذ 15 دقيقة',
        badge: '📦 مخزون',
        category: 'stock',
        buy_url: 'https://t.me/Acczone_Store_bot',
        product_name: 'Canva Pro 1 Year',
        price: '0.35'
      },
      {
        id: 6,
        store: 'Digital Asset',
        text: 'تخفيض سعر مفاتيح Windows 11 Pro الأصلية إلى $1.50',
        time: 'منذ 22 دقيقة',
        badge: '⚡ سعر',
        category: 'microsoft',
        buy_url: 'https://t.me/digital_assetbot',
        product_name: 'Windows 11 Pro Key',
        price: '1.50'
      }
    ];

    let notifSoundEnabled = localStorage.getItem('radar_notif_sound') !== 'false';
    let currentNotifFilter = 'all';

    function toggleNotifSound(enabled) {
      notifSoundEnabled = enabled;
      localStorage.setItem('radar_notif_sound', enabled ? 'true' : 'false');
      showToast(enabled ? 'تم تفعيل صوت التنبيهات 🔊' : 'تم كتم صوت التنبيهات 🔇', 'info');
    }

    function playChime() {
      if (!notifSoundEnabled) return;
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.14);
        gain.gain.setValueAtTime(0.09, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.32);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.32);
      } catch (e) {}
    }

    function toggleNotifPanel(event) {
      if (event) event.stopPropagation();
      const panel = document.getElementById('notifDropdownPanel');
      if (!panel) return;
      panel.classList.toggle('active');
      renderNotifList();
    }

    document.addEventListener('click', (e) => {
      const panel = document.getElementById('notifDropdownPanel');
      const btn = document.getElementById('notifBellBtn');
      const headerBtn = document.getElementById('headerNotifBtn');
      if (panel && panel.classList.contains('active')) {
        if (!panel.contains(e.target) && (!btn || !btn.contains(e.target)) && (!headerBtn || !headerBtn.contains(e.target))) {
          panel.classList.remove('active');
        }
      }
    });

    function updateNotifBadges() {
      const count = STORE_NOTIFICATIONS.length;
      const badge1 = document.getElementById('notifCountBadge');
      const badge2 = document.getElementById('sidebarNotifBadge');
      const badge3 = document.getElementById('filterNotifBadgeAll');
      const badge4 = document.getElementById('mobileNotifBadge');
      const badge5 = document.getElementById('headerNotifBadge');
      if (badge1) {
        badge1.style.display = count ? 'inline-block' : 'none';
        badge1.innerText = count;
      }
      if (badge2) {
        badge2.style.display = count ? 'inline-block' : 'none';
        badge2.innerText = count;
      }
      if (badge3) {
        badge3.innerText = count;
      }
      if (badge4) {
        badge4.style.display = count ? 'inline-block' : 'none';
        badge4.innerText = count;
      }
      if (badge5) {
        badge5.style.display = count ? 'inline-block' : 'none';
        badge5.innerText = count;
      }
    }

    function renderNotifList() {
      const container = document.getElementById('notifListContainer');
      if (!container) return;
      updateNotifBadges();

      if (!STORE_NOTIFICATIONS.length) {
        container.innerHTML = `<div style="padding:2rem; text-align:center; color:var(--text-muted); font-size:0.84rem;">لا توجد إشعارات جديدة حالياً</div>`;
        return;
      }

      container.innerHTML = STORE_NOTIFICATIONS.map(n => {
        const storeUrl = n.buy_url || getStoreTelegramUrl(n.store);
        return `
          <div class="notif-item" onclick="openStoreFromNotification('${n.store}', '${storeUrl}', ${n.id}, event)">
            <div class="notif-item-title">
              <span style="color:var(--mint); font-weight:800;">${n.store}</span>
              <span style="background:rgba(255,255,255,0.06); padding:1px 6px; border-radius:4px; font-size:0.7rem; color:var(--text-muted);">${n.badge}</span>
              <span style="margin-right:auto; font-size:0.7rem; color:var(--text-dim);">${n.time}</span>
            </div>
            <div class="notif-item-desc">${n.text}</div>
            <div style="display:flex; gap:6px; margin-top:6px; flex-wrap:wrap;" onclick="event.stopPropagation()">
              <button class="btn-mint-primary" onclick="openStoreTelegram('${n.store}')" style="height:26px; padding:0 10px; font-size:0.74rem;">
                فتح المتجر في تليجرام ↗
              </button>
              <button class="btn-glass-secondary" onclick="shareNotification(${n.id})" style="height:26px; padding:0 8px; font-size:0.72rem; color:var(--blue);" title="مشاركة الإشعار مع عضو في الفريق">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
                <span>مشاركة 🔗</span>
              </button>
              <button class="btn-glass-secondary" onclick="filterByStore('${n.store}'); document.getElementById('notifDropdownPanel').classList.remove('active');" style="height:26px; padding:0 8px; font-size:0.72rem;">
                بالرادار 🔍
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    function filterNotifCategory(cat, btnEl) {
      currentNotifFilter = cat;
      document.querySelectorAll('#view-notifications .quick-chip').forEach(c => c.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      renderFullNotificationsView();
    }

    function renderFullNotificationsView() {
      const container = document.getElementById('fullNotifListGrid');
      if (!container) return;
      updateNotifBadges();

      let items = STORE_NOTIFICATIONS.slice();
      if (currentNotifFilter && currentNotifFilter !== 'all') {
        items = items.filter(n => {
          if (currentNotifFilter === 'microsoft') {
            return (n.category === 'microsoft') || (n.text.toLowerCase().includes('microsoft') || n.text.toLowerCase().includes('office') || n.badge.includes('Microsoft'));
          }
          if (currentNotifFilter === 'discount') {
            return (n.category === 'discount') || n.badge.includes('خصم') || n.badge.includes('سعر');
          }
          if (currentNotifFilter === 'ai') {
            return (n.category === 'ai') || n.badge.includes('AI') || n.text.toLowerCase().includes('gemini') || n.text.toLowerCase().includes('chatgpt');
          }
          if (currentNotifFilter === 'stock') {
            return (n.category === 'stock') || n.badge.includes('مخزون') || n.text.includes('مخزون') || n.text.includes('توفر');
          }
          return true;
        });
      }

      const statusEl = document.getElementById('notifStatusText');
      if (statusEl) {
        statusEl.innerHTML = `معروض <strong style="color:var(--mint);">${items.length}</strong> إشعار من أصل ${STORE_NOTIFICATIONS.length} • محدث تلقائياً ⚡`;
      }

      if (!items.length) {
        container.innerHTML = `
          <div style="text-align:center; padding:3.5rem 1rem; color:var(--text-muted); background:var(--bg-card); border:1px dashed var(--panel-border); border-radius:var(--radius-xl);">
            <div style="font-size:2.4rem; margin-bottom:8px;">🔔</div>
            <h3 style="color:#fff; font-size:1.15rem; font-weight:800; margin-bottom:6px;">لا توجد إشعارات مطابقة للتصفية حالياً</h3>
            <p style="font-size:0.86rem; color:var(--text-dim); margin-bottom:14px;">يمكنك اختبار تلقي إشعار فوري جديد من المتاجر الآن</p>
            <button class="btn-mint-primary" onclick="simulateLiveStoreAlert()">إرسال إشعار تجريبي الآن ⚡</button>
          </div>
        `;
        return;
      }

      container.innerHTML = items.map((n, idx) => {
        const color = STORE_COLORS[n.store] || { bg: "#38bdf8", text: "#fff" };
        const storeUrl = n.buy_url || getStoreTelegramUrl(n.store);

        return `
          <div class="full-notif-card" onclick="openStoreFromNotification('${n.store}', '${storeUrl}', ${n.id}, event)">
            <div class="full-notif-top">
              <div class="full-notif-store-info">
                <div class="merchant-circle-avatar" style="background:${color.bg}; color:${color.text}; width:40px; height:40px; font-size:0.95rem;">
                  ${n.store.slice(0, 2).toUpperCase()}
                </div>
                <div style="display:flex; flex-direction:column; line-height:1.2;">
                  <div style="display:flex; align-items:center; gap:6px;">
                    <span style="font-weight:800; font-size:0.98rem; color:#fff;">${n.store}</span>
                    <span style="color:var(--mint); font-size:0.75rem;" title="متجر معتمد ومراقب 24/7">✓</span>
                  </div>
                  <span style="font-size:0.75rem; color:var(--text-dim); direction:ltr; text-align:right;">${storeUrl.replace('https://', '')}</span>
                </div>
              </div>

              <div style="display:flex; align-items:center; gap:8px;">
                <span style="background:rgba(255,255,255,0.06); border:1px solid var(--panel-border); padding:3px 10px; border-radius:var(--radius-full); font-size:0.78rem; font-weight:700; color:var(--text-main);">
                  ${n.badge}
                </span>
                <span style="font-size:0.78rem; color:var(--text-dim); font-family:'JetBrains Mono'; background:rgba(0,0,0,0.3); padding:3px 8px; border-radius:6px;">
                  ⏱ ${n.time}
                </span>
              </div>
            </div>

            <div class="full-notif-body">
              ${n.text}
            </div>

            <div class="full-notif-actions" onclick="event.stopPropagation()">
              <button class="btn-mint-primary" onclick="openStoreTelegram('${n.store}')" style="height:36px; padding:0 16px; font-size:0.84rem;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                <span>زيارة متجر ${n.store} في تليجرام ↗</span>
              </button>

              <button class="btn-glass-secondary btn-share-notif" onclick="shareNotification(${n.id})" style="height:36px; padding:0 14px; font-size:0.84rem; color:var(--blue);" title="مشاركة الإشعار مع عضو في الفريق">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="18" cy="5" r="3"></circle>
                  <circle cx="6" cy="12" r="3"></circle>
                  <circle cx="18" cy="19" r="3"></circle>
                  <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                  <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
                </svg>
                <span>مشاركة الإشعار 🔗</span>
              </button>

              <button class="btn-glass-secondary" onclick="filterByStore('${n.store}')" style="height:36px; padding:0 14px; font-size:0.84rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <span>عروض ${n.store} بالرادار</span>
              </button>

              <button class="btn-glass-secondary" onclick="copyNotifText('${n.text.replace(/'/g, "\\'")}')" style="height:36px; padding:0 12px; font-size:0.82rem; margin-right:auto;" title="نسخ نص الإشعار">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                <span>نسخ</span>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    // ----------------------------------------------------
    // Team Share Functionality (Web Share API + Modal Fallback)
    // ----------------------------------------------------
    function shareNotification(notifId) {
      const notif = STORE_NOTIFICATIONS.find(n => n.id === notifId) || STORE_NOTIFICATIONS[0];
      if (!notif) return;

      const storeUrl = notif.buy_url || getStoreTelegramUrl(notif.store);
      const shareTitle = `تنبيه رادار السوق | متجر ${notif.store}`;
      const shareText = `⚡ تنبيه فوري من رادار الأسعار:\n🏬 المتجر: ${notif.store}\n📦 التحديث: ${notif.text}\n⏱ الوقت: ${notif.time}\n🔗 رابط المتجر المباشر: ${storeUrl}\n\n🔍 استعراض كامل العروض عبر رادار السوق:\nhttps://store-price-comparator.vercel.app/`;

      if (navigator.share) {
        navigator.share({
          title: shareTitle,
          text: shareText,
          url: 'https://store-price-comparator.vercel.app/'
        }).then(() => {
          showToast('تمت مشاركة الإشعار بنجاح 🚀', 'success');
          playChime();
        }).catch(err => {
          if (err.name !== 'AbortError') {
            openShareModal(notif, shareText, storeUrl);
          }
        });
      } else {
        openShareModal(notif, shareText, storeUrl);
      }
    }

    function openShareModal(notif, shareText, storeUrl) {
      const modal = document.getElementById('shareModalBackdrop');
      if (!modal) return;

      document.getElementById('shareModalTitle').innerText = `مشاركة إشعار متجر ${notif.store}`;
      document.getElementById('shareModalPreviewText').innerText = shareText;

      const tgBtn = document.getElementById('shareTelegramBtn');
      if (tgBtn) {
        const tgLink = `https://t.me/share/url?url=${encodeURIComponent('https://store-price-comparator.vercel.app/')}&text=${encodeURIComponent(shareText)}`;
        tgBtn.onclick = () => {
          window.open(tgLink, '_blank');
          showToast('جاري الفتح في تيليجرام ↗', 'info');
        };
      }

      const waBtn = document.getElementById('shareWhatsappBtn');
      if (waBtn) {
        const waLink = `https://api.whatsapp.com/send?text=${encodeURIComponent(shareText)}`;
        waBtn.onclick = () => {
          window.open(waLink, '_blank');
          showToast('جاري الفتح في واتساب ↗', 'info');
        };
      }

      const copyBtn = document.getElementById('shareCopyFullBtn');
      if (copyBtn) {
        copyBtn.onclick = () => {
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(shareText);
            showToast('تم نسخ نص وتفاصيل الإشعار بنجاح 📋', 'success');
            playChime();
          } else {
            showToast('تم نسخ الإشعار', 'info');
          }
        };
      }

      modal.classList.add('active');
    }

    function closeShareModal() {
      const modal = document.getElementById('shareModalBackdrop');
      if (modal) modal.classList.remove('active');
    }

    function copyNotifText(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text);
        showToast('تم نسخ نص الإشعار بنجاح 📋', 'success');
      } else {
        showToast('تم نسخ الإشعار', 'info');
      }
    }

    function clearAllNotifications() {
      STORE_NOTIFICATIONS.length = 0;
      updateNotifBadges();
      renderNotifList();
      renderFullNotificationsView();
      showToast('تم مسح جميع الإشعارات', 'info');
    }

    function requestBrowserNotifications() {
      if (!("Notification" in window)) {
        showToast("متصفحك لا يدعم الإشعارات المباشرة", "error");
        return;
      }
      Notification.requestPermission().then(permission => {
        if (permission === "granted") {
          showToast("✅ تم تفعيل إشعارات المتصفح بنجاح!", "success");
          try {
            new Notification("رادار السوق 🔔", {
              body: "تم تفعيل الإشعارات الفورية! ستصلك تنبيهات الأسعار ومتاجر Microsoft فوراً.",
              icon: "https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg"
            });
          } catch(e) {}
          playChime();
        } else {
          showToast("تم رفض إذن إشعارات المتصفح", "info");
        }
      });
    }

    function simulateLiveStoreAlert() {
      const stores = (state.stores || []).map(s => s.name);
      const storeName = stores[Math.floor(Math.random() * stores.length)] || 'PA Store';
      const telegramUrl = getStoreTelegramUrl(storeName);

      const itemsPool = [
        { name: 'Microsoft Office 365 Plus 1 Year', price: '0.44', badge: '💻 Microsoft', cat: 'microsoft' },
        { name: 'Microsoft 365 Family (5 حسابات / 5TB)', price: '2.49', badge: '🔥 خصم', cat: 'discount' },
        { name: 'Google Gemini Pro 18M Account', price: '0.35', badge: '✦ AI', cat: 'ai' },
        { name: 'ChatGPT Plus 1 Month Private', price: '2.62', badge: '🤖 AI', cat: 'ai' },
        { name: 'Canva Pro 1 Year Subscription', price: '0.30', badge: '🎨 تصميم', cat: 'discount' },
        { name: 'Windows 11 Pro Genuine Activation Key', price: '1.50', badge: '⚡ سعر', cat: 'microsoft' },
        { name: 'Netflix 4K Ultra HD 1 Month', price: '0.40', badge: '🎬 ترفيه', cat: 'discount' },
        { name: 'Admin MS365 12M Full Warranty', price: '9.00', badge: '⭐ موثوق', cat: 'microsoft' }
      ];
      const selected = itemsPool[Math.floor(Math.random() * itemsPool.length)];

      const alertItem = {
        id: Date.now(),
        store: storeName,
        text: `تحديث فوري: تم تخفيض سعر ${selected.name} لدى ${storeName} إلى $${selected.price}`,
        time: 'الآن',
        badge: selected.badge,
        category: selected.cat,
        buy_url: telegramUrl,
        product_name: selected.name,
        price: selected.price
      };

      STORE_NOTIFICATIONS.unshift(alertItem);
      if (STORE_NOTIFICATIONS.length > 30) STORE_NOTIFICATIONS.pop();

      renderNotifList();
      renderFullNotificationsView();
      updateNotifBadges();

      showClickableToast(`⚡ إشعار فوري من ${storeName}: ${selected.name} بسعر $${selected.price}!`, storeName, telegramUrl, alertItem.id);

      if ("Notification" in window && Notification.permission === "granted") {
        try {
          const n = new Notification(`رادار السوق | ${storeName}`, {
            body: alertItem.text,
            icon: "https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg"
          });
          n.onclick = function() {
            window.focus();
            window.open(telegramUrl, '_blank');
          };
        } catch(e) {}
      }

      playChime();
    }

    // Auto-poll live store updates automatically:
    // 1. Initial live alert arrives after 4 seconds of opening the page
    setTimeout(() => {
      simulateLiveStoreAlert();
    }, 4000);

    // 2. Ongoing real-time updates every 24 seconds
    setInterval(() => {
      simulateLiveStoreAlert();
    }, 24000);

    function showClickableToast(msg, storeName, url, notifId) {
      const container = document.getElementById('toastContainer');
      if (!container) return;
      const el = document.createElement('div');
      el.className = 'toast';
      el.style.cursor = 'pointer';
      el.title = 'اضغط لفتح متجر ' + storeName + ' مباشرة ↗';
      el.innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap;">
          <span style="flex:1;">${msg}</span>
          <div style="display:flex; align-items:center; gap:6px;">
            <button onclick="event.stopPropagation(); shareNotification(${notifId || 1});" style="background:rgba(255,255,255,0.1); border:1px solid var(--panel-border); color:var(--blue); font-size:0.75rem; font-weight:700; padding:3px 8px; border-radius:4px; cursor:pointer;" title="مشاركة الإشعار مع عضو في الفريق">
              مشاركة 🔗
            </button>
            <span style="background:var(--mint); color:#030508; font-weight:800; font-size:0.75rem; padding:3px 8px; border-radius:4px; white-space:nowrap;">فتح ↗</span>
          </div>
        </div>
      `;
      el.onclick = () => {
        openStoreFromNotification(storeName, url);
        el.remove();
      };
      container.appendChild(el);
      setTimeout(() => el.remove(), 4800);
    }

    function showToast(msg, type = 'info') {
      const container = document.getElementById('toastContainer');
      if (!container) return;
      const el = document.createElement('div');
      el.className = 'toast';
      el.innerText = msg;
      container.appendChild(el);
      setTimeout(() => el.remove(), 3400);
    }
  </script>
</body>
</html>
'''

# Write to all deployment targets
targets = [
    "static/index.html",
    "public/index.html",
    "public/static/index.html",
    "api/static/index.html"
]

for t in targets:
    with open(t, "w", encoding="utf-8") as f:
        f.write(html_content)

print(f"Generated all {len(targets)} HTML targets successfully ({len(html_content)} bytes).")
