#!/usr/bin/env python
"""Create workflow report."""

from aplanat import annot, hist, report
from aplanat.components import depthcoverage
from aplanat.components import simple as scomponents
from aplanat.report import WFReport
from aplanat.util import Colors
from bokeh.layouts import gridplot
import numpy as np
import pandas as pd
from .util import wf_parser  # noqa: ABS101


def plot_qc_stats(read_stats):
    """Plot read QC stats."""
    # read length
    tp = pd.read_csv(
        read_stats, sep='\t', chunksize=1000, iterator=True)
    seq_summary = pd.concat(tp, ignore_index=True)
    total_bases = seq_summary['read_length'].sum()
    mean_length = total_bases / len(seq_summary)
    median_length = np.median(seq_summary['read_length'])
    datas = [seq_summary['read_length']]
    length_hist = hist.histogram(
        datas, colors=[Colors.cerulean], bins=100,
        title="Read length distribution.",
        x_axis_label='Read Length / bases',
        y_axis_label='Number of reads',
        xlim=(0, None))
    length_hist = annot.subtitle(
        length_hist,
        "Mean: {:.0f}. Median: {:.0f}".format(
            mean_length, median_length))

    # read quality
    datas = [seq_summary['acc']]
    mean_q, median_q = np.mean(datas[0]), np.median(datas[0])
    q_hist = hist.histogram(
        datas, colors=[Colors.cerulean], bins=100,
        title="Read quality (wrt reference sequence)",
        x_axis_label="Read Quality",
        y_axis_label="Number of reads",
        xlim=(85, 100))
    q_hist = annot.subtitle(
        q_hist,
        "Mean: {:.0f}. Median: {:.0f}".format(
            mean_q, median_q))
    return gridplot([[length_hist, q_hist]])


def depth_plot_section(read_depth, section):
    """Add read depth plots to a given section."""
    rd_plot = depthcoverage.cumulative_depth_from_dist(read_depth)
    section.markdown("""
### Genome coverage
This section displays basic metrics relating to genome coverage.
""")
    section.plot(gridplot(
        [rd_plot],
        ncols=2)
    )


def main(args):
    """Run the entry point."""
    report_doc = report.HTMLReport(
        "Haploid variant calling Summary Report",
        ("Results generated through the wf-hap-snp nextflow "
            "workflow provided by Oxford Nanopore Technologies"))

    report_doc = WFReport(
        "Low-coverage bam QC", "wf-human-variation",
        revision=args.revision, commit=args.commit)

    section = report_doc.add_section()
    section.markdown(f"""
### Read Quality control
This section displays basic QC metrics indicating read data quality.
This dataset was not processed by the workflow as it did not meet the minimum
bam coverage of {args.low_cov}x required.
""")
    section.plot(plot_qc_stats(args.read_stats))

    if args.read_depth:
        section = report_doc.add_section()
        depth_plot_section(args.read_depth, section)

    report_doc.add_section(
        section=scomponents.version_table(args.versions))
    report_doc.add_section(
        section=scomponents.params_table(args.params))
    # write report
    report_doc.write(args.report)


def argparser():
    """Create argument parser."""
    parser = wf_parser("report_qc")

    parser.add_argument("report", help="Report output file")
    parser.add_argument(
        "--read_stats", default='unknown',
        help="read statistics output from bamstats")
    parser.add_argument(
        "--versions", required=True,
        help="directory containing CSVs containing name,version.")
    parser.add_argument(
        "--params", required=True,
        help="directory containing CSVs containing name,version.")
    parser.add_argument(
        "--revision", default='unknown',
        help="git branch/tag of the executed workflow")
    parser.add_argument(
        "--commit", default='unknown',
        help="git commit of the executed workflow")
    parser.add_argument(
        "--read_depth", default="unknown",
        help="read coverage output from mosdepth")
    parser.add_argument(
        "--low_cov", default="unknown",
        help="define if the QC report should be for low-cov bam")

    return parser
