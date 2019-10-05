#!/usr/bin/python
import sys
import getopt
import os
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description='Annotate spectra')
    parser.add_argument("input_sirius_mgf")
    parser.add_argument("input_quant_table")
    parser.add_argument("output_folder")
    parser.add_argument("conda_activate_bin")
    parser.add_argument("conda_environment")
    parser.add_argument("sirius_bin")

    args = parser.parse_args()

    output_feature_qza = os.path.join(args.output_folder, "feature-table.qza")
    output_mgf_qza = os.path.join(args.output_folder, "sirius.mgf.qza")
    output_fragtree_qza = os.path.join(args.output_folder, "fragmentation_trees.qza")
    output_formula_qza = os.path.join(args.output_folder, "formula.qza")
    output_fingerprints_qza = os.path.join(args.output_folder, "fingerprints.qza")
    output_merged_feature_table_qza = os.path.join(args.output_folder, "merged_feature_table.qza")
    output_merged_data_qza = os.path.join(args.output_folder, "merged_data.qza")

    all_cmd = []
    cmd = "source {} {} && LC_ALL=en_US && export LC_ALL && qiime tools import --input-path {} --output-path {} --type FeatureTable[Frequency]".format(args.conda_activate_bin, args.conda_environment, args.input_quant_table, output_feature_qza)
    all_cmd.append(cmd)

    cmd = "source {} {} && LC_ALL=en_US && export LC_ALL && qiime tools import --input-path {} --output-path {} --type MassSpectrometryFeatures".format(args.conda_activate_bin, args.conda_environment, args.input_sirius_mgf, output_mgf_qza)
    all_cmd.append(cmd)

    cmd = 'source {} {} && LC_ALL=en_US && export LC_ALL && qiime qemistree compute-fragmentation-trees --p-sirius-path {} \
    --i-features {} \
    --p-ppm-max 15 \
    --p-profile orbitrap \
    --p-ionization-mode positive \
    --p-java-flags "-Djava.io.tmpdir=./temp -Xms16G -Xmx64G" \
    --o-fragmentation-trees {}'.format(args.conda_activate_bin, args.conda_environment, args.sirius_bin, output_mgf_qza, output_fragtree_qza)
    all_cmd.append(cmd)

    cmd = 'source {} {} && LC_ALL=en_US && export LC_ALL && qiime qemistree rerank-molecular-formulas --p-sirius-path {} \
    --i-features {} \
    --i-fragmentation-trees {} \
    --p-zodiac-threshold 0.95 \
    --p-java-flags "-Djava.io.tmpdir=./temp -Xms16G -Xmx64G" \
    --o-molecular-formulas {}'.format(args.conda_activate_bin, args.conda_environment, args.sirius_bin, output_mgf_qza, output_fragtree_qza, output_formula_qza)
    all_cmd.append(cmd)

    cmd = 'source {} {} && LC_ALL=en_US && export LC_ALL && qiime qemistree predict-fingerprints --p-sirius-path {} \
    --i-molecular-formulas {} \
    --p-ppm-max 20 \
    --p-java-flags "-Djava.io.tmpdir=./temp -Xms16G -Xmx64G" \
    --o-predicted-fingerprints {}'.format(args.conda_activate_bin, args.conda_environment, args.sirius_bin, output_formula_qza, output_fingerprints_qza)
    all_cmd.append(cmd)

    cmd = 'source {} {} && LC_ALL=en_US && export LC_ALL && qiime qemistree make-hierarchy \
    --i-csi-results {} \
    --i-feature-tables {} \
    --o-tree demo-qemistree.qza \
    --o-merged-feature-table {} \
    --o-merged-feature-data {}'.format(args.conda_activate_bin, args.conda_environment, \
        output_fingerprints_qza, \
        output_feature_qza, \
        output_merged_feature_table_qza, \
        output_merged_data_qza)
    all_cmd.append(cmd)

    for cmd in all_cmd:
        print(cmd)
        os.system(cmd)

if __name__ == "__main__":
    main()
