# Contributing

This project follows the [Contributor Covenant](https://github.com/richardcsuwandi/awesome-bo/blob/main/code-of-conduct.md). By taking part, you agree to that code of conduct.

This is a curated list, not an archive. A keyword match on "Bayesian optimization" is not enough.

The [GitHub README](https://github.com/richardcsuwandi/awesome-bo#readme) is what `awesome-lint` checks. Edit `README.md`, then run `python scripts/sync_docs.py` so the docs pages match.

## What belongs here

**Papers** should present a relevant method, survey, tutorial, or benchmark that substantially contributes to the Bayesian optimization field or its community. Examples include new algorithmic advances, methodological developments, broadly-used libraries, or widely-referenced benchmarks.

**If you are submitting a paper that applies BO in any domain** (such as science, engineering, industry, etc.) but does not introduce new BO methodology, add it under [Applications](applications.md) instead of Papers. Applications is for works that show how BO is being used in practice or in particular fields. Simple case studies that just use off-the-shelf tools (like BoTorch, Ax, Optuna, etc.) should be added to the most relevant domain list (for example, see the [materials list](https://github.com/materials-data-facility/awesome-bayesian-optimization)).

**Software** should be actively maintained (with recent updates), include documentation, and offer real support for BO. Outdated or unsupported software goes under [Unmaintained](unmaintained.md). If a tool is related to hyperparameter optimization but does not use Gaussian Process-based BO (such as TPE, Hyperband variants, and similar), please list it under Related HPO tools and specify this in the description.

**Preprints** must have Bayesian optimization / BayesOpt *in the title*, and BO must be the contribution. The weekly automated bot only proposes additions, but the maintainer has final say and decides whether to merge them.

## How to add something

1. Open an issue with the matching template (paper, software, or resource), **or** open a pull request.
2. Put the entry in the right section and in the right place (see [Where to put it](#where-to-put-it)). Do not append at the bottom of a subsection unless nothing nearby fits.
3. Use this format, and nothing else:

   ```markdown
   - [Name](https://example.com) - Short why-it-belongs sentence.
   ```

   The description starts with an uppercase letter and ends with a period.
4. Prefer a stable landing page (proceedings, OpenReview, arXiv abs, project site) over a raw PDF when both exist.
5. Do not duplicate a URL that is already in the README.
6. One pull request per addition, unless you are doing a small batch of clearly related items.
7. Run `python scripts/sync_docs.py` so the docs site matches the README.

## Where to put it

**Papers.** Within each subsection, newest year first. Same year: alphabetical by title. Two exceptions: Foundations is a reading path, so oldest first. Surveys and Tutorials keeps the two canonical intros at the top, then newest first for the rest.

**Recent Preprints** is newest first. After acceptance, move the entry into the matching Papers subsection by year. Do not leave it at the end of that subsection.

**Software** is not ordered by year. Place a library next to the closest existing tools: same job, same stack, or the one people already compare it to. Example: BayBE sits next to BoFire because both are industrial DOE/BO libraries. Do not dump new entries at the bottom of the list.

## Weekly arXiv pull requests

`scripts/update_papers.py` may open a PR that only adds **Recent Preprints** in `README.md`, then runs `scripts/sync_docs.py`. Review it:

- Drop application papers even if the title contains "Bayesian optimization".
- Keep method papers. After acceptance, insert them into the matching Papers subsection by year and remove them from Recent Preprints.
- Never merge a PR that writes into the curated Papers sections automatically.

## Docs site

```bash
python scripts/sync_docs.py
pip install -r requirements-docs.txt
mkdocs serve
```

Do not edit generated list pages (`docs/books.md`, `docs/papers.md`, and similar) by hand. The site deploys to GitHub Pages on every push that touches `docs/` or `mkdocs.yml`.

## Reporting a problem

Open an issue if a link is dead, a year/venue is wrong, a package is unmaintained, or an entry is off-topic. PRs that just fix that are welcome.
