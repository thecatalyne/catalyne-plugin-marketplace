#!/usr/bin/env python3
"""render-playground.py — Generate a single-file HTML playground from a brand bundle.

Usage:
    render-playground.py --brand-dir <path-to-brand-assets-dir> --out <path-to-playground.html>

Reads:
    {brand-dir}/tokens.json                (required)
    {brand-dir}/brand-identity.yaml        (optional — for name + tagline)
    {brand-dir}/brand-extensions.yaml OR brand.extensions.yaml (optional)
    {brand-dir}/surface-translations.yaml  (optional — for platform matrix)

Writes:
    {out}                                   (single HTML file)

The renderer copies `assets/playground-template.html` and substitutes:
    {{BRAND_NAME}}            — brand name from brand-identity.yaml.identity.name
    {{LOOK_ROOT_VARS}}        — CSS custom properties for the brand's Look
    {{LOOK_A_VARS}}           — same; compare-mode A starts as the brand
    {{LOOK_B_VARS}}           — same; compare-mode B defaults to the first preset
    {{LOOK_DATA_JSON}}        — the Look dict serialized to JSON
    {{PRESETS_DATA_JSON}}     — preset Looks (--no-presets emits [])
    {{HERO_TAGLINE}}, etc.    — see Task 7+; surface-specific copy
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib.look_loader import build_look  # noqa: E402

PLUGIN_ROOT = SCRIPT_DIR.parent
TEMPLATE = PLUGIN_ROOT / "assets" / "playground-template.html"
PRESETS  = PLUGIN_ROOT / "assets" / "playground-presets.json"


# ─── Marketing surface markup ──────────────────────────────────────────────────
MARKETING_BODY_HTML = """
<style>
  .mkt { font-family: var(--font-body); color: var(--color-text-primary); background: var(--color-bg); }
  .mkt section { padding: var(--space-16, 4rem) var(--space-6, 1.5rem); max-width: 1200px; margin: 0 auto; }
  .mkt-hero { text-align: center; padding-top: var(--space-24, 6rem); padding-bottom: var(--space-24, 6rem); }
  .mkt-hero h1 { font-family: var(--font-heading, var(--font-body)); font-size: var(--font-size-display, 3.815rem); font-weight: var(--font-weight-bold, 700); line-height: var(--line-height-tight, 1.1); letter-spacing: var(--letter-spacing-tight, -0.02em); margin: 0 0 var(--space-4, 1rem); }
  .mkt-hero p.lead { font-size: var(--font-size-lead, 1.25rem); color: var(--color-text-secondary); margin: 0 auto var(--space-8, 2rem); max-width: 560px; }
  .mkt-status-row { display: flex; gap: var(--space-2, 0.5rem); flex-wrap: wrap; justify-content: center; margin-top: var(--space-6, 1.5rem); }
  .mkt-logos { display: grid; grid-template-columns: repeat(6, 1fr); gap: var(--space-6, 1.5rem); align-items: center; opacity: var(--opacity-60, 0.6); }
  .mkt-logos div { aspect-ratio: 3/1; background: var(--color-text-tertiary); border-radius: var(--radius-sm, 0.25rem); }
  .mkt-features { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-6, 1.5rem); }
  .mkt-features .icon { width: 40px; height: 40px; border-radius: var(--radius-md, 0.5rem); background: color-mix(in srgb, var(--color-accent) 18%, transparent); display: grid; place-items: center; color: var(--color-accent); margin-bottom: var(--space-3, 0.75rem); font-weight: 700; }
  .mkt-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-6, 1.5rem); text-align: center; }
  .mkt-stats .num { font-family: var(--font-heading); font-size: var(--font-size-display, 3.815rem); font-weight: var(--font-weight-bold, 700); color: var(--color-accent); line-height: 1; }
  .mkt-stats .unit { font-family: var(--font-mono); font-size: var(--font-size-small, 0.875rem); color: var(--color-text-tertiary); }
  .mkt-quote { background: var(--color-surface); border-radius: var(--radius-card); padding: var(--space-12, 3rem); text-align: center; }
  .mkt-quote p { font-size: var(--font-size-h3, 1.953rem); font-style: italic; line-height: var(--line-height-snug, 1.4); margin: 0 0 var(--space-6, 1.5rem); }
  .mkt-quote .who { display: inline-flex; align-items: center; gap: var(--space-3, 0.75rem); }
  .mkt-pricing { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-6, 1.5rem); }
  .mkt-pricing .price { font-family: var(--font-heading); font-size: var(--font-size-h2, 2.441rem); font-weight: var(--font-weight-bold); margin: var(--space-3) 0; }
  .mkt-pricing ul { list-style: none; padding: 0; margin: var(--space-4, 1rem) 0; }
  .mkt-pricing li { padding: var(--space-2, 0.5rem) 0; display: flex; gap: var(--space-2, 0.5rem); align-items: center; }
  .mkt-pricing li::before { content: "✓"; color: var(--color-status-success, #16A34A); font-weight: 700; }
  .mkt-newsletter { display: grid; grid-template-columns: 1fr auto; gap: var(--space-3, 0.75rem); max-width: 480px; margin: 0 auto; }
  .mkt-newsletter-states { display: flex; gap: var(--space-2, 0.5rem); flex-wrap: wrap; justify-content: center; margin-top: var(--space-4, 1rem); }
  .mkt-footer { background: var(--color-surface); padding: var(--space-12, 3rem) var(--space-6, 1.5rem); }
  .mkt-footer .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-6, 1.5rem); max-width: 1200px; margin: 0 auto; }
  .mkt-footer h4 { font-size: var(--font-size-small, 0.875rem); text-transform: uppercase; letter-spacing: var(--letter-spacing-wide, 0.08em); color: var(--color-text-tertiary); margin: 0 0 var(--space-3, 0.75rem); }
  .mkt-footer ul { list-style: none; padding: 0; margin: 0; }
  .mkt-footer li { padding: var(--space-1, 0.25rem) 0; }
  .mkt-footer a { color: var(--color-text-secondary); text-decoration: none; }
  .mkt-footer a:hover { color: var(--color-link-hover, var(--color-link, var(--color-primary))); }
  .mkt-footer .fine { font-family: var(--font-mono); font-size: var(--font-size-caption, 0.64rem); color: var(--color-text-tertiary); margin-top: var(--space-8, 2rem); text-align: center; }

  @media (max-width: 768px) {
    .mkt-features, .mkt-stats, .mkt-pricing, .mkt-logos, .mkt-footer .grid { grid-template-columns: 1fr 1fr; }
    .mkt-hero h1 { font-size: var(--font-size-h1, 3rem); }
  }
</style>

<div class="mkt">

  <!-- 1. Top nav -->
  <nav style="border-bottom: 1px solid var(--color-border); padding: var(--space-3) var(--space-6); display: flex; align-items: center; gap: var(--space-6); background: var(--color-bg);">
    <strong style="font-family: var(--font-heading);">{{BRAND_NAME}}</strong>
    <a href="#" style="color: var(--color-text-primary); text-decoration: none;">Product</a>
    <a href="#" style="color: var(--color-primary); text-decoration: none; font-weight: 600;">Pricing</a>
    <a href="#" style="color: var(--color-text-primary); text-decoration: none;">Docs</a>
    <a href="#" style="color: var(--color-text-secondary); text-decoration: none; margin-left: auto; font-size: var(--font-size-small);">Sign in</a>
    <button class="btn btn-primary btn-sm">Get started</button>
  </nav>

  <!-- 2. Hero -->
  <section class="mkt-hero">
    <span class="badge badge-accent">Beta launch</span>
    <h1>{{HERO_HEADLINE}}</h1>
    <p class="lead">{{HERO_TAGLINE}}</p>
    <div class="row" style="justify-content: center;">
      <button class="btn btn-primary">Start free</button>
      <button class="btn btn-ghost">See how it works →</button>
    </div>

    <!-- 3. Status banner row -->
    <div class="mkt-status-row">
      <div class="banner is-info"  style="min-width: 200px;"><strong>Info</strong>: We're live in beta <button class="dismiss" aria-label="Dismiss">×</button></div>
      <div class="banner is-success" style="min-width: 200px;"><strong>Success</strong>: Plan upgraded</div>
      <div class="banner is-warning" style="min-width: 200px;"><strong>Warning</strong>: Storage 80% full</div>
      <div class="banner is-error"   style="min-width: 200px;"><strong>Error</strong>: Sync failed</div>
    </div>
  </section>

  <!-- 4. Logo cloud -->
  <section>
    <p class="eyebrow" style="text-align: center; margin-bottom: var(--space-6);">Trusted by teams at</p>
    <div class="mkt-logos">
      <div></div><div></div><div></div><div></div><div></div><div></div>
    </div>
  </section>

  <!-- 5. Feature grid -->
  <section>
    <h2 style="text-align: center; font-size: var(--font-size-h2); margin: 0 0 var(--space-12);">Built for teams that ship</h2>
    <div class="mkt-features">
      <div class="card"><div class="icon">A</div><h3>Fast iteration</h3><p class="muted">Trigger redeploys without waiting on CI. Hot reload across the whole stack.</p><a href="#" style="color: var(--color-link, var(--color-primary)); text-decoration: none; font-weight: 600;">Learn more →</a></div>
      <div class="card"><div class="icon">B</div><h3>Type-safe everywhere</h3><p class="muted">End-to-end types from schema to UI. Catch breaking changes before they ship.</p><a href="#" style="color: var(--color-link, var(--color-primary)); text-decoration: none; font-weight: 600;">Learn more →</a></div>
      <div class="card"><div class="icon">C</div><h3>Zero-config preview</h3><p class="muted">Every PR gets a preview URL. Reviewers see real running code, not screenshots.</p><a href="#" style="color: var(--color-link, var(--color-primary)); text-decoration: none; font-weight: 600;">Learn more →</a></div>
      <div class="card"><div class="icon">D</div><h3>Audit-ready logs</h3><p class="muted">Structured event stream, retained 90 days, exportable to your warehouse.</p><a href="#" style="color: var(--color-link, var(--color-primary)); text-decoration: none; font-weight: 600;">Learn more →</a></div>
      <div class="card"><div class="icon">E</div><h3>Composable workflows</h3><p class="muted">Drop-in steps for the things every team rebuilds: queues, scheduling, retries.</p><a href="#" style="color: var(--color-link, var(--color-primary)); text-decoration: none; font-weight: 600;">Learn more →</a></div>
      <div class="card"><div class="icon">F</div><h3>SOC 2-aligned</h3><p class="muted">Granular roles, audit trail, encryption at rest and in flight. SSO included.</p><a href="#" style="color: var(--color-link, var(--color-primary)); text-decoration: none; font-weight: 600;">Learn more →</a></div>
    </div>
  </section>

  <!-- 6. Stats strip -->
  <section>
    <div class="mkt-stats">
      <div><div class="num">10×</div><div class="unit">faster deploys</div></div>
      <div><div class="num">1.2M</div><div class="unit">events/day</div></div>
      <div><div class="num">98%</div><div class="unit">uptime SLA</div></div>
      <div><div class="num">&lt;5ms</div><div class="unit">p99 latency</div></div>
    </div>
  </section>

  <!-- 7. Testimonial -->
  <section>
    <div class="mkt-quote">
      <p>"We replaced three internal tools with this in a quarter. The team gets back two days a week."</p>
      <div class="who">
        <div class="avatar avatar-lg">JD</div>
        <div style="text-align: left;">
          <div style="font-weight: 600;">Jamie Dawson</div>
          <div class="muted" style="font-size: var(--font-size-small);">Head of Platform, Acme</div>
        </div>
      </div>
    </div>
  </section>

  <!-- 8. Pricing -->
  <section>
    <h2 style="text-align: center; font-size: var(--font-size-h2); margin: 0 0 var(--space-12);">Pricing that grows with you</h2>
    <div class="mkt-pricing">
      <div class="card">
        <span class="badge">Starter</span>
        <div class="price">$0<span style="font-size: var(--font-size-body); color: var(--color-text-tertiary); font-weight: 400;">/mo</span></div>
        <ul><li>Up to 3 projects</li><li>10k events/day</li><li>Community support</li><li>7-day log retention</li></ul>
        <button class="btn btn-secondary" style="width: 100%;">Start free</button>
      </div>
      <div class="card card-highlight">
        <span class="badge badge-accent">Most popular</span>
        <div class="price">$29<span style="font-size: var(--font-size-body); color: var(--color-text-tertiary); font-weight: 400;">/mo</span></div>
        <ul><li>Unlimited projects</li><li>1M events/day</li><li>Priority support</li><li>30-day log retention</li><li>Custom domains</li></ul>
        <button class="btn btn-primary" style="width: 100%;">Start trial</button>
      </div>
      <div class="card">
        <span class="badge">Enterprise</span>
        <div class="price">Custom</div>
        <ul><li>SLA + DPA</li><li>SSO / SAML</li><li>Dedicated support</li><li>Audit log export</li><li>On-prem option</li></ul>
        <button class="btn btn-secondary" style="width: 100%;">Talk to sales</button>
      </div>
    </div>
  </section>

  <!-- 9. FAQ accordion -->
  <section style="max-width: 720px;">
    <h2 style="text-align: center; font-size: var(--font-size-h2); margin: 0 0 var(--space-8);">Questions, briefly</h2>
    <div class="accordion">
      <details open><summary>How fast does it deploy?</summary><p>Median deploy is under 30 seconds for a typical project. CI integration is optional.</p></details>
      <details><summary>Can I bring my own domain?</summary><p>Yes — Pro and Enterprise tiers include unlimited custom domains with auto-issued TLS.</p></details>
      <details><summary>What's the data retention policy?</summary><p>Logs retained per your tier. Source data is yours; we never sell or share it.</p></details>
      <details><summary>Do you offer student discounts?</summary><p>Yes — verified students get the Pro tier free for two years. Reach out via support.</p></details>
      <details><summary>How do I cancel?</summary><p>Self-serve from billing. Annual plans are pro-rated; monthly cancels at end of cycle.</p></details>
    </div>
  </section>

  <!-- 10. Newsletter signup with state cycle -->
  <section style="max-width: 640px;">
    <h2 style="text-align: center; font-size: var(--font-size-h3); margin: 0 0 var(--space-6);">Get the monthly changelog</h2>
    <form class="mkt-newsletter" onsubmit="event.preventDefault();">
      <input class="input" type="email" placeholder="you@team.com" />
      <button class="btn btn-primary" type="submit">Subscribe</button>
    </form>
    <div class="mkt-newsletter-states">
      <div><span class="eyebrow">Default</span> <input class="input" placeholder="default" style="margin-top: 4px;" /></div>
      <div><span class="eyebrow">Focus</span>   <input class="input" autofocus placeholder="focus state" style="margin-top: 4px;" /></div>
      <div><span class="eyebrow">Success</span> <input class="input is-success" value="ok@team.com" style="margin-top: 4px;" /><div class="helper is-success">Check inbox</div></div>
      <div><span class="eyebrow">Error</span>   <input class="input is-error"   value="not-an-email" style="margin-top: 4px;" /><div class="helper is-error">Invalid email</div></div>
    </div>
  </section>

  <!-- 11. Footer -->
  <footer class="mkt-footer">
    <div class="grid">
      <div><h4>Product</h4><ul><li><a href="#">Features</a></li><li><a href="#">Pricing</a></li><li><a href="#">Changelog</a></li><li><a href="#">Roadmap</a></li></ul></div>
      <div><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Blog</a></li><li><a href="#">Careers</a></li><li><a href="#">Contact</a></li></ul></div>
      <div><h4>Resources</h4><ul><li><a href="#">Docs</a></li><li><a href="#">API</a></li><li><a href="#">Status</a></li><li><a href="#">Community</a></li></ul></div>
      <div><h4>Legal</h4><ul><li><a href="#">Privacy</a></li><li><a href="#">Terms</a></li><li><a href="#">Security</a></li><li><a href="#" onclick="document.getElementById('mkt-modal').style.display='block'; return false;">See modal</a></li></ul></div>
    </div>
    <div class="fine">© {{BRAND_NAME}} 2026 · v0.1.0</div>
  </footer>

  <!-- 12. Toast (auto-shown) -->
  <div class="toast-stack" id="mkt-toasts">
    <div class="toast is-success"><strong>Welcome!</strong> Your tour is ready.</div>
  </div>

  <!-- 13. Modal (hidden by default) -->
  <div id="mkt-modal" style="display: none;">
    <div class="modal-backdrop" onclick="document.getElementById('mkt-modal').style.display='none';"></div>
    <div class="modal">
      <h2>Confirm action</h2>
      <p class="muted">This will reset all preferences for the current workspace. You can't undo this.</p>
      <div class="row-end" style="margin-top: var(--space-6);">
        <button class="btn btn-ghost" onclick="document.getElementById('mkt-modal').style.display='none';">Cancel</button>
        <button class="btn btn-danger" onclick="document.getElementById('mkt-modal').style.display='none';">Reset</button>
      </div>
    </div>
  </div>

</div>
""".strip()


# ─── App surface markup ────────────────────────────────────────────────────────
APP_BODY_HTML = """
<style>
  .app { display: grid; grid-template-columns: 220px 1fr; height: 100%; min-height: 720px; font-family: var(--font-body); color: var(--color-text-primary); background: var(--color-bg); }
  @media (max-width: 768px) { .app { grid-template-columns: 60px 1fr; } .app .nav-label { display: none; } }
  .app-side { background: var(--color-surface); border-right: 1px solid var(--color-border); padding: var(--space-4) var(--space-3); display: flex; flex-direction: column; gap: var(--space-1); }
  .app-side .logo { font-family: var(--font-heading); font-weight: 700; padding: var(--space-2) var(--space-3); margin-bottom: var(--space-4); }
  .app-side a {
    display: flex; align-items: center; gap: var(--space-3);
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-md);
    color: var(--color-text-secondary);
    text-decoration: none;
    font-size: var(--font-size-small);
  }
  .app-side a:hover { background: var(--color-bg); }
  .app-side a.active { background: color-mix(in srgb, var(--color-primary) 12%, transparent); color: var(--color-primary); border-left: 3px solid var(--color-primary); padding-left: calc(var(--space-3) - 3px); }
  .app-side a[aria-disabled="true"] { opacity: var(--opacity-disabled, 0.4); pointer-events: none; }
  .app-side .indent { padding-left: var(--space-8); font-size: var(--font-size-caption); }

  .app-main { display: flex; flex-direction: column; min-width: 0; }
  .app-topbar { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3) var(--space-6); border-bottom: 1px solid var(--color-border); background: var(--color-surface); }
  .app-search { flex: 1; max-width: 460px; position: relative; }
  .app-search .input { padding-right: 60px; }
  .app-search .kbd { position: absolute; right: var(--space-2); top: 50%; transform: translateY(-50%); }
  .app-bell { position: relative; padding: var(--space-2); cursor: pointer; }
  .app-bell .badge-dot { position: absolute; top: 4px; right: 4px; width: 8px; height: 8px; background: var(--color-status-error, #DC2626); border-radius: 50%; }

  .app-page { flex: 1; padding: var(--space-6); overflow: auto; }
  .breadcrumbs { display: flex; gap: var(--space-2); color: var(--color-text-tertiary); font-size: var(--font-size-small); margin-bottom: var(--space-2); }
  .breadcrumbs a { color: inherit; text-decoration: none; }
  .breadcrumbs span::before { content: "/"; margin-right: var(--space-2); }
  .page-header { display: flex; align-items: end; gap: var(--space-3); margin-bottom: var(--space-6); }
  .page-header h1 { font-family: var(--font-heading); font-size: var(--font-size-h2); margin: 0; flex: 1; }
  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); margin-bottom: var(--space-6); }
  @media (max-width: 768px) { .kpi-row { grid-template-columns: 1fr 1fr; } }
  .kpi-row .card { padding: var(--space-4); }
  .kpi-row .label { font-size: var(--font-size-caption); text-transform: uppercase; letter-spacing: var(--letter-spacing-wide); color: var(--color-text-tertiary); }
  .kpi-row .num { font-family: var(--font-heading); font-size: var(--font-size-h2); font-weight: 700; margin: var(--space-1) 0; }
  .kpi-row .delta-up   { color: var(--color-status-success, #16A34A); font-size: var(--font-size-small); }
  .kpi-row .delta-down { color: var(--color-status-error,   #DC2626); font-size: var(--font-size-small); }

  .app-tabs { margin-bottom: var(--space-4); }

  .empty, .loading, .error-state { padding: var(--space-12); text-align: center; }
  .empty .illustration { width: 80px; height: 80px; background: color-mix(in srgb, var(--color-accent) 18%, transparent); border-radius: var(--radius-card); margin: 0 auto var(--space-3); }
  .skeleton { background: color-mix(in srgb, var(--color-text-tertiary) 18%, transparent); border-radius: var(--radius-sm); height: 14px; margin-bottom: var(--space-2); animation: pulse 1.4s var(--ease-ease-in-out, ease-in-out) infinite; }
  .skeleton.short { width: 40%; }
  .skeleton.med   { width: 65%; }
  @keyframes pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
  .spinner { width: 28px; height: 28px; border: 3px solid var(--color-border); border-top-color: var(--color-primary); border-radius: 50%; animation: spin var(--duration-slow, 500ms) linear infinite; margin: 0 auto; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .form-panel { background: var(--color-surface); border-left: 1px solid var(--color-border); padding: var(--space-6); width: 360px; max-width: 100%; }
  .kbd { display: inline-block; font-family: var(--font-mono); font-size: var(--font-size-caption); padding: 2px var(--space-2); border: 1px solid var(--color-border-strong); background: var(--color-bg); border-radius: var(--radius-sm); color: var(--color-text-secondary); }
</style>

<div class="app">

  <!-- Side nav -->
  <aside class="app-side">
    <div class="logo">{{BRAND_NAME}}</div>
    <a href="#" class="active">📊 <span class="nav-label">Dashboard</span></a>
    <a href="#">📁 <span class="nav-label">Projects</span></a>
    <a href="#" class="indent"><span class="nav-label">Active</span></a>
    <a href="#" class="indent"><span class="nav-label">Archived</span></a>
    <a href="#">👥 <span class="nav-label">Team</span></a>
    <a href="#">⚙️ <span class="nav-label">Settings</span></a>
    <a href="#" aria-disabled="true">🚧 <span class="nav-label">Beta features</span></a>
  </aside>

  <!-- Main column -->
  <div class="app-main">

    <!-- Top bar -->
    <header class="app-topbar">
      <div class="app-search">
        <input class="input" placeholder="Search projects, members, files…" />
        <span class="kbd">⌘K</span>
      </div>
      <button class="app-bell" aria-label="Notifications">🔔<span class="badge-dot"></span></button>
      <div class="avatar" title="You">JD</div>
    </header>

    <!-- Page content -->
    <div class="app-page">
      <div class="breadcrumbs"><a href="#">Workspace</a><span><a href="#">Acme Inc.</a></span><span>Dashboard</span></div>
      <div class="page-header">
        <h1>Dashboard</h1>
        <button class="btn btn-secondary btn-sm">Export</button>
        <button class="btn btn-primary btn-sm">New project</button>
      </div>

      <!-- Tab strip -->
      <nav class="tabs app-tabs">
        <button class="active">Overview</button>
        <button>Activity</button>
        <button>Insights</button>
        <button>Settings</button>
      </nav>

      <!-- KPI cards -->
      <div class="kpi-row">
        <div class="card"><div class="label">Active users</div><div class="num">12,480</div><div class="delta-up">↑ 4.2% vs last week</div><svg class="sparkline" viewBox="0 0 80 20"><polyline fill="none" stroke="currentColor" stroke-width="1.5" points="0,15 10,12 20,14 30,9 40,11 50,7 60,8 70,4 80,2" style="color: var(--color-accent);"/></svg></div>
        <div class="card"><div class="label">Revenue</div>     <div class="num">$48.2k</div><div class="delta-up">↑ 12% MoM</div>      <svg class="sparkline" viewBox="0 0 80 20"><polyline fill="none" stroke="currentColor" stroke-width="1.5" points="0,18 10,16 20,15 30,12 40,13 50,10 60,9 70,5 80,3"  style="color: var(--color-status-success, #16A34A);"/></svg></div>
        <div class="card"><div class="label">Churn</div>       <div class="num">2.1%</div>  <div class="delta-down">↓ 0.4 pp</div>     <svg class="sparkline" viewBox="0 0 80 20"><polyline fill="none" stroke="currentColor" stroke-width="1.5" points="0,4 10,6 20,5 30,8 40,7 50,9 60,11 70,12 80,14" style="color: var(--color-status-error,   #DC2626);"/></svg></div>
        <div class="card"><div class="label">p99 latency</div> <div class="num">4.8ms</div> <div class="delta-up">↓ 0.7ms</div>      <svg class="sparkline" viewBox="0 0 80 20"><polyline fill="none" stroke="currentColor" stroke-width="1.5" points="0,8 10,9 20,10 30,7 40,8 50,6 60,7 70,5 80,4"  style="color: var(--color-primary);"/></svg></div>
      </div>

      <!-- Data table -->
      <div class="card" style="padding: 0; margin-bottom: var(--space-6);">
        <table class="table">
          <thead><tr><th>Project</th><th>Owner</th><th>Status</th><th>Updated</th><th></th></tr></thead>
          <tbody>
            <tr><td>website-redesign</td><td><div class="row"><div class="avatar">JD</div>Jamie</div></td><td><span class="badge badge-success">Active</span></td><td class="muted">2h ago</td><td class="row-actions"><button class="btn btn-ghost btn-sm">⋯</button></td></tr>
            <tr><td>billing-portal</td><td><div class="row"><div class="avatar">SM</div>Sam</div></td><td><span class="badge badge-warning">Review</span></td><td class="muted">5h ago</td><td class="row-actions"><button class="btn btn-ghost btn-sm">⋯</button></td></tr>
            <tr><td>onboarding-flow</td><td><div class="row"><div class="avatar">AR</div>Avery</div></td><td><span class="badge badge-info">Planned</span></td><td class="muted">1d ago</td><td class="row-actions"><button class="btn btn-ghost btn-sm">⋯</button></td></tr>
            <tr><td>analytics-dashboard</td><td><div class="row"><div class="avatar">RK</div>Riley</div></td><td><span class="badge badge-error">Blocked</span></td><td class="muted">3d ago</td><td class="row-actions"><button class="btn btn-ghost btn-sm">⋯</button></td></tr>
          </tbody>
        </table>
        <div class="row" style="padding: var(--space-3) var(--space-4); justify-content: space-between; border-top: 1px solid var(--color-border);">
          <span class="muted" style="font-size: var(--font-size-small);">Page 1 of 12</span>
          <div class="row"><button class="btn btn-ghost btn-sm">Prev</button><button class="btn btn-ghost btn-sm">Next</button></div>
        </div>
      </div>

      <!-- States row: empty / loading / error -->
      <div class="row" style="gap: var(--space-4); align-items: stretch;">
        <div class="card empty" style="flex: 1;">
          <div class="illustration"></div>
          <h3 style="margin: 0 0 var(--space-2);">No archived projects</h3>
          <p class="muted" style="margin: 0 0 var(--space-3);">When you archive a project, it'll appear here.</p>
          <button class="btn btn-primary btn-sm">Archive a project</button>
        </div>
        <div class="card loading" style="flex: 1;">
          <div class="spinner"></div>
          <p class="muted" style="margin: var(--space-3) 0 0;">Loading insights…</p>
          <div style="margin-top: var(--space-4); text-align: left;">
            <div class="skeleton"></div><div class="skeleton med"></div><div class="skeleton short"></div>
          </div>
        </div>
        <div class="card error-state" style="flex: 1;">
          <div class="banner is-error" style="margin-bottom: var(--space-3);"><strong>Sync failed</strong></div>
          <p class="muted" style="margin: 0 0 var(--space-3);">We couldn't reach the source. Retry, or contact support if this keeps happening.</p>
          <button class="btn btn-secondary btn-sm">Retry</button>
        </div>
      </div>

      <div class="divider"></div>

      <!-- Form panel inline (drawer-style) -->
      <div class="form-panel">
        <h3 style="margin: 0 0 var(--space-4);">New project</h3>
        <label class="field"><span>Name</span><input class="input" placeholder="e.g. growth-experiments" /></label>
        <label class="field"><span>Description</span><textarea class="textarea" rows="3" placeholder="One sentence is fine"></textarea></label>
        <label class="field"><span>Visibility</span>
          <select class="select"><option>Workspace only</option><option>Public</option><option>Restricted</option></select>
        </label>
        <label class="field"><span>Tags</span>
          <div class="row" style="flex-wrap: wrap; gap: var(--space-1);">
            <span class="chip">growth ×</span><span class="chip">q2 ×</span><span class="chip">+ add</span>
          </div>
        </label>
        <label class="checkbox"><input type="checkbox" checked /> Notify team on create</label><br><br>
        <div style="margin: var(--space-3) 0;">Severity:&nbsp;
          <label class="radio"><input type="radio" name="sev" /> Low</label>&nbsp;
          <label class="radio"><input type="radio" name="sev" checked /> Med</label>&nbsp;
          <label class="radio"><input type="radio" name="sev" /> High</label>
        </div>
        <label class="row"><span>Auto-archive after 90 days</span>
          <span class="switch"><input type="checkbox" checked /><span class="track"></span><span class="thumb"></span></span>
        </label>
        <div class="row-end" style="margin-top: var(--space-6);">
          <button class="btn btn-ghost">Cancel</button>
          <button class="btn btn-primary">Create</button>
        </div>
        <p class="helper" style="margin-top: var(--space-3);">Default state row above: <input class="input" disabled placeholder="disabled" /></p>
      </div>

      <!-- Tooltip + popover demos -->
      <div class="row" style="gap: var(--space-6); margin-top: var(--space-6);">
        <div class="tooltip-wrap"><button class="btn btn-secondary btn-sm">Hover me</button><span class="tooltip">Tooltip via brand motion</span></div>
        <div class="popover" style="display: inline-block;"><strong>Popover</strong><p class="muted" style="margin: var(--space-2) 0 0;">Higher elevation, lives above the page.</p></div>
      </div>

      <!-- Toast stack (in-surface, distinct from page-level) -->
      <div class="toast-stack" style="position: static; right: auto; bottom: auto; margin-top: var(--space-6);">
        <div class="toast is-success"><strong>Saved</strong> — preferences updated</div>
        <div class="toast is-info"><strong>Heads up</strong> — a teammate joined the workspace</div>
        <div class="toast is-error"><strong>Limit reached</strong> — upgrade to add more projects</div>
      </div>

      <!-- Settings variant (small inline section) -->
      <div class="divider"></div>
      <h2 style="font-family: var(--font-heading); font-size: var(--font-size-h3); margin: 0 0 var(--space-4);">Settings preview</h2>
      <div class="card stack">
        <div class="row" style="justify-content: space-between;"><span>API key</span><div class="row"><span class="mono" style="font-size: var(--font-size-small);">sk-••••••8e2c</span><button class="btn btn-ghost btn-sm">Copy</button></div></div>
        <div class="row" style="justify-content: space-between;"><span>Email</span><div class="row"><span class="muted">jamie@acme.com</span><button class="btn btn-ghost btn-sm">Edit</button></div></div>
        <div class="row" style="justify-content: space-between;"><span>Two-factor auth</span><span class="switch"><input type="checkbox" checked /><span class="track"></span><span class="thumb"></span></span></div>
      </div>

    </div>
  </div>
</div>
""".strip()


# ─── Slide surface markup ──────────────────────────────────────────────────────
SLIDE_BODY_HTML = """
<style>
  .deck { display: grid; grid-template-rows: 1fr 80px; height: 100%; min-height: 720px; background: var(--color-text-primary); padding: var(--space-6); gap: var(--space-4); }
  .slide-stage { background: var(--color-bg); border-radius: var(--radius-card); position: relative; overflow: hidden; aspect-ratio: 16 / 9; max-height: 100%; max-width: 1280px; margin: 0 auto; width: 100%; }
  .slide { position: absolute; inset: 0; padding: 8% 10%; display: none; flex-direction: column; justify-content: center; gap: var(--space-4); color: var(--color-text-primary); }
  .slide.active { display: flex; }
  .slide h1 { font-family: var(--font-heading); font-size: 5vw; line-height: var(--line-height-tight); margin: 0; letter-spacing: var(--letter-spacing-tight); }
  .slide h2 { font-family: var(--font-heading); font-size: 3.5vw; margin: 0; }
  .slide p  { font-size: 1.6vw; line-height: var(--line-height-snug); margin: 0; color: var(--color-text-secondary); }
  .slide ul { font-size: 1.6vw; line-height: var(--line-height-snug); margin: 0; padding-left: var(--space-6); color: var(--color-text-primary); }
  .slide-eyebrow { font-size: 1vw; text-transform: uppercase; letter-spacing: var(--letter-spacing-wide); color: var(--color-accent); font-weight: 700; }
  .slide-footer { position: absolute; bottom: var(--space-3); left: var(--space-6); right: var(--space-6); display: flex; justify-content: space-between; font-family: var(--font-mono); font-size: 0.8vw; color: var(--color-text-tertiary); }

  .slide-section-num { font-family: var(--font-heading); font-size: 14vw; line-height: 1; color: var(--color-accent); font-weight: 700; }
  .slide-stat-num { font-family: var(--font-heading); font-size: 16vw; line-height: 1; color: var(--color-primary); font-weight: 700; }
  .slide-stat-unit { font-family: var(--font-mono); font-size: 1.6vw; color: var(--color-text-tertiary); margin-top: var(--space-3); }

  .slide-quote { font-style: italic; }
  .slide-quote::before { content: "\\201C"; font-size: 12vw; line-height: 0.6; color: var(--color-accent); display: block; margin-bottom: var(--space-3); }

  .slide-cols { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-8); height: 100%; align-items: stretch; }
  .slide-cols > div { padding: var(--space-6); border-radius: var(--radius-card); background: var(--color-surface); display: flex; flex-direction: column; gap: var(--space-3); }
  .slide-cols .check::before { content: "\\2713 "; color: var(--color-status-success, #16A34A); font-weight: 700; }
  .slide-cols .x::before     { content: "\\2717 "; color: var(--color-status-error,   #DC2626); font-weight: 700; }

  .slide-img { background: color-mix(in srgb, var(--color-accent) 25%, var(--color-surface)); border-radius: var(--radius-card); flex: 1; }
  .slide-caption { font-size: 1.1vw; color: var(--color-text-tertiary); }

  .slide-bars { display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--space-3); align-items: end; height: 60%; }
  .slide-bars > div { background: var(--color-primary); border-radius: var(--radius-sm); }
  .slide-bars > div:nth-child(1) { background: var(--color-brand-300, var(--color-primary)); height: 30%; }
  .slide-bars > div:nth-child(2) { background: var(--color-brand-500, var(--color-primary)); height: 55%; }
  .slide-bars > div:nth-child(3) { background: var(--color-brand-700, var(--color-primary)); height: 80%; }
  .slide-bars > div:nth-child(4) { background: var(--color-accent); height: 95%; }
  .slide-bars > div:nth-child(5) { background: var(--color-brand-600, var(--color-primary)); height: 70%; }

  .slide-logo-grid { display: grid; grid-template-columns: 1fr 1fr; height: 100%; align-items: center; gap: var(--space-6); }
  .slide-logo-grid > div { padding: var(--space-12); display: grid; place-items: center; border-radius: var(--radius-card); }
  .slide-logo-grid .light { background: var(--color-bg); color: var(--color-text-primary); }
  .slide-logo-grid .dark  { background: var(--color-text-primary); color: var(--color-text-inverse); }

  .thumbs { display: flex; gap: var(--space-2); justify-content: center; align-items: center; padding: 0 var(--space-4); overflow-x: auto; }
  .thumbs button { appearance: none; border: 1px solid transparent; background: var(--color-surface); border-radius: var(--radius-sm); width: 56px; height: 32px; cursor: pointer; flex-shrink: 0; font: inherit; font-size: var(--font-size-caption); color: var(--color-text-tertiary); }
  .thumbs button.active { border-color: var(--color-accent); color: var(--color-accent); }
</style>

<div class="deck" data-deck>

  <div class="slide-stage" data-stage>
    <div class="slide active" data-slide="1">
      <span class="slide-eyebrow">{{BRAND_NAME}}</span>
      <h1>The fastest path from idea to ship.</h1>
      <p>Jamie Dawson · 2026 · Brand kit demo deck</p>
      <div class="slide-footer"><span>1 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>

    <div class="slide" data-slide="2">
      <div class="row" style="align-items: end; gap: var(--space-8);">
        <div class="slide-section-num">01</div>
        <h2 style="margin-bottom: 1.5vw;">Why teams choose us</h2>
      </div>
      <div class="slide-footer"><span>2 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>

    <div class="slide" data-slide="3">
      <span class="slide-eyebrow">Three things</span>
      <h2>What changes when you adopt this</h2>
      <ul>
        <li>Deploys go from minutes to seconds</li>
        <li>Reviewers see real running code, not screenshots</li>
        <li>Audit trails come for free, not as a sprint at the end</li>
      </ul>
      <div class="slide-footer"><span>3 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>

    <div class="slide" data-slide="4">
      <h2>Before / after</h2>
      <div class="slide-cols">
        <div>
          <h3 style="margin: 0;">Before</h3>
          <p class="x">Ship blocked on CI flakiness</p>
          <p class="x">Reviewers download screenshots</p>
          <p class="x">Audit logs reconstructed quarterly</p>
        </div>
        <div>
          <h3 style="margin: 0;">After</h3>
          <p class="check">Deploys finish in &lt;30s</p>
          <p class="check">Each PR has a live preview URL</p>
          <p class="check">Audit log streams to your warehouse</p>
        </div>
      </div>
      <div class="slide-footer"><span>4 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>

    <div class="slide" data-slide="5" style="text-align: center; align-items: center;">
      <span class="slide-eyebrow">Real numbers</span>
      <div class="slide-stat-num">10×</div>
      <div class="slide-stat-unit">faster median deploy</div>
      <p style="max-width: 60%;">Across 240 teams running over the last twelve months.</p>
      <div class="slide-footer"><span>5 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>

    <div class="slide" data-slide="6">
      <p class="slide-quote">We replaced three internal tools with this in a quarter. The team gets back two days a week.</p>
      <p style="font-style: normal; margin-top: var(--space-4);">— Jamie Dawson, Head of Platform, Acme</p>
      <div class="slide-footer"><span>6 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>

    <div class="slide" data-slide="7">
      <h2>Architecture at a glance</h2>
      <div class="slide-img"></div>
      <p class="slide-caption">Diagram placeholder — drop a real image in production.</p>
      <div class="slide-footer"><span>7 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>

    <div class="slide" data-slide="8">
      <h2>Adoption curve</h2>
      <div class="slide-bars" style="margin-top: var(--space-4);"><div></div><div></div><div></div><div></div><div></div></div>
      <p class="slide-caption" style="margin-top: var(--space-3);">Quarterly active workspaces — Q1 to Q5.</p>
      <div class="slide-footer"><span>8 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>

    <div class="slide" data-slide="9">
      <h2 style="margin-bottom: var(--space-4);">Wordmark — light + inverse</h2>
      <div class="slide-logo-grid">
        <div class="light"><strong style="font-family: var(--font-heading); font-size: 4vw;">{{BRAND_NAME}}</strong></div>
        <div class="dark"><strong style="font-family: var(--font-heading); font-size: 4vw;">{{BRAND_NAME}}</strong></div>
      </div>
      <div class="slide-footer"><span>9 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>

    <div class="slide" data-slide="10" style="text-align: center; align-items: center;">
      <h1>Thank you.</h1>
      <p style="font-size: 2vw;">jamie@acme.com · acme.example</p>
      <div style="width: 120px; height: 120px; background: var(--color-text-primary); border-radius: var(--radius-sm); margin-top: var(--space-4);"></div>
      <div class="slide-footer"><span>10 / 10</span><span>{{BRAND_NAME}}</span></div>
    </div>
  </div>

  <div class="thumbs" data-thumbs>
    <button data-thumb="1" class="active">1</button>
    <button data-thumb="2">2</button>
    <button data-thumb="3">3</button>
    <button data-thumb="4">4</button>
    <button data-thumb="5">5</button>
    <button data-thumb="6">6</button>
    <button data-thumb="7">7</button>
    <button data-thumb="8">8</button>
    <button data-thumb="9">9</button>
    <button data-thumb="10">10</button>
  </div>
</div>
""".strip()


def _yaml_or_none(p: Path) -> dict | None:
    if not p.exists():
        return None
    try:
        return yaml.safe_load(p.read_text())
    except yaml.YAMLError:
        return None


def emit_css_vars(look: dict, *, indent: str = "  ") -> str:
    """Flatten Look.tokens into CSS custom properties.

    Convention:
      primitive.color.scales.brand.500   → --color-brand-500
      primitive.color.palette.primary    → --color-primary
      primitive.color.anchors.{name}     → --color-anchor-{name}
      primitive.typography.fontFamily.X  → --font-X
      primitive.typography.fontSize.X    → --font-size-X
      primitive.typography.fontWeight.X  → --font-weight-X
      primitive.space.X                  → --space-X (calc with --density)
      primitive.radius.X                 → --radius-X
      primitive.shadow.X                 → --shadow-X
      primitive.borderWidth.X            → --border-width-X
      primitive.opacity.X                → --opacity-X
      primitive.zIndex.X                 → --z-X
      primitive.breakpoint.X             → --bp-X
      primitive.motion.easing.X          → --ease-X
      primitive.motion.duration.X        → --duration-X
      semantic.{light|dark}.color.X      → --color-X (mode applied via [data-mode])
      semantic.status.X                  → --color-status-X
      semantic.elevation.X               → --elevation-X
      semantic.opacity.X                 → --opacity-{name}
    """
    lines: list[str] = []
    tokens = look.get("tokens", {})
    primitive = tokens.get("primitive", {})

    color = primitive.get("color", {})
    for fam, steps in color.get("scales", {}).items():
        if isinstance(steps, dict):
            for step, val in steps.items():
                if isinstance(val, (str, int, float)):
                    lines.append(f"{indent}--color-{fam}-{step}: {val};")
    for role, val in color.get("palette", {}).items():
        if isinstance(val, (str, int, float)):
            lines.append(f"{indent}--color-{role}: {val};")
    for name, val in color.get("anchors", {}).items():
        if name.startswith("__"):
            continue
        if isinstance(val, (str, int, float)):
            lines.append(f"{indent}--color-anchor-{name}: {val};")

    typo = primitive.get("typography", {})
    for role, chain in typo.get("fontFamily", {}).items():
        if isinstance(chain, list):
            value = ", ".join(f'"{f}"' if " " in f else f for f in chain)
        else:
            value = chain
        lines.append(f"{indent}--font-{role}: {value};")
    for label, val in typo.get("fontSize", {}).items():
        lines.append(f"{indent}--font-size-{label}: {val};")
    for label, val in typo.get("fontWeight", {}).items():
        lines.append(f"{indent}--font-weight-{label}: {val};")
    for label, val in typo.get("letterSpacing", {}).items():
        lines.append(f"{indent}--letter-spacing-{label}: {val};")
    for label, val in typo.get("lineHeight", {}).items():
        lines.append(f"{indent}--line-height-{label}: {val};")
    for label, val in typo.get("scale", {}).items():
        lines.append(f"{indent}--scale-{label}: {val};")

    # Density is applied as a runtime multiplier on every space step. Emitting
    # calc(val * var(--density, 1)) here means the JS density handler only has
    # to write `--density: <multiplier>` once per change instead of rewriting
    # every --space-* value. Mirrors playground's lookToCss.ts emitSpaceWithDensity.
    lines.append(f"{indent}--density: 1;")
    for step, val in primitive.get("space", {}).items():
        lines.append(f"{indent}--space-{step}: calc({val} * var(--density, 1));")
    for step, val in primitive.get("radius", {}).items():
        lines.append(f"{indent}--radius-{step}: {val};")
    for step, val in primitive.get("shadow", {}).items():
        lines.append(f"{indent}--shadow-{step}: {val};")
    for label, val in primitive.get("borderWidth", {}).items():
        lines.append(f"{indent}--border-width-{label}: {val};")
    for step, val in primitive.get("opacity", {}).items():
        lines.append(f"{indent}--opacity-{step}: {val};")
    for label, val in primitive.get("zIndex", {}).items():
        lines.append(f"{indent}--z-{label}: {val};")
    for label, val in primitive.get("breakpoint", {}).items():
        lines.append(f"{indent}--bp-{label}: {val};")

    motion = primitive.get("motion", {})
    for label, val in motion.get("easing", {}).items():
        lines.append(f"{indent}--ease-{label}: {val};")
    for label, val in motion.get("duration", {}).items():
        lines.append(f"{indent}--duration-{label}: {val};")

    semantic = tokens.get("semantic", {})
    # Light mode is the default scope; dark goes under [data-mode="dark"] (handled in CSS, not here).
    for role, val in semantic.get("light", {}).get("color", {}).items():
        if isinstance(val, (str, int, float)):
            lines.append(f"{indent}--color-{role}: {val};")
    for role, val in semantic.get("status", {}).items():
        if isinstance(role, str) and role.startswith("$"):
            continue
        if isinstance(val, (str, int, float)):
            lines.append(f"{indent}--color-status-{role}: {val};")

    return "\n".join(lines) if lines else f"{indent}/* no tokens emitted — Look had no primitive/semantic data */"


def build_glossary_html(look: dict) -> str:
    """Walk the Look's tokens and emit one live-render entry per token.

    Each entry: rendered component (using brand tokens), token name, plain-language
    caption, current value, plugin token path. Grouped by primitive → semantic →
    status → motion → component → extensions.
    """
    parts: list[str] = []
    parts.append('<style>')
    parts.append('.gloss { padding: var(--space-6); max-width: 1100px; margin: 0 auto; font-family: var(--font-body); color: var(--color-text-primary); background: var(--color-bg); }')
    parts.append('.gloss-section { margin-bottom: var(--space-12); }')
    parts.append('.gloss-section h2 { font-family: var(--font-heading); font-size: var(--font-size-h2); margin: 0 0 var(--space-2); border-bottom: 2px solid var(--color-primary); padding-bottom: var(--space-2); }')
    parts.append('.gloss-section h3 { font-family: var(--font-heading); font-size: var(--font-size-h4); margin: var(--space-6) 0 var(--space-3); }')
    parts.append('.gloss-entry { display: grid; grid-template-columns: 220px 1fr; gap: var(--space-6); padding: var(--space-4) 0; border-bottom: 1px solid var(--color-border); align-items: start; }')
    parts.append('.gloss-entry .render { display: flex; align-items: center; justify-content: center; min-height: 56px; }')
    parts.append('.gloss-entry .meta .name { font-weight: var(--font-weight-semibold); font-family: var(--font-mono); font-size: var(--font-size-small); }')
    parts.append('.gloss-entry .meta .caption { color: var(--color-text-secondary); font-size: var(--font-size-small); margin: var(--space-1) 0; }')
    parts.append('.gloss-entry .meta .value { font-family: var(--font-mono); font-size: var(--font-size-caption); color: var(--color-text-tertiary); }')
    parts.append('.gloss-strip { display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; height: 56px; border-radius: var(--radius-sm); overflow: hidden; }')
    parts.append('.gloss-strip > div { display: grid; place-items: end; padding: 4px; font-family: var(--font-mono); font-size: 10px; }')
    parts.append('.gloss-tile { width: 56px; height: 56px; border-radius: var(--radius-md); border: 1px solid var(--color-border); }')
    parts.append('.gloss-shadow-tile { width: 80px; height: 56px; background: var(--color-surface); border-radius: var(--radius-md); }')
    parts.append('.gloss-typescale > * { display: block; line-height: 1; margin: 4px 0; font-family: var(--font-heading); }')
    parts.append('.gloss-spacing { display: flex; gap: 0; align-items: center; }')
    parts.append('.gloss-spacing > div { background: var(--color-primary); height: 24px; }')
    parts.append('.gloss-zstack { position: relative; height: 80px; }')
    parts.append('.gloss-zstack > div { position: absolute; padding: var(--space-1) var(--space-2); border-radius: var(--radius-sm); font-size: var(--font-size-caption); font-family: var(--font-mono); background: var(--color-surface); border: 1px solid var(--color-border); box-shadow: var(--shadow-sm); }')
    parts.append('</style>')

    parts.append('<div class="gloss">')
    parts.append(f'<h1 style="font-family: var(--font-heading); font-size: var(--font-size-h1);">Glossary — {look.get("name", "Brand")} tokens in context</h1>')
    parts.append('<p class="muted">Every Look-tunable token rendered as the actual UI element it controls. Compare-mode renders each entry twice for direct diff.</p>')

    tokens = look.get("tokens", {})
    primitive = tokens.get("primitive", {})
    semantic  = tokens.get("semantic", {})

    # ── PRIMITIVE — Color ────────────────────────────────────────────────────
    parts.append('<div class="gloss-section"><h2>Primitive — Color</h2>')
    color = primitive.get("color", {})

    parts.append('<h3>Palette (named role colors)</h3>')
    for role, val in (color.get("palette") or {}).items():
        if not isinstance(val, (str, int, float)):
            continue
        parts.append(_gloss_entry(
            render=f'<div class="gloss-tile" style="background: {val};"></div>',
            name=f"--color-{role}",
            caption=f"Named role color — {role}.",
            value=str(val),
        ))

    for fam_name, scale in (color.get("scales") or {}).items():
        parts.append(f'<h3>Scale — {fam_name}</h3>')
        if isinstance(scale, dict):
            steps = [(k, v) for k, v in scale.items() if not str(k).startswith("_") and isinstance(v, (str, int, float))]
            def _fg_for(step_key: str) -> str:
                try:
                    return "#FFF" if int(step_key) >= 500 else "#000"
                except (ValueError, TypeError):
                    return "#000"
            strip = '<div class="gloss-strip">' + "".join(
                f'<div style="background: {v}; color: {_fg_for(str(k))};">{k}</div>'
                for k, v in steps
            ) + '</div>'
            parts.append(_gloss_entry(
                render=strip,
                name=f"--color-{fam_name}-50…900",
                caption=f"10-step ramp for the {fam_name} family.",
                value=f"{len(steps)} steps",
            ))

    anchors = (color.get("anchors") or {})
    real_anchors = {k: v for k, v in anchors.items() if not str(k).startswith("_") and v}
    if real_anchors:
        parts.append('<h3>Anchors (named hexes)</h3>')
        for name, val in real_anchors.items():
            if not isinstance(val, (str, int, float)):
                continue
            parts.append(_gloss_entry(
                render=f'<div class="gloss-tile" style="background: {val};"></div>',
                name=f"--color-anchor-{name}",
                caption=f"Anchor hex — {name}.",
                value=str(val),
            ))
    parts.append('</div>')

    # ── PRIMITIVE — Typography ───────────────────────────────────────────────
    parts.append('<div class="gloss-section"><h2>Primitive — Typography</h2>')
    typo = primitive.get("typography", {})
    for role in ("heading", "body", "mono"):
        family = (typo.get("fontFamily") or {}).get(role)
        if family:
            chain = ", ".join(family) if isinstance(family, list) else str(family)
            parts.append(_gloss_entry(
                render=f'<span style="font-family: var(--font-{role}); font-size: var(--font-size-h3);">The quick brown fox</span>',
                name=f"--font-{role}",
                caption=f"Font family fallback chain for {role}.",
                value=chain,
            ))
    sizes = typo.get("fontSize") or {}
    if sizes:
        ladder = '<div class="gloss-typescale">' + "".join(
            f'<span style="font-size: var(--font-size-{k});">{k}</span>' for k in sizes
        ) + '</div>'
        parts.append(_gloss_entry(
            render=ladder,
            name="--font-size-{step}",
            caption="Modular size scale — extreme top to extreme bottom.",
            value=f"{len(sizes)} steps",
        ))
    weights = typo.get("fontWeight") or {}
    if weights:
        ladder = "".join(
            f'<span style="font-weight: var(--font-weight-{k}); font-size: var(--font-size-lead); display: block;">{k}</span>' for k in weights
        )
        parts.append(_gloss_entry(
            render=ladder,
            name="--font-weight-{label}",
            caption="Weight scale — same word at every supported weight.",
            value=", ".join(str(v) for v in weights.values()),
        ))
    parts.append('</div>')

    # ── PRIMITIVE — Form (space, radius, shadow, opacity, zIndex, breakpoint)
    parts.append('<div class="gloss-section"><h2>Primitive — Form</h2>')

    space = primitive.get("space") or {}
    if space:
        parts.append('<h3>Spacing scale</h3>')
        for step, val in space.items():
            parts.append(_gloss_entry(
                render=f'<div class="gloss-spacing"><div style="width: var(--space-{step});"></div></div>',
                name=f"--space-{step}",
                caption=f"Space step {step}.",
                value=str(val),
            ))

    radius = primitive.get("radius") or {}
    if radius:
        parts.append('<h3>Radius scale</h3>')
        for label, val in radius.items():
            parts.append(_gloss_entry(
                render=f'<div class="gloss-tile" style="background: var(--color-primary); border-radius: var(--radius-{label});"></div>',
                name=f"--radius-{label}",
                caption=f"Corner radius — {label}.",
                value=str(val),
            ))

    shadow = primitive.get("shadow") or {}
    if shadow:
        parts.append('<h3>Shadow scale</h3>')
        for label, val in shadow.items():
            parts.append(_gloss_entry(
                render=f'<div class="gloss-shadow-tile" style="box-shadow: var(--shadow-{label});"></div>',
                name=f"--shadow-{label}",
                caption=f"Elevation — {label}.",
                value=str(val)[:80],
            ))

    opacity = primitive.get("opacity") or {}
    if opacity:
        parts.append('<h3>Opacity scale</h3>')
        for step, val in opacity.items():
            parts.append(_gloss_entry(
                render=f'<div class="gloss-tile" style="background: var(--color-text-primary); opacity: var(--opacity-{step});"></div>',
                name=f"--opacity-{step}",
                caption=f"Opacity {step}.",
                value=str(val),
            ))

    zindex = primitive.get("zIndex") or {}
    if zindex:
        parts.append('<h3>Z-index scale</h3>')
        stack = '<div class="gloss-zstack">'
        offset = 0
        for label, val in zindex.items():
            stack += f'<div style="left: {offset}px; top: {offset}px; z-index: var(--z-{label});">{label}</div>'
            offset += 12
        stack += '</div>'
        parts.append(_gloss_entry(
            render=stack,
            name="--z-{label}",
            caption="Layer stack — base < dropdown < sticky < modal < toast.",
            value=", ".join(str(v) for v in zindex.values()),
        ))

    bp = primitive.get("breakpoint") or {}
    if bp:
        parts.append('<h3>Breakpoint scale</h3>')
        for label, val in bp.items():
            parts.append(_gloss_entry(
                render=f'<span class="badge">{label} → {val}</span>',
                name=f"--bp-{label}",
                caption=f"Breakpoint — {label}.",
                value=str(val),
            ))
    parts.append('</div>')

    # ── PRIMITIVE — Motion ───────────────────────────────────────────────────
    motion = primitive.get("motion") or {}
    if motion:
        parts.append('<div class="gloss-section"><h2>Primitive — Motion</h2>')
        for label, val in (motion.get("easing") or {}).items():
            parts.append(_gloss_entry(
                render=f'<button class="btn btn-secondary btn-sm" onmouseover="this.style.transitionTimingFunction=\'var(--ease-{label})\'; this.style.transform=\'translateX(20px)\';" onmouseleave="this.style.transform=\'translateX(0)\';" style="transition: transform var(--duration-normal);">Hover →</button>',
                name=f"--ease-{label}",
                caption=f"Easing curve — {label}. Hover the button to see motion.",
                value=str(val),
            ))
        for label, val in (motion.get("duration") or {}).items():
            parts.append(_gloss_entry(
                render=f'<span class="badge">{label} = {val}</span>',
                name=f"--duration-{label}",
                caption=f"Duration step — {label}.",
                value=str(val),
            ))
        parts.append('</div>')

    # ── SEMANTIC — Color (light + dark) + Status ─────────────────────────────
    parts.append('<div class="gloss-section"><h2>Semantic — Color (light)</h2>')
    for role, val in (semantic.get("light", {}).get("color") or {}).items():
        if not isinstance(val, (str, int, float)):
            continue
        substrate = _semantic_substrate(role, val)
        parts.append(_gloss_entry(
            render=substrate,
            name=f"--color-{role}",
            caption=f"Semantic role — {role}. Rendered on the actual UI element it controls.",
            value=str(val),
        ))
    parts.append('</div>')

    parts.append('<div class="gloss-section"><h2>Semantic — Color (dark)</h2>')
    parts.append('<p class="muted">Dark-mode tokens shown as swatches; full dark surfaces are tested via the Mode control tab.</p>')
    for role, val in (semantic.get("dark", {}).get("color") or {}).items():
        if not isinstance(val, (str, int, float)):
            continue
        parts.append(_gloss_entry(
            render=f'<div class="gloss-tile" style="background: {val};"></div>',
            name=f"--color-{role} (dark)",
            caption=f"Dark-mode value for {role}.",
            value=str(val),
        ))
    parts.append('</div>')

    parts.append('<div class="gloss-section"><h2>Semantic — Status</h2>')
    for status, val in (semantic.get("status") or {}).items():
        if isinstance(status, str) and status.startswith("$"):
            continue
        if not isinstance(val, (str, int, float)):
            continue
        parts.append(_gloss_entry(
            render=(
                f'<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; align-items: center;">'
                f'<div class="banner is-{status}"><strong>{status.title()}</strong></div>'
                f'<span class="badge badge-{status}">{status.title()}</span>'
                f'<button class="btn btn-sm" style="background: {val}; color: #FFF;">Action</button>'
                f'<span style="color: {val}; font-size: 24px;">●</span>'
                f'</div>'
            ),
            name=f"--color-status-{status}",
            caption=f"Status color — {status}. Banner / pill / button / icon variants.",
            value=str(val),
        ))
    parts.append('</div>')

    # ── COMPONENT overrides ──────────────────────────────────────────────────
    component = tokens.get("component") or {}
    if component:
        parts.append('<div class="gloss-section"><h2>Component overrides</h2>')
        for cname, props in component.items():
            parts.append(_gloss_entry(
                render=f'<button class="btn btn-primary">{cname}</button>',
                name=f"tokens.component.{cname}",
                caption=f"Component-tier override block for {cname}.",
                value=", ".join(f"{k}=…" for k in (props.keys() if isinstance(props, dict) else [])),
            ))
        parts.append('</div>')

    # ── EXTENSIONS ────────────────────────────────────────────────────────────
    extensions = tokens.get("extensions") or {}
    motifs = ((extensions.get("form") or {}).get("motifs") or {})
    if motifs:
        parts.append('<div class="gloss-section"><h2>Extensions — Motifs</h2>')
        for mname, mdata in motifs.items():
            if isinstance(mname, str) and mname.startswith("$"):
                continue
            description = (mdata.get("description") if isinstance(mdata, dict) else "") or ""
            parts.append(_gloss_entry(
                render='<div style="width: 80px; height: 80px; background: var(--color-accent); border-radius: var(--radius-card); display: grid; place-items: center; color: var(--color-text-inverse); font-family: var(--font-heading);">' + str(mname)[:1].upper() + '</div>',
                name=f"extensions.form.motifs.{mname}",
                caption=description or f"Brand-extension motif — {mname}.",
                value=str(mdata)[:80] if mdata else "",
            ))
        parts.append('</div>')

    parts.append('</div>')  # close .gloss
    return "\n".join(parts)


def _gloss_entry(*, render: str, name: str, caption: str, value: str) -> str:
    return (
        '<div class="gloss-entry">'
        f'<div class="render">{render}</div>'
        '<div class="meta">'
        f'<div class="name">{name}</div>'
        f'<div class="caption">{caption}</div>'
        f'<div class="value">{value}</div>'
        '</div></div>'
    )


def build_control_panes_html(look: dict) -> str:
    """Generate the four control panes (Colors / Type / Form / Mode) populated
    from the brand's Look. Each control writes a CSS variable on the active
    `[data-look]` scope when changed.
    """
    tokens = look.get("tokens", {})
    primitive = tokens.get("primitive", {})
    semantic_light = (tokens.get("semantic", {}).get("light", {}) or {}).get("color") or {}

    # Colors pane — every semantic light role with a string value
    color_rows = []
    for role, val in semantic_light.items():
        if not isinstance(val, (str, int, float)):
            continue
        color_rows.append(
            f'<div class="pg-control-row">'
            f'<label for="ctl-color-{role}">--color-{role}</label>'
            f'<input id="ctl-color-{role}" type="color" data-css-var="--color-{role}" value="{_to_hex(val)}" />'
            f'<input type="text" data-css-var-text="--color-{role}" value="{val}" />'
            f'</div>'
        )

    families = (primitive.get("typography", {}).get("fontFamily") or {})
    fonts_safelist = [
        "Inter", "Manrope", "DM Sans", "Plus Jakarta Sans", "IBM Plex Sans", "Source Sans 3",
        "Roboto", "Open Sans", "Nunito", "Work Sans", "Outfit", "Karla",
        "Playfair Display", "Lora", "Merriweather", "Crimson Pro",
        "Space Grotesk", "Space Mono", "JetBrains Mono", "Fira Code", "IBM Plex Mono",
    ]
    type_rows = []
    for role in ("heading", "body", "mono"):
        chain = families.get(role)
        cur = (chain[0] if isinstance(chain, list) and chain else chain) or ""
        opts = "".join(f'<option value="{f}"{" selected" if f == cur else ""}>{f}</option>' for f in fonts_safelist)
        type_rows.append(
            f'<div class="pg-control-row"><label>--font-{role}</label>'
            f'<select data-font-role="{role}">{opts}<option value="__custom__">Custom (from CSS)</option></select></div>'
        )
    base_size = (primitive.get("typography", {}).get("fontSize") or {}).get("body", "1rem")
    type_rows.append(
        f'<div class="pg-control-row"><label>--font-size-body</label>'
        f'<input type="text" data-css-var-text="--font-size-body" value="{base_size}" /></div>'
    )
    scale_ratio = (primitive.get("typography", {}).get("scale") or {}).get("ratio", 1.250)
    type_rows.append(
        f'<div class="pg-control-row"><label>--scale-ratio</label>'
        f'<input type="text" data-css-var-text="--scale-ratio" value="{scale_ratio}" /></div>'
    )

    radius = primitive.get("radius") or {}
    form_rows = []
    for label in ("interactive", "card", "md", "lg"):
        if label in radius:
            form_rows.append(
                f'<div class="pg-control-row"><label>--radius-{label}</label>'
                f'<input type="text" data-css-var-text="--radius-{label}" value="{radius[label]}" /></div>'
            )
    form_rows.append(
        '<div class="pg-control-row"><label>density</label>'
        '<select data-density><option value="compact">Compact</option><option value="comfortable" selected>Comfortable</option><option value="spacious">Spacious</option></select></div>'
    )
    form_rows.append(
        '<div class="pg-control-row"><label>shadow intensity</label>'
        '<select data-shadow-intensity><option value="none">None</option><option value="subtle">Subtle</option><option value="default" selected>Default</option><option value="dramatic">Dramatic</option></select></div>'
    )

    mode_html = (
        '<div class="pg-control-row"><label>Mode</label>'
        '<select data-mode-select><option value="light" selected>Light</option><option value="dark">Dark</option></select></div>'
        '<div class="pg-control-row"><label>Preset (B side)</label>'
        '<select data-preset-select><option value="">— brand —</option></select></div>'
        '<div style="margin-top: var(--space-4);">'
        '<label class="field"><span>Paste look.yaml or look JSON</span>'
        '<textarea class="textarea" rows="6" data-paste-look placeholder="Paste a Look here…"></textarea></label>'
        '<button class="btn btn-secondary btn-sm" data-paste-load>Load into B</button>'
        '</div>'
        '<div style="margin-top: var(--space-4);">'
        '<button class="btn btn-primary btn-sm" data-share-link>Copy share link</button> '
        '<button class="btn btn-ghost btn-sm" data-reset>Reset</button></div>'
    )

    return (
        '<div class="pg-control-pane active" data-pane="colors"><h3>Semantic colors (light)</h3>'
        + "".join(color_rows) +
        '</div>'
        '<div class="pg-control-pane" data-pane="type"><h3>Typography</h3>'
        + "".join(type_rows) +
        '</div>'
        '<div class="pg-control-pane" data-pane="form"><h3>Form</h3>'
        + "".join(form_rows) +
        '</div>'
        '<div class="pg-control-pane" data-pane="mode"><h3>Mode &amp; sharing</h3>'
        + mode_html +
        '</div>'
    )


def _to_hex(val) -> str:
    """Best-effort coerce a CSS color string to #RRGGBB for `<input type="color">`.

    Falls back to #888888 when conversion isn't trivial (named colors, rgb(),
    hsl(), color-mix). The text-input alongside accepts the original string
    verbatim, so non-hex values remain editable.
    """
    if not isinstance(val, str):
        return "#888888"
    v = val.strip()
    if v.startswith("#") and len(v) in (4, 7):
        if len(v) == 4:
            return "#" + "".join(c * 2 for c in v[1:])
        return v.lower()
    return "#888888"


def _semantic_substrate(role: str, val: str) -> str:
    """Render the semantic role on the actual UI element it controls."""
    if role == "bg":
        return f'<div style="background: {val}; padding: var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-md);">Page bg sample</div>'
    if role.startswith("surface"):
        return f'<div class="card" style="background: {val}; padding: var(--space-3); margin: 0;">Card on {role}</div>'
    if role == "text-primary":
        return f'<p style="color: {val}; margin: 0; font-size: var(--font-size-body);">Primary body paragraph.</p>'
    if role == "text-secondary":
        return f'<p style="color: {val}; margin: 0; font-size: var(--font-size-body);">Subhead or meta line.</p>'
    if role == "text-tertiary":
        return f'<p style="color: {val}; margin: 0; font-size: var(--font-size-small);">Caption or quote attribution.</p>'
    if role == "text-disabled":
        return f'<p style="color: {val}; margin: 0;">Disabled state text.</p>'
    if role == "text-inverse":
        return f'<div style="background: var(--color-text-primary); color: {val}; padding: var(--space-2) var(--space-3); border-radius: var(--radius-sm);">Text on dark surface</div>'
    if role.startswith("border-focus"):
        return f'<input class="input" autofocus style="border-color: {val}; box-shadow: 0 0 0 3px {val}40; max-width: 200px;" placeholder="Focused input" />'
    if role.startswith("border"):
        return f'<input class="input" style="border-color: {val}; max-width: 200px;" placeholder="Border sample" />'
    if role.startswith("link"):
        return f'<a href="#" style="color: {val};">A linked phrase</a>'
    return f'<div class="gloss-tile" style="background: {val};"></div>'


def render(brand_dir: Path, out_path: Path, *, no_presets: bool = False) -> None:
    tokens_path = brand_dir / "tokens.json"
    if not tokens_path.exists():
        sys.stderr.write(f"render-playground: tokens.json not found at {tokens_path}\n")
        sys.exit(1)
    tokens_raw = json.loads(tokens_path.read_text())

    identity   = _yaml_or_none(brand_dir / "brand-identity.yaml") or {}
    extensions = _yaml_or_none(brand_dir / "brand-extensions.yaml") \
              or _yaml_or_none(brand_dir / "brand.extensions.yaml") or {}
    surfaces   = _yaml_or_none(brand_dir / "surface-translations.yaml") or {}

    brand_name = (
        (identity.get("identity") or {}).get("name")
        or identity.get("name")
        or "Design Playground"
    )
    brand_tagline = (
        (identity.get("identity") or {}).get("tagline")
        or identity.get("tagline")
        or "Open in any modern browser"
    )

    look = build_look(
        tokens_raw,
        brand_name=brand_name,
        brand_tagline=brand_tagline,
        extensions_raw=extensions,
        surface_translations_raw=surfaces,
    )

    presets = []
    if not no_presets and PRESETS.exists():
        try:
            presets = json.loads(PRESETS.read_text())
        except json.JSONDecodeError:
            presets = []

    def _first_family(chain) -> str | None:
        """Extract the first font family name from a chain (list, str, or CSS-comma string).

        - list:   `["Inter", "system-ui"]` → "Inter"
        - str:    `"Inter, system-ui, sans-serif"` → "Inter"
        - str:    `"'Helvetica Neue', Arial"` → "Helvetica Neue"
        Strips quotes. Returns None for system-only / generic-only chains.
        """
        if isinstance(chain, list) and chain:
            cand = chain[0]
        elif isinstance(chain, str):
            cand = chain.split(",")[0]
        else:
            return None
        name = str(cand).strip().strip("'\"")
        # Skip CSS generics + ui-* keywords — those aren't Google Fonts.
        if not name or name.lower() in {"system-ui", "ui-monospace", "ui-sans-serif", "ui-serif", "ui-rounded", "monospace", "serif", "sans-serif", "inherit", "initial"}:
            return None
        return name

    families = (look["tokens"].get("primitive", {}).get("typography", {}).get("fontFamily") or {})
    family_names: list[str] = []
    for role in ("heading", "body", "mono"):
        first = _first_family(families.get(role))
        if first:
            family_names.append(first)
    seen: set[str] = set()
    family_names = [f for f in family_names if not (f in seen or seen.add(f))]
    if family_names:
        slugs = "&".join(f"family={f.replace(' ', '+')}:wght@300;400;500;600;700" for f in family_names)
        gfonts_link = f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{slugs}&display=swap">'
    else:
        gfonts_link = ""

    template = TEMPLATE.read_text()

    js_yaml_path = PLUGIN_ROOT / "assets" / "vendor" / "js-yaml-4.1.0.min.js"
    if js_yaml_path.exists():
        js_yaml_inline = js_yaml_path.read_text()
    else:
        # Renderer should not block on missing vendor — emit a stub that leaves
        # window.jsyaml undefined so the paste-load handler degrades to JSON-only.
        js_yaml_inline = "/* js-yaml vendor missing — YAML paste disabled */"

    look_root_vars = emit_css_vars(look)
    # In compare mode, A starts as the brand and B starts as the first preset (or A again).
    look_a_vars = look_root_vars
    look_b_vars = emit_css_vars(presets[0]) if presets else look_root_vars

    hero_headline = (
        ((extensions.get("voice") or {}).get("taglines") or [None])[0]
        or brand_tagline
        or "Ship faster. Sleep more."
    )

    marketing_body = (MARKETING_BODY_HTML
        .replace("{{BRAND_NAME}}", brand_name)
        .replace("{{HERO_HEADLINE}}", hero_headline)
        .replace("{{HERO_TAGLINE}}", brand_tagline))

    substitutions = {
        "{{BRAND_NAME}}":        brand_name,
        "{{HERO_HEADLINE}}":     hero_headline,
        "{{HERO_TAGLINE}}":      brand_tagline,
        "{{LOOK_ROOT_VARS}}":    look_root_vars,
        "{{LOOK_A_VARS}}":       look_a_vars,
        "{{LOOK_B_VARS}}":       look_b_vars,
        "{{LOOK_DATA_JSON}}":    json.dumps(look, ensure_ascii=False, indent=2),
        "{{PRESETS_DATA_JSON}}": json.dumps(presets, ensure_ascii=False),
        "{{JS_YAML_INLINE}}":    js_yaml_inline,
        "{{GFONTS_LINK}}":       gfonts_link,
        "{{MARKETING_BODY}}":    marketing_body,
        "{{APP_BODY}}":          APP_BODY_HTML.replace("{{BRAND_NAME}}", brand_name),
        "{{SLIDE_BODY}}":        SLIDE_BODY_HTML.replace("{{BRAND_NAME}}", brand_name),
        "{{GLOSSARY_BODY}}":     build_glossary_html(look),
        "{{CONTROL_PANES}}":     build_control_panes_html(look),
    }

    rendered = template
    for needle, replacement in substitutions.items():
        rendered = rendered.replace(needle, replacement)

    # Tasks 7–10 add more placeholders. Defensive: any remaining {{NAME}} after
    # the surface tasks land must trigger validation FAIL via forbidden_patterns.
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered)


def main() -> int:
    p = argparse.ArgumentParser(description="Render single-file design playground HTML")
    p.add_argument("--brand-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--no-presets", action="store_true", help="skip baked-in compare-mode presets")
    args = p.parse_args()
    render(args.brand_dir, args.out, no_presets=args.no_presets)
    return 0


if __name__ == "__main__":
    sys.exit(main())
