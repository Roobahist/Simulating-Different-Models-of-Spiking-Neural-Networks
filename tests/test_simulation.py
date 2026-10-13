"""Numerical and configuration checks for the reusable reference solvers."""

import math
import random
import unittest

from spiking_models import (
    NeuronParameters,
    SimulationSettings,
    frequency_current_curve,
    simulate,
    step_current,
    uniform_current,
)


class SimulationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parameters = NeuronParameters(resistance=2, capacitance=3)
        self.settings = SimulationSettings(duration=10, time_step=0.1)

    def test_resting_lif_does_not_spike(self) -> None:
        trace = simulate("lif", self.parameters, self.settings, step_current(0))
        self.assertEqual(len(trace.times), 100)
        self.assertEqual(trace.spike_times, ())
        self.assertTrue(all(abs(v + 70) < 1e-12 for v in trace.voltage))

    def test_lif_first_euler_step(self) -> None:
        trace = simulate("lif", self.parameters, self.settings, step_current(2))
        self.assertAlmostEqual(trace.voltage[0], -70 + 0.1 * 2 / 3)

    def test_spiking_resets_voltage(self) -> None:
        trace = simulate("lif", self.parameters, self.settings, step_current(50))
        self.assertGreater(len(trace.spike_times), 0)
        self.assertTrue(all(v < self.parameters.threshold for v in trace.voltage))
        self.assertEqual(len(trace.voltage), len(trace.current))

    def test_delayed_stimulus(self) -> None:
        trace = simulate("lif", self.parameters, self.settings, step_current(1, onset=0.3))
        self.assertEqual(trace.current[:3], (0, 0, 0))
        self.assertEqual(trace.current[3], 1)

    def test_injected_randomness_is_repeatable(self) -> None:
        def sampled(seed: int) -> tuple[float, ...]:
            return simulate(
                "lif", self.parameters, self.settings,
                uniform_current(3, random.Random(seed)),
            ).current

        self.assertEqual(sampled(7), sampled(7))
        self.assertNotEqual(sampled(7), sampled(8))

    def test_all_models_produce_finite_traces(self) -> None:
        for model in ("lif", "eif", "adex", "legacy_adaptive"):
            with self.subTest(model=model):
                trace = simulate(model, self.parameters, self.settings, step_current(1))
                self.assertTrue(all(math.isfinite(v) for v in trace.voltage))
                self.assertTrue(all(math.isfinite(w) for w in trace.adaptation))

    def test_legacy_rule_is_distinct_from_standard_adex(self) -> None:
        current = step_current(50)
        regular = simulate("adex", self.parameters, self.settings, current)
        legacy = simulate("legacy_adaptive", self.parameters, self.settings, current)
        self.assertNotEqual(regular.adaptation, legacy.adaptation)

    def test_validation_and_invalid_input(self) -> None:
        with self.assertRaises(ValueError):
            NeuronParameters(resistance=0)
        with self.assertRaises(ValueError):
            SimulationSettings(duration=10, time_step=0.3)
        with self.assertRaises(ValueError):
            step_current(float("nan"))
        with self.assertRaises(ValueError):
            uniform_current(-1, random.Random(0))
        with self.assertRaises(ValueError):
            simulate("invalid", self.parameters, self.settings, step_current(1))
        with self.assertRaises(ValueError):
            simulate("lif", self.parameters, self.settings, lambda _t: float("nan"))

    def test_f_i_curve_uses_count_based_rates(self) -> None:
        curve = frequency_current_curve((0, 50), "lif", self.parameters, self.settings)
        self.assertEqual(curve[0], (0, 0))
        self.assertGreater(curve[1][1], 0)


if __name__ == "__main__":
    unittest.main()
