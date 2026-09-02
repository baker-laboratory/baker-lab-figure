# External figure references

Use this file when a user cites `figures4papers`, the older
`scientific-figure-making` skill, or another public figure as a visual reference.

Third-party scripts, preview images, and manuscript-specific assets are not
bundled in this public repository because the referenced project did not expose
a redistribution license when this release was prepared. Inspect the current
upstream source and terms directly:

- Project: `figures4papers`
- Upstream: <https://github.com/ChenLiu-1996/figures4papers>

## Use boundary

1. Treat external figures as references for layout grammar, hierarchy, palette,
   axes, legends, and export structure—not as templates whose code or assets can
   automatically be copied.
2. Reimplement the selected pattern with original Python/Matplotlib code and the
   user's own data unless the current upstream license or written permission
   clearly authorizes reuse.
3. Never reuse manuscript-specific labels, metric values, statistical results,
   or visual assets as placeholders for evidence.
4. Record external references and implementation provenance in the QA record
   when they materially influence the result.
5. Preserve the editable SVG/PDF/TIFF and source-data requirements from
   `api.md` and `qa-contract.md`.

## Repository-owned implementation paths

| Requested pattern | Open and use |
|---|---|
| Grouped bars, ablation bars, shared legends | `tutorials.md`, `common-patterns.md` |
| Radar or polar comparison | `chart-types.md`, then implement with original code |
| Trends, sweeps, and reference baselines | `tutorials.md`, `chart-types.md` |
| Heatmap or annotated matrix | `tutorials.md`, `template-catalog.md` |
| Probability or manifold concept panel | `chart-types.md` |
| Submission typography, palette, and export | `api.md`, `design-theory.md` |
| CSV-driven reproducible plots | `template-catalog.md`, `../scripts/plot_templates.py` |

Check the current source license and obtain permission when required before
redistributing, modifying, or publishing third-party materials or close
derivatives.
