namespace LastMile.Common.SwaggerFilters;

using System.Reflection;
using Microsoft.AspNetCore.Authorization;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;

/// <summary>
/// Add cookie authentication to the Swagger UI.
/// </summary>
public class AuthorizationOperationFilter : IOperationFilter
{
    public void Apply(OpenApiOperation operation, OperationFilterContext context)
    {
        _ = context ?? throw new ArgumentNullException(nameof(context));
        _ = operation ?? throw new ArgumentNullException(nameof(operation));

        var authorizeMethod = context.MethodInfo.GetCustomAttributes<AuthorizeAttribute>().Any();
        var authorizeController =
            context.MethodInfo.DeclaringType?.GetCustomAttributes<AuthorizeAttribute>().Any() ?? false;
        if (!authorizeMethod && !authorizeController)
            return;

        var roles = context.MethodInfo.GetCustomAttributes<AuthorizeAttribute>().FirstOrDefault()?.Roles;
        if (!string.IsNullOrWhiteSpace(roles))
            operation.Summary += $" (Roles: {roles})";

        var reference = new OpenApiReference { Type = ReferenceType.SecurityScheme, Id = "Cookie" };
        var referenceScheme = new OpenApiSecurityScheme { Reference = reference };
        var requirement = new OpenApiSecurityRequirement { { referenceScheme, Array.Empty<string>() } };
        operation.Security = new List<OpenApiSecurityRequirement> { requirement };
    }
}
