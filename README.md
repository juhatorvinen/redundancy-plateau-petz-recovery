# Redundancy Plateau and the Quality of Petz Recovery

Code accompanying the paper:

> *Redundancy Plateau and the Quality of Petz Recovery*, \
> Juha Torvinen, Esko Keski-Vakkuri, Nicola Pranzini, 2026

## Overview

This repository contains the code and notebooks used to study the emergence of redundancy plateaus in quantum Darwinism and their relation to the performance of Petz recovery maps. Overall, we aim to

- analyze redundancy plateaus in one-to-all qubit models,
- quantify recovery quality using Petz maps,

and additionally, provide easy tools to

- reproduce all figures from the paper and
- study the basic properties of Petz recovery for one-to-all systems.

---

## Repository structure

- `src/` – Includes core Python functions used in notebooks
- `notebooks/` – Main analysis notebooks used for the figures in the manuscript
- `supplementary-material/` – Introductory content on petz maps and one-to-all systems, great starting point!
- `results/` – Generated figures used in paper

---

## Installation

Included are two different options for reproducing an environment for running the notebooks. Note that these only consider the minimal set of dependencies to ensure compatability: Things like Jupyter support for notebooks and similar things are left out to be solved by the user in the pip option. The conda environment should include everything necessary.

Before installing said dependencies, you can clone the repository to your computer and change directories to it by running the following lines from a terminal:

```bash
git clone https://github.com/juhatorvinen/redundancy-plateau-petz-recovery.git
cd redundancy-plateau-petz-recovery
```

To install dependencies with pip, one can simply run

```bash
pip install -r requirements.txt
```

Alternatively, one can create and activate a conda environment from the provided .yml file with the following commands:

```bash
conda env create -f environment.yml
conda activate petz-env-conda
```

## Reproducing results

We provide individual notebooks for reproducing all the figures appearing in the paper. These can be found in the "notebooks" directory and are quite straight forward to run, as all required details are prepared by default to match results. Precomputed results are available in the "results" directory as running the provided notebooks with preset settings can take a while!

(plots not in initial commit)

## Citation

Update citation instructions later.