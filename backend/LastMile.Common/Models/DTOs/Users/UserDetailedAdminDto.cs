using LastMile.Common.Models.DbModels;

namespace LastMile.Common.Models.DTOs.Users;

public class UserDetailedAdminDto
{
    public UserDetailedAdminDto(ApplicationUser user, ICollection<string> roles)
    {
        Id = user.Id;
        PersonalNumber = user.PersonalNumber;
        UserName = user.UserName;
        Roles = roles;
        Email = user.Email;
        EmailConfirmed = user.EmailConfirmed;
        FullName = user.FullName;
        PhoneNumber = user.PhoneNumber;
        CreatedAt = user.CreatedAt;
        LastLoggedIn = user.LastLoggedIn;
    }

    public string Id { get; set; }

    public string PersonalNumber { get; set; }

    public string? UserName { get; set; }

    public ICollection<string> Roles { get; set; }

    public string? Email { get; set; }

    public bool EmailConfirmed { get; set; }

    public string? FullName { get; set; }

    public string? PhoneNumber { get; set; }

    public DateTimeOffset CreatedAt { get; set; }

    public DateTimeOffset LastLoggedIn { get; set; }
}
