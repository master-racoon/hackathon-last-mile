using System.ComponentModel.DataAnnotations;

namespace LastMile.Common.Models.DTOs;

public class CreateUserDto
{
    [EmailAddress(ErrorMessage = "invalid-email"), MaxLength(256, ErrorMessage = "max-length#256")]
    public required string Email { get; set; }

    public required string UserName { get; set; }

    public required string FullName { get; set; }
}
