using Microsoft.AspNetCore.Identity;
using LastMile.Common.Models;
using LastMile.Common.Models.DbModels;

namespace LastMile.Common.DbSeeding.CustomSeeding;

public class BaseSeed(LastMileDbContext dbContext, UserManager<ApplicationUser> userManager)
{
    // Password is meant to be changed on the live environment manually.
    // Therefore the lack of a serious password here or fetching of password from appsettings
    private const string AdminUserEmail = "admin@LastMile.com"; //if changed, must be updated in developmentSeed as well
    private const string TestUserEmail = "test@LastMile.com";
    private const string TestUserTwoEmail = "test2@LastMile.com";
    private const string TestPassword = "Password123!";
    private const string UserFamilyName = "LastMile";

    public virtual void Seed(bool isDevelopment)
    {
        if (dbContext.Roles.Any())
        {
            return;
        }

        AddRoles();

        if (isDevelopment)
        {
            AddUsers();
        }

        dbContext.SaveChanges();
    }

    private void AddRoles()
    {
        var superAdminRole = new IdentityRole
        {
            Name = Enums.Role.SuperAdmin.ToString(),
            NormalizedName = userManager.NormalizeName(Enums.Role.SuperAdmin.ToString()),
        };

        dbContext.Roles.AddRange(superAdminRole);
    }

    private void AddUsers()
    {
        var adminUser = new ApplicationUser
        {
            Email = AdminUserEmail,
            EmailConfirmed = true,
            UserName = "Admin",
            PersonalNumber = "199001010000",
            FullName = UserFamilyName,
            CreatedAt = DateTimeOffset.UtcNow,
        };

        var testUser = new ApplicationUser
        {
            Email = TestUserEmail,
            EmailConfirmed = true,
            UserName = "TestUser",
            PersonalNumber = "199001010001",
            FullName = UserFamilyName,
            CreatedAt = DateTimeOffset.UtcNow,
        };

        var testUserTwo = new ApplicationUser
        {
            Email = TestUserTwoEmail,
            EmailConfirmed = true,
            UserName = "TestUserTwo",
            PersonalNumber = "199001010002",
            FullName = UserFamilyName,
            CreatedAt = DateTimeOffset.UtcNow,
        };

        userManager.CreateAsync(adminUser, TestPassword).Wait();
        userManager.CreateAsync(testUser, TestPassword).Wait();
        userManager.CreateAsync(testUserTwo, TestPassword).Wait();
        userManager.AddToRoleAsync(adminUser, Enums.Role.SuperAdmin.ToString()).Wait();
    }

    private static void AddCompanies()
    {
        // Companies functionality removed - add back if needed
        /*
        if (dbContext.Companies.Any(c => c.Id == "5591932354"))
            return;

        var company = new Models.DbModels.CompanyInfo.Company
        {
            Id = "5591932354",
            Name = "uBIT AB",
            CareOf = "U Börjesson",
            City = "STOCKHOLM",
            CompanyDescription =
                "Bolaget ska bedriva konsultverksamhet inom IT och teknik samt annan därmed förenlig verksamhet. Bolaget ska också investera i privata onoterade bolag samt annan därmed förenlig verksamhet.",
            CompanyForm = "private",
            CompanyName = "uBIT AB",
            CompanyStatus = [],
            Country = "",
            CreatedAt = DateTimeOffset.Parse("2024-11-04 16:07:05.379144+00", CultureInfo.InvariantCulture),
            Currency = "sek",
            CurrentNbrShares = 569134,
            CurrentValuation = 119859628.78317867M,
            FoundedDate = DateTimeOffset.Parse("2019-01-21 00:00:00+00", CultureInfo.InvariantCulture),
            LatestEvent = DateTimeOffset.Parse("2024-10-25 00:00:00+00", CultureInfo.InvariantCulture),
            OrgNbr = "5591932354",
            OwnershipOrderStatus = "",
            PostalCode = "113 28",
            RaisedCapital = 5359547.0M,
            Region = "Västra Götalands län",
            Status = "ok",
            StreetAddress = "Heimdalsgatan 8",
            UpdatedAt = DateTimeOffset.Parse("2024-11-06 00:00:17.663468+00", CultureInfo.InvariantCulture),
            Directors = [],
        };

        dbContext.Companies.Add(company);
        dbContext.SaveChanges();
        */
    }
}
