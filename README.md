# AIVC-RNA-PRO-FGFR1

Auditable multimodal virtual-cell drug-screening demo: STATE transcriptomics → ProteinTalks proteomics → multimodal ranking → molecular docking.

## Candidate and real results

- Target: **FGFR1**
- Candidate: **Erdafitinib**
- Multimodal rank: **#1**
- Best AutoDock Vina score: **−9.147 kcal/mol**
- Lowest redocking RMSD against PDB 5EW8: **0.886 Å**

Docking scores rank poses; they are not experimental binding free energies or proof of efficacy.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Large datasets, checkpoints, logs, private paths and licensed font files are intentionally excluded.
