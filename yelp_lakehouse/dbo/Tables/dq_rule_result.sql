CREATE TABLE [dbo].[dq_rule_result] (

	[dq_run_id] varchar(8000) NULL, 
	[pipeline_run_id] varchar(8000) NULL, 
	[run_ts] datetime2(6) NULL, 
	[layer] varchar(8000) NULL, 
	[table_name] varchar(8000) NULL, 
	[rule_id] varchar(8000) NULL, 
	[rule_name] varchar(8000) NULL, 
	[rule_type] varchar(8000) NULL, 
	[column_name] varchar(8000) NULL, 
	[severity] varchar(8000) NULL, 
	[dimension] varchar(8000) NULL, 
	[total_count] bigint NULL, 
	[failed_count] bigint NULL, 
	[failed_rate] float NULL, 
	[threshold_rate] float NULL, 
	[status] varchar(8000) NULL, 
	[rule_message] varchar(8000) NULL
);