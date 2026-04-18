CREATE TABLE [dbo].[dim_user] (

	[user_id] varchar(8000) NULL, 
	[name] varchar(8000) NULL, 
	[review_count] int NULL, 
	[average_stars] float NULL, 
	[fans] int NULL, 
	[_ingest_ts] datetime2(6) NULL, 
	[is_current] bit NULL, 
	[effective_from] datetime2(6) NULL, 
	[effective_to] datetime2(6) NULL
);