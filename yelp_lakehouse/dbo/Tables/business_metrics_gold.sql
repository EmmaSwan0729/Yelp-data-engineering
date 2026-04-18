CREATE TABLE [dbo].[business_metrics_gold] (

	[business_id] varchar(8000) NULL, 
	[name] varchar(8000) NULL, 
	[city] varchar(8000) NULL, 
	[state] varchar(8000) NULL, 
	[categories] varchar(8000) NULL, 
	[review_count_total] bigint NULL, 
	[avg_rating] float NULL, 
	[first_review_date_id] int NULL, 
	[last_review_date_id] int NULL, 
	[business_popularity_tier] varchar(8000) NULL, 
	[rating_bucket] varchar(8000) NULL
);