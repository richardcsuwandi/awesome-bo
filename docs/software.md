# Software

Actively maintained libraries. Archived and maintenance-only packages are listed under [Unmaintained](unmaintained.md).

The table covers every actively maintained library listed here, not a shortlist.

| Library | Stack | Constraints | Multi-obj | Mixed / batch | Notes |
| --- | --- | --- | --- | --- | --- |
| [Ax](https://ax.dev/) | BoTorch / GPyTorch | Yes | Yes | Yes | Service layer for experiments. |
| [Vizier](https://github.com/google/vizier) | GP / others | Yes | Yes | Yes | Google's service-style BO. |
| [BoTorch](https://botorch.org/) | PyTorch / GPyTorch | Yes | Yes | Yes | Research toolkit. You write the loop. |
| [Trieste](https://github.com/secondmind-labs/trieste) | TensorFlow / GPflow | Yes | Yes | Yes | Modular ask-tell API. |
| [BoFire](https://github.com/experimental-design/bofire) | BoTorch | Yes | Yes | Yes | Industrial DOE and chemistry. |
| [HEBO](https://github.com/huawei-noah/HEBO) | GPyTorch / others | Yes | Yes | Yes | Strong AutoML competition record. |
| [SMAC3](https://github.com/automl/SMAC3) | RF / GP | Yes | Limited | Yes | Algorithm configuration and HPO. |
| [OpenBox](https://github.com/PKU-DAIR/open-box) | GP / TPE / RF | Yes | Yes | Yes | General black-box system. |
| [Dragonfly](https://github.com/dragonfly/dragonfly) | GP | Yes | Yes | Yes | Parallel and high-dimensional BO. |
| [BayesianOptimization](https://github.com/bayesian-optimization/BayesianOptimization) | scikit-learn | Limited | No | Limited | Small EI-style loop. |
| [emukit](https://github.com/EmuKit/emukit) | GPy | Yes | Limited | Yes | Multi-fidelity emulation. |
| [NUBO](https://github.com/mikediessner/nubo) | PyTorch | Limited | No | Limited | Compact scientist-facing API. |
| [Syne Tune](https://github.com/awslabs/syne-tune) | various | Yes | Yes | Yes | AWS HPO with BO and multi-fidelity. |
| [HyperMapper](https://github.com/luinardi/hypermapper) | RF / GP | Yes | Yes | Yes | Systems autotuning. |
| [CAKE](https://github.com/richardcsuwandi/cake) | BoTorch | Limited | Limited | Limited | LLM-evolved GP kernels. |
| [PlugBO](https://github.com/richardcsuwandi/plugbo) | BoTorch | Yes | Limited | Yes | Agentic plugin loop. |

## Active libraries

- [Ax](https://ax.dev/) - Adaptive experimentation platform on top of BoTorch, with constraints, multi-objective, and mixed spaces.
- [Vizier](https://github.com/google/vizier) - Google's service-style black-box optimization, now open source.
- [BoTorch](https://botorch.org/) - Modular Monte Carlo BO library built on PyTorch and GPyTorch.
- [Trieste](https://github.com/secondmind-labs/trieste) - TensorFlow/GPflow toolbox for batch, constrained, multi-fidelity, and multi-objective BO.
- [BoFire](https://github.com/experimental-design/bofire) - Experimental design and BO for mixed spaces, used in chemical and pharmaceutical settings.
- [HEBO](https://github.com/huawei-noah/HEBO) - Heteroscedastic evolutionary BO from Huawei Noah's Ark Lab.
- [SMAC3](https://github.com/automl/SMAC3) - Sequential model-based algorithm configuration, using random forests or GPs.
- [OpenBox](https://github.com/PKU-DAIR/open-box) - Black-box optimization system with transfer, multi-fidelity, and distributed runs.
- [Dragonfly](https://github.com/dragonfly/dragonfly) - Scalable BO for expensive functions, including parallel and high-dimensional variants.
- [BayesianOptimization](https://github.com/bayesian-optimization/BayesianOptimization) - Small scikit-learn GP implementation of EI-style BO.
- [emukit](https://github.com/EmuKit/emukit) - Multi-fidelity emulation, experimental design, and BO on top of GPy.
- [NUBO](https://github.com/mikediessner/nubo) - Compact PyTorch BO package aimed at scientists writing their own loop.
- [Syne Tune](https://github.com/awslabs/syne-tune) - AWS HPO toolkit with BO, multi-fidelity, and transfer methods.
- [HyperMapper](https://github.com/luinardi/hypermapper) - BO for computer-systems autotuning, including constrained and multi-objective problems.
- [CAKE](https://github.com/richardcsuwandi/cake) - LLM-driven evolution of GP kernels inside BO.
- [PlugBO](https://github.com/richardcsuwandi/plugbo) - Modular agentic interface around a BO loop.

## Related HPO tools

Not GP-BO, but often compared with it.

- [Optuna](https://optuna.org/) - Define-by-run HPO. Default sampler is TPE, not a GP.
- [Hyperopt](https://github.com/hyperopt/hyperopt) - TPE over complex search spaces.

## Domain-specific

- [Gryffin](https://github.com/aspuru-guzik-group/gryffin) - BO for continuous and categorical experimental variables, with physicochemical descriptors.
- [limbo](https://github.com/resibots/limbo) - C++ BO library from robotics.
