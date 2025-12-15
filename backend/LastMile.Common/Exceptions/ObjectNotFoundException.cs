namespace LastMile.Common.Exceptions;

public class ObjectNotFoundException : Exception
{
    public ObjectNotFoundException(string message)
        : base(message) { }

    public ObjectNotFoundException(string message, Exception inner)
        : base(message, inner) { }
}
