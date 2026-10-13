"""Optional noninteractive plots of reproducible neuron simulations."""

from .simulation import SimulationTrace


def plot_trace(trace: SimulationTrace, output: str) -> None:
    """Save trace signals, using an optional Matplotlib dependency."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    has_adaptation = any(value != 0 for value in trace.adaptation)
    fig, axes = plt.subplots(3 if has_adaptation else 2, 1, sharex=True, figsize=(9, 6))
    axes[0].plot(trace.times, trace.voltage)
    axes[0].set_ylabel("Voltage")
    axes[1].plot(trace.times, trace.current)
    axes[1].set_ylabel("Current")
    if has_adaptation:
        axes[2].plot(trace.times, trace.adaptation)
        axes[2].set_ylabel("Adaptation")
    axes[-1].set_xlabel("Time (coursework units)")
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)
