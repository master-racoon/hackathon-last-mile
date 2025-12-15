import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "../backend/api.json",
  output: "src/generated-api",
  plugins: [
    "@hey-api/client-fetch",
    { name: "@hey-api/client-fetch", throwOnError: true },
    { name: "@hey-api/typescript", enums: "typescript" },
    "@tanstack/react-query",
  ],
});
