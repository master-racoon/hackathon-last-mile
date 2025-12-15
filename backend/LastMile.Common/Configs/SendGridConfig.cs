namespace LastMile.Common.Configs;

public class SendGridConfig
{
    public required string ApiKey { get; set; }
    public required string SendFrom { get; set; }
    public required string SenderName { get; set; }
    public required string InvoiceBccEmail { get; set; }
    public required string SuccessfulRegistrationId { get; set; }
    public required string NewBidReceivedId { get; set; }
    public required string AcceptedBidId { get; set; }
    public required string PurchaseAgreementFinalizedSellerId { get; set; }
    public required string PurchaseAgreementFinalizedBuyerId { get; set; }
}
