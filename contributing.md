# Contribution Guidelines

This project follows the [Contributor Covenant](code-of-conduct.md). By taking part, you agree to that code of conduct.

This is a curated list, not an archive. A keyword match on "Bayesian optimization" is not enough.

## What belongs here

**Papers** must introduce a BO *method*, survey, tutorial, or benchmark that the community still uses. Typical yes: a new acquisition function, a high-dimensional algorithm, a constrained-BO formulation, a library paper.

**If you have a domain paper that uses BO** (materials, communications, robotics, drugs, and so on) but does not introduce a BO method, it belongs under [Applications](README.md#applications), not Papers. Applications is pointer papers and domain lists. A single case study that just runs BoTorch, Ax, or Optuna belongs in a domain list such as the [materials list](https://github.com/materials-data-facility/awesome-bayesian-optimization).

**Software** must be maintained (recent commits or releases), documented, and actually used for BO. Unmaintained tools go in [unmaintained.md](unmaintained.md). Related HPO tools that are not GP-BO (TPE, Hyperband-only, and similar) go under Related HPO tools, and the description must say so.

**Preprints** in Recent Preprints must have Bayesian optimization / BayesOpt *in the title*, and BO must be the contribution. The weekly bot only proposes title matches. Humans still merge.

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

## Reporting a problem

Open an issue if a link is dead, a year/venue is wrong, a package is unmaintained, or an entry is off-topic. PRs that just fix that are welcome.

## Docs site

The MkDocs site lives in `docs/`. Edit `README.md`, then run:

```bash
python scripts/sync_docs.py
```

That copies list sections into the matching docs pages. Do not edit `docs/books.md`, `docs/papers.md`, and similar by hand; they will be overwritten. `docs/index.md` and `unmaintained.md` are not generated.

```bash
pip install -r requirements-docs.txt
mkdocs serve
```
