CREATE TABLE [dbo].[business_bronze] (

	[address] varchar(8000) NULL, 
	[business_id] varchar(8000) NULL, 
	[categories] varchar(8000) NULL, 
	[city] varchar(8000) NULL, 
	[is_open] bigint NULL, 
	[latitude] float NULL, 
	[longitude] float NULL, 
	[name] varchar(8000) NULL, 
	[postal_code] varchar(8000) NULL, 
	[review_count] bigint NULL, 
	[stars] float NULL, 
	[state] varchar(8000) NULL, 
	[_source_file] varchar(8000) NULL, 
	[_ingest_ts] datetime2(6) NULL, 
	[_batch_id] varchar(8000) NULL
);