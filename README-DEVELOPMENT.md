# Development, installation, and testing

## Development model

This is an Apache-2.0-derived customization of the upstream `nature-figure`
skill. Preserve milestone commits for:

1. an unchanged upstream import;
2. IPD/Baker policy and backend customization;
3. test-supported fixes and release verification.

Keep the complete upstream `nature-shared` dependency vendored at
`nature-figure/vendor/nature-shared`. Do not update only `SKILL.md`; the router
depends on the manifest, static fragments, references, scripts, assets, and
vendored shared resources.

## Installation

Install or copy the complete `nature-figure` directory. Its full upstream
`nature-shared` dependency is already included under `vendor/`, so no
installation-time sibling path is required.

The quantitative plotting profile requires Python and Matplotlib. PyMuPDF is
required for the automatic PDF collision audit:

```bash
python -m pip install -r nature-figure/requirements.txt
```

The upstream OpenRouter route and non-Python materials retain their own
optional dependencies.

The normalized operational rules from the user-supplied IPD figure guidance are
kept in `references/ipd-baker-figure-requirements.md`. The raw internal HTML is
intentionally excluded from the public distribution; maintain provenance in a
private authorized archive instead of adding the source export to this repository.

## Validation

From the directory containing both skills, run:

```bash
python <skill-creator>/scripts/quick_validate.py nature-figure
python <skill-creator>/scripts/quick_validate.py nature-figure/vendor/nature-shared
python -m unittest discover -s nature-figure/tests -p 'test_*.py'
python -m unittest discover -s nature-figure/vendor/nature-shared/tests -p 'test_*.py'
git diff --check
```

For a behavioral smoke test, generate a Matplotlib figure at final physical
size, export PDF/SVG/TIFF, run the panel-alignment gate when multi-panel, then
run `validate_figure.py --profile ipd-baker`, `audit_pdf_text.py`, and
`audit_figure_collisions.py` on the final artifacts. Inspect the rendered output
at final size; automation does not replace visual QA.

## Upstream updates

Read `UPSTREAM.md` before updating. Import upstream changes as their own
milestone commit, preserve the IPD/Baker profile as a separate layer, rerun the
full validation and rendering tests, and record any policy conflict explicitly.
