using Microsoft.AspNetCore.Authorization;
using LastMile.Common.Models;

namespace LastMile.Common.Helpers;

public class AuthorizeRolesAttribute : AuthorizeAttribute
{
    public AuthorizeRolesAttribute(params Enums.Role[] roles)
    {
        Roles = string.Join(",", roles);
    }
}
