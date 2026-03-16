CREATE TABLE [dbo].[pipeline_sla_config] (

	[pipeline_name] varchar(8000) NULL, 
	[layer] varchar(8000) NULL, 
	[sla_sec] int NULL, 
	[is_active] bit NULL, 
	[created_at] datetime2(6) NULL
);