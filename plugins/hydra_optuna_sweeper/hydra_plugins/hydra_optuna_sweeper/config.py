# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from omegaconf import MISSING

from hydra.core.config_store import ConfigStore
from optuna.samplers import (
    TPESampler,
    RandomSampler,
    CmaEsSampler,
    NSGAIISampler,
    MOTPESampler,
)


class DistributionType(Enum):
    int = 1
    float = 2
    categorical = 3


class Direction(Enum):
    minimize = 1
    maximize = 2


@dataclass
class TPESamplerConfig:
    """
    https://optuna.readthedocs.io/en/stable/reference/generated/optuna.samplers.TPESampler.html
    """

    _target_: str = "hydra_plugins.hydra_optuna_sweeper.config.TPESampler"

    consider_prior: bool = True
    prior_weight: float = 1.0
    consider_magic_clip: bool = True
    consider_endpoints: bool = False
    n_startup_trials: int = 10
    n_ei_candidates: int = 24
    seed: Optional[int] = None
    multivariate: bool = False
    warn_independent_sampling: bool = True


@dataclass
class RandomSamplerConfig:
    """
    https://optuna.readthedocs.io/en/stable/reference/generated/optuna.samplers.RandomSampler.html
    """

    _target_: str = "hydra_plugins.hydra_optuna_sweeper.config.RandomSampler"
    seed: Optional[int] = None


@dataclass
class CmaEsSamplerConfig:
    """
    https://optuna.readthedocs.io/en/stable/reference/generated/optuna.samplers.CmaEsSampler.html
    """

    _target_: str = "hydra_plugins.hydra_optuna_sweeper.config.CmaEsSampler"

    x0: Optional[Dict[str, Any]] = None
    sigma0: Optional[float] = None
    independent_sampler: Optional[Any] = None
    warn_independent_sampling: bool = True
    seed: Optional[int] = None
    consider_pruned_trials: bool = False
    restart_strategy: Optional[Any] = None
    inc_popsize: int = 2
    use_separable_cma: bool = False
    source_trials: Optional[Any] = None


@dataclass
class NSGAIISamplerConfig:
    """
    https://optuna.readthedocs.io/en/stable/reference/generated/optuna.samplers.NSGAIISampler.html
    """

    _target_: str = "hydra_plugins.hydra_optuna_sweeper.config.NSGAIISampler"

    population_size: int = 50
    mutation_prob: Optional[float] = None
    crossover_prob: float = 0.9
    swapping_prob: float = 0.5
    seed: Optional[int] = None
    constraint_func: Optional[Any] = None


@dataclass
class MOTPESamplerConfig:
    """
    https://optuna.readthedocs.io/en/stable/reference/generated/optuna.samplers.MOTPESampler.html
    """

    _target_: str = "hydra_plugins.hydra_optuna_sweeper.config.MOTPESampler"

    consider_prior: bool = True
    prior_weight: float = 1.0
    consider_magic_clip: bool = True
    consider_endpoints: bool = False
    n_startup_trials: int = 10
    n_ehvi_candidates: int = 24
    seed: Optional[int] = None


@dataclass
class DistributionConfig:

    # Type of distribution. "int", "float" or "categorical"
    type: DistributionType

    # Choices of categorical distribution
    # List element type should be Union[str, int, float, bool]
    choices: Optional[List[Any]] = None

    # Lower bound of int or float distribution
    low: Optional[float] = None

    # Upper bound of int or float distribution
    high: Optional[float] = None

    # If True, space is converted to the log domain
    # Valid for int or float distribution
    log: bool = False

    # Discritization step
    # Valid for int or float distribution
    step: Optional[float] = None


@dataclass
class OptunaConfig:

    # Direction of optimization
    # Union[Direction, List[Direction]]
    direction: Any = Direction.minimize

    # Storage URL to persist optimization results
    # For example, you can use SQLite if you set 'sqlite:///example.db'
    # Please refer to the reference for further details
    # https://optuna.readthedocs.io/en/stable/reference/storages.html
    storage: Optional[str] = None

    # Name of study to persist optimization results
    study_name: Optional[str] = None

    # Total number of function evaluations
    n_trials: int = 20

    # Number of parallel workers
    n_jobs: int = 2

    # Sampling algorithm
    # Please refer to the reference for further details
    # https://optuna.readthedocs.io/en/stable/reference/samplers.html
    sampler: Any = MISSING


defaults = [{"sampler": "tpe"}]


@dataclass
class OptunaSweeperConf:
    _target_: str = "hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper"
    defaults: List[Any] = field(default_factory=lambda: defaults)

    optuna_config: OptunaConfig = OptunaConfig()

    search_space: Dict[str, Any] = field(default_factory=dict)


ConfigStore.instance().store(
    group="hydra/sweeper",
    name="optuna",
    node=OptunaSweeperConf,
    provider="optuna_sweeper",
)

ConfigStore.instance().store(
    group="hydra/sweeper/sampler",
    name="tpe",
    package="hydra.sweeper.optuna_config.sampler",
    node=TPESamplerConfig,
    provider="optuna_sweeper",
)

ConfigStore.instance().store(
    group="hydra/sweeper/sampler",
    name="random",
    package="hydra.sweeper.optuna_config.sampler",
    node=RandomSamplerConfig,
    provider="optuna_sweeper",
)

ConfigStore.instance().store(
    group="hydra/sweeper/sampler",
    name="cmaes",
    package="hydra.sweeper.optuna_config.sampler",
    node=CmaEsSamplerConfig,
    provider="optuna_sweeper",
)

ConfigStore.instance().store(
    group="hydra/sweeper/sampler",
    name="nsgaii",
    package="hydra.sweeper.optuna_config.sampler",
    node=NSGAIISamplerConfig,
    provider="optuna_sweeper",
)

ConfigStore.instance().store(
    group="hydra/sweeper/sampler",
    name="motpe",
    package="hydra.sweeper.optuna_config.sampler",
    node=MOTPESamplerConfig,
    provider="optuna_sweeper",
)
