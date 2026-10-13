# Experiment index and historical correspondence

The original repository had three directories named \x60Project1\x60, \x60Project2\x60, and \x60Project3\x60 with notebooks numbered by task. The notebooks have been moved to meaningful locations without altering their cell contents, figures, outputs, parameters, or computational logic.

## Single-neuron models (original Project1)

| New notebook | Original | Description |
| --- | --- | --- |
| \x60notebooks/single_neuron/lif_step.ipynb\x60 | \x60Project1/1_1.ipynb\x60 | LIF neuron, delayed constant-current injection, and a frequency-current plot |
| \x60notebooks/single_neuron/lif_random.ipynb\x60 | \x60Project1/1_2.ipynb\x60 | LIF neuron with sampled random input |
| \x60notebooks/single_neuron/eif_step.ipynb\x60 | \x60Project1/2_1.ipynb\x60 | EIF variant with delayed constant current |
| \x60notebooks/single_neuron/eif_random.ipynb\x60 | \x60Project1/2_2.ipynb\x60 | EIF variant with random input |
| \x60notebooks/single_neuron/adaptive_eif_step.ipynb\x60 | \x60Project1/3_1.ipynb\x60 | Exponential neuron with original adaptation rule |
| \x60notebooks/single_neuron/adaptive_eif_random.ipynb\x60 | \x60Project1/3_2.ipynb\x60 | Exponential/adaptive model with random input |

## Network dynamics (original Project2)

| New notebook | Original | Description |
| --- | --- | --- |
| \x60notebooks/network_dynamics/excitatory_inhibitory_network.ipynb\x60 | \x60Project2/1.ipynb\x60 | Brian2 excitatory and inhibitory network simulation; connectivity visualization |
| \x60notebooks/network_dynamics/decision_network.ipynb\x60 | \x60Project2/2.ipynb\x60 | Brian2 decision simulation with multiple neuronal populations |

## Synaptic plasticity (original Project3)

| New notebook | Original | Description |
| --- | --- | --- |
| \x60notebooks/synaptic_plasticity/stdp_pair.ipynb\x60 | \x60Project3/1.ipynb\x60 | Two-neuron STDP experiment |
| \x60notebooks/synaptic_plasticity/pattern_learning.ipynb\x60 | \x60Project3/2.ipynb\x60 | Pattern-related synaptic simulation |
| \x60notebooks/synaptic_plasticity/pattern_learning_analysis.ipynb\x60 | \x60Project3/2_1.ipynb\x60 | Pattern experiment analysis |
| \x60notebooks/synaptic_plasticity/pattern_learning_variation.ipynb\x60 | \x60Project3/2_2.ipynb\x60 | Pattern experiment variation |
| \x60notebooks/synaptic_plasticity/pattern_learning_parameter_study.ipynb\x60 | \x60Project3/3.ipynb\x60 | Further variation with adjustable coefficient |

The extra \x60Project3/2_2-Copy1.ipynb\x60 and Jupyter checkpoints were moved under \x60archive/notebook-snapshots/\x60 instead of being deleted.

## Numerical and historical caveats

- The first two groups use different modelling conventions: hand-written Euler updates in the first, Brian2 unit-aware equations in the others.
- In the first project's original adaptation notebook, the adaptation update includes the cumulative number of prior spikes at each integration step. This is not the standard event-driven AdEx spike increment.
- Original LIF/EIF notebook frequency plots use an initial interval method. The reusable \x60frequency_current_curve\x60 API uses observed spike count divided by simulated time; plots may differ.
- The new API records spike events at end-of-step times. The original notebooks record some events using the pre-update loop time.
- Existing random-input notebooks generally use global random state and interactive calls, and are not deterministic without modifications.
- The historical network and plasticity notebooks have not been computationally revalidated. The new automated tests cover the standalone single-neuron reference implementation only.
