# VCF Design Decision Library

An interactive single-page web application to browse, filter, edit, and export VMware Cloud Foundation Design Decisions — with a secured Private Library for Low-Level Blueprint Design Decisions.

> **Author:** L.COSCIA  
> **Version:** 1.4  
> **Data:** 1,500+ public DDs (VCF 9.0 embedded · VCF 9.1 via import) + 1,547 private Low-Level DDs across 5 blueprints

---

## Overview

This tool provides a fast, offline-capable interface for the VCF Design Library. All data is embedded directly in the HTML — no server, no dependencies, just open `index.html` in any modern browser.

A **Private Library** section gives authenticated users access to Low-Level Design Decisions for all 5 VCF Fleet deployment blueprints, with High Level Deployment Requirements sourced from Broadcom TechDocs.

---

## Features

### Public Section
| Feature | Description |
|---|---|
| 🔀 **Multi-version Support** | Switch between VCF 9.0 and VCF 9.1 via the header dropdown |
| 🔍 **Search & Filter** | Full-text search across all fields. Filter by Component, Type, Category, Status, Criticality and Marked status |
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
| 🌙 **Dark Theme** | Toggle dark/light mode — preference persisted in `localStorage` |
| 📱 **Responsive** | Sidebar collapses to a slide-in drawer on mobile/tablet |

### Private Section (Authentication Required)
| Feature | Description |
|---|---|
| 🔒 **Secure Login** | SHA-256 hashed passwords, session managed via `sessionStorage` |
| 📋 **Blueprint Selector** | Switch between all 5 VCF Fleet blueprints |
| 📊 **Low-Level DDs** | 1,547 Low-Level Design Decisions across 5 blueprints |
| 🏗️ **HLR Panel** | High Level Deployment Requirements per blueprint (from Broadcom TechDocs) |
| 📧 **Access Request** | Built-in form to request access — email sent automatically to admin via EmailJS |
| ⚙️ **Admin Panel** | Centralized user management: add, activate/deactivate, reset password, delete |

---

## VCF Fleet Blueprints (Private Library)

| Blueprint | Design Decisions |
|---|---|
| VCF Fleet in a Single Site | 312 |
| VCF Fleet in a Single Site with Minimal Footprint | 275 |
| VCF Fleet with Multiple Sites in a Single Region | 322 |
| VCF Fleet with Multiple Sites in a Single Region plus Additional Region(s) | 322 |
| VCF Fleet with Multiple Sites Across Multiple Regions | 316 |

---

## Usage

### Access the Private Library
Click **🔒 Private Library** in the header. If not authenticated, a login modal appears. Contact the administrator to obtain your credentials.

### Request Access
Click **Request Access** in the login modal to open the access request form. The admin receives an email automatically.

### Admin Panel
Accessible to admin users via the **⚙️ Admin** button in the header (visible when logged in as admin):
- **Add user**: fill in username, email, password and role
- **Reset password**: click 🔑 Reset next to any user
- **Deactivate/Activate**: temporarily block or restore access
- **Delete**: permanently remove a user account

### Switch Blueprint (Private Mode)
Use the **Blueprint** dropdown in the purple toolbar to switch between VCF Fleet blueprints. The High Level Deployment Requirements panel updates automatically.

### Switch VCF version (Public Mode)
Use the **version dropdown** in the header to switch between VCF 9.0 and VCF 9.1.

### Export your selection
1. Star Design Decisions with ⭐ or select rows and click **Mark for Export**
2. Click **Export Marked** — an `.xlsx` file is downloaded

---

## File Structure

```
index.html                        ← Full app with all embedded data (open this)
README.md
VCF_LowLevelDesignDecisions/     ← Source xlsx files (5 blueprints)
```

---

## Technical Details

- **Pure HTML/CSS/JS** — no framework, no build step, no backend
- **Authentication**: passwords hashed with SHA-256 via native `SubtleCrypto` API
- **Session**: stored in `sessionStorage` (expires on tab close)
- **Users**: stored as hashed entries in `localStorage` (never plaintext)
- **Email**: [EmailJS](https://emailjs.com) for access request notifications (no backend required)
- **SheetJS (xlsx.js)** loaded from CDN for Excel import/export
- ~1.5 MB total file size (includes all embedded blueprint data)

---

## Data Sources

- **Public DDs**: VMware Cloud Foundation 9.0 Design Library (`.xlsx`) + Broadcom TechDocs
- **Private DDs**: VCF Fleet Blueprint Design Decision Workbooks (5 `.xlsx` files)
- **High Level Requirements**: [Broadcom TechDocs — VCF 9.0 Blueprints](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/design/blueprints.html)

---

## Changelog

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
