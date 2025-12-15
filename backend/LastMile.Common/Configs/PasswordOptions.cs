namespace LastMile.Common.Configs;

public static class PasswordOptions
{
    /// <summary>
    /// The minimum length a password must be.
    /// Defaults to 6 in the IdentityFramework.
    /// </summary>
    public const int RequiredLength = 6;

    /// <summary>
    /// The minimum number of unique chars a password must comprised of.
    /// Defaults to 1 in the IdentityFramework
    /// </summary>
    public const int RequiredUniqueChars = 1;

    /// <summary>
    /// Flag indicating if passwords must contain a non-alphanumeric character.
    /// Defaults to true in the IdentityFramework.
    /// </summary>
    public const bool RequireNonAlphanumeric = false;

    /// <summary>
    /// Flag indicating if passwords must contain a lower case ASCII character.
    /// Defaults to true in the IdentityFramework.
    /// </summary>
    public const bool RequireLowercase = true;

    /// <summary>
    /// Flag indicating if passwords must contain a upper case ASCII character.
    /// Defaults to true in the IdentityFramework.
    /// </summary>
    public const bool RequireUppercase = true;

    /// <summary>
    /// Flag indicating if passwords must contain a digit.
    /// Defaults to true in the IdentityFramework.
    /// </summary>
    public const bool RequireDigit = true;
}
