namespace LastMile.Common.Configs;

public class UrlConfig
{
    public const string UserIdIdentifier = "{userId}";
    public const string TokenIdentifier = "{token}";
    public const string EmailIdentifier = "{email}";
    public const string LinkIdentifier = "{link}";

    public required string SiteBaseUrl { get; set; }
    public required string LoginCallbackPath { get; set; }
    public required string PlaceBidCallbackPath { get; set; }
    public required string AcceptBidCallbackPath { get; set; }
}
