# Spiking Neural Network Simulations

Educational simulations of **individual spiking neurons**, **recurrent neural networks**, and **synaptic plasticity**, developed as a collection of Python/Jupyter coursework experiments in 2022. This repository preserves the original experimental notebooks and reports while introducing a testable Python reference implementation for the single-neuron models.

## Experiments

| Group | Contents | Historical report |
| --- | --- | --- |
| Single-neuron dynamics | Leaky integrate-and-fire (LIF), exponential integrate-and-fire (EIF), and an adaptation variant; each with step and stochastic input | [Single-neuron report](reports/single-neuron-models.pdf) |
| Network dynamics | Brian2 excitatory/inhibitory network and a multi-population decision network | [Network report](reports/network-dynamics.pdf) |
| Synaptic plasticity | Brian2 spike-timing-dependent plasticity (STDP) and repeated spike-pattern experiments | [Plasticity report](reports/synaptic-plasticity.pdf) |

See [experiment index](docs/experiments.md) for notebook descriptions, original names, and limitations.

## Run the reference single-neuron simulation

Requires **Python 3.10 or newer**. From the repository root:

```bash
python -m pip install -e .
python -m spiking_models --model lif --duration 200 --time-step 0.05 --amplitude 4 --onset 10
python -m spiking_models --model eif --amplitude 4 --delta 1
python -m spiking_models --model adex --amplitude 10 --spike-adaptation 1
python -m spiking_models --model legacy_adaptive --amplitude 10
```

The command prints JSON including spike count, spike times, and the observed spike rate. To generate a plot:

```bash
python -m pip install -e ".[plot]"
python -m spiking_models --model lif --output trace.png
```

For reproducible random-input experiments:

```bash
python -m spiking_models --model lif --random-max 20 --seed 42
```

Physical parameter values and time units in the standalone Python solver follow **consistent abstract coursework units**. The Brian2 notebooks use Brian2 unit objects (such as `ms`, `mV`, `namp`) and are a separate experimental implementation, not interchangeable with the standalone solver.

## Work with the original notebooks

```bash
python -m pip install -e ".[notebooks]"
jupyter notebook notebooks/
```

The original notebooks are **historical artifacts** and may contain interactive `input()` calls, fixed parameter values, plots stored as cell outputs, and global Brian2 state. Re-executing them may be computationally expensive, yield different random results, or require further manual adaptation. They have been **moved, not rewritten**, to preserve the historical scientific work. The archival compressed submissions remain available under `archive/`.

## Python API

```python
from spiking_models import NeuronParameters, SimulationSettings, simulate, step_current

trace = simulate(
    model="lif",
    parameters=NeuronParameters(resistance=5, capacitance=6),
    settings=SimulationSettings(duration=200, time_step=0.05),
    current=step_current(amplitude=4, onset=10),
)
print(len(trace.spike_times), trace.firing_rate)
```

`simulate` accepts any callable that provides finite current samples, so model logic is decoupled from input generation. `uniform_current` accepts an injected, seeded `random.Random` instance. An optional plotting function is separate from the solver.

**Model fidelity note:** The original single-neuron notebooks include a nonstandard adaptation term proportional to the cumulative spike count. The `legacy_adaptive` option retains that update rule; `adex` follows the common instantaneous adaptation increment at each spike. Output timing and the frequency-current definition have also been clarified in the standalone solver. Do not assume numerical identity with the original notebooks without establishing a controlled regression baseline.

## Quality and maintenance

```bash
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
ruff check src tests
```

CI runs syntax checks, linting, unit tests, and a CLI smoke test on two supported Python versions. No external services, deployment, or Docker are needed for these research scripts. Architecture and source layout are described in [architecture](docs/architecture.md), and instructions for future contributors are in [AGENTS.md](AGENTS.md).

## Known limitations

- The Brian2 experiments are preserved as original notebooks, not yet extracted into a fully tested script-based network simulator.
- Historical reports and compressed archives are included for provenance; do not treat stored notebook output cells as reproducibility evidence.
- The standalone Euler solver is educational, not a validated neuroscience library or a claim of research-grade numerical accuracy.
- No results, performance measurements, or scientific comparisons are claimed without re-running the original experiments.
