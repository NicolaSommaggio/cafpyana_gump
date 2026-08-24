#!/usr/bin/env python3
"""Variante di run_gumple_pipeline.py: tutti i sistematici tranne detvar_spline."""
import os
import sys

workspace_root = os.getcwd()
sys.path.insert(0, workspace_root + "/../gump/")
from sbruce import *
sys.path.insert(0, workspace_root + "/../maple/")
import loaddf
import cafpyana_gump.analysis_village.gumple.custom_post_selection as custom_post_selection

INPUT = "/pnfs/icarus/scratch/users/nsommagg/df_store/n_ICARUS_Run4_CV_fullsel_evtrec_000007_light.df"
OUTPUT = "/exp/icarus/app/users/nsommagg/cafpyana_gump/n_Icarus_Run4_CV_fullsel_no_d_var_000007_light_MAPLEonly.root"
TEMP_STAGE1 = OUTPUT.replace(".root", "_stage1_tmp.root")

df, _, _ = loaddf.loadl(
    [INPUT],
    njob=1,
    xsec_univ=False,
    flux_univ=False,
    sep_flux_univ=True,     # flusso: acceso
    sep_g4_univ=True,       # Geant4: acceso
    xsec_spline=True,       # cross-section GENIE: acceso
    pot_spline=True,        # POT systematic: acceso
    match_Enu=True,         # is_mc=True
    load_truth=True,        # is_mc=True
    detvar_spline=False,    # <-- QUESTO è quello che vuoi spento
    spline_dir="rwt_outputs",
    include_syst=True,      # deve restare True, altrimenti scatta l'early return e salta TUTTO
    reweight_aFF=True,
    preselection=custom_post_selection.maple_sel_only,
    detector="ICARUS Run4",
    lightmem=True,
)

export_dataframe_to_uproot(df, TEMP_STAGE1)
run_makesbruce_macro(TEMP_STAGE1, OUTPUT)
os.remove(TEMP_STAGE1)
print(f"Completato: {OUTPUT}")