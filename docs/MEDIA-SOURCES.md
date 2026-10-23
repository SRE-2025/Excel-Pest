# Service imagery and Austin flyover

Updated October 23, 2026. Production assets are self-hosted; no Hibu/original-site photography or third-party video URLs are used in rendered service pages or homepage cards.

## Completed images

18 individually generated, visually distinct editorial illustrations: 12 service details and six separate homepage cards. Created with the built-in OpenAI image-generation tool, not an external API/CLI. These are illustrative imagery, not photographs of Excel employees, customers, completed work or actual named properties. Pest images are not identification-reference photographs.

The complete final prompts, original generation filenames, and final asset paths are in [image-prompts.json](../content/media/image-prompts.json). Service outputs are in `site/assets/images/services/`; card outputs are in `site/assets/images/cards/`. Each has 480px and 960px WebP versions. No original generated PNGs are delivered to website visitors. Optimization: FFmpeg/libwebp, quality 78, compression level 6, proportional resizing. Original generated PNGs remain preserved outside the repository.

Every detail page has its own image, aligned beside the copy with a 430px desktop maximum. Homepage card images differ from their destination detail images. Cards remain clickable across their full area. Responsive `srcset`, native lazy loading, asynchronous decoding and intrinsic dimensions reduce unnecessary downloads and layout shifts. No generated team/owner portraits were substituted for missing client photographs.

## Genuine Austin video

- Creator: Alex Blizky; Pexels asset 3398069.
- [Source and location description](https://www.pexels.com/da-dk/video/3398069/): Pennybacker Bridge over the Colorado River in Austin, Texas. The bridge, Lake Austin, limestone and wooded hills were also checked visually against the downloaded footage.
- [Original 1920×1080 download](https://videos.pexels.com/video-files/3398069/3398069-hd_1920_1080_30fps.mp4): 14.058 seconds, 29.97 fps, 9,177,746 bytes.
- Source SHA-256: `e3cd5d37c2af02437b70f47bb6c16355813c1730501555645486f14e1ba1d2ee`.
- [Pexels license](https://www.pexels.com/license/), checked October 23, 2026: website use and editing permitted; attribution optional. No suggestion of photographer endorsement or ownership by Excel is made.
- Desktop output: `site/assets/video/austin-pennybacker-desktop.mp4`, 1920×1080, 24 fps, 4,888,986 bytes.
- Mobile output: `site/assets/video/austin-pennybacker-mobile.mp4`, native-resolution 608×1080 portrait crop, 24 fps, 1,614,606 bytes (67.0% smaller than desktop). This retains the source's full vertical detail instead of enlarging a 720p landscape crop to fill a phone.
- Encoding: H.264, slow preset, CRF 25 desktop / 26 mobile, yuv420p, no audio, fast-start metadata. Mobile filter: `crop=608:1080:(iw-608)/2:0,fps=24`.
- Posters are actual first frames of this footage: `site/assets/images/austin-pennybacker-mobile.webp` (608×1080, 48,746 bytes) and `austin-pennybacker-1600.webp` (1600×900, 96,118 bytes).

The poster loads at high priority before video. Only one video source is selected for the viewport. Reduced-motion, Save-Data and 2G connections receive no automatic video download; an explicit Play button remains available. Playback pauses offscreen/in hidden tabs. Errors retain the still image. Without JavaScript the still, headline and calls to action remain visible. The full-screen intro and delayed headline animation were removed.

## Fonts and mobile rendering

Inter (400–700) and Fraunces (400–600, variable optical size) are locally hosted WOFF2 Latin subsets from Google Fonts. Font files total 115,560 bytes. Licenses and original copyright notices are included beside them in `site/assets/fonts/Inter-OFL.txt` and `Fraunces-OFL.txt`. `font-display: swap` and same-origin font preloads remove the external Google Fonts stylesheet dependency.

Phones do not use the blur-heavy scroll reveals, moving/fading hero text, or continuous ticker animation. Scroll UI updates are batched to animation frames. The hero video supplies the motion without delaying access to the headline or estimate button.

## Verification

- `python tools/verify_media.py`: 18 unique image hashes, 12 detail-page images, six non-reused cards, responsive URL checks, missing-media detection and byte budgets. Also run with `--base /Excel-Pest` after a preview build.
- `node tools/test_media.cjs`: desktop/mobile playback; pause/keyboard; offscreen pause; reduced motion; Save-Data; 2G; video failure; no-JS poster; full-card corner clicks; decode all 12 detail images. Local-only requests, no leads or analytics.
- `node tools/test_layout.cjs`: 19 routes at phone and desktop sizes; no overflow or script errors; right-side image dimensions/alignment.
- Existing metadata, links, scope and conversion-event regression tests remain required.
- `node tools/measure_mobile.cjs`: repeatable throttled Chrome lab observations. These are not field Core Web Vitals or a Lighthouse score. Baseline comparisons include the old external font/media dependencies; real users and networks will vary.

Future replacements must retain per-page uniqueness, source/license records, image byte budgets, and reduced-motion/data-saver behavior. Do not restore the old 640×360 third-party clip or generic landscape footage.

### Mobile lab observations, October 23

Three fresh-cache runs per version at 390×844, DPR 2, 4× CPU slowdown, 1.6 Mbps download and 150ms simulated latency. Same local HTML hosting; the old version retained external fonts/media. Median largest-content paint: **8.356s before → 2.760s after**. Median first-contentful paint: **4.428s → 2.760s**. Median layout shift: **0.00375 → 0.000191**. The new flyover played in all three runs and had no failed requests. The old clip reported aborted range requests and did not advance in one sampled run. This is a directional local lab comparison, not a production speed guarantee or a field score; 2.760s still leaves headroom for future tuning. Full samples: [mobile-lab.json](../content/media/mobile-lab.json).
