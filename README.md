Process which uses dlt(https://dlthub.com/docs/intro) to download raw JSON data from the CISA Known Exploited Vulnerability catalog and loads it into a duckdb database using a Pydantic data model.

This is more of proof of concept to see what creating a pipeline using dlt looks like in an effort to see how using an upsert style flow would work. 

To run loading data into a development database:

`ENV_FOR_DYNACONF=development python data_pipeline.py`