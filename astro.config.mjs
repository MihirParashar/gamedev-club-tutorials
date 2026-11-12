// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { pluginLineNumbers } from '@expressive-code/plugin-line-numbers';

// Where the repo lives on GitHub. Change this one line if the repo moves
// (for example, into a club organization). The "Edit this page" links and the
// GitHub icon in the header both come from it.
const repo = 'https://github.com/MihirParashar/gamedev-club-tutorials';

// https://astro.build/config
export default defineConfig({
	// SITE_URL and SITE_BASE are set by the deploy workflow. Locally they are
	// empty and the site is served from http://localhost:4321/.
	site: process.env.SITE_URL || undefined,
	base: process.env.SITE_BASE || undefined,
	integrations: [
		starlight({
			title: 'IMSA Game Dev Club',
			description:
				'Step-by-step game development tutorials written by and for the IMSA Game Dev Club.',
			social: [{ icon: 'github', label: 'GitHub', href: repo }],
			editLink: { baseUrl: `${repo}/edit/main/` },
			credits: false,
			customCss: [
				'@fontsource/atkinson-hyperlegible-next/400.css',
				'@fontsource/atkinson-hyperlegible-next/400-italic.css',
				'@fontsource/atkinson-hyperlegible-next/600.css',
				'@fontsource/atkinson-hyperlegible-next/700.css',
				'@fontsource/atkinson-hyperlegible-mono/400.css',
				'@fontsource/atkinson-hyperlegible-mono/600.css',
				'@fontsource/pixelify-sans/500.css',
				'./src/styles/custom.css',
			],
			components: {
				Hero: './src/components/Hero.astro',
				PageTitle: './src/components/PageTitle.astro',
			},
			// To add a tutorial: create the page in src/content/docs/, then add a
			// line here. The number in the label is what members see in the menu.
			sidebar: [
				{
					label: 'Tutorials',
					items: [
						{ label: '1. Set up Python and pygame', slug: 'setup' },
						{ label: '2. Rain Dodge', slug: 'rain-dodge' },
						{ label: '3. Extend Rain Dodge', slug: 'extend-rain-dodge' },
						{ label: '4. Pop', slug: 'pop' },
						{ label: '5. Brick Buster', slug: 'brick-buster' },
						{ label: '6. Coin Climb', slug: 'coin-climb' },
						{ label: '7. Shoot Back', slug: 'shoot-back' },
						{ label: '8. Start your own game', slug: 'your-own-game' },
					],
				},
				{ label: 'Fix or add a tutorial', slug: 'contributing' },
			],
			expressiveCode: {
				// One dark theme in both light and dark mode, matching the editor
				// most members use.
				themes: ['dark-plus'],
				plugins: [pluginLineNumbers()],
				defaultProps: {
					showLineNumbers: false,
					// Long lines wrap instead of hiding their ends off the right edge.
					// A wrapped row has no line number, so it still reads as one line.
					wrap: true,
					preserveIndent: true,
					// Terminal commands: no fake window bar.
					overridesByLang: {
						'sh,bash,powershell': { frame: 'none', wrap: false },
					},
				},
				styleOverrides: {
					borderRadius: '6px',
					borderColor: 'var(--gdc-code-border)',
					codeBackground: 'var(--gdc-code-bg)',
					codeFontSize: '0.875rem',
					codeLineHeight: '1.7',
					codePaddingInline: '1.75rem',
					frames: {
						editorActiveTabBackground: 'var(--gdc-code-bg)',
						editorActiveTabIndicatorTopColor: '#FFD23F',
						editorActiveTabIndicatorBottomColor: 'transparent',
						editorTabBarBackground: 'var(--gdc-code-tab-bar)',
						editorTabBarBorderBottomColor: 'var(--gdc-code-border)',
						terminalBackground: 'var(--gdc-code-bg)',
						terminalTitlebarBackground: 'var(--gdc-code-tab-bar)',
						terminalTitlebarBorderBottomColor: 'var(--gdc-code-border)',
						frameBoxShadowCssValue: 'none',
					},
					// New lines are green with a +. Changed lines use the site's gold.
					textMarkers: {
						insBackground: '#4CC38A26',
						insBorderColor: '#4CC38A',
						insDiffIndicatorColor: '#4CC38A',
						markBackground: '#FFD23F22',
						markBorderColor: '#FFD23F',
						lineMarkerAccentWidth: '3px',
					},
				},
			},
		}),
	],
});
