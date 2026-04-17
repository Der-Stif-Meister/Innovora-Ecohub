# Team Management System - Testing & Verification Guide

## ✅ Complete Feature Verification Checklist

Ready to test the new team management system? Follow this comprehensive guide.

---

## 🚀 Pre-Testing Setup

### 1. Verify Database is Updated
```bash
# Run from project root
python -c "from app import db, TeamMember; print('TeamMember columns:', [c.name for c in TeamMember.__table__.columns])"
```

Expected columns: id, name, role, department, bio, image_filename, email, show_email, linkedin_url, twitter_url, facebook_url, tiktok_url, other_url, created_at, updated_at

### 2. Create Admin User (if not exists)
```bash
python -c "
from app import app, db, Admin
from werkzeug.security import generate_password_hash

app.app_context().push()
existing = Admin.query.filter_by(username='admin').first()
if not existing:
    admin = Admin(username='admin', email='admin@ecohub.com')
    admin.password = generate_password_hash('admin123')
    db.session.add(admin)
    db.session.commit()
    print('Admin user created: admin / admin123')
else:
    print('Admin user already exists')
"
```

### 3. Start Flask Development Server
```bash
# Make sure you're in the project root
python -m flask run --debug
# Server runs on http://localhost:5000
```

---

## 🧪 Feature Testing Workflow

### Phase 1: Admin Authentication

#### Test 1.1: Admin Login
- Navigate to `http://localhost:5000/admin/login`
- Enter credentials: `admin` / `admin123`
- ✅ Should redirect to `/admin/dashboard`

#### Test 1.2: Protected Routes
- Try to access `/admin/team` without login
- ✅ Should redirect to login page

---

### Phase 2: Team Management Admin Panel

#### Test 2.1: Access Team Management
- Go to `/admin/dashboard`
- Click **Team** (👥) in sidebar
- ✅ Should display empty team grid or existing members
- ✅ Should show "Add Team Member" button

#### Test 2.2: View Team Grid
- ✅ Grid layout displays correctly
- ✅ Cards have proper dimensions
- ✅ Image placeholders show for members without images
- ✅ Pagination shows if > 12 members

---

### Phase 3: Add Team Member - Complete Flow

#### Test 3.1: Open Add Form
- Click **"Add Team Member"** button
- ✅ Form page loads at `/admin/team/add`
- ✅ All fields display correctly
- ✅ Image preview area is ready

#### Test 3.2: Form Validation
- Click **Add** without filling required fields
- ✅ Should show error: "Name and role are required"
- Fill only "Name", leave "Role" empty
- ✅ Should show error message

#### Test 3.3: Add Member Without Image
1. Fill in:
   - Name: "Alex Johnson"
   - Role: "Sustainability Manager"
   - Department: "Environmental Impact"
   - Bio: "Expert in carbon footprint reduction with 8 years of experience in sustainable practices."
   - Email: "alex@ecohub.com"
   - ✅ Check "Show email" checkbox
   - LinkedIn: "https://linkedin.com/in/alexjohnson"
   - Twitter: "https://twitter.com/alexgreen"
2. Click **"Add Team Member"**
3. ✅ Should show success message
4. ✅ Redirect to `/admin/team`
5. ✅ New member appears in grid

#### Test 3.4: Add Member With Image
1. Fill in:
   - Name: "Sarah Chen"
   - Role: "Lead Engineer"
   - Department: "Technology"
   - Bio: "Passionate about renewable energy solutions. Coding since 2015."
   - Email: "sarah@ecohub.com"
   - ✅ Uncheck "Show email" checkbox
   - Facebook: "https://facebook.com/sarahchen"
   - TikTok: "https://tiktok.com/@sarahchen"
2. Upload an image file (PNG/JPG/WebP, < 5MB)
3. ✅ Image preview appears when selected
4. Click **"Add Team Member"**
5. ✅ Image saves to `static/uploads/` with timestamp
6. ✅ Member displays in admin list with image thumbnail

#### Test 3.5: Image Validation
- Try uploading a file > 5MB
  - ✅ Should be rejected by Flask config
- Try uploading a non-image file (PDF, EXE)
  - ✅ Should be rejected by file type check
- Try uploading GIF
  - ✅ Should be rejected (only JPG, PNG, WebP allowed)

---

### Phase 4: Edit Team Member

#### Test 4.1: Access Edit Form
- Go to `/admin/team`
- Click **Edit** button on a member card
- ✅ Form page loads at `/admin/team/<id>/edit`
- ✅ All fields pre-populated with current data

#### Test 4.2: Update Without Image
- Change Bio: "Updated bio text with more details..."
- Change Department: "New Department"
- Update Twitter URL to different value
- Click **"Update Team Member"**
- ✅ Shows success message
- ✅ Changes appear on public page

#### Test 4.3: Update With New Image
1. Current image displays at top
2. Upload new image
3. ✅ Image preview shows new image
4. Click **"Update Team Member"**
5. ✅ Old image deleted from filesystem
6. ✅ New image displays in admin grid and public page

#### Test 4.4: Clear Image (Keep Existing)
- View member with existing image
- Don't upload new image
- Update other fields
- Click **"Update Team Member"**
- ✅ Existing image remains unchanged

---

### Phase 5: Delete Team Member

#### Test 5.1: Delete Flow
- Go to `/admin/team`
- Click **Delete** button on a member card
- ✅ Confirmation dialog appears
- Click **OK** to confirm
- ✅ Member removed from grid
- ✅ Shows success message
- ✅ Image file deleted from filesystem

#### Test 5.2: Verify Deletion
- Go to `/team` public page
- ✅ Deleted member no longer appears

---

### Phase 6: Public Team Page Display

#### Test 6.1: Page Load
- Navigate to `http://localhost:5000/team`
- ✅ Page loads within 2 seconds
- ✅ Smooth animations play
- ✅ All team members display

#### Test 6.2: Card Display
For each team member card, verify:
- ✅ Profile image displays correctly (or placeholder if none)
- ✅ Member name shows
- ✅ Role displays in accent-green
- ✅ Department shows below role
- ✅ Bio truncates to 3 lines with ellipsis
- ✅ Card number badge appears (top-right)

#### Test 6.3: Email Display
- **For members with `show_email=true`:**
  - ✅ Email displays with envelope icon
  - ✅ Email is clickable (mailto link)
  - Test clicking email → Opens email client/default handler
- **For members with `show_email=false`:**
  - ✅ Email does NOT display
  - ✅ No email link present

#### Test 6.4: Social Media Icons
For each configured social link:
- ✅ LinkedIn icon shows if `linkedin_url` is set
- ✅ Twitter icon shows if `twitter_url` is set
- ✅ Facebook icon shows if `facebook_url` is set
- ✅ TikTok icon shows if `tiktok_url` is set
- ✅ Website icon shows if `other_url` is set
- ✅ Clicking icon opens link in new tab
- ✅ Icons with no URL don't display

#### Test 6.5: Hover Effects
- Hover over team card
- ✅ Card lifts up (-14px)
- ✅ Shadow enhances
- ✅ Smooth transition (no janky animation)

- Hover over profile image
- ✅ Image scales smoothly (1.08x)

- Hover over social icon
- ✅ Icon lifts (-5px) and scales (1.1x)
- ✅ Icon changes color to platform color (LinkedIn: #0077b5, etc.)
- ✅ Shadow appears under icon

---

### Phase 7: Responsive Design Testing

#### Test 7.1: Desktop (1920x1080)
- ✅ Grid shows ~3-4 columns
- ✅ Cards maintain aspect ratio
- ✅ Spacing (gap: 2.5rem) looks balanced
- ✅ Text readability excellent

#### Test 7.2: Tablet (768x1024)
- ✅ Grid shows 1 column
- ✅ Gap reduced to 1.8rem
- ✅ Cards take full width
- ✅ Touch-friendly icon sizes (34px)
- ✅ All content visible without horizontal scroll

#### Test 7.3: Mobile (375x667)
- ✅ Single column layout
- ✅ Card badges properly sized (35px)
- ✅ Text sizes readable
- ✅ Social icons properly spaced
- ✅ Email link clickable on touch
- ✅ No horizontal overflow
- ✅ Images load and display correctly

---

### Phase 8: Animations Testing

#### Test 8.1: Page Load Animation
- Refresh `/team` page
- ✅ Team grid fades in smoothly (0.8s)
- ✅ Cards have staggered appearance (0.1s delay between cards)

#### Test 8.2: Hover Animations
- Hover over card
- ✅ Smooth lift effect (no lag)
- ✅ Shadow transition smooth
- ✅ Image scale smooth

---

### Phase 9: Data Persistence

#### Test 9.1: Refresh Page
- Add member with full details
- Refresh `/team` page
- ✅ Member data persists
- ✅ Images still display

#### Test 9.2: Edit and Save
- Edit member email
- Refresh page
- ✅ Email change persists
- ✅ Other fields unchanged

#### Test 9.3: Multiple Sessions
- Open `/team` in two browser tabs
- Add member in Tab 1
- Switch to Tab 2 and refresh
- ✅ New member appears in Tab 2
- ✅ Data is consistent

---

### Phase 10: Navigation & Links

#### Test 10.1: Navbar Links
- From `/team` page, check navbar
- ✅ All links functional
- ✅ Team link highlighted (if routing handles it)
- ✅ Language switcher works

#### Test 10.2: Footer Links
- Scroll to footer
- ✅ All social links functional
- ✅ Quick navigation links work

#### Test 10.3: Admin Sidebar
- From `/admin/team`, check sidebar
- ✅ Team link highlighted with .active class
- ✅ Other admin links functional
- ✅ Logout works

---

### Phase 11: Internationalization (i18n)

#### Test 11.1: Language Switching
- Navigate to `/team`
- Click language switcher
- ✅ Team page title translates to selected language
- ✅ Team page subtitle updates
- ✅ Navigation updates
- ✅ Settings persist across page refresh

#### Test 11.2: Multiple Languages
- Supported languages: EN, ES, FR, DE, ZH, PT, AR, JA
- ✅ Team title translates correctly in all languages
- ✅ No missing translation strings
- ✅ All content readable in each language

---

### Phase 12: Error Handling

#### Test 12.1: Non-existent Team Member
- Try to access `/admin/team/9999/edit`
- ✅ Should return 404 Not Found

#### Test 12.2: Invalid File Upload
- Upload 10MB video file
- ✅ Should reject with max-size error
- Upload .txt file
- ✅ Should reject with file-type error

#### Test 12.3: Database Error Simulation
- Intentionally break connection (stop DB)
- Try to delete member
- ✅ Should show user-friendly error message
- ✅ Should not expose technical details

---

## 📊 Performance Testing

### Test Load Times
- Home page: < 1s
- Team list (admin): < 1s
- Public team page: < 1s
- Add member form: < 0.5s
- Edit member form: < 0.5s

### Test Image Load Times
- Thumbnail (admin): < 0.3s
- Full image (public): < 0.8s
- Multiple (5+) images: < 2s total

---

## 🔍 Browser Compatibility Testing

Test on:
- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile Safari (iOS)
- ✅ Chrome Mobile (Android)

Expected results: All features work consistently across browsers

---

## 📝 Test Results Template

```
Team Management System - Test Results
Date: ____________________
Tester: ____________________
Browser: ____________________
Device: ____________________

ADMIN FEATURES:
[ ] Add member - PASS/FAIL
[ ] Edit member - PASS/FAIL
[ ] Delete member - PASS/FAIL
[ ] Image upload - PASS/FAIL
[ ] Form validation - PASS/FAIL

PUBLIC FEATURES:
[ ] Team page loads - PASS/FAIL
[ ] Cards display correctly - PASS/FAIL
[ ] Email display (conditional) - PASS/FAIL
[ ] Social icons (conditional) - PASS/FAIL
[ ] Hover effects work - PASS/FAIL
[ ] Animations smooth - PASS/FAIL

RESPONSIVE:
[ ] Desktop layout - PASS/FAIL
[ ] Tablet layout - PASS/FAIL
[ ] Mobile layout - PASS/FAIL

PERFORMANCE:
[ ] Page load < 2s - PASS/FAIL
[ ] Animations smooth - PASS/FAIL
[ ] Images optimize - PASS/FAIL

OVERALL: ✅ PASS / ❌ FAIL

Notes:
_________________________________________________
_________________________________________________
```

---

## ✅ Final Verification Checklist

- [ ] Database has all new columns
- [ ] Admin can add team members
- [ ] Admin can edit team members (including images)
- [ ] Admin can delete team members
- [ ] Public team page displays all members
- [ ] Email display toggle works
- [ ] Social icons display conditionally
- [ ] Images upload and delete correctly
- [ ] Animations play smoothly
- [ ] Responsive design works on all devices
- [ ] Navigation working throughout
- [ ] i18n translations working
- [ ] Error handling graceful
- [ ] Performance acceptable
- [ ] All browsers compatible
- [ ] Code committed to GitHub

---

## 🎉 You're Ready to Deploy!

Once all tests pass, your team management system is production-ready!

**Deploy to:**
- Railway: Follow RAILWAY_DEPLOYMENT.md
- Render: Follow RENDER_DEPLOYMENT.md
- Other: Use standard Flask deployment practices

---

**Last Updated:** April 17, 2026
**System Version:** 2.0 (Advanced)
**Status:** Ready for Testing ✅
