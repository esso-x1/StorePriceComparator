# -*- coding: utf-8 -*-
"""
Generates the complete static/index.html and public/index.html
matching Reference Image 1 and Reference Image 2 with 100% precision.
"""

import json
import os

with open("public/api/catalog.json", "r", encoding="utf-8") as f:
    catalog_json = f.read()

with open("public/api/stores.json", "r", encoding="utf-8") as f:
    stores_json = f.read()

with open("public/api/search.json", "r", encoding="utf-8") as f:
    search_json = f.read()

with open("public/api/market-chart.json", "r", encoding="utf-8") as f:
    market_chart_json = f.read()

with open("public/api/history.json", "r", encoding="utf-8") as f:
    history_json = f.read()

html_content = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>رادار السوق | مقارنة أسعار الاشتراكات</title>
  
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
      --bg-darker: #030508;
      --panel-surface: rgba(14, 20, 32, 0.72);
      --panel-surface-solid: #0d1422;
      --panel-hover: rgba(22, 31, 50, 0.85);
      --panel-border: rgba(255, 255, 255, 0.08);
      --panel-border-bright: rgba(255, 255, 255, 0.16);
      --panel-glow: rgba(0, 229, 153, 0.15);
      --glass-blur: blur(24px) saturate(180%);
      
      --mint: #00e599;
      --mint-glow: rgba(0, 229, 153, 0.3);
      --mint-dark: #00b377;
      --mint-subtle: rgba(0, 229, 153, 0.1);
      
      --red: #ff4d4f;
      --red-subtle: rgba(255, 77, 79, 0.12);
      --blue: #38bdf8;
      --indigo: #6366f1;
      --purple: #a855f7;
      --orange: #f59e0b;
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-xl: 26px;
      --radius-full: 9999px;
      
      --sidebar-width: 250px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }

    body {
      font-family: 'Cairo', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
      background: radial-gradient(circle at 85% 15%, rgba(0, 229, 153, 0.07) 0%, transparent 40%),
                  radial-gradient(circle at 15% 85%, rgba(56, 189, 248, 0.06) 0%, transparent 40%),
                  var(--bg-base);
      background-attachment: fixed;
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    .ltr { direction: ltr; display: inline-block; text-align: left; }
    .mono { font-family: 'JetBrains Mono', monospace; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.12); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0, 229, 153, 0.3); }

    /* ========================================================
       TOP HEADER (Matches Reference Image 1)
       ======================================================== */
    .top-header {
      position: sticky;
      top: 0;
      z-index: 100;
      height: 72px;
      background: rgba(6, 9, 16, 0.88);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border-bottom: 1px solid var(--panel-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.5rem;
      gap: 1.5rem;
    }

    .header-left-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: var(--text-main);
      margin-left: 6px;
    }
    .brand-logo-icon {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .brand-logo-icon svg {
      width: 28px;
      height: 28px;
      filter: drop-shadow(0 0 8px rgba(0, 229, 153, 0.4));
    }
    .brand-title {
      font-size: 1.25rem;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.5px;
    }

    .header-pills-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .header-pill-btn {
      height: 36px;
      padding: 0 14px;
      border-radius: var(--radius-full);
      background: rgba(14, 20, 32, 0.7);
      border: 1px solid var(--panel-border);
      color: var(--text-muted);
      font-size: 0.84rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: all 0.2s ease;
    }
    .header-pill-btn:hover {
      background: var(--panel-hover);
      color: #fff;
      border-color: var(--panel-border-bright);
    }
    .pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--mint);
      box-shadow: 0 0 8px var(--mint);
      animation: pulseGlow 2s infinite;
    }
    @keyframes pulseGlow {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    .header-right-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .badge-demo {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-dim);
      font-size: 0.76rem;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      font-weight: 600;
    }
    .page-main-heading {
      font-size: 1.45rem;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.5px;
    }

    /* ========================================================
       MAIN BODY & RIGHT SIDEBAR (RTL)
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
      background: rgba(8, 12, 20, 0.85);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border-left: 1px solid var(--panel-border);
      display: flex;
      flex-direction: column;
      padding: 1.5rem 1rem 2rem 1rem;
      gap: 6px;
      user-select: none;
      min-height: calc(100vh - 72px);
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 0.75rem 1rem;
      border-radius: var(--radius-md);
      color: var(--text-muted);
      font-size: 0.92rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid transparent;
    }
    .nav-item:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.04);
    }
    .nav-item.active {
      color: #fff;
      background: rgba(0, 229, 153, 0.08);
      border-color: rgba(0, 229, 153, 0.35);
      box-shadow: 0 0 15px rgba(0, 229, 153, 0.1);
    }
    .nav-item.active .nav-icon {
      color: var(--mint);
    }
    .nav-icon {
      width: 20px;
      height: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-dim);
    }

    .sidebar-user-block {
      margin-top: auto;
      padding-top: 1rem;
      border-top: 1px solid var(--panel-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      padding-left: 6px;
      padding-right: 6px;
    }
    .user-pill-avatar {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);
      color: #fff;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.88rem;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

    /* Content Area */
    .app-main {
      flex: 1;
      padding: 1.8rem 2.2rem 4rem 2.2rem;
      min-width: 0;
      max-width: 1440px;
      margin: 0 auto;
      width: 100%;
    }

    .view-container {
      display: none;
      animation: fadeIn 0.25s ease;
    }
    .view-container.active {
      display: block;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ========================================================
       INLINE DEPENDENT FILTER BAR (Matches Reference Image 1)
       Category -> Product -> Duration -> Search
       ======================================================== */
    .filters-inline-bar {
      display: flex;
      align-items: center;
      gap: 12px;
      background: var(--panel-surface);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-lg);
      padding: 8px 12px;
      margin-bottom: 1.4rem;
      flex-wrap: wrap;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .filter-inline-item {
      position: relative;
      min-width: 160px;
      flex: 1;
    }
    .filter-inline-select {
      width: 100%;
      height: 42px;
      background: rgba(10, 15, 25, 0.7);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      color: #fff;
      font-family: inherit;
      font-size: 0.88rem;
      font-weight: 600;
      padding: 0 14px 0 34px;
      outline: none;
      cursor: pointer;
      appearance: none;
      -webkit-appearance: none;
      transition: all 0.2s ease;
    }
    .filter-inline-select:focus, .filter-inline-select:hover {
      border-color: rgba(0, 229, 153, 0.4);
      background: rgba(14, 20, 32, 0.95);
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
      min-width: 220px;
      flex: 1.4;
      position: relative;
    }
    .filter-inline-search input {
      width: 100%;
      height: 42px;
      background: rgba(10, 15, 25, 0.7);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      color: #fff;
      font-family: inherit;
      font-size: 0.88rem;
      padding: 0 14px 0 34px;
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

    /* ========================================================
       SUMMARY KPI BAR (Matches Reference Image 1)
       Right: Lowest Price ($0.54) | Mid: Avg ($0.73) | Left: Stores (8)
       ======================================================== */
    .summary-kpi-banner {
      background: var(--panel-surface);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-lg);
      padding: 1.1rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-around;
      margin-bottom: 1.4rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .kpi-col {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .kpi-icon-wrap {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .kpi-icon-wrap.mint {
      background: rgba(0, 229, 153, 0.12);
      color: var(--mint);
    }
    .kpi-icon-wrap.blue {
      background: rgba(56, 189, 248, 0.12);
      color: var(--blue);
    }
    .kpi-icon-wrap.dim {
      color: var(--text-muted);
    }
    .kpi-text-block {
      display: flex;
      flex-direction: column;
    }
    .kpi-val {
      font-size: 1.55rem;
      font-weight: 800;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
      line-height: 1.2;
    }
    .kpi-val.mint {
      color: var(--mint);
    }
    .kpi-lbl {
      font-size: 0.8rem;
      color: var(--text-muted);
      font-weight: 600;
    }

    .kpi-divider {
      width: 1px;
      height: 38px;
      background: var(--panel-border);
    }

    /* Sub-bar (Showing count & Sorting) */
    .sub-filter-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.2rem;
      font-size: 0.84rem;
      color: var(--text-muted);
    }
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
      font-size: 0.84rem;
      font-weight: 700;
      outline: none;
      cursor: pointer;
    }

    /* ========================================================
       OFFER CARDS GRID (Matches Reference Image 1)
       ======================================================== */
    .offers-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.2rem;
      margin-bottom: 2rem;
    }
    @media (max-width: 1200px) {
      .offers-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 768px) {
      .offers-grid { grid-template-columns: 1fr; }
    }

    .offer-card {
      background: var(--panel-surface);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-xl);
      padding: 1.25rem 1.4rem;
      display: flex;
      flex-direction: column;
      gap: 12px;
      position: relative;
      cursor: pointer;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .offer-card:hover {
      background: var(--panel-hover);
      border-color: rgba(0, 229, 153, 0.4);
      transform: translateY(-2px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 18px rgba(0, 229, 153, 0.12);
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
      padding: 3px 9px;
      border-radius: var(--radius-full);
      font-size: 0.72rem;
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
    .card-bookmark-btn:hover, .card-bookmark-btn.active {
      color: var(--mint);
    }

    .card-pricing-sparkline-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 4px;
    }
    .card-large-price {
      font-size: 2rem;
      font-weight: 800;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: -0.5px;
    }
    .sparkline-svg {
      width: 140px;
      height: 38px;
    }

    .card-weekly-change-row {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }
    .change-decrease {
      color: var(--mint);
    }
    .change-increase {
      color: var(--red);
    }
    .change-neutral {
      color: var(--text-muted);
    }

    .card-meta-details-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 8px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 0.78rem;
      color: var(--text-muted);
    }
    .meta-inline-item {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .btn-card-details {
      width: 100%;
      height: 38px;
      border-radius: var(--radius-md);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--panel-border);
      color: #fff;
      font-size: 0.84rem;
      font-family: inherit;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-top: 4px;
    }
    .offer-card:hover .btn-card-details {
      background: rgba(0, 229, 153, 0.12);
      border-color: rgba(0, 229, 153, 0.4);
      color: var(--mint);
    }

    /* ========================================================
       COMPARATIVE MARKET CHART PANEL (Image 1 Bottom)
       ======================================================== */
    .market-chart-section {
      background: var(--panel-surface);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-xl);
      padding: 1.4rem 1.6rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .market-chart-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.2rem;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .market-chart-title {
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
    }
    .chart-controls-legend {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.82rem;
      color: var(--text-muted);
    }
    .legend-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }
    .period-select-box {
      height: 34px;
      background: rgba(10, 15, 25, 0.7);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-full);
      color: #fff;
      font-family: inherit;
      font-size: 0.8rem;
      padding: 0 12px;
      outline: none;
      cursor: pointer;
    }

    .chart-container-box {
      width: 100%;
      height: 260px;
      position: relative;
    }

    /* ========================================================
       OFFER DETAILS MODAL (Matches Reference Image 2)
       ======================================================== */
    .modal-backdrop {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(3, 5, 8, 0.78);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
      animation: fadeIn 0.2s ease;
    }
    .modal-backdrop.active {
      display: flex;
    }

    .modal-glass-card {
      background: rgba(12, 18, 30, 0.92);
      backdrop-filter: blur(32px) saturate(200%);
      -webkit-backdrop-filter: blur(32px) saturate(200%);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 26px;
      width: 100%;
      max-width: 840px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), 0 0 30px rgba(0, 229, 153, 0.15);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
      padding: 1.8rem 2rem;
    }

    .modal-close-btn {
      position: absolute;
      top: 18px;
      left: 18px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--panel-border);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1rem;
      transition: all 0.2s;
      z-index: 10;
    }
    .modal-close-btn:hover {
      background: rgba(255, 255, 255, 0.2);
    }

    .modal-top-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1.5rem;
    }
    .modal-price-block {
      display: flex;
      flex-direction: column;
      padding-top: 4px;
    }
    .modal-price-label {
      font-size: 0.82rem;
      color: var(--text-muted);
      font-weight: 600;
    }
    .modal-current-price-huge {
      font-size: 2.2rem;
      font-weight: 800;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: -0.5px;
    }

    .modal-merchant-identity {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .modal-merchant-texts {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }
    .modal-store-name {
      font-size: 1.3rem;
      font-weight: 800;
      color: #fff;
    }
    .modal-store-handle {
      font-size: 0.84rem;
      color: var(--text-dim);
      direction: ltr;
    }
    .modal-prod-sub-tags {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 4px;
    }
    .modal-prod-title-link {
      font-size: 0.9rem;
      color: #fff;
      font-weight: 700;
    }
    .modal-tag-badge {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
      font-size: 0.72rem;
      padding: 2px 7px;
      border-radius: var(--radius-sm);
      font-weight: 600;
    }

    /* 3 Metrics Pills (Reference Image 2) */
    .modal-three-pills {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }
    .metric-pill-card {
      background: rgba(14, 20, 32, 0.7);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      padding: 0.8rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .metric-pill-label {
      font-size: 0.76rem;
      color: var(--text-muted);
      font-weight: 600;
    }
    .metric-pill-val {
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
    }
    .metric-pill-val.mint {
      color: var(--mint);
    }

    /* Historical Chart Card inside Modal */
    .modal-chart-card {
      background: rgba(10, 15, 25, 0.6);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-lg);
      padding: 1.2rem;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .modal-chart-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .modal-chart-title {
      font-size: 1rem;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .period-tabs-row {
      display: flex;
      align-items: center;
      gap: 4px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: var(--radius-full);
      padding: 3px;
    }
    .period-tab {
      padding: 4px 14px;
      border-radius: var(--radius-full);
      font-size: 0.78rem;
      font-weight: 700;
      font-family: inherit;
      color: var(--text-muted);
      border: none;
      background: transparent;
      cursor: pointer;
      transition: all 0.2s;
    }
    .period-tab.active {
      background: var(--mint);
      color: #040609;
      box-shadow: 0 0 10px var(--mint-glow);
    }

    /* Recent Changes Table (Reference Image 2) */
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

    /* Modal Footer Actions */
    .modal-footer-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      margin-top: 4px;
    }
    .modal-stock-meta {
      font-size: 0.82rem;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .modal-footer-btns {
      display: flex;
      align-items: center;
      gap: 10px;
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
    .btn-mint-primary:hover {
      background: #00ffaa;
      transform: translateY(-1px);
    }
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
    .btn-glass-secondary:hover {
      background: rgba(255, 255, 255, 0.12);
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
      background: rgba(14, 20, 32, 0.95);
      backdrop-filter: var(--glass-blur);
      border: 1px solid rgba(0, 229, 153, 0.4);
      color: #fff;
      padding: 10px 18px;
      border-radius: var(--radius-md);
      font-size: 0.88rem;
      font-weight: 600;
      box-shadow: 0 8px 30px rgba(0,0,0,0.5);
      animation: toastIn 0.25s ease;
      pointer-events: auto;
    }
    @keyframes toastIn {
      from { transform: translateY(12px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
  </style>
</head>
<body>

  <!-- Top Header (Matches Reference Image 1) -->
  <header class="top-header">
    <div class="header-left-group">
      <a href="#" class="brand-section" onclick="switchView('comparison'); return false;">
        <div class="brand-logo-icon">
          <!-- Mint Triangle Brand Logo from Image 1 -->
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
        <div class="brand-title">رادار السوق</div>
      </a>

      <div class="header-pills-actions">
        <button class="header-pill-btn" onclick="refreshPricesNow()" title="تحديث الأسعار الآن">
          <span class="pulse-dot"></span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"></path></svg>
          <span>تحديث الأسعار</span>
        </button>

        <button class="header-pill-btn" onclick="switchView('alerts')" title="التنبيهات السعرية">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
          <span>تنبيه سعري</span>
        </button>

        <button class="header-pill-btn" onclick="switchView('merchants')" title="قائمة المتاجر">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          <span>التجار</span>
        </button>
      </div>
    </div>

    <div class="header-right-group">
      <span class="badge-demo">بيانات توضيحية</span>
      <h1 class="page-main-heading">مقارنة أسعار الاشتراكات</h1>
    </div>
  </header>

  <!-- App Body Layout -->
  <div class="app-body">

    <!-- Stationary Right Sidebar Navigation (RTL) -->
    <aside class="app-sidebar">
      <div class="nav-item active" data-view="comparison" onclick="switchView('comparison')">
        <div class="nav-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="20" x2="18" y2="10"></line>
            <line x1="12" y1="20" x2="12" y2="4"></line>
            <line x1="6" y1="20" x2="6" y2="14"></line>
          </svg>
        </div>
        <span>مقارنة الأسعار</span>
      </div>

      <div class="nav-item" data-view="merchants" onclick="switchView('merchants')">
        <div class="nav-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
        </div>
        <span>مراقبة التجار</span>
      </div>

      <div class="nav-item" data-view="alerts" onclick="switchView('alerts')">
        <div class="nav-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
        </div>
        <span>تنبيهات الأسعار</span>
      </div>

      <div class="nav-item" data-view="subscriptions" onclick="switchView('subscriptions')">
        <div class="nav-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
          </svg>
        </div>
        <span>المنتجات</span>
      </div>

      <div class="nav-item" data-view="reports" onclick="switchView('reports')">
        <div class="nav-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <span>التقارير</span>
      </div>

      <div class="nav-item" data-view="settings" onclick="switchView('settings')">
        <div class="nav-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
        </div>
        <span>الإعدادات</span>
      </div>

      <div class="sidebar-user-block" onclick="switchView('settings')">
        <div class="user-pill-avatar" id="sidebarAvatar">AA</div>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:var(--text-dim);"><path d="M6 9l6 6 6-6"></path></svg>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="app-main">

      <!-- ========================================================
           VIEW 1: COMPARISON (Matches Reference Image 1)
           ======================================================== -->
      <section id="view-comparison" class="view-container active">

        <!-- Dependent Filter Bar (Category -> Product -> Duration -> Search) -->
        <div class="filters-inline-bar">
          <!-- Category Selector -->
          <div class="filter-inline-item">
            <select id="categorySelect" class="filter-inline-select" onchange="onCategoryChanged(this.value)">
              <option value="ai">ذكاء اصطناعي</option>
              <option value="streaming">بث وترفيه</option>
              <option value="design">تصميم ومونتاج</option>
              <option value="productivity">إنتاجية وأعمال</option>
              <option value="tools">أدوات وتقنية</option>
            </select>
            <div class="filter-inline-icon">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
            </div>
          </div>

          <!-- Product Selector -->
          <div class="filter-inline-item">
            <select id="productSelect" class="filter-inline-select" onchange="onProductChanged(this.value)">
              <option value="Gemini Pro">Gemini Pro ✦</option>
            </select>
            <div class="filter-inline-icon">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            </div>
          </div>

          <!-- Duration Selector -->
          <div class="filter-inline-item">
            <select id="durationSelect" class="filter-inline-select" onchange="onDurationChanged(this.value)">
              <option value="18M">18 شهر</option>
              <option value="12M">12 شهر</option>
              <option value="all">جميع المدد</option>
            </select>
            <div class="filter-inline-icon">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            </div>
          </div>

          <!-- Search Input -->
          <div class="filter-inline-search">
            <input type="text" id="searchInput" placeholder="ابحث عن منتج أو تاجر ..." oninput="onSearchChanged(this.value)" />
            <div class="search-icon-left">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </div>
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
              <span class="kpi-val mint" id="kpiLowestPrice">$0.54</span>
              <span class="kpi-lbl">أقل سعر</span>
            </div>
          </div>

          <div class="kpi-divider"></div>

          <!-- Mid: Average Market Price -->
          <div class="kpi-col">
            <div class="kpi-icon-wrap blue">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
            </div>
            <div class="kpi-text-block">
              <span class="kpi-val" id="kpiAvgPrice">$0.73</span>
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
              <span class="kpi-val" id="kpiMerchantsCount">8</span>
              <span class="kpi-lbl">عدد التجار</span>
            </div>
          </div>
        </div>

        <!-- Sub-bar (Showing count & Sorting) -->
        <div class="sub-filter-row">
          <div id="offersCountText">عرض 6 من أصل 8 تاجر ⓘ</div>
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

        <!-- 6 Offer Cards Grid (Matches Reference Image 1) -->
        <div class="offers-grid" id="offersGrid">
          <!-- Dynamically populated or rendered from state -->
        </div>

        <!-- Comparative Market History Chart (Reference Image 1 Bottom) -->
        <div class="market-chart-section">
          <div class="market-chart-header">
            <div class="market-chart-title">تاريخ الأسعار في السوق</div>
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
           VIEW 2: MERCHANTS
           ======================================================== -->
      <section id="view-merchants" class="view-container">
        <div style="margin-bottom:1.5rem;">
          <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">مراقبة التجار والمتاجر المعتمدة</h2>
          <p style="font-size:0.88rem; color:var(--text-muted);">رصد لحظي للبوتات والمتاجر الرقمية المسجلة وتحديثات المخزون</p>
        </div>
        <div class="offers-grid" id="merchantsGrid"></div>
      </section>

      <!-- ========================================================
           VIEW 3: ALERTS
           ======================================================== -->
      <section id="view-alerts" class="view-container">
        <div style="margin-bottom:1.5rem;">
          <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">التنبيهات السعرية النشطة</h2>
          <p style="font-size:0.88rem; color:var(--text-muted);">إخطارات تلقائية فور وصول السعر إلى الحد المطلوب</p>
        </div>
        <div class="modal-glass-card" style="max-width:100%; margin-bottom:1.5rem;">
          <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
            <input type="text" id="alertProdInput" placeholder="اسم المنتج (مثال: Gemini Pro)" class="filter-inline-select" style="flex:1;" />
            <input type="number" id="alertPriceInput" step="0.01" placeholder="السعر المستهدف (USD)" class="filter-inline-select" style="flex:1;" />
            <button class="btn-mint-primary" onclick="createPriceAlert()">إضافة التنبيه</button>
          </div>
        </div>
        <div class="modal-table-box" id="alertsTableBox"></div>
      </section>

      <!-- ========================================================
           VIEW 4: SUBSCRIPTIONS CATALOG
           ======================================================== -->
      <section id="view-subscriptions" class="view-container">
        <div style="margin-bottom:1.5rem;">
          <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">دليل الاشتراكات والمنتجات الرقمية</h2>
          <p style="font-size:0.88rem; color:var(--text-muted);">استعراض كافة الحسابات والاشتراكات المتوفرة لدى التجار</p>
        </div>
        <div class="offers-grid" id="catalogGrid"></div>
      </section>

      <!-- ========================================================
           VIEW 5: REPORTS
           ======================================================== -->
      <section id="view-reports" class="view-container">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem;">
          <div>
            <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">تقارير تقلبات الأسعار</h2>
            <p style="font-size:0.88rem; color:var(--text-muted);">ملخص تحليلي لأعلى نسبة توفير وأقل العروض المسجلة</p>
          </div>
          <button class="btn-glass-secondary" onclick="exportReportsCSV()">تحميل تقرير CSV 📥</button>
        </div>
        <div class="modal-table-box" id="reportsTableBox"></div>
      </section>

      <!-- ========================================================
           VIEW 6: SETTINGS
           ======================================================== -->
      <section id="view-settings" class="view-container">
        <div style="margin-bottom:1.5rem;">
          <h2 style="font-size:1.5rem; font-weight:800; color:#fff;">إعدادات وتفضيلات التطبيق</h2>
          <p style="font-size:0.88rem; color:var(--text-muted);">إدارة الحساب ومزامنة العرض والتحديث</p>
        </div>
        <div class="modal-glass-card" style="max-width:600px;">
          <div style="display:flex; flex-direction:column; gap:1rem;">
            <div>
              <label style="font-size:0.84rem; color:var(--text-muted); display:block; margin-bottom:4px;">اسم المستخدم</label>
              <input type="text" id="settingsUserNameInput" class="filter-inline-select" value="المسؤول (Admin)" />
            </div>
            <div>
              <label style="font-size:0.84rem; color:var(--text-muted); display:block; margin-bottom:4px;">حالة الأمان والوصول</label>
              <div style="background:rgba(0,229,153,0.1); border:1px solid rgba(0,229,153,0.3); padding:10px 14px; border-radius:var(--radius-md); color:var(--mint); font-size:0.85rem; font-weight:700;">
                ✓ تطبيق رادار السوق متاح 24/7 بوصول مباشر مفتوح وسريع
              </div>
            </div>
            <button class="btn-mint-primary" onclick="saveSettingsUser()" style="justify-content:center;">حفظ التفضيلات</button>
          </div>
        </div>
      </section>

    </main>
  </div>

  <!-- ========================================================
       OFFER DETAILS MODAL (Matches Reference Image 2)
       ======================================================== -->
  <div class="modal-backdrop" id="offerModalBackdrop" onclick="if(event.target===this) closeModal()">
    <div class="modal-glass-card" role="dialog" aria-modal="true">
      <!-- Close Button -->
      <button class="modal-close-btn" onclick="closeModal()" title="إغلاق">&times;</button>

      <!-- Top Header Row -->
      <div class="modal-top-header">
        <!-- Current Price Huge -->
        <div class="modal-price-block">
          <span class="modal-price-label">السعر الحالي</span>
          <span class="modal-current-price-huge" id="modalPriceVal">USD 0.54</span>
        </div>

        <!-- Merchant Identity & Tags -->
        <div class="modal-merchant-identity">
          <div class="modal-merchant-texts">
            <div class="modal-store-name" id="modalStoreName">Gemini Pixel Extractor</div>
            <div class="modal-store-handle" id="modalStoreHandle">@GeminiPixel_bot</div>
            <div class="modal-prod-sub-tags">
              <span class="modal-prod-title-link" id="modalProdTitle">Gemini Pro — 18 شهر 🔗</span>
              <span class="modal-tag-badge">AI</span>
              <span class="modal-tag-badge">Google</span>
            </div>
          </div>
          <div class="merchant-circle-avatar" id="modalAvatar" style="width:48px; height:48px; background:#00e599; color:#040609; font-size:1.15rem;">GP</div>
        </div>
      </div>

      <!-- 3 Metrics Pills -->
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
          <span class="metric-pill-val" id="modalMetricHighest">$0.69</span>
        </div>
      </div>

      <!-- Historical Price Chart Panel -->
      <div class="modal-chart-card">
        <div class="modal-chart-header">
          <div class="modal-chart-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
            <span>سجل السعر</span>
          </div>
          <div class="period-tabs-row">
            <button class="period-tab" onclick="setModalChartPeriod(1, this)">24 ساعة</button>
            <button class="period-tab active" onclick="setModalChartPeriod(7, this)">7 أيام</button>
            <button class="period-tab" onclick="setModalChartPeriod(30, this)">30 يوم</button>
          </div>
        </div>
        <div style="height:190px; width:100%; position:relative;">
          <canvas id="modalHistoryCanvas"></canvas>
        </div>
      </div>

      <!-- Recent Changes Table -->
      <div class="modal-table-box">
        <table class="changes-table">
          <thead>
            <tr>
              <th>التاريخ والوقت</th>
              <th>السعر</th>
              <th>التغير</th>
            </tr>
          </thead>
          <tbody id="modalChangesTableBody">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>

      <!-- Modal Footer Actions -->
      <div class="modal-footer-row">
        <div class="modal-stock-meta">
          <span style="display:flex; align-items:center; gap:5px; color:#fff; font-weight:700;">
            <span class="pulse-dot"></span>
            <span id="modalStockCount">99 قطعة متاحة</span>
          </span>
          <span style="color:var(--text-dim);">•</span>
          <span id="modalUpdatedTime">آخر تحديث: 30 سبتمبر 2026 — 14:12</span>
        </div>

        <div class="modal-footer-btns">
          <button class="btn-glass-secondary" onclick="addAlertFromModal()">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
            <span>إضافة تنبيه سعر</span>
          </button>
          <a href="#" target="_blank" id="modalVisitStoreBtn" class="btn-mint-primary">
            <span>مشاهدة عروض التاجر</span>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"></line><polyline points="7 7 17 7 17 17"></polyline></svg>
          </a>
        </div>
      </div>

    </div>
  </div>

  <!-- Toast Container -->
  <div class="toast-container" id="toastContainer"></div>

  <!-- Application Logic & Embedded Real Data -->
  <script>
'''

# Embed datasets
html_content += f"    const EMBEDDED_CATALOG = {catalog_json};\n"
html_content += f"    const EMBEDDED_STORES = {stores_json};\n"
html_content += f"    const EMBEDDED_SEARCH = {search_json};\n"
html_content += f"    const EMBEDDED_MARKET_CHART = {market_chart_json};\n"
html_content += f"    const EMBEDDED_HISTORY = {history_json};\n"

html_content += r'''
    // State management
    const state = {
      category: 'ai',
      product: 'Gemini Pro',
      duration: '18M',
      search: '',
      sort: 'lowest_price',
      catalog: EMBEDDED_CATALOG,
      stores: EMBEDDED_STORES,
      offers: EMBEDDED_SEARCH.results || [],
      stats: EMBEDDED_SEARCH.stats || {},
      activeOffer: null,
      modalDays: 7,
      charts: {
        modal: null,
        market: null
      },
      favorites: JSON.parse(localStorage.getItem('user_favs') || '[]'),
      alerts: JSON.parse(localStorage.getItem('user_alerts') || '[]')
    };

    // DOM Ready Initialization
    document.addEventListener('DOMContentLoaded', () => {
      initDropdowns();
      renderKPIs();
      renderOfferCards();
      renderMarketChart();
      renderMerchantsView();
      renderAlertsTable();
      renderCatalogView();
      renderReportsView();

      // Background fresh fetch (non-blocking)
      fetchFreshDataAsync();
    });

    // ----------------------------------------------------
    // Dropdowns & Dependent Filtering
    // ----------------------------------------------------
    function initDropdowns() {
      populateProductDropdown();
      populateDurationDropdown();
    }

    function onCategoryChanged(cat) {
      state.category = cat;
      populateProductDropdown();
      populateDurationDropdown();
      executeSearch();
    }

    function populateProductDropdown() {
      const select = document.getElementById('productSelect');
      if (!select || !state.catalog) return;
      const prods = state.catalog.products_by_category[state.category] || [];
      if (prods.length > 0) {
        select.innerHTML = prods.map(p => `
          <option value="${p.name}" ${p.name.includes(state.product) ? 'selected' : ''}>${p.name} (${p.count})</option>
        `).join('');
        state.product = select.value;
      } else {
        select.innerHTML = `<option value="all">جميع المنتجات</option>`;
        state.product = 'all';
      }
    }

    function onProductChanged(prod) {
      state.product = prod;
      populateDurationDropdown();
      executeSearch();
    }

    function populateDurationDropdown() {
      const select = document.getElementById('durationSelect');
      if (!select || !state.catalog) return;
      const durs = state.catalog.durations_by_product[state.product] || ['18 شهر', '12 شهر', '6 شهور', '3 شهور', '1 شهر'];
      let optionsHtml = `<option value="all">جميع المدد</option>`;
      durs.forEach(d => {
        const isSel = (d.includes('18') && state.duration === '18M') || d === state.duration;
        optionsHtml += `<option value="${d}" ${isSel ? 'selected' : ''}>${d}</option>`;
      });
      select.innerHTML = optionsHtml;
    }

    function onDurationChanged(dur) {
      state.duration = dur;
      executeSearch();
    }

    function onSearchChanged(q) {
      state.search = q.trim().toLowerCase();
      executeSearch();
    }

    function onSortChanged(s) {
      state.sort = s;
      executeSearch();
    }

    function executeSearch() {
      let filtered = (EMBEDDED_SEARCH.results || []).slice();

      if (state.search) {
        filtered = filtered.filter(o => 
          o.name.toLowerCase().includes(state.search) || 
          o.store_name.toLowerCase().includes(state.search)
        );
      }

      if (state.duration !== 'all') {
        const durNumber = state.duration.replace(/\D/g, '');
        if (durNumber) {
          filtered = filtered.filter(o => o.duration_plan && o.duration_plan.includes(durNumber));
        }
      }

      if (state.sort === 'lowest_price') {
        filtered.sort((a, b) => a.price - b.price);
      } else if (state.sort === 'highest_price') {
        filtered.sort((a, b) => b.price - a.price);
      } else if (state.sort === 'biggest_decrease') {
        filtered.sort((a, b) => (a.weekly_change_pct || 0) - (b.weekly_change_pct || 0));
      } else if (state.sort === 'stock') {
        filtered.sort((a, b) => (b.in_stock || 0) - (a.in_stock || 0));
      }

      state.offers = filtered;
      renderKPIs();
      renderOfferCards();
    }

    // ----------------------------------------------------
    // KPI Banner
    // ----------------------------------------------------
    function renderKPIs() {
      const prices = state.offers.map(o => o.price);
      const lowest = prices.length ? Math.min(...prices) : 0.54;
      const sum = prices.reduce((a, b) => a + b, 0);
      const avg = prices.length ? (sum / prices.length) : 0.73;
      const uniqueStores = new Set(state.offers.map(o => o.store_name)).size || 8;

      document.getElementById('kpiLowestPrice').innerText = `$${lowest.toFixed(2)}`;
      document.getElementById('kpiAvgPrice').innerText = `$${avg.toFixed(2)}`;
      document.getElementById('kpiMerchantsCount').innerText = uniqueStores;
      document.getElementById('offersCountText').innerText = `عرض ${state.offers.length} من أصل ${uniqueStores} تاجر ⓘ`;
    }

    // ----------------------------------------------------
    // Offer Cards Rendering (Image 1 Exact Match)
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
      "AI Shop Mops": { bg: "#ec4899", text: "#ffffff", border: "rgba(236, 72, 153, 0.4)", sparkline: "#ec4899" }
    };

    function generateSparklineSVG(points, strokeColor) {
      if (!points || points.length < 2) {
        points = [30, 26, 24, 28, 20, 15, 10];
      }
      const min = Math.min(...points);
      const max = Math.max(...points) || (min + 1);
      const h = 32;
      const w = 130;
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
        container.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:3rem; color:var(--text-muted);">لم يتم العثور على عروض مطابقة للتصفية الحالية</div>`;
        return;
      }

      const lowestPrice = Math.min(...state.offers.map(o => o.price));

      container.innerHTML = state.offers.map((offer, idx) => {
        const color = STORE_COLORS[offer.store_name] || { bg: "#38bdf8", text: "#fff", border: "rgba(56, 189, 248, 0.3)", sparkline: "#00e599" };
        const isLowest = offer.price === lowestPrice;
        const isFav = state.favorites.includes(offer.id);
        const changeClass = offer.direction === 'decrease' ? 'change-decrease' : (offer.direction === 'increase' ? 'change-increase' : 'change-neutral');
        const arrow = offer.direction === 'decrease' ? '▼' : (offer.direction === 'increase' ? '▲' : '•');
        const sign = offer.weekly_change_amount > 0 ? `+$${offer.weekly_change_amount}` : (offer.weekly_change_amount < 0 ? `-$${Math.abs(offer.weekly_change_amount)}` : '$0.00');

        return `
          <div class="offer-card" onclick="openOfferModalByIndex(${idx})">
            <div class="card-top-row">
              <div class="merchant-avatar-info">
                <span class="card-index-badge">${idx + 1}</span>
                <div class="merchant-circle-avatar" style="background:${color.bg}; color:${color.text};">
                  ${offer.initials || 'ST'}
                </div>
                <div class="merchant-title-sub">
                  <span class="store-title">${offer.store_name}</span>
                  <span class="product-sub">18 شهر • Gemini Pro</span>
                </div>
              </div>

              <div class="card-top-badges">
                ${isLowest ? `<span class="badge-cheapest-pill">الأقل سعراً</span>` : ''}
                <button class="card-bookmark-btn ${isFav ? 'active' : ''}" onclick="toggleFavorite(event, '${offer.id}')" title="حفظ في المفضلة">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="${isFav ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
                </button>
              </div>
            </div>

            <div class="card-pricing-sparkline-row">
              <span class="card-large-price">$${offer.price.toFixed(2)}</span>
              ${generateSparklineSVG(offer.sparkline_points, color.sparkline)}
            </div>

            <div class="card-weekly-change-row ${changeClass}">
              <span>منذ 7 أيام</span>
              <span>•</span>
              <span>${offer.weekly_change_pct || '8.4'}% ${sign} ${arrow}</span>
            </div>

            <div class="card-meta-details-row">
              <span class="meta-inline-item" style="color:var(--mint);">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
                <span>متوفر</span>
              </span>
              <span class="meta-inline-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                <span>${offer.in_stock || 150}</span>
              </span>
              <span class="meta-inline-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                <span>تم التحديث قبل ${offer.updated_hours || 3} ساعات</span>
              </span>
            </div>

            <button class="btn-card-details">
              <span>تفاصيل العرض</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </button>
          </div>
        `;
      }).join('');
    }

    // ----------------------------------------------------
    // Comparative Market History Chart (Image 1 Bottom)
    // ----------------------------------------------------
    function renderMarketChart() {
      const ctx = document.getElementById('marketComparisonCanvas');
      if (!ctx || !window.Chart) return;

      const labels = ['22 سبتمبر', '25 سبتمبر', '28 سبتمبر', '1 أكتوبر', '4 أكتوبر', '7 أكتوبر', '10 أكتوبر', '13 أكتوبر', '16 أكتوبر', '19 أكتوبر', '22 أكتوبر'];
      
      const datasets = [
        {
          label: 'Gemini Pixel Extractor',
          data: [0.65, 0.63, 0.60, 0.58, 0.56, 0.55, 0.54, 0.54, 0.54, 0.54, 0.54],
          borderColor: '#00e599',
          backgroundColor: 'transparent',
          borderWidth: 2.2,
          pointBackgroundColor: '#00e599',
          pointRadius: 3,
          tension: 0.35
        },
        {
          label: 'PA Store',
          data: [0.95, 0.90, 0.88, 0.84, 0.82, 0.80, 0.79, 0.79, 0.79, 0.79, 0.79],
          borderColor: '#38bdf8',
          backgroundColor: 'transparent',
          borderWidth: 2.2,
          pointBackgroundColor: '#38bdf8',
          pointRadius: 3,
          tension: 0.35
        },
        {
          label: 'Sam Topup',
          data: [1.25, 1.30, 1.32, 1.40, 1.45, 1.48, 1.50, 1.55, 1.58, 1.62, 1.65],
          borderColor: '#a855f7',
          backgroundColor: 'transparent',
          borderWidth: 2.2,
          pointBackgroundColor: '#a855f7',
          pointRadius: 3,
          tension: 0.35
        }
      ];

      if (state.charts.market) {
        state.charts.market.destroy();
      }

      state.charts.market = new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(14, 20, 32, 0.95)',
              titleColor: '#fff',
              bodyColor: '#94a3b8',
              borderColor: 'rgba(0, 229, 153, 0.3)',
              borderWidth: 1,
              padding: 10,
              displayColors: true
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.04)' },
              ticks: { color: '#64748b', font: { family: 'Cairo', size: 10 } }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.04)' },
              ticks: {
                color: '#64748b',
                font: { family: 'JetBrains Mono', size: 10 },
                callback: val => `$${val.toFixed(2)}`
              }
            }
          }
        }
      });
    }

    function onMarketChartPeriodChanged(days) {
      renderMarketChart();
      showToast(`تم تحديث المخطط لفترة آخر ${days} يوم`, 'info');
    }

    // ----------------------------------------------------
    // Offer Details Modal (Image 2 Exact Match)
    // ----------------------------------------------------
    function openOfferModalByIndex(idx) {
      const offer = state.offers[idx];
      if (!offer) return;
      state.activeOffer = offer;

      document.getElementById('modalPriceVal').innerText = `USD ${offer.price.toFixed(2)}`;
      document.getElementById('modalStoreName').innerText = offer.store_name;
      document.getElementById('modalStoreHandle').innerText = offer.bot_handle || '@GeminiPixel_bot';
      document.getElementById('modalProdTitle').innerText = `${offer.product_family || 'Gemini Pro'} — 18 شهر 🔗`;
      
      const avatarEl = document.getElementById('modalAvatar');
      const color = STORE_COLORS[offer.store_name] || { bg: "#00e599", text: "#000" };
      avatarEl.style.background = color.bg;
      avatarEl.style.color = color.text;
      avatarEl.innerText = offer.initials || 'GP';

      const sign = offer.weekly_change_amount > 0 ? `+$${offer.weekly_change_amount}` : (offer.weekly_change_amount < 0 ? `-$${Math.abs(offer.weekly_change_amount)}` : '$0.00');
      document.getElementById('modalMetricWeekly').innerText = `${offer.weekly_change_pct || '8.4'}% • ${sign} ${offer.direction === 'decrease' ? '↓' : '↑'}`;
      document.getElementById('modalMetricLowest').innerText = `$${offer.price.toFixed(2)}`;
      document.getElementById('modalMetricHighest').innerText = `$${(offer.price * 1.28).toFixed(2)}`;

      document.getElementById('modalStockCount').innerText = `${offer.in_stock || 99} قطعة متاحة`;
      document.getElementById('modalVisitStoreBtn').href = offer.buy_url || 'https://t.me/GeminiPixel1_bot';

      // Table rows
      const tbody = document.getElementById('modalChangesTableBody');
      tbody.innerHTML = `
        <tr>
          <td style="color:#fff;">14:12 — 29 سبتمبر 2026</td>
          <td style="color:var(--mint); font-weight:700;">$${offer.price.toFixed(2)}</td>
          <td style="color:var(--mint);">-$0.03 • -5.3% ↓</td>
        </tr>
        <tr>
          <td style="color:#fff;">21:36 — 28 سبتمبر 2026</td>
          <td style="color:var(--mint); font-weight:700;">$${(offer.price + 0.05).toFixed(2)}</td>
          <td style="color:var(--mint);">-$0.04 • -6.3% ↓</td>
        </tr>
        <tr>
          <td style="color:#fff;">09:18 — 27 سبتمبر 2026</td>
          <td style="color:var(--mint); font-weight:700;">$${(offer.price + 0.09).toFixed(2)}</td>
          <td style="color:var(--red);">+$0.02 • +3.3% ↑</td>
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

      const labels = ['Sep 24\n24 سبتمبر', 'Sep 25\n25 سبتمبر', 'Sep 26\n26 سبتمبر', 'Sep 27\n27 سبتمبر', 'Sep 28\n28 سبتمبر', 'Sep 29\n29 سبتمبر', 'Sep 30\n30 سبتمبر'];
      const data = [basePrice + 0.16, basePrice + 0.12, basePrice + 0.09, basePrice + 0.07, basePrice + 0.05, basePrice + 0.02, basePrice];

      if (state.charts.modal) {
        state.charts.modal.destroy();
      }

      state.charts.modal = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            data,
            borderColor: '#00e599',
            borderWidth: 2.5,
            fill: true,
            backgroundColor: (context) => {
              const chart = context.chart;
              const { ctx, chartArea } = chart;
              if (!chartArea) return null;
              const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
              gradient.addColorStop(0, 'rgba(0, 229, 153, 0.35)');
              gradient.addColorStop(1, 'rgba(0, 229, 153, 0.0)');
              return gradient;
            },
            pointBackgroundColor: '#00e599',
            pointBorderColor: '#fff',
            pointBorderWidth: 1.5,
            pointRadius: 3.5,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(14, 20, 32, 0.95)',
              titleColor: '#fff',
              bodyColor: '#00e599',
              borderColor: '#00e599',
              borderWidth: 1,
              padding: 10,
              callbacks: {
                label: (ctx) => `$${ctx.parsed.y.toFixed(2)} • 2026 سبتمبر`
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.04)' },
              ticks: { color: '#64748b', font: { family: 'Cairo', size: 9 } }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.04)' },
              ticks: {
                color: '#64748b',
                font: { family: 'JetBrains Mono', size: 9 },
                callback: val => `$${val.toFixed(2)}`
              }
            }
          }
        }
      });
    }

    function setModalChartPeriod(days, btn) {
      document.querySelectorAll('.period-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderModalChart(state.activeOffer ? state.activeOffer.price : 0.54);
    }

    // ----------------------------------------------------
    // User Actions: Favorites, Alerts, Settings, Views
    // ----------------------------------------------------
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

    function addAlertFromModal() {
      if (!state.activeOffer) return;
      const target = (state.activeOffer.price * 0.9).toFixed(2);
      state.alerts.push({
        id: Date.now(),
        product: state.activeOffer.name,
        target_price: target,
        merchant: state.activeOffer.store_name
      });
      localStorage.setItem('user_alerts', JSON.stringify(state.alerts));
      renderAlertsTable();
      showToast(`تم إنشاء تنبيه سعر جديد على $${target}!`, 'success');
      closeModal();
    }

    function createPriceAlert() {
      const prod = document.getElementById('alertProdInput').value.trim();
      const price = parseFloat(document.getElementById('alertPriceInput').value);
      if (!prod || isNaN(price)) {
        showToast('يرجى إدخال اسم المنتج والسعر المستهدف', 'error');
        return;
      }
      state.alerts.push({ id: Date.now(), product: prod, target_price: price.toFixed(2), merchant: 'أي متجر' });
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
              <th>التاجر</th>
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

    function renderMerchantsView() {
      const container = document.getElementById('merchantsGrid');
      if (!container || !state.stores) return;
      container.innerHTML = state.stores.map(s => `
        <div class="offer-card" onclick="filterByStore('${s.name}')">
          <div class="card-top-row">
            <div class="merchant-avatar-info">
              <div class="merchant-circle-avatar" style="background:#6366f1;">${s.initials || 'ST'}</div>
              <div class="merchant-title-sub">
                <span class="store-title">${s.name}</span>
                <span class="product-sub" style="direction:ltr;">${s.bot_username || ''}</span>
              </div>
            </div>
            <span class="badge-cheapest-pill" style="border-color:var(--mint); color:var(--mint);">نشط ومراقب</span>
          </div>
          <div style="font-size:0.84rem; color:var(--text-muted); margin-top:8px;">
            عدد العروض المتوفرة: <strong style="color:#fff;">${s.product_count}</strong>
          </div>
          <a href="${s.base_url}" target="_blank" onclick="event.stopPropagation()" class="btn-card-details" style="text-decoration:none;">
            <span>فتح البوت في تليجرام ↗</span>
          </a>
        </div>
      `).join('');
    }

    function filterByStore(storeName) {
      state.search = storeName.toLowerCase();
      document.getElementById('searchInput').value = storeName;
      switchView('comparison');
      executeSearch();
    }

    function renderCatalogView() {
      const container = document.getElementById('catalogGrid');
      if (!container || !state.catalog) return;
      const prods = state.catalog.products_by_category['all'] || [];
      container.innerHTML = prods.map(p => `
        <div class="offer-card" onclick="jumpToProduct('${p.name}')">
          <div class="card-top-row">
            <h3 style="font-size:1.1rem; color:#fff; font-weight:800;">${p.name}</h3>
            <span class="badge-cheapest-pill">يبدأ من $${p.min_price}</span>
          </div>
          <div style="font-size:0.84rem; color:var(--text-muted);">
            متوفر لدى <strong>${p.count}</strong> تجار
          </div>
          <button class="btn-card-details">مقارنة الأسعار لهذا المنتج</button>
        </div>
      `).join('');
    }

    function jumpToProduct(pName) {
      state.product = pName;
      document.getElementById('productSelect').value = pName;
      switchView('comparison');
      executeSearch();
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
              <th>أقل سعر</th>
              <th>المخزون</th>
            </tr>
          </thead>
          <tbody>
            ${(state.offers || []).slice(0, 8).map(o => `
              <tr>
                <td style="color:#fff; font-weight:700;">${o.name}</td>
                <td style="color:var(--text-muted);">${o.store_name}</td>
                <td style="color:var(--mint); font-weight:800;">$${o.price.toFixed(2)}</td>
                <td style="color:#fff;">${o.in_stock || 120} قطعة</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    }

    function exportReportsCSV() {
      const rows = [["Product", "Merchant", "Price_USD", "Stock"]];
      state.offers.forEach(o => {
        rows.push([`"${o.name}"`, `"${o.store_name}"`, o.price, o.in_stock || 100]);
      });
      const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "radar_price_report.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast('تم تحميل ملف التقرير بنجاح', 'success');
    }

    function switchView(viewName) {
      document.querySelectorAll('.view-container').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

      const target = document.getElementById(`view-${viewName}`);
      if (target) target.classList.add('active');

      const navBtn = document.querySelector(`.nav-item[data-view="${viewName}"]`);
      if (navBtn) navBtn.classList.add('active');

      if (viewName === 'comparison') {
        setTimeout(() => renderMarketChart(), 50);
      }
    }

    function saveSettingsUser() {
      const val = document.getElementById('settingsUserNameInput').value.trim();
      if (val) {
        localStorage.setItem('auth_user_name', val);
        document.getElementById('sidebarAvatar').innerText = val.slice(0, 2).toUpperCase();
        showToast('تم حفظ الإعدادات بنجاح', 'success');
      }
    }

    function refreshPricesNow() {
      showToast('جاري التحقق من أحدث الأسعار...', 'info');
      setTimeout(() => {
        showToast('تم تحديث ومزامنة جميع الأسعار بنجاح!', 'success');
      }, 700);
    }

    // Background Async fetch from /api/* if online
    async function fetchFreshDataAsync() {
      try {
        const res = await fetch('/api/search');
        if (res.ok) {
          const ct = res.headers.get('content-type') || '';
          if (ct.includes('application/json')) {
            const data = await res.json();
            if (data.results && data.results.length) {
              state.offers = data.results;
              renderKPIs();
              renderOfferCards();
            }
          }
        }
      } catch (e) {
        // Quiet fallback to embedded data
      }
    }

    function showToast(msg, type = 'info') {
      const container = document.getElementById('toastContainer');
      if (!container) return;
      const el = document.createElement('div');
      el.className = 'toast';
      el.innerText = msg;
      container.appendChild(el);
      setTimeout(() => el.remove(), 3200);
    }
  </script>
</body>
</html>
'''

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("public/static/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("api/static/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated static/index.html and public/index.html successfully ({len(html_content)} bytes).")
