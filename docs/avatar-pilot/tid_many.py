# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Pose data adapted from SIGN-HUB, TİD Phonology 2.1.1, under CC BY-NC-SA 4.0.
# Right hand starts open by the upper chest and gathers its fingertips.
OPEN = ((-0.12, 0, 0.23), (-0.12, 0, 0.06), (-0.12, 0, -0.10), (-0.12, 0, -0.23))
GATHER = ((-0.46, 0, -0.34), (-0.55, 0, -0.04), (-0.57, 0, 0.22), (-0.61, 0, 0.43))
START = (-1.02, -0.83, 1.15)
END = (-1.02, -0.85, 1.20)
poses = (
    (1, START, -0.24, OPEN, (-0.08,) * 4, (0, 0, 0)),
    (9, START, -0.24, OPEN, (-0.08,) * 4, (0, 0, 0)),
    (25, END, -0.24, GATHER, (-0.30,) * 4, (-0.65, 0, -0.50)),
    (37, END, -0.24, GATHER, (-0.30,) * 4, (-0.65, 0, -0.50)),
)
