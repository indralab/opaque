import pytest
import numpy as np
from scipy.stats import beta
from opaque.simulations.prevalence import run_trial_for_theta
from opaque.stats import equal_tailed_interval, highest_density_interval


@pytest.mark.parametrize(
    "test_input",
    [
        (0.4, 80, 20, 7, 3, 100),
        (0.8, 20, 5, 60, 40, 20),
        (0.2, 10, 5, 8, 2, 1000)
    ],
)
def test_equal_tailed_interval(test_input):
    n_trials = 100
    theta, sens_a, sens_b, spec_a, spec_b, sample_size = test_input
    hits = 0
    random_state = np.random.RandomState(561)
    sens_dist = beta(sens_a, sens_b)
    spec_dist = beta(spec_a, spec_b)
    sens_dist.random_state = random_state
    spec_dist.random_state = random_state
    for _ in range(n_trials):
        sensitivity = sens_dist.rvs()
        specificity = spec_dist.rvs()
        n, t, _, _, _ = run_trial_for_theta(
            (
                theta,
                sensitivity,
                specificity,
                sample_size,
                random_state,
            ),
        )
        interval = equal_tailed_interval(
            n, t, sens_a, sens_b, spec_a, spec_b, alpha=0.1
        )
        if interval[0] <= theta <= interval[1]:
            hits += 1
    coverage_rate = hits / n_trials
    assert coverage_rate > 0.8


@pytest.mark.parametrize(
    "test_input", [(0.4, 80, 20, 7, 3, 100), (0.8, 20, 5, 60, 40, 20)]
)
def test_highest_density_interval(test_input):
    n_trials = 100
    theta, sens_a, sens_b, spec_a, spec_b, sample_size = test_input
    hits = 0
    random_state = np.random.RandomState(1105)
    sens_dist = beta(sens_a, sens_b)
    spec_dist = beta(spec_a, spec_b)
    sens_dist.random_state = random_state
    spec_dist.random_state = random_state
    for _ in range(n_trials):
        sensitivity = sens_dist.rvs()
        specificity = spec_dist.rvs()
        n, t, _, _, _ = run_trial_for_theta(
            (
                theta,
                sensitivity,
                specificity,
                sample_size,
                random_state,
            ),
        )
        interval = highest_density_interval(
            n, t, sens_a, sens_b, spec_a, spec_b, alpha=0.1
        )
        if interval[0] <= theta <= interval[1]:
            hits += 1
    coverage_rate = hits / n_trials
    assert coverage_rate > 0.8
