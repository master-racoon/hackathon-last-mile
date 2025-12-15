namespace LastMile.Common.Models.DTOs;

/// <summary>
/// Requests the client to redirect to the specified URL.
/// Used in place of redirects, where API's are used through fetch.
/// </summary>
public class ClientSideRedirectDto
{
    public required string RedirectUrl { get; set; }
}

/// <summary>
/// Requests the client to redirect to the specified URL.
/// Used in place of redirects, where API's are used through fetch.
/// Also includes a dto related to the current action.s
/// </summary>
public class ClientSideRedirectDto<T> : ClientSideRedirectDto
    where T : class
{
    public required T Data { get; set; }
}
