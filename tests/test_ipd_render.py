from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib


matplotlib.use("Agg", force=True)

import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


SKILL = Path(__file__).parents[1]
WIDTH_MM = 183.0
HEIGHT_MM = 55.0
DPI = 600
IPD_COLORS = ("#4b2e83", "#4196b5", "#b41f85")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ALIGNMENT = load_module(
    "nature_figure_ipd_alignment_test",
    SKILL / "scripts/audit_panel_alignment.py",
)
COLLISIONS = load_module(
    "nature_figure_ipd_collision_test",
    SKILL / "scripts/audit_figure_collisions.py",
)
PDF_TEXT = load_module(
    "nature_figure_ipd_pdf_text_test",
    SKILL / "scripts/audit_pdf_text.py",
)
VALIDATOR = load_module(
    "nature_figure_ipd_validator_test",
    SKILL / "scripts/validate_figure.py",
)


STATIC_SMOKE_SOURCE = r'''
import matplotlib as mpl
import matplotlib.pyplot as plt
from audit_panel_alignment import require_matplotlib_panel_alignment

IPD_COLORS = ("#4b2e83", "#4196b5", "#b41f85")
width_mm = 183
height_mm = 55

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 6,
    "axes.labelsize": 6,
    "axes.titlesize": 7,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
})

fig, axes = plt.subplots(1, 2, figsize=(width_mm / 25.4, height_mm / 25.4))
axes[0].plot([0, 1, 2, 3], [0.20, 0.45, 0.55, 0.67], color=IPD_COLORS[0])
axes[0].plot([0, 1, 2, 3], [0.15, 0.28, 0.40, 0.52], color=IPD_COLORS[1])
axes[1].plot([0, 1, 2, 3], [0.75, 0.64, 0.48, 0.31], color=IPD_COLORS[2])
for ax in axes:
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Response (a.u.)")
require_matplotlib_panel_alignment(fig, strict=True)
fig.savefig("ipd_smoke.svg")
fig.savefig("ipd_smoke.pdf")
fig.savefig("ipd_smoke.tiff", dpi=600)
'''


def dimension_in_points(value: str) -> float:
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)pt", value)
    if not match:
        raise AssertionError(f"expected an SVG dimension in points, got {value!r}")
    return float(match.group(1))


class IpdMatplotlibRenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="nature-figure-ipd-test-")
        cls.output_dir = Path(cls.temporary.name)
        cls.pdf = cls.output_dir / "ipd_smoke.pdf"
        cls.svg = cls.output_dir / "ipd_smoke.svg"
        cls.tiff = cls.output_dir / "ipd_smoke.tiff"
        cls.alignment_json = cls.output_dir / "ipd_smoke.alignment.json"
        cls.alignment_svg = cls.output_dir / "ipd_smoke.alignment.svg"

        rc = {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 6,
            "axes.labelsize": 6,
            "axes.titlesize": 7,
            "xtick.labelsize": 6,
            "ytick.labelsize": 6,
            "legend.fontsize": 6,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
        }
        with mpl.rc_context(rc):
            fig, axes = plt.subplots(
                1,
                2,
                figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4),
            )
            fig.subplots_adjust(left=0.10, right=0.98, bottom=0.23, top=0.88, wspace=0.42)
            x = [0, 1, 2, 3]
            axes[0].plot(
                x,
                [0.20, 0.45, 0.55, 0.67],
                color=IPD_COLORS[0],
                marker="o",
                linewidth=1.1,
                markersize=3,
            )
            axes[0].plot(
                x,
                [0.15, 0.28, 0.40, 0.52],
                color=IPD_COLORS[1],
                marker="s",
                linewidth=1.1,
                markersize=3,
            )
            axes[1].plot(
                x,
                [0.75, 0.64, 0.48, 0.31],
                color=IPD_COLORS[2],
                marker="o",
                linewidth=1.1,
                markersize=3,
            )
            for index, ax in enumerate(axes):
                ax.set_xlabel("Time (min)")
                ax.set_ylabel("Response (a.u.)")
                ax.set_xticks(x)
                ax.set_ylim(0, 1)
                ax.text(
                    0.03,
                    0.96,
                    chr(ord("a") + index),
                    transform=ax.transAxes,
                    va="top",
                    fontsize=6,
                    fontweight="bold",
                )

            fig.canvas.draw()
            cls.line_colors = tuple(
                line.get_color().lower() for ax in axes for line in ax.lines
            )
            cls.text_sizes = tuple(
                text.get_fontsize()
                for ax in axes
                for text in (
                    ax.xaxis.label,
                    ax.yaxis.label,
                    *ax.get_xticklabels(),
                    *ax.get_yticklabels(),
                    *ax.texts,
                )
            )
            cls.alignment_report = ALIGNMENT.require_matplotlib_panel_alignment(
                fig,
                json_out=cls.alignment_json,
                overlay_svg=cls.alignment_svg,
                tolerance_pt=1.5,
                gutter_tolerance_pt=1.5,
                strict=True,
            )
            # Deliberately omit bbox_inches="tight": the declared physical
            # canvas is part of the IPD figure contract.
            fig.savefig(cls.svg)
            fig.savefig(cls.pdf)
            fig.savefig(cls.tiff, dpi=DPI)
            plt.close(fig)

        cls.collision_report = COLLISIONS.audit_pdf(cls.pdf)
        cls.pdf_text_report = PDF_TEXT.audit_pdf(cls.pdf.read_bytes(), minimum_pt=5.0)
        cls.validator_findings = {
            row.check_id: row
            for row in VALIDATOR.validate_source(
                STATIC_SMOKE_SOURCE,
                "python",
                profile="ipd-baker",
            )
        }

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_exports_all_required_formats(self):
        for path in (self.svg, self.pdf, self.tiff):
            self.assertTrue(path.is_file())
            self.assertGreater(path.stat().st_size, 0)

    def test_declared_physical_canvas_is_preserved(self):
        expected_width_pt = WIDTH_MM / 25.4 * 72.0
        expected_height_pt = HEIGHT_MM / 25.4 * 72.0

        try:
            import pymupdf as fitz
        except ImportError:  # PyMuPDF historically exported the module as fitz.
            import fitz  # type: ignore[no-redef]

        with fitz.open(self.pdf) as document:
            page = document[0]
            self.assertAlmostEqual(page.rect.width, expected_width_pt, delta=0.02)
            self.assertAlmostEqual(page.rect.height, expected_height_pt, delta=0.02)

        svg_root = ET.parse(self.svg).getroot()
        self.assertAlmostEqual(
            dimension_in_points(svg_root.attrib["width"]),
            expected_width_pt,
            delta=0.02,
        )
        self.assertAlmostEqual(
            dimension_in_points(svg_root.attrib["height"]),
            expected_height_pt,
            delta=0.02,
        )

        raster = mpimg.imread(self.tiff)
        expected_width_px = int(WIDTH_MM / 25.4 * DPI)
        expected_height_px = int(HEIGHT_MM / 25.4 * DPI)
        self.assertAlmostEqual(raster.shape[1], expected_width_px, delta=1)
        self.assertAlmostEqual(raster.shape[0], expected_height_px, delta=1)

    def test_ipd_colors_and_six_point_text_are_rendered(self):
        self.assertEqual(self.line_colors, IPD_COLORS)
        self.assertTrue(self.text_sizes)
        self.assertEqual(set(self.text_sizes), {6.0})

        svg_source = self.svg.read_text(encoding="utf-8").lower()
        for color in IPD_COLORS:
            self.assertIn(color, svg_source)

    def test_existing_qa_gates_accept_the_smoke_figure(self):
        self.assertEqual(self.alignment_report["verdict"], "PASS")
        self.assertEqual(self.alignment_report["summary"]["fail"], 0)
        self.assertEqual(self.alignment_report["summary"]["warn"], 0)
        self.assertTrue(self.alignment_json.is_file())
        self.assertTrue(self.alignment_svg.is_file())
        persisted_alignment = json.loads(self.alignment_json.read_text(encoding="utf-8"))
        self.assertEqual(persisted_alignment["verdict"], "PASS")

        self.assertTrue(self.collision_report["auditable"])
        self.assertEqual(self.collision_report["summary"]["fail"], 0)
        self.assertEqual(self.collision_report["verdict"], "PASS")

        self.assertTrue(self.pdf_text_report["auditable"])
        self.assertEqual(self.pdf_text_report["below_minimum_count"], 0)
        self.assertGreaterEqual(self.pdf_text_report["minimum_found_pt"], 5.0)

        failures = {
            check_id: row.message
            for check_id, row in self.validator_findings.items()
            if row.level == "FAIL"
        }
        self.assertEqual(failures, {})
        self.assertEqual(
            self.validator_findings["PANEL-ALIGNMENT-GATE"].level,
            "PASS",
        )
        self.assertEqual(
            self.validator_findings["BACKEND-EXCLUSIVE"].level,
            "PASS",
        )
        for check_id in (
            "IPD-BACKEND",
            "IPD-NO-SEABORN",
            "IPD-PHYSICAL-CANVAS",
            "IPD-PALETTE",
            "IPD-FONT-DEFAULT",
        ):
            self.assertEqual(self.validator_findings[check_id].level, "PASS", check_id)


if __name__ == "__main__":
    unittest.main()
