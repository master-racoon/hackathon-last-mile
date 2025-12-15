import {
  focusManager,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";
import { client } from "./generated-api/client.gen";
import { assertValue } from "./lib/utils";

const baseUrl = assertValue(
  import.meta.env?.VITE_BASE_API_URL,
  "VITE_BASE_API_URL"
);

client.setConfig({
  baseUrl,
  credentials: "include",
});

const queryClient = new QueryClient();

// https://github.com/TanStack/query/discussions/6568
focusManager.setEventListener((handleFocus) => {
  function focusHandler() {
    handleFocus();
  }

  window.addEventListener("visibilitychange", focusHandler, false);
  window.addEventListener("focus", focusHandler);

  return () => {
    window.removeEventListener("visibilitychange", focusHandler);
    window.removeEventListener("focus", focusHandler);
  };
});

createRoot(document.getElementById("root") as HTMLElement).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>
);
