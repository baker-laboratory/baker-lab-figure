# IPD/Baker Lab figure profile

This file is an always-loaded customization of the upstream `nature-figure`
workflow. Apply it to every figure task in this installed variant. The fixed
Python/Matplotlib backend and the prohibition on R/Seaborn plotting are profile
invariants, not per-task preferences. For all other rule conflicts, use this
order:

1. Mandatory requirements of the exact target journal and submission stage.
2. The user's explicit instructions for the current task, except a request to
   replace the fixed quantitative plotting backend.
3. The IPD/Baker Lab rules in this profile.
4. The remaining upstream `nature-figure` defaults.

Read `references/ipd-baker-figure-requirements.md` when planning, generating,
revising, assembling, or auditing an IPD/Baker Lab figure, or when the source
and strength of a rule matter.

## Fixed backend for quantitative plots

- For data-driven plots and plot revisions, use Python with Matplotlib only.
  Do not ask the user to choose Python or R, do not call the persisted backend
  preference script, and do not import or generate Seaborn or R plotting code.
- NumPy, pandas, SciPy, and other non-visual Python libraries may be used for
  data handling or statistics. Matplotlib remains the only plotting backend.
- The bundled R and Seaborn-related upstream materials remain in the skill for
  provenance and future upstream merges, but they are inactive for production
  plotting. If a bundled example uses Seaborn, study its scientific or layout
  pattern and reimplement the requested result in Matplotlib.
- The separate upstream AI-schematic/OpenRouter route remains available when
  explicitly requested; it is not a quantitative plotting backend.
- PyMOL or ChimeraX may generate protein-structure renders. Matplotlib may
  assemble or annotate their exported panels. Do not claim that Matplotlib
  generated a three-dimensional molecular rendering that came from another
  program.

## Figure contract and content

- Start from the one scientific question or conclusion the figure must make
  clear. Simplify every panel around that purpose and remove decorative or
  repetitive content that does not support it.
- Set the target journal's final physical width and height before plotting so
  that text, line weights, markers, and raster resolution are judged at their
  delivered size rather than after arbitrary resizing.
- Give colors stable semantic meaning across the paper. Define the mapping in
  the figure contract and keep it consistent across panels and figures.
- Prefer the IPD colors when they fit the scientific roles: purple `#4b2e83`,
  cyan `#4196b5`, and magenta `#b41f85`. Journal requirements, accessibility,
  and the user's explicit semantic mapping take priority. Do not force all
  three colors into every figure.
- Label every color or encoding that is necessary to understand the panel.
  When color alone would be ambiguous or inaccessible, add a redundant cue
  such as marker shape, line style, direct label, or lightness difference.

## Typography, captions, and whitespace

- At final publication size, use Arial approximately 6 pt for internal figure
  text unless the journal requires another size. A 5 pt rendered-glyph floor
  remains a blocking QA minimum, not the preferred IPD default.
- The IPD recommendation of Arial 9 pt with a bold figure title applies to the
  manuscript figure caption/legend. Do not draw the full caption inside the
  plotting canvas unless the user or journal explicitly requests that layout.
- Make the caption self-contained enough to identify every panel, encoding,
  sample, denominator, error-bar definition, statistical test, and abbreviation
  needed to interpret the figure.
- Reduce uninformative whitespace without crowding labels or uncertainty. Use
  alignment and distribution deliberately when combining panels.

## Data panels

- Label axes and units, and choose major and minor ticks that match the data.
- For SEC traces or other instrument-exported curves, preserve the raw export,
  export tabular data such as CSV when possible, and replot it in Matplotlib so
  typography and semantic colors match the rest of the paper. This implements
  the Wiki's intent to avoid inconsistent instrument-default plots while
  honoring the user's Matplotlib-only backend choice.
- Do not infer or reconstruct quantitative values from pixels when source data
  or plotting code is required for a defensible revision.

## Protein-structure panels

- Use PyMOL or ChimeraX for new protein-structure renders when those tools are
  available. Avoid their unmodified default colors and orientations.
- Choose orientation and zoom to expose the design feature, interface, motif,
  conformational change, or comparison that supports the figure's claim.
- Keep structure colors consistent with the manuscript and label them clearly.
- Treat trajectory movies as a separate supplementary deliverable and preserve
  their rendering commands and provenance.

## Assembly and final-size QA

- Matplotlib is the reproducible default for automatic multi-panel assembly.
  Inkscape remains an acceptable IPD-standard manual finishing tool when the
  user wants vector editing; preserve editable text and source provenance.
- Use align/distribute operations or equivalent measured layout constraints so
  comparable panels have intentional edges, sizes, and gutters.
- Inspect every panel and the complete figure at final physical size. When a
  physical printout is available, print the entire figure to assess resolution
  and readability. Otherwise inspect at 100% final size and report that a
  physical print check was not performed.
- Continue to run all upstream source, panel-alignment, PDF-text, and collision
  QA gates. Passing automation does not replace final visual inspection.
