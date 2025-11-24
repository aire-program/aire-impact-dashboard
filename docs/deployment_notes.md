# Deployment Notes

## Local Development
1. Clone the repository.
2. `pip install -r requirements.txt`
3. `python scripts/generate_dummy_data.py`
4. `streamlit run app/main.py`

## Original Internal Deployment
This dashboard was originally deployed on an internal VM within the MSU network, accessible only via VPN. It connected to a live SQL database which has been replaced here by static CSVs for privacy and portability.

## Production Considerations
- For a live deployment, replace `app/data_loader.py` with a SQL connector.
- Ensure `secrets.toml` is configured if adding authentication.
