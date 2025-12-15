using Microsoft.OpenApi.Models;
// using LastMile.Common.Models.DTOs.Chat;
using Swashbuckle.AspNetCore.SwaggerGen;

namespace LastMile.Common.SwaggerFilters;

/// <summary>
/// Adds schemas, that are required client side but not used in APIs.
/// </summary>
public class AddNonApiSchemasDocumentFilter : IDocumentFilter
{
    public void Apply(OpenApiDocument swaggerDoc, DocumentFilterContext context)
    {
        // Add non-API schemas here as needed
        // context.SchemaGenerator.GenerateSchema(typeof(YourDto), context.SchemaRepository);
    }
}
