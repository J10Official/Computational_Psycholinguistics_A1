# Disordered Speech Analysis with APROCSA

A computational psycholinguistics coursework project analyzing connected-speech transcripts, perceptual ratings, and associations between transcript-derived features and rated speech characteristics.

## Read the analysis

| Artifact | Purpose |
|---|---|
| [disordered-speech-analysis.pdf](disordered-speech-analysis.pdf) | Written report |
| [aprocsa_analysis.ipynb](aprocsa_analysis.ipynb) | Main analysis notebook, explanations, and saved outputs |
| [transcript_parser.py](transcript_parser.py) | CHAT transcript parsing and feature extraction |
| [aprocsa_heatmap.png](aprocsa_heatmap.png) | Saved perceptual-rating visualization |
| [correlation_scatter_plots.png](correlation_scatter_plots.png) | Saved feature/rating comparisons |

The notebook covers descriptive transcript analysis, correlation analysis, and exploratory regression with leave-one-out evaluation. See the report and notebook for methods and results.

## Reproduction requirements

The notebook imports pandas, NumPy, Matplotlib, seaborn, SciPy, and scikit-learn, alongside the local transcript parser. Open it in a compatible Jupyter environment and review its cells before execution.

The code expects a local `transcripts/` directory containing the source CHAT transcripts. That directory is not included in this repository snapshot. Obtain the appropriate source data independently and preserve the expected path before rerunning transcript-dependent cells. Saved results can be read without acquiring or executing the data pipeline.

This repository is an exploratory coursework artifact; its analyses are presented in the context of the supplied dataset and assignment.
