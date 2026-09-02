# IPD/Baker Lab figure requirements

Use this reference for IPD/Baker Lab figure planning, generation, revision,
assembly, or audit. It records the source requirements and their operational
interpretation in this customized `nature-figure` installation.

## Authority and precedence

The source was a user-supplied export of internal IPD figure guidance, inspected
locally in August 2026. The source title, internal page path, raw export, private
links, images, and access details are intentionally not redistributed or
identified in this public repository. Separate private visualization notes were
not supplied and must not be represented as inspected.

Treat the fixed Python/Matplotlib backend and the prohibition on R/Seaborn
plotting as invariants of this customized profile. For other requirements,
apply mandatory target-journal rules first, then the user's explicit current
instructions, then these IPD/Baker recommendations, then general upstream
`nature-figure` guidance.

## Normalized checklist

### General good practices

- Check the target journal's figure formatting before beginning.
- Set the final physical figure width and height before composing the figure.
- Use Arial approximately 9 pt for the manuscript caption, with a bold figure
  title, and Arial approximately 6 pt for internal figure text when the journal
  permits.
- Choose a paper-wide color system and standardize the purpose of every color.
- Suggested IPD colors are purple `#4b2e83`, cyan `#4196b5`, and magenta
  `#b41f85`.
- A custom palette may be used when it better fits the data, accessibility, or
  journal requirements; record its semantic mapping.
- Make the figure caption sufficiently descriptive for the reader to interpret
  the panels and encodings.
- Reduce uninformative whitespace and inspect a physical printout when possible.
- Simplify the figure around the question: *What am I trying to show?*

### Protein-structure panels

- Generate structure images with PyMOL or ChimeraX when available.
- Do not use unmodified program-default colors and orientations.
- Choose orientation and zoom purposefully to show what is scientifically
  important about the design or protein.
- Label all colors and keep them meaningful in the manuscript context.
- Preserve commands and provenance for supplementary trajectory movies.

The internal source noted separate private guidance for structure rendering and
trajectory preparation. That material is excluded from this public release; do
not invent or attribute its contents.

### Plotted-data panels

- Label axes properly and select major/minor ticks appropriate for the data.
- For SEC traces, export the instrument data as CSV and replot it in a common
  plotting workflow rather than using inconsistent internal SEC plotting
  output. The Wiki names GraphPad or similar software. This customized skill
  implements that intent with Python/Matplotlib.

### Combining panels

- The Wiki identifies Inkscape as the standard IPD tool for assembling figures.
- Use align and distribute operations to create intentional, professional panel
  geometry.
- Print the entire final figure to assess resolution when physical printing is
  available; otherwise inspect it at final physical size on screen.
- Separate private assembly notes mentioned by the source are excluded from
  this public release; do not represent them as inspected.

### Example provenance

The Wiki identifies the RFdiffusion paper as an example of these practices:

- Watson, J. L. et al. *De novo design of protein structure and function with
  RFdiffusion*. Nature 620, 1089–1100 (2023).
- https://www.nature.com/articles/s41586-023-06415-8

Use the paper as an example, not as a source of additional mandatory IPD rules
unless its figures are actually inspected for the current task.

## Operational audit record

For an IPD/Baker figure, record:

1. target journal, stage, and final dimensions;
2. one-sentence figure claim and panel evidence roles;
3. color-to-meaning mapping and accessibility redundancy;
4. final internal font sizes and caption handling;
5. axis labels, units, ticks, sample sizes, denominators, error bars, and tests;
6. structure-rendering program, orientation rationale, and color labels when
   applicable;
7. source-data and code provenance, including instrument-export transformations;
8. panel alignment, whitespace, PDF text, collision, final-size, and physical
   print status.
