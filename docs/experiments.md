# Experiment index and historical correspondence

The original repository had three directories named `Project1`, `Project2`, and `Project3` with notebooks numbered by task. The notebooks have been moved to meaningful locations without altering their cell contents, figures, outputs, parameters, or computational logic.

## Single-neuron models (original Project1)

| New notebook | Original | Description |
| --- | --- | --- |
| `notebooks/single_neuron/lif_step.ipynb` | `Project1/1_1.ipynb` | LIF neuron, delayed constant-current injection, and a frequency-current plot |
| `notebooks/single_neuron/lif_random.ipynb` | `Project1/1_2.ipynb` | LIF neuron with sampled random input |
| `notebooks/single_neuron/eif_step.ipynb` | `Project1/2_1.ipynb` | EIF variant with delayed constant current |
| `notebooks/single_neuron/eif_random.ipynb` | `Project1/2_2.ipynb` | EIF variant with random input |
| `notebooks/single_neuron/adaptive_eif_step.ipynb` | `Project1/3_1.ipynb` | Exponential neuron with original adaptation rule |
| `notebooks/single_neuron/adaptive_eif_random.ipynb` | `Project1/3_2.ipynb` | Exponential/adaptive model with random input |

## Network dynamics (original Project2)

| New notebook | Original | Description |
| --- | --- | --- |
| `notebooks/network_dynamics/excitatory_inhibitory_network.ipynb` | `Project2/1.ipynb` | Brian2 excitatory and inhibitory network simulation; connectivity visualization |
| `notebooks/network_dynamics/decision_network.ipynb` | `Project2/2.ipynb` | Brian2 decision simulation with multiple neuronal populations |

## Synaptic plasticity (original Project3)

| New notebook | Original | Description |
| --- | --- | --- |
| `notebooks/synaptic_plasticity/stdp_pair.ipynb` | `Project3/1.ipynb` | Two-neuron STDP experiment |
| `notebooks/synaptic_plasticity/pattern_learning.ipynb` | `Project3/2.ipynb` | Pattern-related synaptic simulation |
| `notebooks/synaptic_plasticity/pattern_learning_analysis.ipynb` | `Project3/2_1.ipynb` | Pattern experiment analysis |
| `notebooks/synaptic_plasticity/pattern_learning_variation.ipynb` | `Project3/2_2.ipynb` | Pattern experiment variation |
| `notebooks/synaptic_plasticity/pattern_learning_parameter_study.ipynb` | `Project3/3.ipynb` | Further variation with adjustable coefficient |

The extra `Project3/2_2-Copy1.ipynb` and Jupyter checkpoints were moved under `archive/notebook-snapshots/` instead of being deleted.

## Numerical and historical caveats

- The first two groups use different modelling conventions: hand-written Euler updates in the first, Brian2 unit-aware equations in the others.
- In the first project's original adaptation notebook, the adaptation update includes the cumulative number of prior spikes at each integration step. This is not the standard event-driven AdEx spike increment.
- Original LIF/EIF notebook frequency plots use an initial interval method. The reusable `frequency_current_curve` API uses observed spike count divided by simulated time; plots may differ.
- The new API records spike events at end-of-step times. The original notebooks record some events using the pre-update loop time.
- Existing random-input notebooks generally use global random state and interactive calls, and are not deterministic without modifications.
- The historical network and plasticity notebooks have not been computationally revalidated. The new automated tests cover the standalone single-neuron reference implementation only.
