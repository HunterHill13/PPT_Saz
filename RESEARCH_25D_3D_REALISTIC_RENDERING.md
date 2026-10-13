# Research Report: True Dimensional & Visual Paradigm Diversity in PowerPoint (2.5D Isometric, 3D Volumetric / Claymorphism, Photorealistic & Tactile Art)

**Date:** October 2026  
**Status:** Completed  
**Author:** AI Presentation Research & Engineering Agent (PPT_Saz Core)

---

## 1. Executive Summary & Root Cause Analysis

### The Problem
Despite introducing 9 distinct layout archetypes and 22 color themes in v5.5, visual inspections revealed that presentations still look predominantly like **"the same flat 2D vector shapes with different color palettes"**.

### Root Cause
1. **Zero Lighting Model & Solid Hex Fills:** 100% of shapes in `art_style_skins.py` and `infographic_layouts.py` use flat single-color hex fills (`fill="#HEX"`). Without surface illumination, light-angle variance, ambient occlusion, or specularity, the human eye inherently classifies them as flat 2D vector wireframes.
2. **Absence of Multi-Face Geometric Extrusion:** Cards, steps, and diagram nodes are rendered as single 2D bounding boxes (even when shaped as polygons or octagons), completely missing the 3-dimensional planar faces (Top, Left, Right/Front) required for 2.5D isometric projection.
3. **Absence of Tactile Photographic/Material Textures:** Realistic and editorial themes lack genuine organic grain, photographic depth-of-field overlays, tactile paper fibers, or brushed metal/marble substrates.

---

## 2. Dimensional Paradigm Matrix: 4 Distinct Visual Realities

To break completely free from "flat 2D recoloring", PPT_Saz must support **4 fundamentally distinct Dimensional Paradigms**:

| Paradigm | Visual Dimensionality | Lighting & Physics | Geometric Architecture | Native PowerPoint Implementation |
| :--- | :--- | :--- | :--- | :--- |
| **1. 2.5D Isometric World** | True 30° Axonometric Projection | Multi-directional key light (`+25%` top luminance, `-15%` left shadow, `-35%` right shadow) | Tri-planar extruded polygon slabs, floating isometric pedestals, isometric grid lines | Native DrawingML `<polygon>` with calculated affine vertices & cast floor shadows |
| **2. 3D Volumetric / Claymorphism** | Tactile 3D Soft-Body & Specular Studios | Phong/Blinn specular highlight + deep soft ambient occlusion drop shadows | Inflated 3D rounded capsules, floating 3D spheres/toruses, glossy bevel rims | Dual layer: DrawingML `<a:gradFill>` (specular linear/radial) + `<a:outerShdw>` OR native OOXML `<a:sp3d>` bevels |
| **3. Photorealistic & Material Texture** | Authentic Cinematic & Photographic Depth | Real-world chiaroscuro, optical lens vignettes, directional ray spotlights | Organic substrates: dark Italian marble, brushed titanium, matte frosted glass, luxury archival paper | High-resolution procedural/photographic texture tiles + glassmorphism multi-layer frosted cards |
| **4. Architectural / Flat Constructivist** | Pure Graphic 2D (Intentional Contrast) | Flat technical drafting, zero faux-3D | Blueprint CAD construction vectors, Swiss grid crosshairs, Neo-brutalist hard black offsets | Retain crisp razor-sharp vector lines to create intentional stylistic contrast |

---

## 3. Deep-Dive: Implementation Mechanics

### 3.1 Paradigm 1: 2.5D Isometric Extrusion Engine
- **Isometric Math:** Standard axonometric projection with $\theta = 30^\circ$ ($\cos 30^\circ \approx 0.866$, $\sin 30^\circ = 0.5$).
- **Extruded Slab Architecture:**
  - **Top Face (Platform):** Lit from overhead, base hex color lightened by 20–30%. This is the canvas where text, badges, and icons reside.
  - **Left Face (Side Wall):** Intermediate shadow face, base hex color shaded by 15–20%.
  - **Right/Front Face (Thickness Wall):** Primary shadow face, base hex color darkened by 35–45%.
  - **Cast Floor Shadow:** A sheared semi-transparent black polygon (`rgba(0,0,0,0.25)`) projected onto the ground plane at $(y + \text{depth} + 12\text{px})$.

### 3.2 Paradigm 2: 3D Volumetric & Claymorphism Engine
- **Lighting Model:**
  - Multi-stop linear gradients simulating curved 3D surfaces (Top highlight $\to$ Body tone $\to$ Reflected rim light).
  - Radial specular highlights simulating a direct studio softbox.
- **Native OOXML 3D Support:**
  - DrawingML natively supports 3D shape beveling via `<a:sp3d extrusionH="25400" prstMaterial="plastic"><a:bevelT w="76200" h="50800" prst="circle"/></a:sp3d>`.
  - Combined with `<a:scene3d><a:camera prst="isometricOffAxis1Top"/><a:lightRig rig="threePt" dir="t"/></a:scene3d>`, PowerPoint natively renders shapes with real hardware-accelerated 3D shading!

### 3.3 Paradigm 3: Photorealistic & Tactile Material Engine
- **Substrates:** Dark obsidian/marble with gold metallic veins, frosted acrylic glass with luminous edge borders, architectural cyanotype blueprint paper, and textured handmade linen.
- **Glassmorphism Over Realism:** A semi-transparent frosted card (`opacity="0.85"`, white border `0.5px`, soft blur shadow) floating over a rich dark photographic/procedural background produces an unmistakable high-end editorial feel.

---

## 4. Next Step: Grill-Me Alignment
We will now engage the user in a structured `/grill-me` session to confirm how these 4 dimensional paradigms should be assigned and controlled across the skill.
