import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
	docs: defineCollection({
		loader: docsLoader(),
		schema: docsSchema({
			// Extra fields a tutorial page can set at the top of its file.
			extend: z.object({
				// Position in the "Start here" list on the homepage.
				number: z.number().optional(),
				// Roughly how long the tutorial takes, e.g. "About 60 minutes".
				time: z.string().optional(),
				// File name (without .md) of the tutorial to do before this one.
				first: z.string().optional(),
				// What the reader should already know.
				needs: z.string().optional(),
				// Caption under the homepage screenshot.
				heroCaption: z.string().optional(),
			}),
		}),
	}),
};
