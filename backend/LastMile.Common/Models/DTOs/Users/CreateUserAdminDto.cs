namespace LastMile.Common.Models.DTOs.Users;

public class CreateUserAdminDto : CreateUserDto
{
    public required string CurrentPassword { get; set; }

    public required Enums.Role AdminRole { get; set; }
}
