"""Public command-line entry point smoke test."""

import contextlib
import io
import json
import unittest

from spiking_models.__main__ import main


class CliTests(unittest.TestCase):
    def test_cli_emits_json(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main(["--model", "lif", "--duration", "10", "--time-step", "0.1"])
        self.assertEqual(status, 0)
        data = json.loads(output.getvalue())
        self.assertEqual(data["model"], "lif")
        self.assertEqual(data["spike_count"], len(data["spike_times"]))


if __name__ == "__main__":
    unittest.main()
