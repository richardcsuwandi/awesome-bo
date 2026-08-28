# Awesome Bayesian Optimization [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

<p align="center">
  <a href="https://github.com/richardcsuwandi/awesome-bo#readme">
    <img src="media/logo.svg" width="256" alt="Awesome Bayesian Optimization">
  </a>
</p>

A curated list of Bayesian optimization resources, maintained by [Richard Cornelius Suwandi](https://richardcsuwandi.github.io).

Website: [richardcsuwandi.github.io/awesome-bo](https://richardcsuwandi.github.io/awesome-bo/).

## Contents

- [Getting Started](#getting-started)
- [Books](#books)
- [Software](#software)
- [Papers](#papers)
  - [Surveys and Tutorials](#surveys-and-tutorials)
  - [Foundations](#foundations)
  - [Surrogate Design](#surrogate-design)
  - [Acquisition Functions](#acquisition-functions)
  - [High-Dimensional](#high-dimensional)
  - [Constrained and Safe](#constrained-and-safe)
  - [Multi-Objective](#multi-objective)
  - [Multi-Fidelity, Multi-Task, and Transfer](#multi-fidelity-multi-task-and-transfer)
  - [Batch and Parallel](#batch-and-parallel)
  - [Discrete and Mixed Spaces](#discrete-and-mixed-spaces)
  - [Preferential Feedback](#preferential-feedback)
  - [Meta-Learning](#meta-learning)
  - [LLMs and BO](#llms-and-bo)
- [Benchmarks](#benchmarks)
- [Applications](#applications)
- [Community](#community)
- [Videos](#videos)
- [Blogs](#blogs)
- [Recent Preprints](#recent-preprints)

## Getting Started

- [Exploring Bayesian Optimization](https://distill.pub/2020/bayesian-optimization/) - Interactive Distill article on GPs, acquisition functions, and the BO loop (Agnihotri and Batra, 2020).
- [Gaussian Processes for Machine Learning](https://gaussianprocess.org/gpml/) - Rasmussen and Williams, 2006. The GP textbook. Read this if Distill's GP section was not enough.
- [A Tutorial on Bayesian Optimization](https://arxiv.org/abs/1807.02811) - Frazier, 2018. The standard short tutorial, including noisy EI, batch, multi-fidelity, and constraints.
- [Recent Advances in Bayesian Optimization](https://bayesopt-tutorial.github.io/) - AAAI 2023 tutorial (slides and syllabus) covering high-dimensional, discrete, and causal BO.

Then read Garnett's book for theory, or Bayesian Optimization in Action for a Python walkthrough (under Books).

Pick a library. Ax is the service: you declare the search space and the metric, and Ax chooses the next experiment, fits the model, and runs the loop. BoTorch is the PyTorch library Ax is built on. You write that loop yourself: fit a GPyTorch model, define an acquisition, optimize it. Use Ax if you want to run an experiment. Use BoTorch if you are implementing a method, or changing the surrogate or the acquisition. Vizier is the other service-style option. All three are listed under Software.

## Books

- [Bayesian Decision-making Algorithms](https://bayesianalgorithms.com/) - Alexander Terenin, 2026. Working draft on Bayesian decision making algorithms, including decision-making under uncertainty and explore-exploit tradeoffs.
- [Bayesian Optimization](https://bayesoptbook.com/) - Roman Garnett, 2023. Theory-first textbook with a free HTML edition.
- [Bayesian Optimization in Action](https://www.manning.com/books/bayesian-optimization-in-action) - Quan Nguyen, 2023. Practitioner book with Python examples.
- [Bayesian Optimization: Theory and Practice Using Python](https://link.springer.com/book/10.1007/978-1-4842-9063-7) - Peng Liu, 2023. Walkthrough of implementing BO in Python.
- [Bayesian Approach to Global Optimization](https://link.springer.com/book/10.1007/978-94-009-0909-0) - Jonas Mockus, 1989. The classical monograph that introduced much of the modern framing.
- [Probabilistic Numerics](https://www.probabilistic-numerics.org/textbooks/probabilistic_numerics/) - Hennig, Osborne, and Kersting, 2022. BO as a numerical method, with GPs and quadrature.

## Software

Actively maintained libraries. Archived and maintenance-only packages are listed in [unmaintained.md](unmaintained.md).

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

### Related HPO tools

Not GP-BO, but often compared with it.

- [Optuna](https://optuna.org/) - Define-by-run HPO. Default sampler is TPE, not a GP.
- [Hyperopt](https://github.com/hyperopt/hyperopt) - TPE over complex search spaces.

### Domain-specific

- [Gryffin](https://github.com/aspuru-guzik-group/gryffin) - BO for continuous and categorical experimental variables, with physicochemical descriptors.
- [limbo](https://github.com/resibots/limbo) - C++ BO library from robotics.

## Papers

Canonical method papers, grouped by problem setting. Each section is a short reading list, not an archive. Newest year first, same year by title. Foundations is oldest first. The Surveys section starts with Shahriari, then Brochu.

### Surveys and Tutorials

- [Taking the Human Out of the Loop](https://ieeexplore.ieee.org/document/7352306/) - Shahriari et al., Proceedings of the IEEE, 2016. The standard survey of methods and applications.
- [A Tutorial on Bayesian Optimization of Expensive Cost Functions](https://arxiv.org/abs/1012.2599) - Brochu, Cora, and de Freitas, 2010. Early tutorial that still reads well.
- [Active Learning and Bayesian Optimization: A Unified Perspective to Learn with a Goal](https://link.springer.com/article/10.1007/s11831-024-10064-z) - Survey connecting BO and active learning.
- [Recent Advances in Bayesian Optimization](https://dl.acm.org/doi/10.1145/3582078) - Wang, Jin, Lai, and others, ACM Computing Surveys, 2023. Broad survey of methods through about 2022.
- [Recent Advances in Bayesian Optimization (slides)](https://bayesopt-tutorial.github.io/syllabus/fullslides.pdf) - AAAI 2023 tutorial slides (Doppa, Aglietti, Gardner, and others).

### Foundations

- [On Bayesian Methods for Seeking the Extremum](https://link.springer.com/chapter/10.1007/978-3-662-38527-2_55) - Mockus, Tiesis, and Zilinskas, 1975. The original expected-improvement argument.
- [Efficient Global Optimization of Expensive Black-Box Functions](https://link.springer.com/article/10.1023/A:1008306431147) - Jones, Schonlau, and Welch, 1998. EGO and expected improvement.
- [Gaussian Processes for Global Optimization](https://www.robots.ox.ac.uk/~mosb/public/pdf/132/Osborne%202010%20Gaussian%20Processes%20for%20Global%20Optimization.pdf) - Osborne, Garnett, and Roberts, LION 2008. GP surrogates for global optimization.
- [Gaussian Process Optimization in the Bandit Setting](https://proceedings.mlr.press/v9/srinivas10a.html) - Srinivas, Krause, Kakade, and Seeger, AISTATS 2010. GP-UCB and no-regret bounds.
- [Convergence Rates of Efficient Global Optimization Algorithms](https://www.jmlr.org/papers/v12/bull11a.html) - Bull, JMLR 2011. When EGO converges, and at what rate.
- [Practical Bayesian Optimization of Machine Learning Algorithms](https://papers.nips.cc/paper/2012/hash/05311655a15b75fab86956663e1819cd-Abstract.html) - Snoek, Larochelle, and Adams, NeurIPS 2012. MCMC GPs and EI for hyperparameter tuning.
- [Scalable Bayesian Optimization Using Deep Neural Networks](https://proceedings.mlr.press/v37/snoek15.html) - Snoek et al., ICML 2015. DNGO: neural-net surrogates when GPs get expensive.
- [GPyTorch: Blackbox Matrix-Matrix Gaussian Process Inference with GPU Acceleration](https://papers.nips.cc/paper/2018/hash/27e8e17134dd7083b050476733207ea1-Abstract.html) - Gardner, Pleiss, Bindel, Weinberger, and Wilson, NeurIPS 2018. The GP engine under BoTorch.
- [BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization](https://proceedings.neurips.cc/paper/2020/hash/f5b1b89d98b7286673128a5fb112cb9a-Abstract.html) - Balandat et al., NeurIPS 2020. The library paper behind most current PyTorch BO.

### Surrogate Design

Kernels, input transforms, and non-GP surrogates. DNGO is under Foundations.

- [Adaptive Kernel Design for Bayesian Optimization Is a Piece of CAKE with LLMs](https://proceedings.neurips.cc/paper_files/paper/2025/hash/c03a2610bca2712b984b331fd4f7bb6f-Abstract-Conference.html) - Suwandi et al., NeurIPS 2025. LLM-driven evolution of GP kernels during BO.
- [A Study of Bayesian Neural Network Surrogates for Bayesian Optimization](https://openreview.net/forum?id=SA19ijj44B) - Li, Rudner, and Wilson, ICLR 2024. When BNNs help as BO surrogates, and when they do not.
- [Bayesian Optimization with Conformal Prediction Sets](https://proceedings.mlr.press/v206/stanton23a.html) - Stanton, Maddox, and Wilson, AISTATS 2023. Distribution-free uncertainty in the loop.
- [Bayesian Optimization with Informative Covariance](https://arxiv.org/abs/2208.02704) - Tighineanu et al., TMLR 2023. Encode known structure in the kernel.
- [Kernel Identification Through Transformers](https://proceedings.neurips.cc/paper/2021/hash/56c3b2c6ea3a83aaeeff35eeb45d700d-Abstract.html) - Simpson et al., NeurIPS 2021. KITT: recommend a kernel from data in one forward pass.
- [Differentiable Compositional Kernel Learning for Gaussian Processes](https://proceedings.mlr.press/v80/sun18d.html) - Sun et al., ICML 2018. Neural kernel networks.
- [Bayesian Optimization with Robust Bayesian Neural Networks](https://papers.nips.cc/paper/2016/hash/a96d3afec184766bfeca7a9f989fc7e7-Abstract.html) - Springenberg, Klein, Falkner, and Hutter, NeurIPS 2016. BOHAMIANN: MCMC Bayesian neural nets as surrogates.
- [Deep Kernel Learning](https://proceedings.mlr.press/v51/wilson16.html) - Wilson, Hu, Salakhutdinov, and Xing, AISTATS 2016. A deep net as the feature map of a GP kernel.
- [Input Warping for Bayesian Optimization of Non-Stationary Functions](https://proceedings.mlr.press/v32/snoek14.html) - Snoek, Swersky, Zemel, and Adams, ICML 2014. Learn a warping so a stationary kernel fits better.
- [Gaussian Process Kernels for Pattern Discovery and Extrapolation](https://proceedings.mlr.press/v28/wilson13.html) - Wilson and Adams, ICML 2013. Spectral mixture kernels.
- [Structure Discovery in Nonparametric Regression through Compositional Kernel Search](https://proceedings.mlr.press/v28/duvenaud13.html) - Duvenaud, Lloyd, Grosse, Tenenbaum, and Ghahramani, ICML 2013. Grammar over sums and products of kernels.

### Acquisition Functions

- [FunBO: Discovering Acquisition Functions for Bayesian Optimization with FunSearch](https://proceedings.mlr.press/v267/aglietti25a.html) - Aglietti et al., ICML 2025. LLM search over acquisition functions written as code.
- [Unexpected Improvements to Expected Improvement for Bayesian Optimization](https://arxiv.org/abs/2310.20708) - Ament et al., NeurIPS 2023. LogEI, a numerically stable EI.
- [Joint Entropy Search for Maximally-Informed Bayesian Optimization](https://proceedings.neurips.cc/paper/2022/hash/4b03821747e89ce803b2dac590f6a39b-Abstract-Conference.html) - Hvarfner, Hutter, and Nardi, NeurIPS 2022. Information gain on the joint optimum and optimal value.
- [πBO: Augmenting Acquisition Functions with User Beliefs for Bayesian Optimization](https://openreview.net/forum?id=FegbkY6WDg) - Hvarfner, Stoll, Souza, Lindauer, Hutter, and Nardi, ICLR 2022. Weight the acquisition by a user prior over the optimum.
- [Why Non-myopic Bayesian Optimization is Promising and How Far Should We Look-ahead?](https://proceedings.mlr.press/v108/yue20b.html) - Yue and Kontar, AISTATS 2020. How much lookahead actually helps.
- [Maximizing Acquisition Functions for Bayesian Optimization](https://arxiv.org/abs/1805.10122) - Wilson, Hutter, and Deisenroth, NeurIPS 2018. Monte Carlo acquisition via autodiff.
- [Parallelised Bayesian Optimisation via Thompson Sampling](https://proceedings.mlr.press/v84/kandasamy18a.html) - Kandasamy et al., AISTATS 2018. TS as a simple batch acquisition.
- [Max-value Entropy Search for Efficient Bayesian Optimization](https://proceedings.mlr.press/v70/wang17e.html) - Wang and Jegelka, ICML 2017. Information about the maximum value rather than its location.
- [GLASSES: Relieving The Myopia Of Bayesian Optimisation](https://proceedings.mlr.press/v51/gonzalez16b.html) - González, Osborne, and Lawrence, AISTATS 2016. Non-myopic planning.
- [Predictive Entropy Search for Efficient Global Optimization of Black-box Functions](https://proceedings.neurips.cc/paper/2014/hash/6488484c982e9af5c35689523ba1abfe-Abstract.html) - Hernández-Lobato, Hoffman, and Ghahramani, NeurIPS 2014. Tractable information-theoretic acquisition.
- [Entropy Search for Information-Efficient Global Optimization](https://jmlr.org/papers/v13/hennig12a.html) - Hennig and Schuler, JMLR 2012. Select queries that reduce entropy of the argmax.
- [The Knowledge-Gradient Policy for Correlated Normal Beliefs](https://pubsonline.informs.org/doi/10.1287/ijoc.1080.0314) - Frazier, Powell, and Dayanik, INFORMS JOC 2009. Value of information when beliefs are correlated.

### High-Dimensional

- [NeST-BO: Fast Local Bayesian Optimization via Newton-Step Targeting of Gradient and Hessian Information](https://openreview.net/forum?id=1MHLQM0MKM) - Tang, Kudva, and Paulson, AISTATS 2026. Local BO that targets a Newton step.
- [Standard Gaussian Process is All You Need for High-Dimensional Bayesian Optimization](https://openreview.net/forum?id=kX8h23UG6v) - Xu, Wang, Phillips, and Zhe, ICLR 2025. Lengthscale init, not a fancy surrogate, is often the failure mode.
- [Understanding High-Dimensional Bayesian Optimization](https://proceedings.mlr.press/v267/papenmeier25a.html) - Papenmeier, Poloczek, and Nardi, ICML 2025. Why vanilla GP-BO fails in high-d, and a simple MLE fix.
- [Vanilla Bayesian Optimization Performs Great in High Dimensions](https://proceedings.mlr.press/v235/hvarfner24a.html) - Hvarfner, Hellsten, and Nardi, ICML 2024. Careful GP priors often beat specialized high-d methods.
- [Sparse Bayesian Optimization](https://proceedings.mlr.press/v206/liu23b.html) - Liu et al., AISTATS 2023. Sparsity in the input for high-d problems.
- [The Behavior and Convergence of Local Bayesian Optimization](https://proceedings.neurips.cc/paper_files/paper/2023/hash/e8f4eae0a41cab67fdead3aa6b77f083-Abstract-Conference.html) - Wu, Kim, Garnett, and Gardner, NeurIPS 2023. When local BO converges, and when it does not.
- [Increasing the Scope as You Learn](https://arxiv.org/abs/2205.13357) - Papenmeier, Nardi, and Poloczek, NeurIPS 2022. BAxUS: grow the embedding as budget grows.
- [Local Bayesian Optimization via Maximizing Probability of Descent](https://proceedings.neurips.cc/paper_files/paper/2022/hash/555479a201da27c97aaeed842d16ca49-Abstract-Conference.html) - Nguyen, Wu, Gardner, and Garnett, NeurIPS 2022. Local BO by following estimated descent.
- [High-dimensional Bayesian Optimization with Sparse Axis-Aligned Subspaces](https://proceedings.mlr.press/v161/eriksson21a.html) - Eriksson and Jankowiak, UAI 2021. SAASBO: sparsity-inducing priors on lengthscales.
- [Re-Examining Linear Embeddings for High-Dimensional Bayesian Optimization](https://arxiv.org/abs/2001.11659) - Letham, Calandra, Rai, and Bakshy, NeurIPS 2020. ALEBO.
- [A Framework for Bayesian Optimization in Embedded Subspaces](https://proceedings.mlr.press/v89/nayebi19a.html) - Nayebi, Munteanu, and Ihler, AISTATS 2019. HeSBO, hashing into a low-d embedding.
- [Scalable Global Optimization via Local Bayesian Optimization](https://proceedings.neurips.cc/paper/2019/hash/6c990b7aca7bc7058f5e98ea909e924b-Abstract.html) - Eriksson, Pearce, Gardner, Turner, and Poloczek, NeurIPS 2019. TuRBO: trust-region local BO.
- [Optimization, Fast and Slow](https://proceedings.mlr.press/v80/mcleod18a.html) - McLeod, Roberts, and Osborne, ICML 2018. Switch between local search and BO.
- [Discovering and Exploiting Additive Structure for Bayesian Optimization](https://proceedings.mlr.press/v54/gardner17a.html) - Gardner, Guo, Weinberger, Garnett, and Grosse, AISTATS 2017. Learn which additive decomposition to use.
- [Bayesian Optimization in a Billion Dimensions via Random Embeddings](https://arxiv.org/abs/1301.1942) - Wang et al., JAIR 2016. REMBO: optimize in a random low-dimensional subspace.
- [High Dimensional Bayesian Optimisation and Bandits via Additive Models](https://proceedings.mlr.press/v37/kandasamy15.html) - Kandasamy, Schneider, and Póczos, ICML 2015. Additive GP structure.

### Constrained and Safe

- [Scalable Constrained Bayesian Optimization](https://proceedings.mlr.press/v139/eriksson21a.html) - Eriksson and Poloczek, ICML 2021. SCBO: TuRBO with constraints.
- [A General Framework for Constrained Bayesian Optimization using Information-based Search](https://jmlr.org/papers/volume17/15-616/15-616.html) - Hernández-Lobato et al., JMLR 2016. PESC.
- [Safe Exploration for Optimization with Gaussian Processes](https://proceedings.mlr.press/v37/sui15.html) - Sui, Gotovos, Burdick, and Krause, ICML 2015. SafeOpt.
- [Bayesian Optimization with Inequality Constraints](https://proceedings.mlr.press/v32/gardner14.html) - Gardner, Kusner, Xu, Weinberger, and Cunningham, ICML 2014. Constrained EI.
- [Bayesian Optimization with Unknown Constraints](https://arxiv.org/abs/1403.5607) - Gelbart, Snoek, and Adams, UAI 2014. Constraints that are themselves expensive black boxes.

### Multi-Objective

- [Multi-Objective Bayesian Optimization over High-Dimensional Search Spaces](https://proceedings.mlr.press/v180/daulton22a.html) - Daulton, Eriksson, Balandat, and Bakshy, UAI 2022. MORBO: local trust regions for high-d multi-objective BO.
- [Parallel Bayesian Optimization of Multiple Noisy Objectives with Expected Hypervolume Improvement](https://proceedings.mlr.press/v139/daulton21a.html) - Daulton, Balandat, and Bakshy, ICML 2021. NEHVI under noise.
- [Differentiable Expected Hypervolume Improvement](https://proceedings.neurips.cc/paper/2020/hash/60cb558c40e4f18479664069d9642d5a-Abstract.html) - Daulton, Balandat, and Bakshy, NeurIPS 2020. qEHVI for parallel MOBO.
- [Efficient Computation of Expected Hypervolume Improvement Using Box Decomposition Algorithms](https://link.springer.com/article/10.1007/s10898-019-00798-7) - Yang, Emmerich, Deutz, and Bäck, JOGO 2019. Fast EHVI.
- [Predictive Entropy Search for Multi-objective Bayesian Optimization](https://proceedings.mlr.press/v48/hernandez-lobatoa16.html) - Hernández-Lobato, Hernández-Lobato, Shah, and Adams, ICML 2016. PESMO: information gain on the Pareto set.
- [ParEGO: A Hybrid Algorithm with On-line Landscape Approximation for Expensive Multiobjective Optimization Problems](https://ieeexplore.ieee.org/document/1583627) - Knowles, IEEE TEVC 2006. Scalarization plus EGO.

### Multi-Fidelity, Multi-Task, and Transfer

- [Pre-trained Gaussian Processes for Bayesian Optimization](https://www.jmlr.org/papers/v25/23-0269.html) - Wang et al., JMLR 2024. HyperBO: transfer a GP prior from related tasks.
- [Few-Shot Bayesian Optimization with Deep Kernel Surrogates](https://openreview.net/forum?id=bJxgv5C3sYc) - Wistuba and Grabocka, ICLR 2021. Deep kernels for few-shot HPO.
- [Multi-fidelity Bayesian Optimization with Max-value Entropy Search](https://arxiv.org/abs/1901.08295) - Takeno et al., NeurIPS 2020. Information-theoretic multi-fidelity acquisition.
- [BOHB: Robust and Efficient Hyperparameter Optimization at Scale](https://proceedings.mlr.press/v80/falkner18a.html) - Falkner, Klein, and Hutter, ICML 2018. TPE plus Hyperband.
- [Fast Bayesian Optimization of Machine Learning Hyperparameters on Large Datasets](https://proceedings.mlr.press/v54/klein17a.html) - Klein, Falkner, Bartels, Hennig, and Hutter, AISTATS 2017. FABOLAS.
- [Multi-fidelity Bayesian Optimisation with Continuous Approximations](https://proceedings.mlr.press/v70/kandasamy17a.html) - Kandasamy, Dasarathy, Schneider, and Póczos, ICML 2017. Continuous fidelity rather than a discrete ladder.
- [Gaussian Process Bandit Optimisation with Multi-fidelity Evaluations](https://proceedings.mlr.press/v48/kandasamy16.html) - Kandasamy et al., ICML 2016. MF-GP-UCB.
- [Freeze-Thaw Bayesian Optimization](https://arxiv.org/abs/1406.3896) - Swersky, Snoek, and Adams, 2014. Pause and resume training runs using a GP over learning curves.
- [Multi-Task Bayesian Optimization](https://proceedings.neurips.cc/paper/2013/hash/f33ba15effa5c10e873bf3842afb46a6-Abstract.html) - Swersky, Snoek, and Adams, NeurIPS 2013. Share data across related tasks.
- [Global Optimization of Stochastic Black-Box Systems via Sequential Kriging Meta-Models](https://link.springer.com/article/10.1007/s10898-005-2454-3) - Huang, Allen, Notz, and Zeng, JOGO 2006. Early multi-fidelity EGO.

### Batch and Parallel

- [GIBBON: General-purpose Information-Based Bayesian Optimisation](https://proceedings.mlr.press/v139/moss21a.html) - Moss, Leslie, Gonzalez, Rayson, and Gal, ICML 2021. Cheap batch information-theoretic acquisition.
- [Batched Large-scale Bayesian Optimization in High-dimensional Spaces](https://proceedings.mlr.press/v84/wang18c.html) - Wang, Gehring, Kohli, and Jegelka, AISTATS 2018. Ensemble batch BO in high-d.
- [Batch Bayesian Optimization via Local Penalization](https://proceedings.mlr.press/v51/gonzalez16a.html) - González, Dai, Hennig, and Lawrence, AISTATS 2016. Penalize around pending points.
- [Batched Gaussian Process Bandit Optimization via Determinantal Point Processes](https://papers.nips.cc/paper/2016/hash/a1d7311f2a312426d710e1c617fcbc8c-Abstract.html) - Kathuria, Deshpande, and Kohli, NeurIPS 2016. Diverse batches via DPPs.
- [The Parallel Knowledge Gradient Method for Batch Bayesian Optimization](https://proceedings.mlr.press/v48/wu16.html) - Wu and Frazier, ICML 2016. Parallel KG.
- [Parallelizing Exploration-Exploitation Tradeoffs with Gaussian Process Bandit Optimization](https://jmlr.org/papers/v15/desautels14a.html) - Desautels, Krause, and Burdick, JMLR 2014. GP-BUCB.
- [Parallel Gaussian Process Optimization with Upper Confidence Bound and Pure Exploration](https://link.springer.com/chapter/10.1007/978-3-642-40988-2_15) - Contal, Buffoni, Robicquet, and Vayatis, ECML 2013. GP-UCB-PE.

### Discrete and Mixed Spaces

- [Bounce: Reliable High-Dimensional Bayesian Optimization for Combinatorial and Mixed Spaces](https://proceedings.mlr.press/v202/papenmeier23a.html) - Papenmeier, Nardi, and Poloczek, ICML 2023. Nested embeddings plus trust regions.
- [Think Global and Act Local](https://proceedings.mlr.press/v139/wan21b.html) - Wan, Nguyen, Ha, Ru, and Osborne, ICML 2021. High-dimensional categorical and mixed spaces.
- [Bayesian Optimisation over Multiple Continuous and Categorical Inputs](https://proceedings.mlr.press/v119/ru20a.html) - Ru, Alvi, Nguyen, Osborne, and Roberts, ICML 2020. CoCaBO.
- [Combinatorial Bayesian Optimization using the Graph Cartesian Product](https://arxiv.org/abs/1902.00448) - Oh, Gavves, and Welling, NeurIPS 2019. COMBO.
- [Bayesian Optimization of Combinatorial Structures](https://proceedings.mlr.press/v80/baptista18a.html) - Baptista and Poloczek, ICML 2018. BOCS.

### Preferential Feedback

- [qEUBO: A Decision-Theoretic Acquisition Function for Preferential Bayesian Optimization](https://proceedings.mlr.press/v206/astudillo23a.html) - Astudillo, Lin, Bakshy, and Frazier, AISTATS 2023. Expected utility of the best option.
- [Preference Exploration for Efficient Bayesian Optimization with Multiple Outcomes](https://proceedings.mlr.press/v151/jerry-lin22a.html) - Lin, Astudillo, Frazier, and Bakshy, AISTATS 2022. Learn a utility from pairwise comparisons, then optimize it.
- [Preferential Bayesian Optimization](https://proceedings.mlr.press/v70/gonzalez17a.html) - González, Dai, Damianou, and Lawrence, ICML 2017. Optimize from pairwise comparisons rather than numeric scores.

### Meta-Learning

- [PFNs4BO: In-Context Learning for Bayesian Optimization](https://proceedings.mlr.press/v202/muller23a.html) - Müller, Feurer, Hollmann, and Hutter, ICML 2023. Prior-fitted networks as BO surrogates.
- [Initializing Bayesian Hyperparameter Optimization via Meta-Learning](https://ojs.aaai.org/index.php/AAAI/article/view/9354) - Feurer, Springenberg, and Hutter, AAAI 2015. Warm-start the BO prior from related tasks.

### LLMs and BO

The LLM is the optimizer (no GP), or it occupies one slot in a BO loop. CAKE is under Surrogate Design. FunBO is under Acquisition Functions. PlugBO is under Software and Blogs.

- [Agentic Bayesian Optimization through Surrogate-Augmented Autoresearch](https://arxiv.org/abs/2608.00316) - Brunzema et al., 2026. An LLM agent runs the loop; a BoTorch backend holds the posterior.
- [LLINBO: Trustworthy LLM-in-the-Loop Bayesian Optimization](https://arxiv.org/abs/2505.14756) - Chang, Azvar, Okwudire, and Al Kontar, 2025. Keep a GP in the loop so LLM proposals stay uncertainty-aware.
- [Reasoning BO: Enhancing Bayesian Optimization with Long-Context Reasoning Power of LLMs](https://arxiv.org/abs/2505.12833) - Yang et al., 2025. Reasoning models and a knowledge graph to guide BO sampling.
- [Large Language Models as Optimizers](https://proceedings.iclr.cc/paper_files/paper/2024/hash/3339f19c5fcee3ad74502947a32be9e6-Abstract-Conference.html) - Yang et al., ICLR 2024. OPRO: the LLM proposes candidates from a textual history, with no GP posterior.
- [Large Language Models to Enhance Bayesian Optimization](https://openreview.net/forum?id=OOxotBmGol) - Liu, Astorga, Seedat, and van der Schaar, ICLR 2024. LLAMBO: LLM warm-start, surrogate, and sampler inside a BO loop.

## Benchmarks

- [HPOBench](https://github.com/automl/HPOBench) - Containerized multi-fidelity HPO problems.
- [YAHPO Gym](https://github.com/slds-lmu/yahpo_gym) - Fast surrogate HPO benchmarks.
- [HPO-B](https://github.com/releaunifreiburg/HPO-B) - Transfer-HPO benchmark with related tasks.
- [LassoBench](https://github.com/ksehic/LassoBench) - High-dimensional weighted-Lasso HPO.
- [COCO / BBOB](https://github.com/numbbo/coco) - Noiseless and noisy black-box testbeds used beyond BO.
- [Bayesmark](https://github.com/uber/bayesmark) - Scoring harness for comparing BO libraries on ML models.

## Applications

Pointer papers and domain lists. New application papers that only use BO should go to a domain list, not here.

- [Bayesian Optimization for Learning Gaits under Uncertainty](https://link.springer.com/article/10.1007/s10472-015-9463-9) - Calandra et al., 2015. Early robotics application.
- [Accelerating Bayesian Optimization for Biological Sequence Design with Denoising Autoencoders](https://proceedings.mlr.press/v162/stanton22a.html) - Stanton et al., ICML 2022. Latent-space BO for sequences.
- [Bayesian Optimization for Automated Model Selection](https://papers.nips.cc/paper/2016/hash/3bbfdde8842a5c44a0323518eec97cbe-Abstract.html) - Malkomes, Schaff, and Garnett, NeurIPS 2016. BO over kernel and model families.
- [Awesome Bayesian Optimization (materials)](https://github.com/materials-data-facility/awesome-bayesian-optimization) - Materials-science software and papers.

## Community

- [Gaussian Process Summer School](https://gpss.cc/) - Annual lectures on GPs, often including BO.
- [AutoML](https://www.automl.org/) - HPO, NAS, and BO research group and conference.
- [Probabilistic Numerics](https://www.probabilistic-numerics.org/) - GPs, quadrature, and BO as numerical methods.
- [Advances in Bayesian Optimization](https://nips.cc/virtual/2022/tutorial/55806) - NeurIPS 2022 tutorial (Doppa, Aglietti, Gardner).
- [BoTorch documentation](https://botorch.org/docs/overview) - Tutorials for TuRBO, SAASBO, qEHVI, and constraints.

## Videos

- [Bayesian Optimization (Garnett, 2023)](https://www.youtube.com/watch?v=wZODGJzKmD0) - Lecture at the Probabilistic Numerics Spring School.
- [A Gentle Introduction to Bayesian Optimization (Baird, 2023)](https://www.youtube.com/watch?v=IVaWl2tL06c) - Accelerate Conference, University of Toronto.
- [Bayesian Optimization: Fundamentals, Implementation, and Practice (Nguyen, 2022)](https://www.youtube.com/watch?v=ImXOdgEgaTM) - PyData Global.
- [Bayesian Optimization (Frazier, 2018)](https://www.youtube.com/watch?v=c4KKvyWW_Xk) - INFORMS tutorial talk.
- [Bayesian Optimization (Hoffman, 2018)](https://www.youtube.com/watch?v=C5nqEHpdyoE) - UAI tutorial.
- [Bayesian Optimization with scikit-learn (Huijskens, 2017)](https://www.youtube.com/watch?v=jtRPxRnOXnk) - PyData London.
- [Global Optimization with Gaussian Processes (González, 2015)](https://www.youtube.com/watch?v=rG10zqtu8F4) - Gaussian Process Summer School.

## Blogs

- [PlugBO: A Modular Framework for Agentic Bayesian Optimization](https://richardcsuwandi.github.io/blog/2026/plug-bo/) - Richard Cornelius Suwandi, 2026.
- [A Unified View of Bayesian Optimization and Active Learning](https://richardcsuwandi.github.io/blog/2024/learn-with-a-goal/) - Richard Cornelius Suwandi, 2024.
- [Bayesian Optimization](https://krasserm.github.io/2018/03/21/bayesian-optimization/) - Martin Krasser, 2018. From-scratch GP and EI derivation.
- [Bayesian Optimization with scikit-learn](https://thuijskens.github.io/2016/12/29/bayesian-optimisation/) - Thomas Huijskens, 2016.

## Recent Preprints

Unreviewed method papers (Bayesian optimization is the contribution). Capped at 20, newest first. After peer review, open a PR to move an entry into the matching Papers section. Application papers are dropped on sight.

- [GRAPE: Gradient Refinement and Progress-Aware Exploitation for Query-Efficient High-Dimensional Bayesian Optimization](https://arxiv.org/abs/2608.25116) - 2026. High-dimensional BO with gradient refinement.
- [Adaptive KappaSharp: Condition-Number Shaping for Preferential Bayesian Optimization](https://arxiv.org/abs/2608.07859) - 2026. Preferential BO via condition-number shaping.
- [BOCoDe: Engineering-Centered Benchmarking for Bayesian Optimization](https://arxiv.org/abs/2608.15073) - 2026. Engineering BO benchmark.
- [Constraint-Bound Agnostic Bayesian Optimization: One Model for All Thresholds](https://arxiv.org/abs/2607.23448) - 2026. One constrained-BO model across thresholds.
- [Maximally Robust Satisficing Bayesian Optimization](https://arxiv.org/abs/2607.13652) - 2026. Satisficing under robustness requirements.
- [How Many Initial Points Does Bayesian Optimization Need?](https://arxiv.org/abs/2607.04356) - 2026. Design of the initial design.
- [Information-Theoretic Bayesian Optimization for Bilevel Optimization Problems](https://arxiv.org/abs/2509.21725) - 2025. Information-theoretic BO for bilevel problems.

## Contributing

See [contributing.md](contributing.md). Use the issue templates or open a pull request.
