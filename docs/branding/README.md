# RTOComply.ai Branding Assets

## Logo Files

### Main Logo
- **File**: [logo.png](file:///home/syspac/work/rtocomply-ai-backend/docs/branding/logo.png)
- **Usage**: Website header, marketing materials, documentation
- **Format**: PNG with transparency
- **Color Scheme**: Deep blue (#1E3A8A) with tech blue accent (#3B82F6)

### Favicon
- **File**: [favicon.png](file:///home/syspac/work/rtocomply-ai-backend/docs/branding/favicon.png)
- **Usage**: Browser tab icon, app icon
- **Format**: PNG (512x512px)
- **Optimized**: Designed to be recognizable at small sizes

## Converting Favicon to .ico Format

To create a `.ico` file from the favicon PNG, use one of these methods:

### Method 1: Using ImageMagick (Recommended)
```bash
# Install ImageMagick if needed
# Ubuntu/Debian: sudo apt-get install imagemagick
# macOS: brew install imagemagick

# Convert to multi-size .ico
convert docs/branding/favicon.png -define icon:auto-resize=256,128,64,48,32,16 docs/branding/favicon.ico
```

### Method 2: Using Online Tool
1. Go to https://convertio.co/png-ico/
2. Upload `docs/branding/favicon.png`
3. Convert and download `favicon.ico`

### Method 3: Using Python (PIL)
```python
from PIL import Image

img = Image.open('docs/branding/favicon.png')
img.save('docs/branding/favicon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
```

## Usage in Frontend

### HTML (Portal)
```html
<!-- In your <head> tag -->
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="shortcut icon" href="/favicon.ico">
```

### Next.js
Place `favicon.ico` in the `public/` directory, and it will be automatically served.

## Brand Guidelines

- **Primary Color**: Deep Blue #1E3A8A
- **Accent Color**: Tech Blue #3B82F6
- **Typography**: Modern sans-serif (e.g., Inter, Roboto, or similar)
- **Minimum Clear Space**: 10% of logo width on all sides
- **Minimum Size**: 32px height for digital, 0.5 inch for print
