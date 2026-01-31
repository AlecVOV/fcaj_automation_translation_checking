/**
 * Define Auth Challenge Lambda
 * Determines what challenge to present to the user
 */

export const handler = async (event) => {
  console.log('DefineAuthChallenge:', JSON.stringify(event, null, 2));
  
  if (event.request.session.length === 0) {
    // First attempt - send OTP
    event.response.issueTokens = false;
    event.response.failAuthentication = false;
    event.response.challengeName = 'CUSTOM_CHALLENGE';
  } else if (
    event.request.session.length === 1 &&
    event.request.session[0].challengeName === 'CUSTOM_CHALLENGE' &&
    event.request.session[0].challengeResult === true
  ) {
    // OTP correct - issue tokens
    event.response.issueTokens = true;
    event.response.failAuthentication = false;
  } else {
    // OTP wrong or too many attempts
    event.response.issueTokens = false;
    event.response.failAuthentication = true;
  }
  
  console.log('DefineAuthChallenge response:', JSON.stringify(event.response, null, 2));
  return event;
};
