# Quick Start Guide - EcoHub Website

## 🚀 How to Run the Website

### Option 1: Direct Browser Open (Easiest)
1. Navigate to the project folder: `EcoHub-Website`
2. Right-click on `index.html`
3. Select "Open with" → Choose your browser
4. Website loads instantly!

### Option 2: Local Development Server
```bash
# If you have Python installed
cd EcoHub-Website
python -m http.server 8000

# Then open: http://localhost:8000
```

### Option 3: VS Code Live Server
1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

## 📋 File Guide

| File | Purpose |
|------|---------|
| `index.html` | Main website structure - edit content here |
| `css/styles.css` | All styling, colors, responsive design |
| `js/script.js` | Interactivity, animations, mobile menu |
| `README.md` | Full documentation |
| `assets/` | Folder for logos, images |

## ✏️ How to Edit Content

### Change Text Content
1. Open `index.html` with a text editor
2. Find the section you want to edit
3. Modify the text between tags
4. Save the file
5. Refresh your browser

### Examples:
```html
<!-- Hero Section -->
<h1 class="hero-title">Turning Waste Into Opportunity</h1>

<!-- About Section -->
<h2 class="section-title">Who We Are</h2>

<!-- Founder Message -->
<p class="founder-quote">Your quote here...</p>
```

## 🎨 Customize Colors

Edit in `css/styles.css` (around line 10):
```css
:root {
    --primary-green: #1e4226;      /* Main color */
    --accent-green: #66cc33;       /* Highlight color */
    --light-green: #8bb336;        /* Alternative green */
    /* Change these hex codes to your colors */
}
```

## 📱 Responsive Breakpoints

The site automatically adapts to:
- **Desktop**: Full layout (1200px+)
- **Tablet**: Optimized grid (768px - 1199px)
- **Mobile**: Hamburger menu (below 768px)

## 🔗 Update Links

In `index.html`, update social and contact links:
```html
<a href="https://facebook.com/ecohubgroup" class="social-icon">f</a>
<p class="contact-info">Email: your-email@ecohubgroup.com</p>
<p class="contact-info">Phone: +1 (555) XXX-XXXX</p>
```

## 🎦 Key Sections in index.html

1. **Navigation** - Lines 1-30
2. **Hero** - Lines 30-50
3. **About** - Lines 50-70
4. **Focus Areas** - Lines 70-110
5. **Featured Project** - Lines 110-150
6. **Join Movement** - Lines 150-165
7. **Founder Message** - Lines 165-180
8. **Footer** - Lines 180-210

## 🐛 Troubleshooting

### Website looks broken
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Try a different browser

### Mobile menu not working
- Check internet connection
- Ensure `js/script.js` loads (check browser console)

### Colors not changing
- Save CSS file (Ctrl+S)
- Hard refresh browser (Ctrl+Shift+R)
- Check for typos in color codes

## 📤 Deploy to Web

### Free Hosting Options:
1. **Netlify** - Drag & drop folder
2. **GitHub Pages** - Push to GitHub
3. **Vercel** - Connect GitHub repo
4. **Firebase** - Google's hosting service

## 🎯 Next Steps

1. ✅ Review all content
2. ✅ Update contact information
3. ✅ Add logos to assets folder
4. ✅ Test on mobile devices
5. ✅ Deploy to chosen hosting
6. ✅ Share with team

## 🔐 File Backups

Before making major changes:
```bash
# Copy current version
cp index.html index.html.backup
cp css/styles.css css/styles.css.backup
cp js/script.js js/script.js.backup
```

## ✨ Need Help?

Check the detailed `README.md` file for:
- Complete feature list
- All customization options
- Accessibility features
- Performance information
- Deployment guides

---

**You're all set! Start editing and make it your own!** 🌍💚
