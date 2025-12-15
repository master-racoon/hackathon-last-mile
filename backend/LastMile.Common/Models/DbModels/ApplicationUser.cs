using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Identity;

namespace LastMile.Common.Models.DbModels;

public class ApplicationUser : IdentityUser
{
    public ICollection<IdentityRole>? Roles { get; set; }

    public DateTimeOffset LastLoggedIn { get; set; }

    [Required]
    public required DateTimeOffset CreatedAt { get; set; }

    [RegularExpression(@"^[^^!#$%*=<>;{}""]*$", ErrorMessage = "Last name can not contain any of ^!#$%*=<>;{}\"")]
    public required string FullName { get; set; }

    public required string PersonalNumber { get; set; }
}
