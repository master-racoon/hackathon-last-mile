using Microsoft.AspNetCore.Mvc;
using LastMile.Common.Helpers;
using LastMile.Common.Models;

namespace LastMile.Controllers;

[ApiExplorerSettings(GroupName = "v1")]
[ApiController]
[Route("api/[controller]")]
public class UserControllerBase : ControllerBase { }

[AuthorizeRoles(Enums.Role.SuperAdmin)]
[ApiExplorerSettings(GroupName = "v1-admin")]
[ApiController]
[Area("admin")]
[Route("api/[area]/[controller]")]
public class AdminControllerBase : ControllerBase { }
