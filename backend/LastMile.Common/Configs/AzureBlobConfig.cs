namespace LastMile.Common.Configs;

public class AzureBlobConfig
{
    /// <summary>
    /// The connection string for the storage account.
    /// </summary>
    public required string ConnectionString { get; set; }

    public required string StorageAccountName { get; set; }

    public required string StorageAccountKey { get; set; }

    public required string FileContainerName { get; set; }
}
