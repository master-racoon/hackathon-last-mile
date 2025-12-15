using Microsoft.AspNetCore.Mvc;

namespace LastMile.Common.Exceptions;

/// <summary>
/// Coded api exception. Localized client side.
/// </summary>
public class ApiException(ApiErrorCode ErrorCode) : Exception(ErrorCode.ToString())
{
    public ApiErrorCode ErrorCode { get; } = ErrorCode;
}

public class ApiExceptionDetails : ProblemDetails
{
    public ApiErrorCode? ErrorCode { get; set; }
}

public enum ApiErrorCode
{
    BidCannotBeCancelled,
    BidCannotBeUpdated,
    BidPriceCannotBeDecreased,
}
