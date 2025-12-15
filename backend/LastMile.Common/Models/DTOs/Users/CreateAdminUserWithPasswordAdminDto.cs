namespace LastMile.Common.Models.DTOs.Users;

public class CreateAdminUserWithPasswordAdminDto : CreateUserDto
{
    public required string CurrentPassword { get; set; }

    public required Enums.Role AdminRole { get; set; }

    public required string NewUserPassword { get; set; }
}
