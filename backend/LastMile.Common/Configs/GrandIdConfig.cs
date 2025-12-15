namespace LastMile.Common.Configs;

public class GrandIdConfig
{
    /// <summary>
    /// Public key for login with BankID.
    /// </summary>
    public required string AuthApiKey { get; set; }

    /// <summary>
    /// Private key for login with BankID.
    /// </summary>
    public required string AuthAuthenticateServiceKey { get; set; }

    /// <summary>
    /// Public key for signing messages with BankID.
    /// </summary>
    public required string SignApiKey { get; set; }

    /// <summary>
    /// Private key for signing messages with BankID.
    /// </summary>
    public required string SignAuthenticateServiceKey { get; set; }

    /// <summary>
    /// API base url.
    /// Test/Staging/Production environment use the same keys on different domains.
    /// https://docs.grandid.com/
    /// </summary>
    public required string BaseUrl { get; set; }
}
