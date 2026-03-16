CREATE TABLE [dbo].[gold_dq_report] (

	[run_id] varchar(8000) NULL, 
	[layer] varchar(8000) NULL, 
	[dataset] varchar(8000) NULL, 
	[rule_name] varchar(8000) NULL, 
	[rule_type] varchar(8000) NULL, 
	[column_name] varchar(8000) NULL, 
	[metric_value] float NULL, 
	[threshold] float NULL, 
	[status] varchar(8000) NULL, 
	[checked_at] datetime2(6) NULL, 
	[details] varchar(8000) NULL
);