# EcoHub Group - Modern Sustainability Website

A modern, fully responsive website for EcoHub Group - a sustainability initiative dedicated to transforming environmental challenges into innovative solutions through youth empowerment and community impact.

## 🌱 Features

✅ **Fully Responsive Design** - Mobile-first approach, optimized for all devices
✅ **Modern UI/UX** - Clean design with eco-friendly color scheme
✅ **Smooth Animations** - Scroll effects and hover transitions
✅ **Interactive Navigation** - Mobile-friendly hamburger menu with smooth scroll
✅ **Professional Sections**:
   - Navigation Bar with sticky positioning
   - Hero Section with CTA buttons
   - About/Mission Section
   - Focus Areas (4 responsive cards)
   - Featured Project Showcase
   - Call-to-Action Section
   - Founder Message
   - Footer with Social Links

## 📁 Project Structure

```
EcoHub-Website/
├── index.html           # Main HTML file
├── css/
│   └── styles.css      # All styling and responsive design
├── js/
│   └── script.js       # Interactivity and animations
├── assets/
│   └── (logos and images)
└── README.md           # This file
```

## 🎨 Color Scheme

- **Primary Green**: #1e4226 (Dark forest green)
- **Accent Green**: #66cc33 (Bright eco-green)
- **Light Green**: #8bb336 (Muted sage green)
- **White**: #ffffff
- **Light Gray**: #f9f9f9
- **Text Color**: #333333 & #666666

## 🚀 Getting Started

1. **Clone or download** the project files
2. **Open `index.html`** in your web browser
3. No build process required - it's ready to use!

### Local Development

For development with live reload, you can use:

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js (http-server)
npx http-server

# Or simply open index.html in your browser
```

## 📱 Responsive Breakpoints

- **Desktop**: 1200px and above (full layout)
- **Tablet**: 768px - 1199px (optimized grid)
- **Mobile**: Below 768px (stacked layout with hamburger menu)
- **Small Mobile**: Below 480px (optimized font sizes and spacing)

## ✨ Key Sections

### Navigation Bar
- Sticky positioning for easy access
- Smooth scroll navigation
- Mobile hamburger menu
- Brand logo and text

### Hero Section
- Large headline with gradient text
- Subheading
- Three CTA buttons (Join, Explore, Partner)
- Eco-gradient background

### About Section
- Mission description
- Inspirational quote with styling
- Light gray background for contrast

### Focus Areas
- 4 responsive cards (1-4 columns based on screen size)
- Hover animations
- Icon-based visual design

### Featured Project
- Two-column layout (responsive)
- Project description with benefits list
- Placeholder image area

### Join the Movement
- Dark green background with white text
- Two prominent CTA buttons
- Motivational messaging

### Founder Message
- Quote-style layout
- Founder name and title
- Central positioning

### Footer
- Multi-column layout
- Social media links
- Contact information
- Copyright notice

## 🎯 Interactive Features

### Mobile Menu
- Hamburger icon for mobile
- Smooth open/close animation
- Auto-closes on link click

### Scroll Effects
- Section animations on scroll
- Smooth scroll behavior for anchor links
- Active nav link highlighting

### Button Interactions
- Ripple effect on click
- Hover animations with lift effect
- Toast notifications for CTA buttons

### Accessibility
- Keyboard navigation support
- Focus visible styling
- Semantic HTML
- Proper heading hierarchy

## 🔧 Customization

### Change Colors
Edit the CSS variables in `css/styles.css`:
```css
:root {
    --primary-green: #1e4226;
    --accent-green: #66cc33;
    /* ... other colors ... */
}
```

### Update Content
Edit the text content directly in `index.html`. Key sections:
- Hero title and subtitle
- About section text
- Focus area cards
- Project information
- Founder message

### Add New Sections
1. Create HTML structure in `index.html`
2. Add CSS styling to `css/styles.css`
3. Add animation/interactivity to `js/script.js` if needed

## 📞 Contact Information

Update footer contact details in `index.html`:
```html
<p class="contact-info">Email: info@ecohubgroup.com</p>
<p class="contact-info">Phone: +1 (555) 123-4567</p>
```

## 🔗 Social Media Links

Customize social links in the footer:
```html
<a href="https://facebook.com/ecohub" class="social-icon">f</a>
<a href="https://twitter.com/ecohub" class="social-icon">𝕏</a>
<!-- Add more as needed -->
```

## 🌐 Deployment

### Deploy to Netlify
1. Push to GitHub
2. Connect repository to Netlify
3. Set build command: (leave empty)
4. Set publish directory: `.`

### Deploy to Vercel
1. Push to GitHub
2. Import project in Vercel
3. Deploy (no build needed)

### Deploy to GitHub Pages
1. Push to GitHub
2. Enable GitHub Pages in settings
3. Select main branch as source

## ⚡ Performance

- Lightweight HTML/CSS/JS (no frameworks)
- Optimized images and assets
- Smooth animations using CSS transitions
- Fast load time
- Mobile-friendly performance

## ♿ Accessibility

- Semantic HTML structure
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance
- Focus indicators for keyboard users

## 📄 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Future Enhancements

Potential additions:
- Contact form with validation and backend
- Blog/News section
- Project gallery with filters
- Team member profiles
- Donation/sponsorship system
- Newsletter subscription
- Search functionality
- Dark mode toggle

## 📝 License

This website template is created for EcoHub Group. All content and design are proprietary.

## 🤝 Contributing

To contribute or suggest improvements:
1. Create a feature branch
2. Make your changes
3. Submit feedback

---

**Let's build a sustainable future together! 🌍💚**

Created for EcoHub Group - Innovating for Climate, Sustainability & Environment
