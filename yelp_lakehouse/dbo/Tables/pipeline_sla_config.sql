CREATE TABLE [dbo].[pipeline_sla_config] (

	[pipeline_name] varchar(8000) NULL, 
	[layer] varchar(8000) NULL, 
	[max_duration_sec] int NULL, 
	[min_success_rate] float NULL, 
	[max_blocked_rate] float NULL, 
	[is_active] bit NULL, 
	[update_at] datetime2(6) NULL
);