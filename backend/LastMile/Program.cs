using System.Globalization;
using System.Reflection;
using System.Text.Json.Serialization;
using Hangfire;
using Hangfire.PostgreSql;
// using LastMile.Common.Clients; // Commented out - Clients folder removed
using LastMile.Common.Configs;
using LastMile.Common.Models;
using LastMile.Common.Models.DbModels;
using LastMile.Common.Services;
using LastMile.Common.SwaggerFilters;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using Microsoft.OpenApi.Models;
using Microsoft.OpenApi.Writers;
using Newtonsoft.Json;
using Swashbuckle.AspNetCore.Swagger;
using PasswordOptions = LastMile.Common.Configs.PasswordOptions;

const string hangfireDashboardAuthenticationPolicy = "HangfireAuthPolicy";

// MARK: Buildtime
var builder = WebApplication.CreateBuilder(args);

// Create sample contract pdfs in development
if (builder.Environment.IsDevelopment()) { }

builder.Logging.AddAzureWebAppDiagnostics();

builder.Services.AddRouting(options => options.LowercaseUrls = true);

builder
    .Services.AddControllers()
    .AddJsonOptions(options => options.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter()));

// Already added through "AddControllers" but we need custom policy here
builder.Services.AddAuthorization(options =>
{
    // Policy to be applied to hangfire endpoint
    options.AddPolicy(
        hangfireDashboardAuthenticationPolicy,
        policyBuilder =>
        {
            policyBuilder.RequireAuthenticatedUser();
            policyBuilder.RequireRole(Enums.Role.SuperAdmin.ToString());
        }
    );
});

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo { Version = "v1", Title = "LastMile API" });
    options.SwaggerDoc("v1-admin", new OpenApiInfo { Version = "v1 Admin", Title = "LastMile Admin API" });
    options.DocumentFilter<ReactAdminOperationPathFilter>();

    options.SupportNonNullableReferenceTypes();
    options.EnableAnnotations(enableAnnotationsForInheritance: true, enableAnnotationsForPolymorphism: true);
    options.SchemaFilter<SetAllRequiredSchemaFilter>();
    options.DocumentFilter<AddNonApiSchemasDocumentFilter>();
    options.OperationFilter<AuthorizationOperationFilter>();

    var textInfo = CultureInfo.InvariantCulture.TextInfo;
    options.CustomOperationIds(api =>
    {
        var action = api.ActionDescriptor.RouteValues["action"];
        var controller = api.ActionDescriptor.RouteValues["controller"];
        return $"{controller}{action}";
    });

    var xmlFilename = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    options.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, xmlFilename));
});

builder.Services.AddDbContext<LastMileDbContext>(options =>
{
    options.UseNpgsql(
        builder.Configuration.GetConnectionString("LastMileDbConnection"),
        b => b.MigrationsAssembly("LastMile")
    );
});

builder.Services.AddSignalR();

builder.Services.AddHangfire(configuration =>
    configuration
        .SetDataCompatibilityLevel(CompatibilityLevel.Version_170)
        .UseSimpleAssemblyNameTypeSerializer()
        .UseSerializerSettings(
            new JsonSerializerSettings
            {
                TypeNameHandling = TypeNameHandling.Auto,
                DefaultValueHandling = DefaultValueHandling.IgnoreAndPopulate,
                NullValueHandling = NullValueHandling.Ignore,
                CheckAdditionalContent = true,
                ReferenceLoopHandling = ReferenceLoopHandling.Ignore,
            }
        )
        .UsePostgreSqlStorage(
            c => c.UseNpgsqlConnection(builder.Configuration.GetConnectionString("HangfireConnection")),
            new PostgreSqlStorageOptions { QueuePollInterval = TimeSpan.FromMinutes(1) }
        )
);

builder.Services.AddHangfireServer();

// if (builder.Environment.IsProduction())
// {
//     builder.Services.AddRaygun(builder.Configuration);
// }

builder
    .Services.AddIdentity<ApplicationUser, IdentityRole>()
    .AddEntityFrameworkStores<LastMileDbContext>()
    .AddDefaultTokenProviders();

builder.Services.Configure<IdentityOptions>(options =>
{
    // Password settings
    options.Password.RequireDigit = PasswordOptions.RequireDigit;
    options.Password.RequireLowercase = PasswordOptions.RequireLowercase;
    options.Password.RequireUppercase = PasswordOptions.RequireUppercase;
    options.Password.RequireNonAlphanumeric = PasswordOptions.RequireNonAlphanumeric;
    options.Password.RequiredLength = PasswordOptions.RequiredLength;
    options.Password.RequiredUniqueChars = PasswordOptions.RequiredUniqueChars;

    // Lockout settings.
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.Lockout.AllowedForNewUsers = true;

    // Sign in settings
    options.SignIn.RequireConfirmedEmail = false;

    // General settings
    options.User.RequireUniqueEmail = false;
});

builder.Services.ConfigureApplicationCookie(options =>
{
    options.ExpireTimeSpan = TimeSpan.FromMinutes(
        builder.Configuration.GetSection("CookieSettings").GetValue<int>("SignatureExpirationTimeInMinutes")
    );
    options.SlidingExpiration = true;
    options.Cookie.SameSite =
        builder.Configuration.GetSection("CookieSettings").GetValue<string>("SameSite") == "strict"
            ? SameSiteMode.Strict
            : SameSiteMode.None;
    options.Cookie.SecurePolicy = builder.Configuration.GetSection("CookieSettings").GetValue<bool>("Secure")
        ? CookieSecurePolicy.Always
        : CookieSecurePolicy.None;
    options.Cookie.HttpOnly = true;

    // Allow subdomains to access cookie
    options.Cookie.Domain = builder.Configuration.GetSection("CookieSettings").GetValue<string>("Domain");
    options.Cookie.Name = builder.Configuration.GetSection("CookieSettings").GetValue<string>("Name");

    options.LoginPath = null;
    options.LogoutPath = null;
    options.AccessDeniedPath = null;
    options.Events.OnRedirectToLogin = context =>
    {
        if (context.Response.StatusCode != 200)
            return Task.FromResult<object?>(null);
        context.Response.StatusCode = 401;
        return Task.FromResult<object?>(null);
    };
    options.Events.OnRedirectToAccessDenied = context =>
    {
        context.Response.StatusCode = 403;
        return Task.FromResult<object?>(null);
    };
});

// MARK: Configs
builder.Services.Configure<UrlConfig>(builder.Configuration.GetSection(nameof(UrlConfig)));
builder.Services.Configure<AzureBlobConfig>(builder.Configuration.GetSection(nameof(AzureBlobConfig)));

// MARK: Services
builder.Services.AddScoped<UserService>();
builder.Services.AddScoped<AccountService>();

// MARK: Runtime
var app = builder.Build();

// Migrate and seed database
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<LastMileDbContext>();
    await dbContext.Database.MigrateAsync();
    var config = scope.ServiceProvider.GetRequiredService<IOptions<EnvironmentConfig>>().Value;
    LastMileDbContext.SeedCustomData(app.Services, builder.Environment.IsDevelopment());
}

// Update OpenAPI document for client generation
using (var scope = app.Services.CreateScope())
{
    using var streamWriter = File.CreateText("../api.json");
    var writer = new OpenApiJsonWriter(streamWriter);
    scope.ServiceProvider.GetRequiredService<ISwaggerProvider>().GetSwagger("v1").SerializeAsV3(writer);
}

var corsOrigins = builder.Configuration.GetSection("Cors").GetSection("Origins").Get<string[]>();
Console.WriteLine("CORS origins: " + string.Join(", ", corsOrigins ?? []));
if (corsOrigins == null || corsOrigins.Length == 0)
    throw new("No origins defined in configuration");

app.UseExceptionHandler("/error");
app.UseCors(options => options.WithOrigins(corsOrigins).AllowAnyMethod().AllowAnyHeader().AllowCredentials());

// Needed for admin panel
app.UseSwagger();
app.UseSwaggerUI();

if (app.Environment.IsProduction())
{
    app.UseHttpsRedirection();
}

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.MapHangfireDashboardWithAuthorizationPolicy(hangfireDashboardAuthenticationPolicy);

//Add background workers for services
// RecurringJob.AddOrUpdate<CompanyService>("run-predictions", x => x.UpdatePredictions(), Cron.Daily(0));

await app.RunAsync();
