# Full-Stack Starter Template# LastMile

A clean, production-ready full-stack application template with:This repository contains the backend and frontend for LastMile.

- **Backend**: ASP.NET Core 9.0 with PostgreSQL, Entity Framework Core, and ASP.NET IdentityWe are tracking tasks in [Linear](https://linear.app/LastMile/team/SEC/active).

- **Frontend**: React 18 with TypeScript, Vite, TailwindCSS, and Tanstack Query

- **DevOps**: Docker Compose for easy local development## Get started

## FeaturesEach project can be run individually. It's quicker to get the full stack running with [Docker](https://www.docker.com/products/docker-desktop/): `docker compose up`.

### BackendOnce projects are running you can find them at:

- ✅ ASP.NET Core 9.0 Web API

- ✅ PostgreSQL database with Entity Framework Core- Database (PostgreSQL): `localhost:5433`, Username: `postgres`, Password: `Password123!`, Database: `default`

- ✅ ASP.NET Identity for authentication- [Backend API Docs](http://localhost:5000/swagger/index.html)

- ✅ Swagger/OpenAPI documentation- [Frontend](http://localhost:3000)

- ✅ CORS configuration

- ✅ Auto-migration on startupThe development admin credentials are: `admin@LastMile.com` and `Password123!`

- ✅ Hot reload with dotnet watch

### Without Docker

### Frontend

- ✅ React 18 with TypeScriptIf you're not using Docker, you'll need to manually set up your PostgreSQL database:

- ✅ Vite for fast development

- ✅ TailwindCSS for styling1. Install PostgreSQL and ensure it's running on your system.

- ✅ React Router for navigation2. Update appsettings connection strings to point to the local PostgreSQL instance (port, password, etc.).

- ✅ Tanstack Query for data fetching

- ✅ shadcn/ui component library ready### Mobile Testing

- ✅ Hot module replacement

Our docker compose setup configures vite proxy to allow testing on mobile.

### Development ExperienceThis means you can run `ngrok http 3000` to proxy the frontend, and it will pull in it's own backend.

- ✅ Docker Compose for one-command startupThe only change necessary is adding your ngrok url to the .net secrets as:

- ✅ PostgreSQL database with persistent data

- ✅ Environment-based configuration```json

- ✅ Vite proxy for API calls (no CORS issues in dev)"UrlConfig:SiteBaseUrl": "https://b767-31-211-255-185.ngrok-free.app",

- ✅ Swagger UI for API testing"CookieSettings:Domain": "b767-31-211-255-185.ngrok-free.app"

````

## Get Started

### With Docker (Recommended)

1. **Prerequisites**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

2. **Start everything**:
   ```bash
   docker compose up
````

3. **Access the applications**:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API**: [http://localhost:5000/swagger](http://localhost:5000/swagger)
   - **Database**: `localhost:5433` (Username: `postgres`, Password: `Password123!`, Database: `default`)

### Without Docker

#### Backend

1. **Prerequisites**:

   - [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0)
   - PostgreSQL running locally

2. **Update connection string** in `backend/LastMile/appsettings.json`:

   ```json
   {
     "ConnectionStrings": {
       "DefaultConnection": "Server=localhost;Database=yourdb;Port=5432;User Id=postgres;Password=yourpassword;"
     }
   }
   ```

3. **Run the backend**:
   ```bash
   cd backend/LastMile
   dotnet restore
   dotnet run
   ```

#### Frontend

1. **Prerequisites**:

   - [Node.js 20+](https://nodejs.org/)

2. **Install and run**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Project Structure

```
.
├── backend/
│   ├── LastMile/                 # Main API project
│   │   ├── Controllers/          # API controllers
│   │   ├── Program.cs            # Application entry point
│   │   └── appsettings.json      # Configuration
│   └── LastMile.Common/          # Shared library
│       ├── Models/               # Database models
│       ├── Extensions/           # Extension methods
│       └── SwaggerFilters/       # Swagger customization
├── frontend/
│   └── src/
│       ├── App.tsx               # Main app component
│       ├── main.tsx              # Entry point
│       ├── lib/                  # Utilities
│       └── components/           # React components (add your own)
└── docker-compose.yaml           # Docker orchestration
```

## Common Tasks

### Adding a New API Endpoint

1. Create a controller in `backend/LastMile/Controllers/`:

   ```csharp
   [ApiController]
   [Route("api/[controller]")]
   public class MyController : BaseController
   {
       [HttpGet]
       public IActionResult Get()
       {
           return Ok(new { message = "Hello!" });
       }
   }
   ```

2. The API will be available at `http://localhost:5000/api/my`

### Adding a Database Model

1. Create a model in `backend/LastMile.Common/Models/`:

   ```csharp
   public class MyEntity
   {
       public int Id { get; set; }
       public string Name { get; set; } = string.Empty;
   }
   ```

2. Add it to `LastMileDbContext.cs`:

   ```csharp
   public DbSet<MyEntity> MyEntities { get; set; }
   ```

3. Create and apply migration:
   ```bash
   cd backend/LastMile
   dotnet ef migrations add AddMyEntity
   # Migration will auto-apply on next startup
   ```

### Adding a Frontend Page

1. Create a component in `frontend/src/`:

   ```tsx
   function MyPage() {
     return <div>My Page</div>;
   }
   ```

2. Add route in `App.tsx`:
   ```tsx
   <Route path="/my-page" element={<MyPage />} />
   ```

### API Client Generation

The backend automatically generates `api.json` on startup. You can use this with tools like:

- [openapi-typescript](https://www.npmjs.com/package/openapi-typescript)
- [openapi-generator](https://openapi-generator.tech/)

Example is already configured in `frontend/package.json`:

```bash
npm run generate-api
```

## Configuration

### Backend (`appsettings.json`)

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Your PostgreSQL connection string"
  },
  "Cors": {
    "Origins": ["http://localhost:3000"]
  }
}
```

### Frontend (`vite.config.ts`)

The frontend is configured to proxy API calls to `/backend` → `http://backend:5000` in Docker.

## Tech Stack

### Backend

- ASP.NET Core 9.0
- Entity Framework Core 9.0
- PostgreSQL (via Npgsql)
- ASP.NET Identity
- Swashbuckle (Swagger/OpenAPI)

### Frontend

- React 18
- TypeScript 5
- Vite 6
- TailwindCSS 3
- Tanstack Query
- React Router 6
- shadcn/ui (components ready to add)

## License

MIT - Use this template however you like!
