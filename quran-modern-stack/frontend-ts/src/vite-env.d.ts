/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_RUST_API_URL: string;
  readonly VITE_GO_SEARCH_URL: string;
  readonly VITE_APP_TITLE: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
