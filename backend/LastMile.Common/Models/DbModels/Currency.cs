using System.ComponentModel.DataAnnotations;

namespace LastMile.Common.Models.DbModels;

public class Currency
{
    public required string Id { get; set; }
    public required string Code { get; set; }
    public required string CurrencyId { get; set; }

    [Required]
    public required string Name { get; set; }
}
