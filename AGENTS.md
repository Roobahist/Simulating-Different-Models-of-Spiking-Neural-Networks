# Repository guidance

This is an educational neuroscience simulation archive with an actively maintained standalone Python reference implementation.

- Read \x60README.md\x60 and \x60docs/experiments.md\x60 before changing models or notebook mappings.
- Source package lives under \x60src/spiking_models/\x60. Keep numerical computation independent of plotting and the CLI.
- \x60simulation.simulate\x60 is the single high-level solver. Supply current as a callable; inject random generators rather than relying on hidden global state.
- Keep model parameters in \x60NeuronParameters\x60, time parameters in \x60SimulationSettings\x60, and user flags in the CLI. Preserve meaningful mathematical constants.
- Treat \x60legacy_adaptive\x60 as a separately defined **nonstandard** adaptation rule; do not silently substitute standard AdEx.
- Historical Jupyter notebooks, raw images, compressed submissions, and reports are provenance. Avoid rewriting them or claiming results were replicated without a measured comparison.
- Add narrow tests for model updates and bad inputs. Run \x60python -m unittest discover -s tests -v\x60 and \x60ruff check src tests\x60.
- Optional Brian2 and Matplotlib dependencies belong behind extras. Don't introduce infrastructure or Docker without an actual runtime need.
- Use Python snake_case names and short comments explaining mathematical constraints or surprising historical choices.
- Never commit credentials, local environments, generated outputs, or notebook checkpoints.
