using Microsoft.AspNetCore.Mvc;

namespace LastMile.Controllers;

/// <summary>
/// Sample controller demonstrating a basic API endpoint
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class SampleController : UserControllerBase
{
    /// <summary>
    /// Get a hello world message
    /// </summary>
    [HttpGet]
    public IActionResult GetHello()
    {
        return Ok(new { message = "Hello from the API!" });
    }
}
