namespace LastMile.Common.Models.DbModels;

public class Country
{
    public required Guid Id { get; set; }

    public required string Name { get; set; }

    public required string Code { get; set; }
}
