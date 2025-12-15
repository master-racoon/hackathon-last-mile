interface ImportMetaEnv {
  readonly VITE_PROXY_ENABLED: boolean;
  readonly VITE_PROXY_TARGET: string;
  readonly VITE_BASE_API_URL: string;
  readonly VITE_ALGOLIA_ID: string;
  readonly VITE_ALGOLIA_SEARCH_KEY: string;
  readonly VITE_ALGOLIA_INDEX: string;
  readonly VITE_MINIMUM_LISTING_VALUE: number;
  readonly VITE_MINIMUM_BID_VALUE: number;
  readonly VITE_GTAG_ID: string;
  readonly VITE_ROBOTS: string;
  readonly VITE_HOW_IT_WORKS_URL?: string; // New environment variable for How It Works page
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
