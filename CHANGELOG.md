# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.4.0]
### Added
- `--depth_intervals` will output a bedGraph file with entries for each genomic interval featuring homogeneous depth
- `--phase_methyl` will output haplotype-level methylation calls, using the HP tags added by whatshap in the wf-human-snp workflow
- `--sv_benchmark` will benchmark SV calls with Truvari
    - The workflow uses the 'NIST_SVs_Integration_v0.6' truth set and benchmarking should be carried out on HG002 data.
### Changed
- Added coverage barrier to wf-human-variation
- When the SNP and SV subworkflows are both selected, the workflow will use the results of the SV subworkflow to refine the SNP calls
    - This new behaviour can be disabled with `--skip_refine_snp_with_sv`
- Updated to Oxford Nanopore Technologies PLC. Public License
- Workflow requires target regions to have 20x mean coverage to permit analysis
### Fixed
- `report_sv.py` now handles empty VCF files
- `report_str.py` now handles mono-allelic STR 
- WhatsHap processes do not block for long time with CRAM inputs due to missing REF_PATH
- filterCalls failure when input BED has more than three columns
- get_genome assumed STR subworkflow was always enabled, preventing CNV analysis with hg19
- "genome build (...) is not compatible with this workflow" was incorrectly thrown when the workflow stopped before calling get_genome

## [v1.3.0]
### Added
- `--str` enables STR genotyping using Straglr (compatible with genome build 38 only)
### Changed
- Minor performance improvement when checking for empty VCF in aggregate pileup steps

## [v1.2.0]
### Added
- `--cnv` enables CNV calling using QDNAseq

## [v1.1.0]
### Changed
* Updated Dorado container image to use Dorado v0.1.1
    * Latest models are now v4.0.0
    * Workflow prints a more helpful error when Dorado fails due to unknown model name
* Updated wf-human-snp container image to load new Clair3 models for v4 basecalling
* Default `basecaller_cfg` set to `dna_r10.4.1_e8.2_400bps_sup@v4.0.0`
### Added
* `--basecaller_args` may be used to provide custom arguments to the basecalling process

## [v1.0.1]
### Changed
* Default `basecaller_cfg` set to `dna_r10.4.1_e8.2_400bps_sup@v3.5.2`
* Updated description in manifest

## [v1.0.0]
### Added
* `nextflow run epi2me-labs/wf-human-variation --version` will now print the workflow version number and exit
### Changed
* `--modbam2bed_args` can be used to further configure the wf-methylation `modbam2bed` process
* `modbam2bed` outputs are now prefixed with `<sample_name>.methyl`
* `--basecall_cfg` is now required by the SNP calling subworkflow to automatically pick a suitable Clair3 model
    * Users no longer have to provide `--model` for the SNP calling subworkflow
* Tidied workflow parameter schema
    * Some advanced options that are primarily used for benchmarking are now hidden but can be listed with `--help --show_hidden_params`
* wf-basecalling subworkflow now separates reads into pass and fail CRAMs based on mean qscore
    * The workflow will index and align both the pass and fail reads and provide a CRAM for each in the output directory
    * Only pass reads are used for downstream variant calling
* Updated wf-human-variation-snp container to use Sniffles v2.0.7
### Removed
* `-profile conda` is no longer supported, users should use `-profile standard` (Docker) or `-profile singularity` instead
* `--report_name` is no longer required and reports will be prefixed with `--sample_name` instead
### Fixed
* Workflow will exit with "No files match pattern" if no suitable files are found to basecall
    * Ensure to set `--dorado_ext` to `fast5` or `pod5` as appropriate

## [v0.4.1]
### Fixed
* JBrowse2 configuration failed to load AlignmentTrack for CRAM output

## [v0.4.0]
### Added
* Workflow will now output a JBrowse2 `jbrowse.json` configuration
* Workflow reports will be visible in the Nextflow Tower reports tab
### Changed
* wf-basecalling 0.0.1 has been integrated to wf-human-variation
    * Basecalling is now conducted with Dorado
    * Basecalling options have changed, users are advised to check the basecalling options in `--help` for guidance
* GPU accelerated processes can now have their process directives generically modified in downstream user profiles using `withLabel:gpu`
* `mapula` will no longer run by default due to performance issues on large data sets and must be enabled with `--mapula`
    * This step will be deprecated and replaced with an equivalent in a future release
### Fixed
* uBAM input no longer requires an index
* CRAM is written to the output directory in all cases where alignment was completed

## [v0.3.1]
### Fixed
* `check_for_alignment` did not support uBAM
* Set `PYTHONNOUSERSITE` to reduce risk of environment bleed

## [v0.3.0]
### Added
* Experimental guppy subworkflow
    * We do not provide a Docker container for Guppy at this time, users will need to override `process.withLabel:wf_guppy.container`
### Changed
* `--ubam` option removed, users can now pass unaligned or aligned BAM (or CRAM) to `--bam`
    * If the input BAM is aligned and the provided `--ref` does not match the SQ lines (exact match to name and size) the file will be realigned to `--ref`
    * If the input CRAM is aligned and the provided `--ref` does not match the SQ lines (exact match to name and size) the file will be realigned to `--ref`, but will also require the old reference to be provided with `--old_ref` to avoid reference lookups
    * If the input is not aligned, the file will be aligned to `--ref`
### Fixed
* Chunks without variants will no longer terminate the workflow at the `create_candidates` step

## [v0.2.3]
### Added
* [`mapula`](https://github.com/epi2me-labs/mapula) used to generate basic alignment QC statistics in both CSV and JSON
### Changed
* Updated Clair3 to 0.1.12 (build 6) which bundles Longphase 1.3 to enable CRAM support and small improvement to accuracy
* `mosdepth` artifacts are now written to the output directory
    * Additionally outputs read counts at 1,10,20,30X coverage thresholds for each region in the input BAM (or each sequence of the reference if no BED is provided)
* Simplified `wf-human-sv` Docker image and conda definition
### Fixed
* Outdated conda environment definitions
* Docker based profiles no longer requires an internet connection to fetch the `cram_cache` cache building script

## [v0.2.2]
### Fixed
* "No such property" when using the `minimap2_ubam` alignment step
* Slow performance on `minimap2_ubam` step when providing CRAM as `--ubam`
* Slow performance on `snp:readStats` process
### Removed
* "Missing reference index" warning was unnecessary

## [v0.2.0]
### Added
* An experimental methylation subworkflow has been integrated, using [`modbam2bed`](https://github.com/epi2me-labs/modbam2bed) to aggregate modified base counts (input BAM should have `MM` and `ML` tags), enable this with `--methyl`
### Changed
* Workflow experimentally supports CRAM as input, uBAM input uses CRAM for intermediate files
* Reference FAI is now created if it does not exist, rather than raising an error
* `--sniffles_args` may be used to provide custom arguments to the `sniffles2` process
* Output files are uniformly prefixed with `--sample_name`
* Output alignment from `--ubam` is now CRAM formatted
### Fixed
* Existence of Clair3 model directory is checked before starting workflow
* `--GVCF` and `--include_all_ctgs` are correctly typed as booleans
    * `--GVCF` now outputs GVCF files to the output directory as intended
    * `--include_all_ctgs` no longer needs to be set as `--include_all_ctgs y`

## [v0.1.1]
### Added
* `--ubam_bam2fq_threads` and `--ubam_sort_threads` allow finer control over the resourcing of the alignment step
    * The number of CPU required for `minimap2_ubam` is sum(`ubam_bam2fq_threads`, `ubam_map_threads`, `ubam_sort_threads`)
### Changed
* `--ubam_threads` is now `--ubam_map_threads` and only sets the threads for the mapping specifically
* `--ref` is now required by the schema, preventing obscure errors when it is not provided
* Print helpful warning if neither `--snp` or `--sv` have been specified
* Fastqingress metadata map
* Disable dag creation by default to suppress graphviz warning
### Fixed
* Tandem repeat BED is now correctly set by `--tr_bed`
* Update `fastcat` dependency to 0.4.11 to catch cases where input FASTQ cannot be read
* Sanitize fastq intermittent null object error
### Note
- Switched to "new flavour" CI, meaning that containers are released from workflows independently

## [v0.1.0]
# Added
- Ported wf-human-snp (v0.3.2) to modules/wf-human-snp
- Ported wf-human-sv (v0.1.0) to modules/wf-human-sv

## [v0.0.0]
- Initialised wf-human-variation from wf-template #195cab5
