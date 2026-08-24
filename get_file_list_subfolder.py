#!/usr/bin/env python3
"""
Genera la lista dei path completi dei file .root
per alcune sottocartelle di /pnfs/sbn/scratch/users/twester/Run4_ReCAF2026/flatcaf/

Uso:
    python3 list_flatcaf_paths.py --folders 000000 000005 000010
    python3 list_flatcaf_paths.py --range 0 10          # cartelle 000000-000009
    python3 list_flatcaf_paths.py --all                 # tutte le cartelle
    python3 list_flatcaf_paths.py --range 0 10 --out lista.txt
"""

import argparse
import os
from pathlib import Path

BASE_DIR = Path("/pnfs/sbn/scratch/users/twester/Run4_ReCAF2026/flatcaf")


def get_root_files(folder: Path):
    """Ritorna la lista di tutti i file .root trovati ricorsivamente in 'folder'."""
    return [str(p) for p in folder.rglob("*.root")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--folders", nargs="+",
        help="Nomi espliciti delle cartelle top-level (es. 000000 000005)"
    )
    group.add_argument(
        "--range", nargs=2, type=int, metavar=("START", "END"),
        help="Range di indici (es. 0 10 -> 000000 ... 000009)"
    )
    group.add_argument(
        "--all", action="store_true",
        help="Usa tutte le cartelle top-level presenti in BASE_DIR"
    )
    parser.add_argument(
        "--out", type=str, default=None,
        help="File di output dove salvare i path (uno per riga). Se omesso, stampa a schermo."
    )
    args = parser.parse_args()

    if not BASE_DIR.exists():
        raise SystemExit(f"Errore: {BASE_DIR} non esiste o non è montata.")

    # Determina la lista di cartelle target
    if args.folders:
        folder_names = args.folders
    elif args.range:
        start, end = args.range
        folder_names = [f"{i:06d}" for i in range(start, end)]
    else:  # --all
        folder_names = sorted(
            p.name for p in BASE_DIR.iterdir() if p.is_dir()
        )

    all_paths = []
    for name in folder_names:
        folder_path = BASE_DIR / name
        if not folder_path.is_dir():
            print(f"Attenzione: {folder_path} non esiste, la salto.")
            continue
        files = get_root_files(folder_path)
        print(f"{name}: trovati {len(files)} file .root")
        all_paths.extend(files)

    print(f"\nTotale file trovati: {len(all_paths)}")

    if args.out:
        with open(args.out, "w") as f:
            f.write("\n".join(all_paths) + "\n")
        print(f"Lista salvata in: {args.out}")
    else:
        print("\n".join(all_paths))


if __name__ == "__main__":
    main()