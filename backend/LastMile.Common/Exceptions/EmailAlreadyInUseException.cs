namespace LastMile.Common.Exceptions;

public class EmailAlreadyInUseException : Exception
{
    /// <summary>
    /// The https://tools.ietf.org/html/rfc7807 type name of the exception
    /// </summary>
    public const string ProblemDetailType = "email_already_used";

    public EmailAlreadyInUseException(string message)
        : base(message) { }

    public EmailAlreadyInUseException(string message, Exception inner)
        : base(message, inner) { }
}
