# Replicating Card & Krueger (1994): the sign survives, the precision does not

*Worked example for the ECON 5200 Replication Study. A sample of the README the Section 6 row grades: copy its
shape, not its content.*

## The one command

```bash
pip install -r requirements.txt
python run_all.py
```

`run_all.py` downloads David Card's public file, rebuilds Table 1 and the four robustness exercises, and writes
`output/table1.csv`, `output/robustness.csv`, `output/figure_chain.png` and `output/numbers.json`. Every number
in `report.pdf` is in `output/numbers.json`. Runtime: about 30 seconds, most of it the wild cluster bootstrap.

## Data

`njmin.zip` from https://davidcard.berkeley.edu/data_sets/njmin.zip, downloaded at run time by `download_data.py`
rather than committed: it is Card's distribution, and fetching it keeps the provenance visible. The codebook and
Card's own `check.sas` come in the same archive and define every variable used here.

## Layout

| path | what it is |
|---|---|
| `download_data.py` | fetches and unpacks `njmin.zip` into `data/` |
| `run_all.py` | Sections 2 and 3, in order; writes `output/` |
| `report.pdf` | the report (12 pages at most) |
| `ai-appendix.md` | which sections used AI, with the P.R.I.M.E. entries and transcripts |

## Checkpoints, as the commit history shows them

- Section 1 and the replication table committed by the Sections 1–2 checkpoint.
- Repository made public the next day, for the auditor.
- Robustness and Section 4 committed after the audit pairs were assigned; the audit issue filed on the partner's
  repository by the deadline.

## AI use

*Which sections used AI (Sections 1 and 2 may not), with the entries in `ai-appendix.md`.*
