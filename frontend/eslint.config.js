// eslint.config.js
import { defineConfig, globalIgnores } from "eslint/config"
import globals from "globals"
import js from "@eslint/js"
import pluginVue from "eslint-plugin-vue"
import tseslint from "typescript-eslint"
import skipFormatting from "@vue/eslint-config-prettier/skip-formatting"

export default defineConfig([
  {
    name: "app/files-to-lint",
    files: ["**/*.{js,mjs,jsx,ts,tsx,vue}"],   // added ts,tsx
  },

  globalIgnores(["**/dist/**", "**/dist-ssr/**", "**/coverage/**"]),

  {
    languageOptions: {
      globals: {
        ...globals.browser,
      },
      parser: tseslint.parser,
      parserOptions: {
        project: "./tsconfig.json",
        extraFileExtensions: [".vue"],          //  allow .vue with TS
      },
    },
  },

  js.configs.recommended,
  ...pluginVue.configs["flat/essential"],
  ...tseslint.configs.recommended,              //  enable TS rules
  skipFormatting,
])
