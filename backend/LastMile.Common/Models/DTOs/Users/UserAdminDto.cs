using EntityFrameworkCore.Projectables;
using LastMile.Common.Models.DbModels;

namespace LastMile.Common.Models.DTOs.Users;

public class UserAdminDto
{
    [Projectable]
    public static UserAdminDto ToAdminUserDto(ApplicationUser user) =>
        new()
        {
            Id = user.Id,
            PersonalNumber = user.PersonalNumber,
            UserName = user.UserName,
            Email = user.Email,
            FullName = user.FullName,
            PhoneNumber = user.PhoneNumber,
            EmailConfirmed = user.EmailConfirmed,
            CreatedAt = user.CreatedAt,
            LastLoggedIn = user.LastLoggedIn,
        };

    public required string Id { get; set; }

    public required string PersonalNumber { get; set; }

    public required string? UserName { get; set; }

    public required string? Email { get; set; }

    public required string? FullName { get; set; }

    public required string? PhoneNumber { get; set; }

    public required bool EmailConfirmed { get; set; }

    public required DateTimeOffset CreatedAt { get; set; }

    public required DateTimeOffset LastLoggedIn { get; set; }
}
