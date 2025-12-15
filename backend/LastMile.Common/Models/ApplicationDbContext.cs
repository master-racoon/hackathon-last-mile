using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using LastMile.Common.DbSeeding.CustomSeeding;
using LastMile.Common.Extensions;
using LastMile.Common.Models.DbModels;

namespace LastMile.Common.Models;

public class LastMileDbContext : IdentityDbContext<ApplicationUser>
{
    // Add your DbSets here
    // Example: public DbSet<YourEntity> YourEntities { get; set; }

    public LastMileDbContext(DbContextOptions<LastMileDbContext> options)
        : base(options) { }

    /// <summary>
    /// Used to seed database with custom seeding logic.
    /// Running this every start up is not a good idea
    /// Can be used for e.g. unit tests and manual testing
    ///
    /// This method should be run from e.g. Startup.Configure
    /// </summary>
    public static void SeedCustomData(IServiceProvider serviceProvider, bool isDevelopment)
    {
        using var serviceScope = serviceProvider.CreateScope();
        var context = serviceScope.ServiceProvider.GetRequiredService<LastMileDbContext>();
        var userManager = serviceScope.ServiceProvider.GetRequiredService<UserManager<ApplicationUser>>();
        new BaseSeed(context, userManager).Seed(isDevelopment);
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        // We want to be able to use MARS and are not using SavePoints anyway
    }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        builder.HasUtcConversion();

        ConfigureCustomPrimaryKeys(builder);
        ConfigureCustomRelations(builder);
        ConfigureCustomConstraints(builder);
        ConfigureCustomSerialization(builder);
        ConfigureCustomIndices(builder);
        ConfigureCustomDiscriminators(builder);
        ConfigureCustomDeletionBehaviour(builder);
        ConfigureGlobalFilters(builder);
        SeedMigrationData(builder);
    }

    private static void ConfigureCustomPrimaryKeys(ModelBuilder builder)
    {
        // Add custom primary key configurations here
    }

    private static void ConfigureCustomRelations(ModelBuilder builder)
    {
        // Configure ApplicationUser roles relationship
        builder
            .Entity<ApplicationUser>()
            .HasMany(u => u.Roles)
            .WithMany(nameof(Users))
            .UsingEntity<IdentityUserRole<string>>(
                userRole => userRole.HasOne<IdentityRole>().WithMany().HasForeignKey(ur => ur.RoleId).IsRequired(),
                userRole => userRole.HasOne<ApplicationUser>().WithMany().HasForeignKey(ur => ur.UserId).IsRequired()
            );

        // Add your custom entity relationships here
    }

    private static void ConfigureCustomConstraints(ModelBuilder builder)
    {
        // Add custom constraints here
    }

    private static void ConfigureCustomDiscriminators(ModelBuilder builder)
    {
        // Add custom discriminators for inheritance here
    }

    private static void ConfigureCustomSerialization(ModelBuilder builder)
    {
        // Add custom serialization configurations here
    }

    private static void ConfigureCustomIndices(ModelBuilder builder)
    {
        // Add custom indices here
    }

    private static void ConfigureCustomDeletionBehaviour(ModelBuilder builder)
    {
        // Add custom deletion behavior here
    }

    private static void ConfigureGlobalFilters(ModelBuilder builder)
    {
        // Add global query filters here
    }

    private static void SeedMigrationData(ModelBuilder builder)
    {
        // Add migration data seeding here
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        SetCreatedAndUpdatedAt();
        return await base.SaveChangesAsync(true, cancellationToken);
    }

    public override int SaveChanges()
    {
        SetCreatedAndUpdatedAt();
        return base.SaveChanges();
    }

    private void SetCreatedAndUpdatedAt()
    {
        var currentTime = DateTimeOffset.UtcNow;
        foreach (var entry in ChangeTracker.Entries())
        {
            if (entry.State != EntityState.Modified && entry.State != EntityState.Added)
                continue;
            if (entry.Entity is not IDbModelBase dbModelEntry)
                continue;
            dbModelEntry.UpdatedAt = currentTime;
            // We need to compare against minvalue to see if the datetime has been manually assigned
            // (as that is desirable to do in some scenarios)
            if (entry.State == EntityState.Added && dbModelEntry.CreatedAt == DateTimeOffset.MinValue)
            {
                dbModelEntry.CreatedAt = currentTime;
            }
        }
    }
}
