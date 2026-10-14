# VCF Design Decision Library

An interactive single-page web application to browse, filter, edit, and export VMware Cloud Foundation Design Decisions — with full access to Blueprint Deployment References across all 5 VCF Fleet blueprints.

> **Author:** L.COSCIA  
> **Version:** 2.3  
> **Data:** 680 DDs VCF 9.0 (473 Both + 156 Excel + 51 Web Doc) · 1,154 DDs VCF 9.1 (825 Both + 277 Excel + 52 Web Doc) · 1,330 DDs VCF 9.1.1 (1,191 Both + 87 Excel + 52 Web Doc) · 19 Blueprints (5 fleet topologies + 14 VCF 9.1/9.1.1)

---

## Overview

This tool provides a fast, offline-capable interface for the VCF Design Library. All data is embedded directly in the HTML — no server, no dependencies, just open `index.html` in any modern browser. No login required.

---

## Features

| Feature | Description |
|---|---|
| 📐 **Blueprint View** | Switch between all 5 VCF Fleet blueprints with High Level Deployment Requirements (Physical Hosts, VLANs, Virtual Networking) |
| 📚 **Design Library View** | Full access to all Design Decisions of the selected version (680 / 1,154 / 1,330) — toggle via the tab bar |
| 🔀 **Multi-version Support** | Switch between VCF 9.0, VCF 9.1 and VCF 9.1.1 via the header dropdown |
| 🔍 **Search & Filter** | Full-text search across all fields. Filter by Component, Type, Category, Source, Status, Criticality, Marked status and Change vs 9.1 |
| ⊞ **Group by Category** | Toggle category grouping with collapsible sections |
| ↔ **Resizable Columns** | Drag column borders to adjust width |
| 🖱️ **Click-to-Edit ID** | Click directly on a Design Decision ID to instantly open its edit modal |
| ✏️ **Edit Design Decisions** | Edit any field: Type, Status, Criticality, Justification, Implication, Notes |
| ⭐ **Mark for Export** | Star individual rows or bulk-mark a selection |
| 📤 **Excel Export** | Export marked / selected / filtered decisions in the original Excel format |
| 📥 **Import Excel** | Drag & drop or browse to import an updated Design Library `.xlsx` |
| ＋ **Temporary DD** | Add custom Design Decisions for the session (marked TEMP) |
| 📝 **Bulk Notes** | Apply notes to all selected Design Decisions at once |
| 🔖 **Source Tracking** | Each DD tagged with its origin: Excel, Web Doc, or Both |
| 🆕 **Change vs 9.1** | VCF 9.1.1 DDs carry NEW / CHANGED / RENUM badges (renumbered DDs show their 9.1 ID), with a matching sidebar filter |
| 🌙 **Dark Theme** | Toggle dark/light mode — preference persisted in `localStorage` |
| 📱 **Responsive** | Sidebar collapses to a slide-in drawer on mobile/tablet |

---

## VCF Fleet Blueprints

| Blueprint | Description |
|---|---|
| VCF Fleet in a Single Site | Single-site standard deployment |
| VCF Fleet in a Single Site with Minimal Footprint | Single-site minimal footprint |
| VCF Fleet with Multiple Sites in a Single Region | Multi-site, single region |
| VCF Fleet with Multiple Sites in a Single Region plus Additional Region(s) | Multi-site, multi-region |
| VCF Fleet with Multiple Sites Across Multiple Regions | Full multi-region |

---

## Usage

### Switch between Blueprint and Design Library
Use the **tab bar** at the top of the content area to toggle between:
- **📐 Blueprint** — selects one of 5 VCF Fleet blueprints; shows the HLR panel (Physical Hosts, VLANs, Virtual Networking) and the blueprint's design decisions
- **📚 Design Library** — shows the full library of the selected version with all filters active

### Switch VCF version
Use the **version dropdown** in the header to switch between VCF 9.0, VCF 9.1 and VCF 9.1.1.

### Export your selection
1. Star Design Decisions with ⭐ or select rows and click **Mark for Export**
2. Click **Export Marked** — an `.xlsx` file is downloaded

---

## File Structure

```
index.html                        ← Full app with all embedded data (open this)
README.md
VCF_LowLevelDesignDecisions/     ← Source xlsx files (5 blueprints)
tools/                            ← Dataset build scripts (VCF 9.1.1) + TechDocs-derived inputs in tools/data/
```

---

## Technical Details

- **Pure HTML/CSS/JS** — no framework, no build step, no authentication
- **SheetJS (xlsx.js)** loaded from CDN for Excel import/export
- ~3.7 MB total file size (includes all embedded datasets and blueprint data)

---

## Data Sources

- **DDs**: VMware Cloud Foundation Design Library Excel files (9.0, 9.1, 9.1.1 — `.xlsx`, not versioned) + Broadcom TechDocs
- **Blueprint DDs**: VCF Fleet Blueprint Design Decision Workbooks (5 `.xlsx` files)
- **High Level Requirements**: [Broadcom TechDocs — VCF 9.0 Blueprints](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/design/blueprints.html)

---

## Rebuilding the VCF 9.1.1 dataset

Requires Python 3 with `openpyxl`, and the Excel files `VCF91 - Design Library.xlsx` and `VCF911 - Design Library.xlsx` in the project root.

```bash
python3 -I -B tools/build_vcf911.py . /tmp/vcf911.json \
  --web-ids tools/data/web_ids_91x.txt --web-only tools/data/web_only_911.json
python3 -I -B tools/update_index.py index.html --v911 /tmp/vcf911.json \
  --v91-excel "VCF91 - Design Library.xlsx" --web-ids tools/data/web_ids_91x.txt \
  --web-only-91 tools/data/web_only_91.json --drop-parasites \
  --vdefend-blueprint tools/data/vdefend_blueprint_ids.txt
```

- `component` / `type` come from the ID (`tools/vcf_dd_lib.py`, mirrored by `ddComponent()` / `ddType()` in `index.html`).
- `source`: Both if the ID appears on the VCF 9.1.x TechDocs design pages (`web_ids_91x.txt`), else Excel; web-only DDs are added as Web Doc.
- `delta` / `prev_id`: computed against the VCF 9.1 Excel.
- `update_index.py` is idempotent: it removes scrape artifacts (`--drop-parasites`), completes the 9.1 Excel import (`--v91-excel`), re-applies the 9.1 type rule, replaces the 9.1.1 array and fills the vDefend blueprint (`vdefend_blueprint_ids.txt`).

## Changelog

### v2.3 — VCF 9.1.1 Dedicated Dataset
- VCF 9.1.1 has its own dataset from `VCF911 - Design Library.xlsx` — **1,330 Design Decisions** (1,191 Both · 87 Excel · 52 Web Doc)
- vs VCF 9.1: 187 new · 92 changed · 107 renumbered · 10 removed — NEW / CHANGED / RENUM badges and *Change vs 9.1* filter
- New components **vDefend** (MDS/SSP/WDS/DVP/SEC-*) and **License Hub** (LH)
- Type derived from REQD / RECD / RCMD anywhere in the ID (9.1 and 9.1.1); Type filter and modal lists are data-driven (adds *Choice*)
- VCF 9.1 full reimport: +164 Excel rows that were cut after Excel row 1184 (PAIF-* and vDefend sections), 53 older Web Doc PAIF rows superseded, +51 web-only DDs from the VCF 9.1.x TechDocs pages — **1,154 DDs** (825 Both · 277 Excel · 52 Web Doc)
- Removed web-scrape artifacts (header or sentence used as ID): 7 in VCF 9.0 (→ **680 DDs**), 6 in VCF 9.1, none in 9.1.1
- **Lateral Security with vDefend Blueprint** populated with **101 DDs** (vDefend MDS/SSP/WDS/DVP + License Hub, as listed on the TechDocs blueprint pages)
- ID column wider by default and auto-fitted to the longest ID + badges
- Export title / file name follow the selected version; built-in import uses the same component/type rules

### v2.2 — VCF 9.1.1 Added
- Added VCF 9.1.1 (GA September 3, 2026) to the version selector, initially reusing the VCF 9.1 dataset and blueprints
- About: 9.1.1 what's new, Bill of Materials and upgrade prerequisites

### v2.1 — VCF 9.1 Full Dataset
- Integrated official Broadcom Excel (VCF 9.1) + web cross-reference — **998 Design Decisions** (772 Both · 166 Excel · 60 Web Doc)
- Added **14 new VCF 9.1 blueprints** with HLR data: Fleet Management, Monitoring, Troubleshooting, Edge (×3), Multi-Tenant, VKS, Private AI, vDefend, Backup & Restore, Instance Recovery, Fleet DR, Cyber Recovery
- Blueprint selector reorganized into 4 categories (19 blueprints total)
- Scraped **164 pages** from VCF 9.0 Design Library — **687 Design Decisions** (670 Excel + 17 Web Doc)

### v2.0 — Open Access & Data Quality
- Removed authentication gate — app is now fully public with no login required
- Removed Supabase, EmailJS SDKs and all auth/admin code (~756 lines)
- Added **Design Library tab**: toggle between Blueprint view and full 670-DD library
- Blueprint toolbar and HLR panel now always visible on load
- Fixed **20 duplicate IDs** (sequential renumbering or -A/B/C/D suffixes for option groups)
- Fixed 1 malformed ID (`VCF-VSAN-SC_RCMD-001` → `VCF-VSAN-SC-RCMD-001`) and 2 REQD/RCMD type mismatches
- Removed **6 legacy SDDC Manager entries** superseded by VCF Operations in VCF 9
- Dataset: 685 → **670 Design Decisions** across **28 components**

### v1.6 — Invite Flow & Admin Fixes
- Set-password modal when a user accepts an invite link (before first login)
- Approve access request via **`generateLink`** — bypasses Supabase SMTP rate limit
- Invite link copy-to-clipboard fallback modal for admin
- Fixed action name mismatch (`create_user`, `delete_user`) between client and Edge Function

### v1.5 — Supabase Auth
- Migrated authentication from localStorage/SHA-256 to **Supabase Auth** (bcrypt server-side)
- Persistent JWT sessions across browsers and private navigation
- User management via **Supabase Edge Function** — service role key never exposed client-side
- Supabase PostgreSQL with Row Level Security on `profiles` table

### v1.4 — Private Library & Admin Panel
- Added **Private Library** section with SHA-256 authentication and session management
- Embedded **1,547 Low-Level Design Decisions** across 5 VCF Fleet blueprints
- Blueprint selector with **High Level Deployment Requirements** panel (Broadcom TechDocs)
- **Admin Panel**: centralized user management (add, deactivate, reset password, delete)
- **Access Request form**: sends automatic email to admin via EmailJS

### v1.3 — Multi-version Support
- Added version selector dropdown in the header (VCF 9.0 / VCF 9.1)
- VCF 9.0 data embedded; VCF 9.1 slot ready for Excel import
- Switching version resets all filters, selections and marks

### v1.2 — Click-to-Edit & Marked Filter
- Clicking on a Design Decision ID now instantly opens its edit modal
- Added Marked Status filter in the sidebar (All / ⭐ Marked only / ☆ Unmarked only)

### v1.1 — Source Tracking & Deduplication
- Added Source field (Excel / Web Doc / Both) with color-coded badges
- Integrated 42 missing DDs sourced from official VCF 9.0 documentation
- Deduplicated the dataset — cleaned to a unique set

### v1.0 — Initial Release
Full Design Decision explorer with search, filters, pagination, column resize, edit modal, Excel import/export, category grouping, mark for export, bulk notes, temporary DD, dark theme and responsive layout.

---

*Generated with [Claude](https://claude.ai)*
