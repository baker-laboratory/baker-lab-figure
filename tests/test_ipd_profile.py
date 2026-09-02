from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path


SKILL = Path(__file__).parents[1]
MANIFEST = SKILL / "manifest.yaml"


def yaml_block(source: str, key: str, indent: int) -> str:
    """Return one indentation-delimited YAML mapping/list block.

    The profile tests intentionally avoid a PyYAML test dependency. The
    manifest subset checked here uses ordinary indentation and scalar values,
    so an indentation-delimited block is sufficient and keeps this test
    runnable with the skill's declared runtime dependencies alone.
    """

    lines = source.splitlines()
    header = " " * indent + f"{key}:"
    try:
        start = next(index for index, line in enumerate(lines) if line == header)
    except StopIteration as exc:
        raise AssertionError(f"missing YAML block: {key!r} at indent {indent}") from exc

    body: list[str] = []
    for line in lines[start + 1 :]:
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            body.append(line)
            continue
        current_indent = len(line) - len(stripped)
        if current_indent <= indent:
            break
        body.append(line)
    return "\n".join(body)


class IpdProfileStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = MANIFEST.read_text(encoding="utf-8")

    def test_ipd_profile_is_always_loaded(self):
        always_load = yaml_block(self.manifest, "always_load", 0)
        self.assertIn("static/core/ipd-baker-profile.md", always_load)

    def test_quantitative_backend_is_fixed_to_matplotlib_without_prompt(self):
        profile = yaml_block(self.manifest, "profile", 0)
        quantitative = yaml_block(profile, "quantitative_backend", 2)
        self.assertRegex(quantitative, r"(?m)^\s{4}language:\s*python\s*$")
        self.assertRegex(quantitative, r"(?m)^\s{4}library:\s*matplotlib\s*$")
        self.assertRegex(quantitative, r"(?m)^\s{4}ask_user:\s*false\s*$")
        self.assertRegex(quantitative, r"(?m)^\s{4}use_saved_preference:\s*false\s*$")
        self.assertIn("- seaborn", quantitative)
        self.assertIn("- r", quantitative)

        backend_values = yaml_block(self.manifest, "values", 4)
        self.assertRegex(
            backend_values,
            r"(?m)^\s{6}python:\s+static/fragments/backend/python\.md\s*$",
        )
        self.assertNotRegex(backend_values, r"(?m)^\s{6}r:\s*")

        preference = yaml_block(self.manifest, "preference", 0)
        self.assertIn("Retained for upstream compatibility only", preference)
        self.assertIn("do not ask for a backend preference", preference)

    def test_upstream_r_materials_remain_bundled_but_inactive(self):
        retained_r_files = (
            SKILL / "static/fragments/backend/r.md",
            SKILL / "references/r-workflow.md",
            SKILL / "references/r-template-index.md",
            SKILL / "scripts/panel_alignment.R",
        )
        for path in retained_r_files:
            self.assertTrue(path.is_file(), f"missing retained upstream resource: {path}")

        unbundled_seaborn = (
            SKILL
            / "assets/figures4papers/figure_ophthal_review/plot_composition.py"
        )
        self.assertFalse(unbundled_seaborn.exists())
        demos = (SKILL / "references/demos.md").read_text(encoding="utf-8")
        self.assertIn("not bundled", " ".join(demos.split()))

        always_load = yaml_block(self.manifest, "always_load", 0)
        backend_values = yaml_block(self.manifest, "values", 4)
        self.assertNotIn("static/fragments/backend/r.md", always_load)
        self.assertNotIn("static/fragments/backend/r.md", backend_values)
        self.assertNotIn(str(unbundled_seaborn.relative_to(SKILL)), self.manifest)
        self.assertIn(
            "upstream maintenance of the retained R workflow only; never for a production",
            self.manifest,
        )

    def test_openrouter_ai_route_is_preserved(self):
        route = yaml_block(self.manifest, "openrouter_image_generation", 2)
        self.assertIn("references/openrouter-image-generation.md", route)
        self.assertIn("scripts/generate_openrouter_schematic.py", route)
        self.assertTrue((SKILL / "references/openrouter-image-generation.md").is_file())
        self.assertTrue((SKILL / "scripts/generate_openrouter_schematic.py").is_file())

    def test_complete_shared_dependency_is_vendored_with_resolvable_routes(self):
        shared = SKILL / "vendor/nature-shared"
        for relative in (
            "SKILL.md",
            "core/nature-results-discussion.md",
            "core/research-compliance.md",
            "journal-formats/nature-machine-intelligence.md",
            "scripts/check_consistency.py",
            "tests/test_check_consistency.py",
        ):
            self.assertTrue((shared / relative).is_file(), relative)

        skill_router = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        multipanel = (SKILL / "references/multipanel-evidence-architecture.md").read_text(
            encoding="utf-8"
        )
        nature_rules = (SKILL / "references/nature-article-requirements.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "vendor/nature-shared/journal-formats/nature-machine-intelligence.md",
            self.manifest,
        )
        self.assertIn("vendor/nature-shared/core/nature-results-discussion.md", skill_router)
        self.assertIn("../vendor/nature-shared/core/nature-results-discussion.md", multipanel)
        self.assertIn("../vendor/nature-shared/core/research-compliance.md", nature_rules)
        self.assertNotIn("../nature-shared/", "\n".join((self.manifest, skill_router)))

    def test_ipd_palette_and_six_point_default_are_encoded(self):
        profile = (SKILL / "static/core/ipd-baker-profile.md").read_text(encoding="utf-8")
        backend = (SKILL / "static/fragments/backend/python.md").read_text(encoding="utf-8")
        templates = (SKILL / "scripts/plot_templates.py").read_text(encoding="utf-8")
        combined = "\n".join((profile, backend, templates)).lower()

        for color in ("#4b2e83", "#4196b5", "#b41f85"):
            self.assertIn(color, combined)
        self.assertIn('"font.size": 6', backend)
        self.assertIn('"axes.labelsize": 6', backend)
        self.assertIn('"xtick.labelsize": 6', backend)
        self.assertIn('"ytick.labelsize": 6', backend)
        self.assertIn('"legend.fontsize": 6', backend)
        self.assertIn("IPD_PALETTE", templates)
        self.assertNotIn("#2166AC", templates)
        self.assertNotIn("#B2182B", templates)
        self.assertIn("require_matplotlib_panel_alignment", templates)

    def test_active_matplotlib_guidance_preserves_declared_canvas(self):
        active_files = (
            "SKILL.md",
            "README.md",
            "README_EN.md",
            "static/core/contract.md",
            "static/core/stance.md",
            "static/core/ipd-baker-profile.md",
            "static/fragments/backend/python.md",
            "references/api.md",
            "references/design-theory.md",
            "references/qa-contract.md",
            "references/ipd-baker-figure-requirements.md",
            "scripts/plot_templates.py",
        )
        tight_export = re.compile(
            r"savefig\s*\([^)]*bbox_inches\s*=\s*['\"]tight['\"]",
            re.DOTALL,
        )
        offenders: list[str] = []
        for relative in active_files:
            source = (SKILL / relative).read_text(encoding="utf-8")
            if relative.endswith(".py"):
                tree = ast.parse(source)
                has_tight_export = any(
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "savefig"
                    and any(
                        keyword.arg == "bbox_inches"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value == "tight"
                        for keyword in node.keywords
                    )
                    for node in ast.walk(tree)
                )
            else:
                has_tight_export = bool(tight_export.search(source))
            if has_tight_export:
                offenders.append(relative)
        self.assertEqual(
            offenders,
            [],
            "active IPD/Matplotlib guidance must repair layout without changing "
            f"the declared physical canvas; offenders: {offenders}",
        )


if __name__ == "__main__":
    unittest.main()
