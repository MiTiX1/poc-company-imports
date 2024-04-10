import polars as pl

def load_db_dump() -> pl.DataFrame:
    df = pl.read_json("./companies.json")
    df.drop_in_place("_id")
    df = df.rename({"name": "input_name"})
    df = df.unnest(["linkedin"])
    df = df.rename({"name": "linkedin_name", "account": "linkedin_url"})
    df = df.select("linkedin_url").drop_nulls().join(df, on="linkedin_url", how="inner").unique()
    return df.with_columns(pl.Series([f"https://www.linkedin.com/company/{i[0]}" for i in df.select("linkedin_url").iter_rows()]).alias("linkedin_url"))
    