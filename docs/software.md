# Software

Actively maintained libraries. Archived and maintenance-only packages are listed under [Unmaintained](unmaintained.md).

- [Ax](https://ax.dev/) - Adaptive experimentation platform on top of BoTorch, with constraints, multi-objective, and mixed spaces.
- [Vizier](https://github.com/google/vizier) - Google's service-style black-box optimization, now open source ([paper](https://proceedings.mlr.press/v188/song22a.html)).
- [BoTorch](https://botorch.org/) - Modular Monte Carlo BO library built on PyTorch and GPyTorch ([paper](https://proceedings.neurips.cc/paper/2020/hash/f5b1b89d98b7286673128a5fb112cb9a-Abstract.html)).
- [Trieste](https://github.com/secondmind-labs/trieste) - TensorFlow/GPflow toolbox for batch, constrained, multi-fidelity, and multi-objective BO ([paper](https://arxiv.org/abs/2302.08436)).
- [BoFire](https://github.com/experimental-design/bofire) - Experimental design and BO for mixed spaces, used in chemical and pharmaceutical settings ([paper](https://jmlr.org/papers/v26/24-1540.html)).
- [BayBE](https://github.com/emdgroup/baybe) - Bayesian DoE with chemical encodings and transfer learning ([paper](https://doi.org/10.1039/D5DD00050E)).
- [HEBO](https://github.com/huawei-noah/HEBO) - Heteroscedastic evolutionary BO from Huawei Noah's Ark Lab ([paper](https://www.jair.org/index.php/jair/article/view/13643)).
- [SMAC3](https://github.com/automl/SMAC3) - Sequential model-based algorithm configuration, using random forests or GPs ([paper](https://jmlr.org/papers/v23/21-0888.html)).
- [OpenBox](https://github.com/PKU-DAIR/open-box) - Black-box optimization system with transfer, multi-fidelity, and distributed runs ([paper](https://jmlr.org/papers/v25/23-0537.html)).
- [Dragonfly](https://github.com/dragonfly/dragonfly) - Scalable BO for expensive functions, including parallel and high-dimensional variants ([paper](https://jmlr.org/papers/v21/18-223.html)).
- [BayesianOptimization](https://github.com/bayesian-optimization/BayesianOptimization) - Small scikit-learn GP implementation of EI-style BO.
- [PyBADS](https://github.com/acerbilab/pybads) - GP-assisted mesh adaptive search for mildly expensive, nonsmooth, or noisy black-box fitting ([paper](https://joss.theoj.org/papers/10.21105/joss.05694)).
- [emukit](https://github.com/EmuKit/emukit) - Multi-fidelity emulation, experimental design, and BO on top of GPy ([paper](https://doi.org/10.25080/gerudo-f2bc6f59-009)).
- [SMT](https://smt.readthedocs.io/en/latest/) - Surrogate modeling toolbox with kriging, mixed and hierarchical GPs, and EGO ([paper](https://doi.org/10.1016/j.advengsoft.2023.103571)).
- [NUBO](https://github.com/mikediessner/nubo) - Compact PyTorch BO package aimed at scientists writing their own loop ([paper](https://www.jstatsoft.org/article/view/v114i01)).
- [Syne Tune](https://github.com/awslabs/syne-tune) - AWS HPO toolkit with BO, multi-fidelity, and transfer methods ([paper](https://proceedings.mlr.press/v188/salinas22a.html)).
- [HyperMapper](https://github.com/luinardi/hypermapper) - BO for computer-systems autotuning, including constrained and multi-objective problems ([paper](https://arxiv.org/abs/1810.05236)).
- [CAKE](https://github.com/richardcsuwandi/cake) - LLM-driven evolution of GP kernels inside BO ([paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/c03a2610bca2712b984b331fd4f7bb6f-Abstract-Conference.html)).
- [PlugBO](https://github.com/richardcsuwandi/plugbo) - Modular agentic interface around a BO loop.

## Related HPO tools

Not GP-BO, but often compared with it.

- [Optuna](https://optuna.org/) - Define-by-run HPO. Default sampler is TPE, not a GP ([paper](https://doi.org/10.1145/3292500.3330701)).
- [Hyperopt](https://github.com/hyperopt/hyperopt) - TPE over complex search spaces ([paper](https://proceedings.scipy.org/articles/Majora-8b375195-003)).

## Domain-specific

- [Gryffin](https://github.com/aspuru-guzik-group/gryffin) - BO for continuous and categorical experimental variables, with physicochemical descriptors ([paper](https://doi.org/10.1063/5.0048164)).
- [limbo](https://github.com/resibots/limbo) - C++ BO library from robotics ([paper](https://joss.theoj.org/papers/10.21105/joss.00545)).
