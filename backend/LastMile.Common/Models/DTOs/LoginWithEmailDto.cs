using System.ComponentModel.DataAnnotations;
using LastMile.Common.Helpers;

namespace LastMile.Common.Models.DTOs;

public class LoginWithEmailDto
{
    [EmailAddress, MaxLength(256)]
    public required string Email { get; set; }

    [MinLength(6), MaxLength(256), DataType(DataType.Password)]
    public required string Password { get; set; }

    [SwaggerOptional]
    public bool StaySignedIn { get; set; } = false; // I.e. IsPersistent
}
