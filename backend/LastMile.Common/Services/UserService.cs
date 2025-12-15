using System.Security.Claims;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using LastMile.Common.Exceptions;
using LastMile.Common.Extensions;
using LastMile.Common.Models;
using LastMile.Common.Models.DbModels;
using LastMile.Common.Models.DTOs.Users;

namespace LastMile.Common.Services;

public class UserService(
    UserManager<ApplicationUser> userManager,
    LastMileDbContext dbContext,
    ILogger<UserService> logger
)
{
    public IQueryable<ApplicationUser> Users => dbContext.Users;

    public static string GetUserIdByClaims(ClaimsPrincipal claimsPrincipal)
    {
        return claimsPrincipal.FindFirstValue(ClaimTypes.NameIdentifier) ?? throw new("No name identifier");
    }

    public async Task<ApplicationUser> GetUserByClaims(ClaimsPrincipal claimsPrincipal)
    {
        return await GetUserById(GetUserIdByClaims(claimsPrincipal));
    }

    public async Task<ApplicationUser> GetUserById(string userId)
    {
        return await dbContext.Users.FirstOrThrowAsync(u => u.Id == userId);
    }

    public async Task<UserDetailedAdminDto> GetUserAsDetailedAdminDto(string userId)
    {
        var user = await dbContext.Users.FirstOrThrowAsync(u => u.Id == userId);

        return new UserDetailedAdminDto(user, await userManager.GetRolesAsync(user));
    }

    public async Task<IdentityResult> AddAdminRoleToUser(string userId, Enums.Role role)
    {
        if (role is not (Enums.Role.SuperAdmin))
            throw new UnsupportedRoleException("Only admin roles can be added or removed manually");

        return await AddRoleToUser(userId, role);
    }

    public async Task<IdentityResult> RemoveAdminRoleFromUser(string userId, Enums.Role role)
    {
        if (role is not (Enums.Role.SuperAdmin))
            throw new UnsupportedRoleException("Only admin roles can be added or removed manually");

        return await RemoveRoleFromUser(userId, role);
    }

    public async Task<IdentityResult> AddRoleToUser(string userId, Enums.Role role)
    {
        var user = await userManager.Users.FirstOrThrowAsync(u => u.Id == userId);

        return await AddRoleToUser(user, role);
    }

    public async Task<IdentityResult> RemoveRoleFromUser(string userId, Enums.Role role)
    {
        var user = await userManager.Users.FirstOrThrowAsync(u => u.Id == userId);

        return await RemoveRoleFromUser(user, role);
    }

    private async Task<IdentityResult> RemoveRoleFromUser(ApplicationUser user, Enums.Role role)
    {
        _ = user ?? throw new ArgumentNullException(nameof(user));

        var result = await userManager.RemoveFromRoleAsync(user, role.ToString());

        if (result.Succeeded)
        {
            logger.LogInformation(
                "User was removed from role: {Role}, Email: {UserEmail}",
                role.ToString(),
                user.Email
            );
        }
        else
        {
            var errors = string.Join(", ", result.Errors.Select(e => e.Code));
            logger.LogInformation(
                "Failed removing user from role: {Role}, Email: {UserEmail}\n" + "Error codes: {Errors}",
                role.ToString(),
                user.Email,
                errors
            );
        }

        return result;
    }

    public async Task<IdentityResult> AddRoleToUser(ApplicationUser user, Enums.Role role)
    {
        _ = user ?? throw new ArgumentNullException(nameof(user));

        var result = await userManager.AddToRoleAsync(user, role.ToString());

        if (result.Succeeded)
        {
            logger.LogInformation("User was added to role: {Role}, Email: {UserEmail}", role.ToString(), user.Email);
        }
        else
        {
            var errors = string.Join(", ", result.Errors.Select(e => e.Code));
            logger.LogInformation(
                "Failed adding user to role: {Role}, Email: {UserEmail}\n" + "Error codes: {Errors}",
                role.ToString(),
                user.Email,
                errors
            );
        }

        return result;
    }

    /// <summary>
    /// RequireUniqueEmail in IdentityOptions cannot be used as that blocks empty emails
    /// Therefore a unique index is placed and this method should be used to give back better error messages
    /// (or simply to check if the email is used without creating a new user)
    /// </summary>
    public async Task<bool> IsEmailFree(string email)
    {
        var normalizedEmail = userManager.NormalizeEmail(email);
        var result = await userManager.Users.AnyAsync(u => u.NormalizedEmail == normalizedEmail);
        return !result;
    }

    /// <summary>
    /// Validates that the email is not already in use.
    /// Throws an EmailAlreadyInUseException if the email is already in use.
    /// </summary>
    /// <exception cref="EmailAlreadyInUseException"></exception>
    public async Task VerifyEmailIsFree(string email)
    {
        if (!await IsEmailFree(email))
        {
            throw new EmailAlreadyInUseException("Email is already in use");
        }
    }

    public async Task<UserDetailedAdminDto> CreateAdminUser(CreateAdminUserAdminDto dto, string creatorEmail)
    {
        if (dto.AdminRole is not (Enums.Role.SuperAdmin))
            throw new UnsupportedRoleException("Only admin roles can be added or removed manually");

        var currentTime = DateTimeOffset.UtcNow;

        var user = new ApplicationUser
        {
            Email = dto.Email,
            CreatedAt = currentTime,
            PersonalNumber = dto.UserName,
            UserName = dto.UserName,
            FullName = dto.FullName,
        };

        await CreateApplicationUser(user, creatorEmail);
        await AddRoleToUser(user, dto.AdminRole);
        return await GetUserAsDetailedAdminDto(user.Id);
    }

    public async Task<UserDetailedAdminDto> CreateAdminUserWithPassword(
        CreateAdminUserWithPasswordAdminDto dto,
        string creatorEmail
    )
    {
        if (dto.AdminRole is not (Enums.Role.SuperAdmin))
            throw new UnsupportedRoleException("Only admin roles can be added or removed manually");

        var currentTime = DateTimeOffset.UtcNow;

        var user = new ApplicationUser
        {
            Email = dto.Email,
            CreatedAt = currentTime,
            PersonalNumber = dto.UserName,
            UserName = dto.UserName,
            FullName = dto.FullName,
        };

        await CreateApplicationUser(user, creatorEmail);
        await AddRoleToUser(user, dto.AdminRole);
        await userManager.AddPasswordAsync(user, dto.NewUserPassword);
        return await GetUserAsDetailedAdminDto(user.Id);
    }

    private async Task CreateApplicationUser(ApplicationUser user, string? creatorEmail)
    {
        if (creatorEmail == null)
        {
            throw new ArgumentException("Creator of new accounts must have an email set");
        }

        var result = await userManager.CreateAsync(user);

        if (result.Succeeded)
        {
            logger.LogInformation(
                "New user created (via admin-panel), Id: {UserId}, Email: {UserEmail}. Created by: {CreatorEmail}",
                user.Id,
                user.Email,
                creatorEmail
            );
            return;
        }
        var errors = string.Join(", ", result.Errors.Select(e => e.Code));
        logger.LogInformation(
            "User admin creation attempt failed, Email: {UserEmail}. Attempt by: {CreatorEmail}\n"
                + "Error codes: {Errors}",
            user.Email,
            creatorEmail,
            errors
        );
        throw new Exception("User creation from admin failed: " + errors); // Internal server error
    }

    public async Task<IdentityResult> DeleteUserById(string userId)
    {
        var user = await userManager.Users.FirstOrThrowAsync(u => u.Id == userId);
        var result = await userManager.DeleteAsync(user);
        if (result.Succeeded)
        {
            logger.LogInformation("User deleted, Id: {UserId}, Email: {UserEmail}", user.Id, user.Email);
        }
        else
        {
            var errors = string.Join(", ", result.Errors.Select(e => e.Code));
            logger.LogWarning(
                "Failed to delete user, Id: {UserId}, Email: {UserEmail}. Errors: {Errors}",
                user.Id,
                user.Email,
                errors
            );
        }
        return result;
    }
}
