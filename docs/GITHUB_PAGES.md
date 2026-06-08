# GitHub Pages Deployment

## Recommended repository name

```text
axezent-library-of-verified-things
```

## Browser upload path

Upload the full folder contents. Make sure this file exists:

```text
.github/workflows/pages.yml
```

## GitHub Pages setup

1. Go to repository Settings.
2. Go to Pages.
3. Set source to GitHub Actions.
4. Push or upload this package.
5. Open the Pages URL after the workflow succeeds.

## Static site files

The site lives in:

```text
site/
```

The workflow uploads that folder as the Pages artifact.
