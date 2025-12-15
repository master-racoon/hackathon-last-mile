namespace LastMile.Common.Exceptions;

public class AuthException : Exception
{
    /// <summary>
    /// The https://tools.ietf.org/html/rfc7807 type name of the exception
    /// </summary>
    public const string ProblemDetailType = "auth_error";

    public AuthException(string message)
        : base(message) { }

    public AuthException(string message, Exception inner)
        : base(message, inner) { }
}

public class TermsException : Exception
{
    /// <summary>
    /// The https://tools.ietf.org/html/rfc7807 type name of the exception
    /// </summary>
    public const string ProblemDetailType = "terms_error";

    public TermsException(string message)
        : base(message) { }

    public TermsException(string message, Exception inner)
        : base(message, inner) { }
}
