CREATE TABLE [dbo].[business_silver] (

	[business_id] varchar(8000) NULL, 
	[name] varchar(8000) NULL, 
	[address] varchar(8000) NULL, 
	[city] varchar(8000) NULL, 
	[state] varchar(8000) NULL, 
	[postal_code] varchar(8000) NULL, 
	[latitude] float NULL, 
	[longitude] float NULL, 
	[stars] float NULL, 
	[review_count] int NULL, 
	[is_open] int NULL, 
	[categories] varchar(8000) NULL, 
	[_ingest_ts] datetime2(6) NULL, 
	[_source_file] varchar(8000) NULL, 
	[_batch_id] varchar(8000) NULL
);