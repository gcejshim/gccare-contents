# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**GC Care 카드뉴스 편집기** - Self-contained HTML editor for creating health card news. Single-file architecture with embedded CSS/JS/html2canvas. Exported files are fully functional editors (self-replicating). No backend required.

**Files:**
- `cardnews_editor.html` - Template editor
- `card01-06.html` - Individual card editors (pre-populated with Excel data)

---

## Architecture

**State Management:**
- `DEFAULTS` - Array of section objects (no, title, body)
- `headerImageURL` - Base64 image or null
- `sectionImages` - Object of section images by index
- `gExportDirHandle` - File System API handle (session memory only)

**Key Functions:**
- `exportHTML()` - Prompt filename → folder → save HTML with state injected
- `saveImage()` - Prompt folder (if needed) → render canvas → save JPG
- `update()` - Read form inputs → update preview
- `buildSectionForms()` / `buildPreviewSections()` - Regenerate UI from DEFAULTS

**Export Flow:**
1. User clicks "HTML 저장" → enters filename → folder selection (if needed)
2. Full DOM serialized with current state (`DEFAULTS`, images) injected
3. Saved to user-selected folder with matching `.jpg` filename
4. Both HTML and IMAGE use same `gExportDirHandle` for consistency

---

## Common Tasks

**Modify Editor:**
- Add/remove sections: Edit `DEFAULTS` array (line ~773)
- Change labels: Update `buildSectionForms()` HTML
- Update styling: Edit `<style>` block
- Pre-populate content: Set custom `DEFAULTS` in `cardXX.html`

**Generate Images:**
```bash
python3 generate_images.py --card 1
```
Creates `images/card01/header.png` + `sec_01-06.png` (Jalnan.ttf font)

---

## Quirks & Limits

- **Session-only**: `gExportDirHandle` lost on page refresh (next save prompts again)
- **File size**: No images ~2MB, with base64 images ~7.6MB+
- **Images**: Paste works in Chrome; drag-drop more universal
- **Nesting**: Exported files can export again (no depth limit)
- **Filenames**: `card02.html` → `card02.jpg` (dynamic matching)

---

## Recent Changes

- ✅ User-specified filenames for exports
- ✅ Unified folder selection (HTML + IMAGE save use same folder)
- ✅ Removed "저장 위치" button (on-demand folder selection)
- ✅ All 6 card files have matching functionality

