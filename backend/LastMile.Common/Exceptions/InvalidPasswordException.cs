namespace LastMile.Common.Exceptions;

public class InvalidPasswordException : Exception
{
    /// <summary>
    /// The https://tools.ietf.org/html/rfc7807 type name of the exception
    /// </summary>
    public const string ProblemDetailType = "invalid_password";

    public InvalidPasswordException(string message)
        : base(message) { }

    public InvalidPasswordException(string message, Exception inner)
        : base(message, inner) { }
}
