namespace LastMile.Common.Models.DTOs.Users;

public class CreateAdminUserAdminDto : CreateUserDto
{
    public required string CurrentPassword { get; set; }

    public required Enums.Role AdminRole { get; set; }
}
