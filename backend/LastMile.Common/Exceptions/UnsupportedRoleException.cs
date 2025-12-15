namespace LastMile.Common.Exceptions;

public class UnsupportedRoleException : Exception
{
    /// <summary>
    /// The https://tools.ietf.org/html/rfc7807 type name of the exception
    /// </summary>
    public const string ProblemDetailType = "unsupported_role";

    public UnsupportedRoleException(string message)
        : base(message) { }

    public UnsupportedRoleException(string message, Exception inner)
        : base(message, inner) { }
}
