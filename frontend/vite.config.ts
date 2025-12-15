import { defineConfig, loadEnv, PluginOption } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import svgr from "vite-plugin-svgr";
import path from "path";

function I18nHotReload(): PluginOption {
  return {
    name: "i18n-hot-reload",
    handleHotUpdate({ file, server }) {
      if (file.includes("locales") && file.endsWith(".json")) {
        console.log("Locale file updated");
        server.ws.send({
          type: "custom",
          event: "locales-update",
        });
      }
    },
  };
}

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const enableProxy = env.VITE_PROXY_ENABLED === "true";

  const proxy = {
    "/backend": {
      target: env.VITE_PROXY_TARGET,
      changeOrigin: true,
      secure: false,
      rewrite: (path) => path.replace(/^\/backend/, ""),
      ws: true,
    },
  };

  return {
    resolve: {
      alias: [{ find: "@", replacement: path.resolve(__dirname, "src") }],
    },
    plugins: [react(), tsconfigPaths(), svgr(), I18nHotReload()],
    server: {
      host: true,
      port: 3000,
      proxy: enableProxy ? proxy : undefined,
      allowedHosts: enableProxy ? true : undefined,
    },
  };
});
