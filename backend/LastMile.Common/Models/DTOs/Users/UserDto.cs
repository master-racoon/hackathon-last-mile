using LastMile.Common.Models.DbModels;

namespace LastMile.Common.Models.DTOs.User;

public class UserDto
{
    /// <summary>
    /// Required includes:
    /// KycApplication
    /// </summary>
    public static UserDto ToUserDto(ApplicationUser user) =>
        new()
        {
            Id = user.Id,
            Email = user.Email,
            UserName = user.UserName,
            FullName = user.FullName,
        };

    public required string Id { get; set; }

    public string? Email { get; set; }

    public string? UserName { get; set; }

    public string? FullName { get; set; }
}
