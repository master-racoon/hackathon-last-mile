namespace LastMile.Common.Models.DbModels;

public interface IDbModelBase
{
    public DateTimeOffset CreatedAt { get; set; }
    public DateTimeOffset UpdatedAt { get; set; }
}

public abstract class DbModelBase : IDbModelBase
{
    /// <summary>
    /// Time the entity was created
    /// </summary>
    public DateTimeOffset CreatedAt { get; set; }

    /// <summary>
    /// Last time the entity was updated
    /// </summary>
    public DateTimeOffset UpdatedAt { get; set; }
}
