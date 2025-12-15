namespace LastMile.Common.SwaggerFilters;

using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;

/// <summary>
/// Simplifies paths for React Admin.
/// </summary>
public class ReactAdminOperationPathFilter : IDocumentFilter
{
    public void Apply(OpenApiDocument swaggerDoc, DocumentFilterContext context)
    {
        _ = swaggerDoc ?? throw new ArgumentNullException(nameof(swaggerDoc));
        _ = context ?? throw new ArgumentNullException(nameof(context));

        if (context.DocumentName != "v1-admin")
            return;

        const string prefix = "/api/admin";

        foreach (var path in swaggerDoc.Paths.Keys.ToList())
        {
            if (!path.StartsWith(prefix, StringComparison.InvariantCulture))
                throw new InvalidOperationException($"Non-admin path: {path}");

            var newPath = path.Substring(prefix.Length);
            var entry = swaggerDoc.Paths[path];
            swaggerDoc.Paths.Remove(path);
            swaggerDoc.Paths.Add(newPath, entry);
        }
    }
}
