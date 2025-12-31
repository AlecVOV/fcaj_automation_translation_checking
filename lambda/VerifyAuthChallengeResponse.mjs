/**
 * Verify Auth Challenge Response Lambda
 * Validates the OTP code provided by user
 */

export const handler = async (event) => {
  console.log('VerifyAuthChallengeResponse:', JSON.stringify(event, null, 2));
  
  const expectedAnswer = event.request.privateChallengeParameters.otp;
  const userAnswer = event.request.challengeAnswer;
  
  console.log(`Expected OTP: ${expectedAnswer}`);
  console.log(`User provided: ${userAnswer}`);
  
  // Compare OTP codes
  if (userAnswer && userAnswer.trim() === expectedAnswer) {
    event.response.answerCorrect = true;
    console.log('OTP verification: SUCCESS');
  } else {
    event.response.answerCorrect = false;
    console.log('OTP verification: FAILED');
  }
  
  return event;
};
