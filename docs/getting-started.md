# Getting started

New to Bayesian optimization? Read these in order, then pick a library.

- [Exploring Bayesian Optimization](https://distill.pub/2020/bayesian-optimization/) - Interactive Distill article on GPs, acquisition functions, and the BO loop (Agnihotri and Batra, 2020).
- [Gaussian Processes for Machine Learning](https://gaussianprocess.org/gpml/) - Rasmussen and Williams, 2006. The GP textbook. Read this if Distill's GP section was not enough.
- [A Tutorial on Bayesian Optimization](https://arxiv.org/abs/1807.02811) - Frazier, 2018. The standard short tutorial, including noisy EI, batch, multi-fidelity, and constraints.
- [Recent Advances in Bayesian Optimization](https://bayesopt-tutorial.github.io/) - AAAI 2023 tutorial (slides and syllabus) covering high-dimensional, discrete, and causal BO.

Then read [Garnett's book](books.md) for theory, or [Bayesian Optimization in Action](https://www.manning.com/books/bayesian-optimization-in-action) for a Python walkthrough.

Pick a library. [Ax](https://ax.dev/) is the service: you declare the search space and the metric, and Ax chooses the next experiment, fits the model, and runs the loop. [BoTorch](https://botorch.org/) is the PyTorch library Ax is built on. You write that loop yourself: fit a GPyTorch model, define an acquisition, optimize it. Use Ax if you want to run an experiment. Use BoTorch if you are implementing a method, or changing the surrogate or the acquisition. [Vizier](https://github.com/google/vizier) is the other service-style option. All three are listed under [Software](software.md).

For lectures, see [Community](community.md).
