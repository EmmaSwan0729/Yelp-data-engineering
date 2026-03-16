CREATE TABLE [dbo].[city_metrics_gold] (

	[state] varchar(8000) NULL, 
	[city] varchar(8000) NULL, 
	[business_count] bigint NULL, 
	[reviews_total] bigint NULL, 
	[weighted_avg_rating] float NULL, 
	[simple_avg_rating] float NULL, 
	[median_avg_rating] float NULL, 
	[high_tier_business_count] bigint NULL, 
	[medium_tier_business_count] bigint NULL, 
	[low_tier_business_count] bigint NULL, 
	[active_business_count_365d] bigint NULL, 
	[reviews_per_business] float NULL, 
	[high_tier_business_share] float NULL, 
	[_gold_build_ts] datetime2(6) NULL
);