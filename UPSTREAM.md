# Upstream provenance

This customized skill vendors the complete upstream `nature-figure` skill and
its complete `nature-shared` dependency from:

- Repository: https://github.com/Yuan1z0825/nature-skills
- Upstream commit: `8630593a086755d2003cbd1a79cd1118c6963202`
- Imported: 2026-08-27
- Upstream license: Apache License 2.0

The unmodified sibling-layout import is preserved in Git commit `7454492`.
For installation stability, a later packaging commit moves the complete
`nature-shared` directory under `nature-figure/vendor/` and updates only the
dependency paths. Later commits add
an IPD/Baker Lab profile, fix quantitative plotting to Python/Matplotlib, and
add profile-specific validation. Upstream R, Seaborn-related examples,
OpenRouter routes, assets, references, and the full vendored shared dependency
remain in the repository for provenance and future upstream merges; the customized
routing rules determine which paths are active for production figure work.

When updating from upstream, first compare against the pinned commit above,
import upstream changes without mixing them with local policy changes, and then
reapply or reconcile the IPD/Baker customization in a separate commit.
