# Deploy on Streamlit Community Cloud

This repository is ready to deploy as a public Streamlit website.

## 1. Upload to GitHub

Create a new GitHub repository and upload the **contents of this folder** so that `app.py` and `requirements.txt` are at the repository root.

Recommended repository name:

`kiremire-k-theory-calculator`

## 2. Deploy

1. Sign in to Streamlit Community Cloud: https://share.streamlit.io/
2. Choose **Create app** / **New app**.
3. Select the GitHub repository.
4. Set the main file path to:

   `app.py`

5. Deploy.

No API keys or secrets are required for Version 1.

## 3. Local test before deployment

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Then open `http://localhost:8501` if the browser does not open automatically.

## 4. Verification

Before publishing a new release, run:

```bash
python verify_examples.py
python -m pytest -q
```

The current release includes the K-theory periodic-table image under `assets/` and its data under `data/`.
