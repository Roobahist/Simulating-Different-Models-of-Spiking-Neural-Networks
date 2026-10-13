"""Single-neuron Euler solvers adapted from the original coursework.

The original adaptation equation is exposed as legacy_adaptive because it
differs from standard adaptive exponential integrate-and-fire (AdEx).
"""

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
import math
import random
from typing import Literal

Model = Literal["lif", "eif", "adex", "legacy_adaptive"]
CurrentSource = Callable[[float], float]


@dataclass(frozen=True)
class NeuronParameters:
    resistance: float = 5.0
    capacitance: float = 6.0
    resting_potential: float = -70.0
    threshold: float = -55.0
    rheobase_potential: float = -60.0
    delta: float = 1.0
    adaptation_coupling: float = 1.0
    spike_adaptation: float = 1.0
    adaptation_tau: float = 4.0

    def __post_init__(self) -> None:
        for name in ("resistance", "capacitance", "delta", "adaptation_tau"):
            value = getattr(self, name)
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")
        for name in (
            "resting_potential", "threshold", "rheobase_potential",
            "adaptation_coupling", "spike_adaptation",
        ):
            if not math.isfinite(getattr(self, name)):
                raise ValueError(f"{name} must be finite")


@dataclass(frozen=True)
class SimulationSettings:
    duration: float = 200.0
    time_step: float = 0.05

    def __post_init__(self) -> None:
        if not all(math.isfinite(x) and x > 0 for x in (self.duration, self.time_step)):
            raise ValueError("duration and time_step must be finite positive values")
        n = round(self.duration / self.time_step)
        if n < 1 or not math.isclose(
            n * self.time_step, self.duration, rel_tol=1e-9, abs_tol=1e-9
        ):
            raise ValueError("duration must be a multiple of time_step")


@dataclass(frozen=True)
class SimulationTrace:
    times: tuple[float, ...]
    voltage: tuple[float, ...]
    current: tuple[float, ...]
    adaptation: tuple[float, ...]
    spike_times: tuple[float, ...]
    settings: SimulationSettings = field(repr=False)

    @property
    def firing_rate(self) -> float:
        """Observed spike count divided by experiment duration."""
        return len(self.spike_times) / self.settings.duration


def step_current(amplitude: float, onset: float = 0.0) -> CurrentSource:
    """Build a delayed current step."""
    if not math.isfinite(amplitude) or not math.isfinite(onset) or onset < 0:
        raise ValueError("amplitude must be finite; onset must be nonnegative")
    return lambda time: amplitude if time >= onset else 0.0


def uniform_current(maximum: float, rng: random.Random, minimum: float = 0.0) -> CurrentSource:
    """Inject a seeded generator instead of depending on global random state."""
    if not all(map(math.isfinite, (minimum, maximum))) or maximum < minimum:
        raise ValueError("current bounds must be finite and ordered")
    return lambda _time: rng.uniform(minimum, maximum)


def simulate(
    model: Model,
    parameters: NeuronParameters,
    settings: SimulationSettings,
    current: CurrentSource,
) -> SimulationTrace:
    """Simulate one neuron using explicit Euler updates and an injected stimulus.

    End-of-step samples are stored. Numerical quantities use consistent
    coursework units, unlike the Brian2 notebooks which use SI quantities.
    """
    if model not in ("lif", "eif", "adex", "legacy_adaptive"):
        raise ValueError(f"Unknown model: {model}")

    dt = settings.time_step
    voltage = parameters.resting_potential
    adaptation = 0.0
    times, voltages, currents, adaptations, spikes = [], [], [], [], []

    for index in range(round(settings.duration / dt)):
        time = index * dt
        injected = float(current(time))
        if not math.isfinite(injected):
            raise ValueError(f"Current must be finite at t={time}")
        if model in ("adex", "legacy_adaptive"):
            # The legacy notebooks add a contribution on every step proportional
            # to cumulative spike count, not an instantaneous jump on a spike.
            legacy_term = (
                parameters.spike_adaptation * parameters.adaptation_tau * len(spikes)
                if model == "legacy_adaptive" else 0.0
            )
            adaptation += dt / parameters.adaptation_tau * (
                parameters.adaptation_coupling * (voltage - parameters.resting_potential)
                - adaptation + legacy_term
            )

        exponential = 0.0
        if model != "lif":
            try:
                exponential = parameters.delta * math.exp(
                    (voltage - parameters.rheobase_potential) / parameters.delta
                )
            except OverflowError as exc:
                raise ValueError("Exponential overflow: review model parameters") from exc

        next_voltage = voltage + dt / (parameters.resistance * parameters.capacitance) * (
            -(voltage - parameters.resting_potential) + exponential
            + parameters.resistance * (injected - adaptation)
        )
        if not math.isfinite(next_voltage):
            raise ValueError("Non-finite voltage: use a smaller time_step")
        if next_voltage >= parameters.threshold:
            spikes.append((index + 1) * dt)
            next_voltage = parameters.resting_potential
            if model == "adex":
                adaptation += parameters.spike_adaptation

        times.append((index + 1) * dt)
        voltages.append(next_voltage)
        currents.append(injected)
        adaptations.append(adaptation)
        voltage = next_voltage

    return SimulationTrace(
        times=tuple(times), voltage=tuple(voltages),
        current=tuple(currents), adaptation=tuple(adaptations),
        spike_times=tuple(spikes), settings=settings,
    )


def frequency_current_curve(
    amplitudes: Iterable[float],
    model: Model,
    parameters: NeuronParameters,
    settings: SimulationSettings,
    source_factory: Callable[[float], CurrentSource] = step_current,
) -> tuple[tuple[float, float], ...]:
    """Use fresh sources for each amplitude and return count-based firing rates."""
    return tuple(
        (amplitude, simulate(model, parameters, settings, source_factory(amplitude)).firing_rate)
        for amplitude in amplitudes
    )
