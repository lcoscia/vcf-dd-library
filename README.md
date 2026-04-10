# VCF Design Decision Library

An interactive single-page web application to browse, filter, edit, and export VMware Cloud Foundation 9.0 Design Decisions.

> **Author:** L.COSCIA  
> **Version:** 1.3  
> **Data:** Design Decisions across 21+ components (VCF 9.0 embedded · VCF 9.1 via Excel import)

---

## Overview

This tool provides a fast, offline-capable interface for the VCF Design Library Excel file. All data is embedded directly in the HTML — no server, no dependencies, just open `index.html` in any modern browser.

---

## Features

| Feature | Description |
|---|---|
| 🔀 **Multi-version Support** | Switch between VCF 9.0 and VCF 9.1 via the header dropdown. VCF 9.0 is embedded; VCF 9.1 is populated by importing an Excel file |
| 🔍 **Search & Filter** | Full-text search across all fields. Filter by Component, Type, Category, Status, Criticality and Marked status |
| ⊞ **Group by Category** | Toggle category grouping with collapsible sections |
| ↔ **Resizable Columns** | Drag column borders to adjust width |
| 🖱️ **Click-to-Edit ID** | Click directly on a Design Decision ID to instantly open its edit modal |
| ✏️ **Edit Design Decisions** | Edit any field: Type, Status, Criticality, Justification, Implication, Notes |
| ⭐ **Mark for Export** | Star individual rows or bulk-mark a selection. Stats by component shown in sidebar |
| ⭐ **Marked Filter** | Filter the table to show only marked or unmarked Design Decisions |
| 📤 **Excel Export** | Export marked / selected / filtered decisions in the original Excel format |
| 📥 **Import Excel** | Drag & drop or browse to import an updated Design Library `.xlsx` |
| ＋ **Temporary DD** | Add custom Design Decisions for the session (marked TEMP, lost on reload) |
| 📝 **Bulk Notes** | Apply notes to all selected Design Decisions at once |
| 🔖 **Source Tracking** | Each DD is tagged with its origin: Excel, Web Doc, or Both. Sortable & filterable |
| 🌙 **Dark Theme** | Toggle dark/light mode — preference persisted in `localStorage` |
| 📱 **Responsive** | Sidebar collapses to a slide-in drawer on mobile/tablet |
| 🔢 **Statistics** | Per-component count of marked DDs shown in the sidebar |

---

## Usage

### Open locally
Simply double-click `index.html` — no installation required.

### Import an updated library
Click **Import Excel** in the header and select a `.xlsx` file with the same structure as the original VCF Design Library.

### Export your selection
1. Star the Design Decisions you want with the ⭐ button on each row, or select rows and click **Mark for Export**
2. Click **Export Marked** in the header — an `.xlsx` file is downloaded in the original format

### Edit a Design Decision
- Click directly on the **ID** of any row to instantly open the edit modal
- Or select a single row (click or checkbox) and click **✏️ Edit** in the toolbar

### Switch VCF version
Use the **version dropdown** in the header (next to the logo) to switch between VCF 9.0 and VCF 9.1. VCF 9.0 data is embedded. To use VCF 9.1, select it then click **Import Excel** to load the corresponding `.xlsx` file.

### Filter marked decisions
Use the **Marked Status** dropdown in the sidebar to show only ⭐ marked or ☆ unmarked decisions.

### Bulk edit notes
Select multiple rows and click **📝 Edit Notes** to apply a note to all selected DDs at once.

---

## File Structure

```
index.html    ← Full app with embedded data (open this)
README.md
```

---

## Technical Details

- **Pure HTML/CSS/JS** — no framework, no build step
- **SheetJS (xlsx.js)** loaded from CDN for Excel import/export (internet required for first load)
- Data embedded as a JavaScript variable — works fully offline after first open
- Dark theme preference stored in `localStorage`

---

## Data Source

VMware Cloud Foundation 9.0 — VCF Design Library  
Original format: `.xlsx` with columns: Design Decision ID, Design Decision, Design Justification, Design Implication, Compliant Status, Design Decision Criticality, Notes

---

## Changelog

### v1.3 — Multi-version Support
- Added version selector dropdown in the header (VCF 9.0 / VCF 9.1)
- VCF 9.0 data embedded; VCF 9.1 slot ready for Excel import
- Switching version resets all filters, selections and marks
- Imported Excel data is stored in the active version slot for the session

### v1.2 — Click-to-Edit & Marked Filter
- Clicking on a Design Decision ID now instantly opens its edit modal
- Added Marked Status filter in the sidebar (All / ⭐ Marked only / ☆ Unmarked only)

### v1.1 — Source Tracking & Deduplication
- Added Source field (Excel / Web Doc / Both) with color-coded badges
- Integrated 42 missing DDs sourced from official VCF 9.0 documentation
- Deduplicated the dataset — cleaned to a unique set
- Added Source filter in sidebar and Source column in table

### v1.0 — Initial Release
Full Design Decision explorer with search, filters, pagination, column resize, edit modal, Excel import/export, category grouping, mark for export, bulk notes, temporary DD, dark theme and responsive layout.

---

*Generated with [Claude](https://claude.ai)*
