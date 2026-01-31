# AWS Cognito Passwordless OTP - Installation Guide

## 📋 Prerequisites

- AWS Account
- Node.js 20+ installed
- VS Code or any code editor

---

## 🚀 Step-by-Step Installation

### Phase 1: Install Dependencies

```bash
cd "d:\Study_SWB\Năm 3\Project A\Project\fcaj_automation_translation_checking"

npm install aws-amplify
```

Expected output:

```
added 1 package
```

---

### Phase 2: Verify Configuration Files

Check that these files exist:

```
✅ .env (with Cognito IDs)
✅ src/config/aws-config.ts
✅ src/stores/authStore.ts (updated with passwordless)
✅ src/views/AdminLoginPage.vue (updated with OTP UI)
✅ src/main.ts (Amplify initialized)
✅ lambda/DefineAuthChallenge.mjs
✅ lambda/CreateAuthChallenge.mjs
✅ lambda/VerifyAuthChallengeResponse.mjs
✅ lambda/CustomMessage.mjs
```

---

### Phase 3: Deploy Lambda Functions

#### Option A: AWS Console (Recommended)

Follow instructions in `lambda/README.md`

#### Option B: Test Locally First (Optional)

Create `test-lambda.js`:

```javascript
import { handler as defineAuth } from './lambda/DefineAuthChallenge.mjs'

const testEvent = {
  request: { session: [] },
  response: {},
}

const result = await defineAuth(testEvent)
console.log('Result:', result)
```

Run:

```bash
node test-lambda.js
```

---

### Phase 4: Start Development Server

```bash
npm run dev
```

Expected output:

```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

### Phase 5: Test Authentication Flow

#### Test 1: Request OTP

1. Open http://localhost:5173/admin
2. Enter email: `binhcanguyen04@gmail.com`
3. Click "Send Verification Code"
4. Check email inbox (or spam)

**Expected:**

- Email received with 6-digit code
- UI shows "Check your email" screen
- Countdown timer starts (5:00)

#### Test 2: Verify OTP

1. Copy 6-digit code from email
2. Paste into verification code input
3. Click "Verify & Login"

**Expected:**

- Redirect to `/admin/dashboard`
- User authenticated

#### Test 3: Test Error Cases

```
❌ Wrong email → "Email not found"
❌ Wrong OTP → "Incorrect code"
❌ Expired OTP → Button disabled
❌ Resend OTP → New code works
```

---

## 🐛 Troubleshooting

### Error: "Cannot find module 'aws-amplify'"

**Fix:**

```bash
npm install aws-amplify
```

### Error: "User Pool ID is undefined"

**Fix:**
Check `.env` file has correct values:

```
VITE_COGNITO_USER_POOL_ID=ap-southeast-1_siF7voqGf
VITE_COGNITO_CLIENT_ID=36lhnthvq59ho8jk1nm82k1h53
```

Restart dev server:

```bash
npm run dev
```

### Error: "Failed to send OTP"

**Possible causes:**

1. Lambda functions not deployed
2. Lambda triggers not attached
3. User not created in Cognito

**Fix:**

1. Check AWS Console → Cognito → Lambda triggers
2. Check CloudWatch logs for errors
3. Verify user exists in User Pool

### Error: "OTP verification failed"

**Check:**

1. OTP not expired (5 minutes)
2. Exact 6 digits (no spaces)
3. Check CloudWatch logs for actual OTP generated

**Debug:**

```
AWS Console → CloudWatch → Log groups
→ /aws/lambda/FCAJ-CreateAuthChallenge
→ Find log: "OTP generated for [email]: 123456"
```

---

## 📊 Verification Checklist

```
Backend (AWS):
☐ User Pool created with correct settings
☐ App Client has ALLOW_CUSTOM_AUTH enabled
☐ 4 Lambda functions deployed
☐ Lambda triggers attached to User Pool
☐ 5 admin users created
☐ Test email delivery working

Frontend:
☐ npm install aws-amplify successful
☐ .env file configured
☐ No TypeScript errors
☐ Dev server starts without errors
☐ /admin page loads
☐ Email input works
☐ OTP verification UI appears
☐ Full authentication flow works
```

---

## 🎯 Next Steps After Installation

### 1. Update Admin Users

```
AWS Console → Cognito → Users → Create user
```

Add your team's emails.

### 2. Customize Email Template

Edit `lambda/CustomMessage.mjs` to change email design.

### 3. Production Deployment

Update `.env.production`:

```
VITE_COGNITO_USER_POOL_ID=your-production-pool-id
VITE_COGNITO_CLIENT_ID=your-production-client-id
```

### 4. Optional: Enable MFA

```
AWS Console → Cognito → User pool → MFA
→ Optional MFA → TOTP
```

### 5. Monitor Usage

```
AWS Console → CloudWatch → Dashboards
→ Create dashboard for:
  - Login attempts
  - OTP requests
  - Failed verifications
```

---

## 📞 Support

If you encounter issues:

1. Check CloudWatch logs
2. Verify all Lambda functions deployed
3. Test Lambda functions individually
4. Check Cognito User Pool settings
5. Verify .env file

---

## 🎉 Success!

If everything works:

- You can login with email OTP
- No password needed
- Session persists for 30 days
- Secure authentication flow

**Enjoy your passwordless authentication system!** 🚀
