# Arabic News Coverage Comparison & Bias Detection 📰

An NLP system that matches news stories about the same event across different Arabic news sources, then compares how each source covers it: the wording used, the facts left out, and the tone, and estimates each source's bias.

> **Status:** 🚧 In progress. The project is currently in the planning phase.

## Overview

News outlets often cover the same event very differently. This project aims to make those differences visible by:

1. Finding articles from different sources that report the same story.
2. Comparing each pair of articles in detail.
3. Detecting bias in each source and visualizing it.

## Data Sources

| Source | Purpose |
|---|---|
| **SaudiNewsNet** | Development and experimentation only |
| **Arabic Billion Words** | A small sample from two newspapers over a shared time period |
| **RSS feeds** (2-3 contrasting sources) | Real-world results; collection starts early |

## Story Matching

Two articles are considered the same story only if **all three** conditions hold:

1. **Semantic similarity:** the articles have a similar meaning.
2. **Date proximity:** published within one to two days of each other.
3. **Shared named entities:** they mention common people or places.

Similarity alone is not enough to match two articles.

## Bias Detection

- **Training:** BABE dataset, using a multilingual model.
- **Evaluation:** 300 Arabic sentences, manually labeled by the team.
- **Comparison:** a baseline model vs. AraBERT.

## Outputs

- **Bias heatmap:** the bias level of each news source.
- **Pairwise comparison report** for every matched pair of articles:
  - Differences in wording
  - Information omitted by each source
  - Tone of each source

## Roadmap

- [ ] Start collecting RSS data
- [ ] Prepare SaudiNewsNet and Arabic Billion Words samples
- [ ] Build the story matching pipeline (similarity + date + entities)
- [ ] Label 300 Arabic sentences for evaluation
- [ ] Train the baseline model and AraBERT on BABE
- [ ] Build the pairwise comparison module
- [ ] Generate the bias heatmap
- [ ] Evaluate and document results

## Team

- Manar Abu-Irsheid
- Alaa Badawi
- Sadeel Aladamat
- Balqees Rwias
