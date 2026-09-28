# Exploratory protocol (version 0.2)

## Question
How stable is spatial overlap between the *association test* maps for `emotion regulation`, `reward`, and `depression` under different positive z-score thresholds?

## Planned comparison
1. Primary descriptive pair: `emotion regulation` × `reward`; secondary: each versus `depression`.
2. Download the same map type from the same Neurosynth release and record URLs, retrieval date, file hashes, and study counts. This analysis retrieves the unthresholded association z maps using the `?unthresholded` endpoint called by the Neurosynth viewer. The ordinary download link may provide an FDR-corrected image; do not mix the two map types. URLs and hashes are in `results/provenance.json`.
3. Verify 3D shape and affine match; report any resampling decision separately. Exclude pairwise nonfinite voxels. Use thresholds z = 2, 3, 4, 5 on positive values.
4. For each threshold report active voxel counts, intersection, Jaccard and Dice. Inspect maps visually in at least three axial slices. Treat this as descriptive threshold sensitivity on unthresholded z maps. Applying a cutoff does not itself provide multiple-comparison correction or independent inference.
5. Describe changes in overlap with threshold and inspect term-specific maps. Do not interpret a voxel count as a number of participants or an effect size.

## Limits and interpretation
This is a descriptive comparison of already computed term maps. Correlated studies, term ambiguity, reporting and publication bias, differing numbers of studies, and spatial autocorrelation rule out a naive statistical significance claim for overlap. `Depression` in an abstract is not equivalent to a patient diagnosis. No individual brain or clinical prediction is evaluated. A formal inferential extension would require a carefully justified spatial null model and control of term/study dependencies; this prototype does not supply one.

## Report template
- Source files and SHA-256 hashes:
- Study counts and Neurosynth version/retrieval date:
- Preprocessing or resampling:
- Threshold table and three representative slices:
- Observation across thresholds:
- Competing explanation and limitations:
- Next falsifiable question:
