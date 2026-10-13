# Repository guidance

This is an educational neuroscience simulation archive with an actively maintained standalone Python reference implementation.

- Read `README.md` and `docs/experiments.md` before changing models or notebook mappings.
- Source package lives under `src/spiking_models/`. Keep numerical computation independent of plotting and the CLI.
- `simulation.simulate` is the single high-level solver. Supply current as a callable; inject random generators rather than relying on hidden global state.
- Keep model parameters in `NeuronParameters`, time parameters in `SimulationSettings`, and user flags in the CLI. Preserve meaningful mathematical constants.
- Treat `legacy_adaptive` as a separately defined **nonstandard** adaptation rule; do not silently substitute standard AdEx.
- Historical Jupyter notebooks, raw images, compressed submissions, and reports are provenance. Avoid rewriting them or claiming results were replicated without a measured comparison.
- Add narrow tests for model updates and bad inputs. Run `python -m unittest discover -s tests -v` and `ruff check src tests`.
- Optional Brian2 and Matplotlib dependencies belong behind extras. Don't introduce infrastructure or Docker without an actual runtime need.
- Use Python snake_case names and short comments explaining mathematical constraints or surprising historical choices.
- Never commit credentials, local environments, generated outputs, or notebook checkpoints.
