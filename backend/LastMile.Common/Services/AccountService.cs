using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using LastMile.Common.Models;
using LastMile.Common.Models.DbModels;
using LastMile.Common.Configs;
using LastMile.Common.Models.DTOs.User;
using LastMile.Common.Extensions;

namespace LastMile.Common.Services;

public class AccountService(
    UserManager<ApplicationUser> userManager,
    SignInManager<ApplicationUser> signInManager,
    ILogger<AccountService> logger,
    UserService userService,
    IOptions<EnvironmentConfig> envConfig,
    LastMileDbContext dbContext
)
{
    private readonly EnvironmentConfig _envConfig = envConfig.Value;

    private static string GenerateUserName(string personalNumber)
    {
        var random = new Random(personalNumber.GetHashCode());
        string randomNumbers(int count) =>
            string.Join("", Enumerable.Range(0, count).Select(_ => (char)('0' + random.Next(0, 8))));
        return $"{randomNumbers(4)}-{randomNumbers(4)}";
    }


    public async Task<(SignInResult, ApplicationUser?)> LoginWithEmail(string email, string password, bool staySignedIn)
    {
        var user = await userManager.FindByEmailAsync(email);
        if (user == null)
        {
            return (SignInResult.Failed, null);
        }

        var result = await signInManager.PasswordSignInAsync(user, password, staySignedIn, false);

        if (result.Succeeded)
        {
            user.LastLoggedIn = DateTimeOffset.UtcNow;
            await userManager.UpdateAsync(user);
            logger.LogInformation("User logged in, Email: {Email}", email);
        }
        else
        {
            logger.LogInformation("User login attempt failed, Email: {Email}", email);
        }

        // Maybe unnecessary to fetch the user again but it's also easier to prevent bugs if we are consistent with what is returned.
        return (result, await userService.GetUserById(user.Id));
    }

    public async Task Logout()
    {
        await signInManager.SignOutAsync();
        logger.LogInformation("User signed out");
    }

    /// <summary>
    /// Refreshes the request senders cookie with the user specified in the id
    /// Note: This can't be used to refresh "someone else's" cookie. I.e. calling this from the admin panel is pointless
    /// </summary>
    public async Task RefreshCookie(string userId)
    {
        var user = await userManager.Users.FirstOrThrowAsync(u => u.Id == userId);

        await signInManager.RefreshSignInAsync(user);
        logger.LogInformation("User refreshed (without password) in, Email: {UserEmail}", user.Email);
    }

    /// <summary>
    /// Verifies (checks) that the supplied password is the current password for the given user
    /// </summary>
    /// <exception cref="ObjectNotFoundException">If not user with the given id was found</exception>
    public async Task<bool> VerifyPassword(string userId, string password)
    {
        var user = await userManager.Users.FirstOrThrowAsync(u => u.Id == userId);

        var result = await userManager.CheckPasswordAsync(user, password);

        return result;
    }

    public async Task UpdateSelf(string userId, UpdateUserDto dto)
    {
        var user = await userManager.Users.FirstOrThrowAsync(u => u.Id == userId);

        // Intentionally not updating full name, keeping the bank id name
        // Intentionally not updating username, using auto generated username
        user.Email = dto.Email;

        await userManager.UpdateAsync(user);
    }
}
