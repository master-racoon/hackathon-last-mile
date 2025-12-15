using System.Reflection;
using Microsoft.OpenApi.Models;
using LastMile.Common.Helpers;
using Swashbuckle.AspNetCore.SwaggerGen;

namespace LastMile.Common.SwaggerFilters;

public class SetAllRequiredSchemaFilter : ISchemaFilter
{
    public void Apply(OpenApiSchema schema, SchemaFilterContext context)
    {
        if (schema.Properties == null)
        {
            return;
        }

        var optionalProps = context
            .Type.GetProperties()
            .Where(t => t.GetCustomAttribute<SwaggerOptionalAttribute>() != null)
            .ToList();

        foreach (var property in schema.Properties)
        {
            if (
                !schema.Required.Contains(property.Key)
                && !optionalProps.Any(op => string.Equals(op.Name, property.Key, StringComparison.OrdinalIgnoreCase))
            )
            {
                schema.Required.Add(property.Key);
            }
        }
    }
}
