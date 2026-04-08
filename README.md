# VCF Design Decision Library

An interactive single-page web application to browse, filter, edit, and export VMware Cloud Foundation 9.0 Design Decisions.

> **Author:** L.COSCIA  
> **Version:** 1.0  
> **Data:** 1,625 Design Decisions across 21 components

---

## Overview

This tool provides a fast, offline-capable interface for the VCF Design Library Excel file. All data is embedded directly in the HTML — no server, no dependencies, just open `VCF-DD-Library.html` in any modern browser.

---

## Features

| Feature | Description |
|---|---|
| 🔍 **Search & Filter** | Full-text search across all fields. Filter by Component, Type, Category, Status and Criticality |
| ⊞ **Group by Category** | Toggle category grouping with collapsible sections |
| ↔ **Resizable Columns** | Drag column borders to adjust width |
| ✏️ **Edit Design Decisions** | Edit any field: Type, Status, Criticality, Justification, Implication, Notes |
| ⭐ **Mark for Export** | Star individual rows or bulk-mark a selection. Stats by component shown in sidebar |
| 📤 **Excel Export** | Export marked / selected / filtered decisions in the original Excel format |
| 📥 **Import Excel** | Drag & drop or browse to import an updated Design Library `.xlsx` |
| ＋ **Temporary DD** | Add custom Design Decisions for the session (marked TEMP, lost on reload) |
| 📝 **Bulk Notes** | Apply notes to all selected Design Decisions at once |
| 🌙 **Dark Theme** | Toggle dark/light mode — preference persisted in `localStorage` |
| 📱 **Responsive** | Sidebar collapses to a slide-in drawer on mobile/tablet |
| 🔢 **Statistics** | Per-component count of marked DDs shown in the sidebar |

---

## Usage

### Open locally
Simply double-click `VCF-DD-Library.html` — no installation required.

### Import an updated library
Click **Import Excel** in the header and select a `.xlsx` file with the same structure as the original VCF Design Library.

### Export your selection
1. Star the Design Decisions you want with the ⭐ button on each row, or select rows and click **Mark for Export**
2. Click **Export Marked** in the header — an `.xlsx` file is downloaded in the original format

### Edit a Design Decision
Select a single row (click or checkbox) and click **✏️ Edit** to open the edit modal. All fields including Type are editable.

### Bulk edit notes
Select multiple rows and click **📝 Edit Notes** to apply a note to all selected DDs at once.

---

## File Structure

```
VCF-DD-Library.html   ← Full app with embedded data (open this)
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

*Generated with [Claude](https://claude.ai)*
