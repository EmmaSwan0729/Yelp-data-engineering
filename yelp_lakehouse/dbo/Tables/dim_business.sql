CREATE TABLE [dbo].[dim_business] (

	[business_id] varchar(8000) NULL, 
	[name] varchar(8000) NULL, 
	[city] varchar(8000) NULL, 
	[state] varchar(8000) NULL, 
	[stars] float NULL, 
	[review_count] int NULL, 
	[categories] varchar(8000) NULL, 
	[_ingest_ts] datetime2(6) NULL, 
	[is_current] bit NULL, 
	[effective_from] datetime2(6) NULL, 
	[effective_to] datetime2(6) NULL
);