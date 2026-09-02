# Figure contract before plotting

A publication-quality scientific figure is a visual argument, not an isolated pretty plot. Every figure starts from a claim, an evidence hierarchy, and a review-risk check before code or aesthetics. Before generating or editing code, establish the contract below.

## Quantitative backend is fixed

For plotting, charting, data visualization, and code-based plot revision, use
Python with Matplotlib. Do not ask the user to choose Python or R, do not call
the persisted backend preference script, and do not import or generate Seaborn
or R plotting code. NumPy, pandas, SciPy, and other non-visual Python libraries
may support data handling or statistics; Matplotlib remains the only plotting
backend.

The upstream R and Seaborn-related materials remain bundled for provenance and
future merges, not as production routes in this IPD/Baker profile. Reimplement
any useful retained template pattern in Matplotlib.

The explicit AI-schematic/OpenRouter route is separate because it does not plot
quantitative data. PyMOL or ChimeraX may render protein structures, with their
outputs assembled or annotated in the figure workflow.

## Matplotlib is exclusive for quantitative rendering

Every quantitative plotting script, preview, SVG/PDF/TIFF/PNG export, and
visual workaround must be produced with Matplotlib. Other languages may be used
for non-visual file inspection or data conversion only when they do not open a
graphics device, import plotting libraries, create figure files, or change the
final visual appearance.

The backend-neutral `audit_panel_alignment.py`, `audit_pdf_text.py` and
`audit_figure_collisions.py` tools may inspect a layout manifest or final PDF
from either backend. They do not redraw the scientific content. The selected
backend must measure its own final axes/grob geometry before the alignment JSON
is audited. Alignment and collision overlays are QA-only, not previews,
substitute exports or submission assets; keep the original selected-backend
figure authoritative.

## Missing runtime/package rule

Check Python and the required Matplotlib dependencies early. If they are
unavailable, stop before rendering and report the exact blocker. You may provide
a Matplotlib script and installation commands, or ask permission to install
dependencies, but do not fall back to R or Seaborn to make a substitute figure.

## Data-integrity gate

Use all user-provided observations and requested variables unless an exclusion has a scientific or statistical justification or the user explicitly requests a subset. Never reduce data merely to make a plot easier or faster to render. For large point clouds, prefer rasterized marks, hexbin/density representations, aggregation with a stated rule, or another backend-native rendering strategy.

If any row, column, replicate, image, or category is excluded, record the before/after counts, the exact rule, and the reason in the QA notes. Preserve the unmodified source data and never silently select convenient columns to satisfy a template.

Plan figures by scientific claims, not by source tables. Do not turn each table into a separate figure when several tables answer the same question. If an effect is defined within matched datasets, subjects, seeds, or tasks, inspect and visualize paired differences rather than relying only on overlapping marginal distributions; large between-unit heterogeneity can hide a strong paired effect.

## The five-point contract

1. **Core conclusion**: write the one-sentence claim the figure must defend and the Results-level scientific question it answers.
2. **Evidence chain**: map each planned panel to one distinct inferential role in that claim, and drop, merge, or demote panels that only redraw another panel's evidence or repeat it under a secondary metric.
3. **Archetype**: classify the figure as `quantitative grid`, `schematic-led composite`, `image plate + quant`, or `asymmetric mixed-modality figure`.
4. **Backend**: use Python/Matplotlib exclusively for quantitative figure drawing, previewing, exporting, and visual QA. Keep AI schematics and PyMOL/ChimeraX structure rendering identified as separate source routes.
5. **Journal/export contract**: set final dimensions, a 5 pt floor for every rendered glyph, editable text, source data, statistics, image-integrity notes, export formats, a blocking multi-panel alignment gate, and automatic rendered collision QA before styling.

The highest-priority rule is: **the chart serves the scientific logic**. Aesthetic polish, template matching, and complex layout are subordinate to making the core conclusion clear, defensible, and reviewable.

For the full method to convert a request into core conclusion, evidence hierarchy, panel map, and review-risk checks, open `references/figure-contract.md`.
For a labelled multi-panel figure or a manuscript-level figure sequence, also
open `references/multipanel-evidence-architecture.md`: use one figure-level
claim as the planning default, give panels complementary evidence roles, and
align successive figures with the Results claim escalation.
