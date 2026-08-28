# Getting started

New to Bayesian optimization? A tutorial, then a book, then a library.

- [Exploring Bayesian Optimization](https://distill.pub/2020/bayesian-optimization/) - Interactive Distill article on GPs, acquisition functions, and the BO loop (Agnihotri and Batra, 2020).
- [Gaussian Processes for Machine Learning](https://gaussianprocess.org/gpml/) - Rasmussen and Williams, 2006. The GP textbook.
- [A Tutorial on Bayesian Optimization](https://arxiv.org/abs/1807.02811) - Frazier, 2018. The standard short tutorial, including noisy EI, batch, multi-fidelity, and constraints.
- [Recent Advances in Bayesian Optimization](https://bayesopt-tutorial.github.io/) - AAAI 2023 tutorial (slides and syllabus) covering high-dimensional, discrete, and causal BO.

Skip the GP book if Distill already made sense.

Then a book: [Garnett](books.md) for theory, or [Bayesian Optimization in Action](https://www.manning.com/books/bayesian-optimization-in-action) for a Python walkthrough.

Then a library. [Ax](https://ax.dev/) and [Vizier](https://github.com/google/vizier) are services: you declare the search space and the metric, and they run the loop. Start with Ax unless you already use Google's stack.

[BoTorch](https://botorch.org/) is the PyTorch toolkit under Ax. You write that loop yourself: fit a GPyTorch model, define an acquisition, optimize it. Use BoTorch when you are implementing a method, or changing the surrogate or the acquisition.

Other libraries are under [Software](software.md). Lectures are under [Community](community.md).
