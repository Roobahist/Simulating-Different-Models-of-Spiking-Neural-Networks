"""Command-line experiment runner for the reusable single-neuron models."""

import argparse
import json
import random

from .simulation import (
    NeuronParameters,
    SimulationSettings,
    simulate,
    step_current,
    uniform_current,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model", choices=("lif", "eif", "adex", "legacy_adaptive"), default="lif"
    )
    parser.add_argument("--duration", type=float, default=200)
    parser.add_argument("--time-step", type=float, default=0.05)
    parser.add_argument("--amplitude", type=float, default=4)
    parser.add_argument("--onset", type=float, default=10)
    parser.add_argument("--random-max", type=float)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--resistance", type=float, default=5)
    parser.add_argument("--capacitance", type=float, default=6)
    parser.add_argument("--resting-potential", type=float, default=-70)
    parser.add_argument("--threshold", type=float, default=-55)
    parser.add_argument("--rheobase-potential", type=float, default=-60)
    parser.add_argument("--delta", type=float, default=1)
    parser.add_argument("--adaptation-coupling", type=float, default=1)
    parser.add_argument("--spike-adaptation", type=float, default=1)
    parser.add_argument("--adaptation-tau", type=float, default=4)
    parser.add_argument("--output", help="Optional PNG output; requires the plot extra")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Construct configuration and dependencies, then run one simulation."""
    args = build_parser().parse_args(argv)
    parameters = NeuronParameters(
        resistance=args.resistance, capacitance=args.capacitance,
        resting_potential=args.resting_potential, threshold=args.threshold,
        rheobase_potential=args.rheobase_potential, delta=args.delta,
        adaptation_coupling=args.adaptation_coupling,
        spike_adaptation=args.spike_adaptation, adaptation_tau=args.adaptation_tau,
    )
    settings = SimulationSettings(duration=args.duration, time_step=args.time_step)
    current = (
        uniform_current(args.random_max, random.Random(args.seed))
        if args.random_max is not None else step_current(args.amplitude, args.onset)
    )
    trace = simulate(args.model, parameters, settings, current)
    if args.output:
        from .plotting import plot_trace

        plot_trace(trace, args.output)
    print(json.dumps({
        "model": args.model,
        "seed": args.seed if args.random_max is not None else None,
        "spike_count": len(trace.spike_times),
        "firing_rate": trace.firing_rate,
        "spike_times": trace.spike_times,
        "output": args.output,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
