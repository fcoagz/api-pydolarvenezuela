import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'

import { theme, useOpenapi, useTheme } from 'vitepress-theme-openapi'
import 'vitepress-theme-openapi/dist/style.css'

import spec from '../../public/openapi.json' assert { type: 'json' }

export default {
  ...DefaultTheme,
  async enhanceApp({app, router, siteData}) {
    // Set the OpenAPI specification.
    const openapi = useOpenapi()
    openapi.setSpec(spec)

    // Optionally, configure the theme.
    const themeConfig = useTheme()
    themeConfig.setLocale('es') // en or es

    // Use the theme.
    theme.enhanceApp({app})
  }
} satisfies Theme
