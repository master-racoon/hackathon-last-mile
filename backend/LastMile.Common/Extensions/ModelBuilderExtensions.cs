using Microsoft.EntityFrameworkCore;

namespace LastMile.Common.Extensions;

public static class ModelBuilderExtensions
{
    /// <summary>
    /// Configures all DateTime and DateTimeOffset properties to use UTC conversion
    /// </summary>
    public static void HasUtcConversion(this ModelBuilder builder)
    {
        // This extension can be used to configure UTC conversion for DateTime properties
        // Implementation depends on your specific requirements
        // Example: Convert all DateTime properties to UTC
        foreach (var entityType in builder.Model.GetEntityTypes())
        {
            foreach (var property in entityType.GetProperties())
            {
                if (property.ClrType == typeof(DateTime) || property.ClrType == typeof(DateTime?))
                {
                    property.SetValueConverter(
                        new Microsoft.EntityFrameworkCore.Storage.ValueConversion.ValueConverter<DateTime, DateTime>(
                            v => v.ToUniversalTime(),
                            v => DateTime.SpecifyKind(v, DateTimeKind.Utc)
                        )
                    );
                }
            }
        }
    }
}
