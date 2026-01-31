import { SESClient, SendEmailCommand } from '@aws-sdk/client-ses'

const ses = new SESClient({ region: 'ap-southeast-1' })

// Việt will config later on
// const ses = new SESClient({ region: 'us-east-1' });

export const handler = async (event) => {
  console.log('CreateAuthChallenge:', JSON.stringify(event, null, 2))

  if (event.request.challengeName !== 'CUSTOM_CHALLENGE') {
    return event
  }

  // Generate 6-digit OTP
  const otp = Math.floor(100000 + Math.random() * 900000).toString()
  const email = event.request.userAttributes.email

  // Send email via SES directly with beautiful HTML template
  try {
    const params = {
      Source: 'quocviet1452005@gmail.com', // Phải là email đã Verified trong SES
      Destination: { ToAddresses: [email] },
      Message: {
        Subject: { Data: 'Your FCAJ Admin Login Code' },
        Body: {
          Html: {
            Data: `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { 
      font-family: Arial, sans-serif; 
      margin: 0; 
      padding: 0; 
      background-color: #f4f4f4; 
    }
    .container { 
      max-width: 600px; 
      margin: 20px auto; 
      background: white; 
      border-radius: 8px; 
      overflow: hidden; 
      box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
    }
    .header { 
      background: linear-gradient(135deg, #232f3e, #374151); 
      color: white; 
      padding: 30px; 
      text-align: center; 
    }
    .header h1 { 
      margin: 0; 
      font-size: 24px; 
    }
    .content { 
      padding: 30px; 
    }
    .code-box { 
      background: #f3f4f6; 
      padding: 30px; 
      text-align: center; 
      margin: 20px 0; 
      border-radius: 8px; 
      border: 2px dashed #d1d5db; 
    }
    .code { 
      font-size: 36px; 
      font-weight: bold; 
      letter-spacing: 8px; 
      color: #232f3e; 
      font-family: 'Courier New', monospace; 
    }
    .warning { 
      background: #fef3c7; 
      border-left: 4px solid #ff9900; 
      padding: 15px; 
      margin: 20px 0; 
      border-radius: 4px; 
      color: #92400e;
    }
    .footer { 
      background: #f9fafb; 
      padding: 20px; 
      text-align: center; 
      color: #6b7280; 
      font-size: 14px; 
      border-top: 1px solid #e5e7eb; 
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>FCAJ Admin Portal</h1>
      <p>Passwordless Authentication</p>
    </div>
    <div class="content">
      <p>Hello,</p>
      <p>Your login verification code is:</p>
      <div class="code-box">
        <div class="code">${otp}</div>
      </div>
      <div class="warning">
        <strong>This code will expire in 5 minutes.</strong>
      </div>
      <p>If you didn't request this code, please ignore this email.</p>
      <p>For security reasons, never share this code with anyone.</p>
    </div>
    <div class="footer">
      <p><strong>FCAJ Translation Validator</strong></p>
      <p>Secured by AWS Cognito</p>
      <p>&copy; ${new Date().getFullYear()} FCAJ. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
            `,
          },
        },
      },
    }

    await ses.send(new SendEmailCommand(params))
    console.log(`Email sent successfully to ${email}`)
  } catch (error) {
    console.error('Failed to send email via SES:', error)
    // Continue auth flow even if email fails (for debugging)
  }

  // Store OTP in metadata for VerifyAuthChallengeResponse to validate
  event.response.privateChallengeParameters = { otp: otp }
  event.response.challengeMetadata = otp
  event.response.publicChallengeParameters = { email: email }

  return event
}
