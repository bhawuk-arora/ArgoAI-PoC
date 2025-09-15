import xarray as xr
import pandas as pd

def run_etl(nc_file: str, out_csv: str):
    ds = xr.open_dataset(nc_file)
    df = ds.to_dataframe().reset_index()

    cols = [c for c in ["LATITUDE", "LONGITUDE", "PRES", "TEMP", "PSAL", "JULD"] if c in df.columns]
    if not cols:
        raise KeyError("No expected columns found in NetCDF file")

    df = df[cols]
    df.columns = [c.lower() for c in df.columns]

    df.to_csv(out_csv, index=False)
    print(f"[ETL] Saved {out_csv}")
    return out_csv

if __name__ == "__main__":
    run_etl("../data/sample_netcdf_data.nc", "../data/argo_profiles.csv")
