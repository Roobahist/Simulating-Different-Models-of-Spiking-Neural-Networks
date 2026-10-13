# Engineering audit

## Baseline inspection

The 2022 repository had one initial Git commit and no root README, dependency manifest, automated tests, or CI. Its principal work was organized as six single-neuron notebooks, two network notebooks, and six synaptic-plasticity notebooks. Additional Jupyter checkpoints, figures, PDF/DOCX reports, PowerPoint slides, and compressed submissions were present.

The first project implements single-neuron LIF, exponential integrate-and-fire, and a custom adaptation variant. The other projects use Brian2 networks, connectivity, decision modeling, STDP, and pattern experiments. Many notebooks rely on global random state, hardcoded parameters, plotting side effects, and interactive calls.

## Implemented

- Renamed and reorganized all 53 original files with identical blob hashes and no deleted historical data.
- Added a small, installable standard-library single-neuron reference package.
- Injected current functions, parameterized model settings, and provided deterministic random inputs.
- Separated plotting and CLI assembly from numerical integration.
- Added explicit adaptation-rule distinction, validation, unit tests, and a CLI smoke test.
- Added Python 3.10/3.12 GitHub CI, an experiment map, architecture diagram, and contributor notes.

## Verification boundaries

The original notebook outputs were not treated as a numerical ground truth. They frequently lack fixed random seeds, and historical parameter sets and end-of-step recording differ from the new solver. The new program must **not** be presented as a byte-for-byte or numerical port of every notebook.

Automated tests validate single-neuron numerical invariants, argument validation, seed repeatability, and the CLI. Brian2 simulations remain notebooks, and the archived PDF/DOCX figures and compressed submissions were not independently regenerated. This environment did not provide a tool for executing the original Brian2 experiments or inspecting all binary archive contents. The 14 original non-checkpoint notebooks were checked for several common credential formats in code cells, with no matches; this is not a comprehensive secret scan of archives, binary metadata, or full Git history.

## Prioritized follow-up work

1. Create deterministic, small Brian2 smoke cases for the two network and synaptic-plasticity experiments, with explicitly seeded NumPy and Brian2 random generators.
2. Choose a historical parameter set and compare saved voltage/spike traces from the legacy code and the new solver using an explained time-index convention.
3. Remove notebook-generated outputs or rebuild notebooks from parameterized scripts only after storing independently verifiable result artifacts.
4. Inspect the original RAR, PDF, DOCX, and slide binaries for sensitive information before any additional public distribution.
5. If needed, pin and lock the notebook dependency environment once confirmed working on supported Python versions.

## Deliberate omissions

No Docker or CD: this is a self-contained educational code/research archive without a service or deployment target. No heavy application frameworks or dependency injection container: a callback and dataclasses are simpler. No automatic re-execution of multi-neuron research models: simulations were not validated against a saved baseline. A lightweight, source-grounded Mermaid architecture diagram was added because Archify was unavailable.
