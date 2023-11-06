// Library for using OpenAI's ChatGPT inside Google Apps Script

function GPT(prompt) {

  var Model_ID = "text-davinci-002";
  var maxTokens = 64;C
  var temperature = 0.5;
  // Build the API payload
var payload = {
  'model': Model_ID, // or your desired model
  'prompt': prompt,
  'temperature': temperature,
  'max_tokens': maxTokens,
};
var options = {
  "method": "post",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + API_KEY
  },
  "payload": JSON.stringify(payload)
};
// Make the API request
var response = UrlFetchApp.fetch("https://api.openai.com/v1/completions", options);
 // Parse the response and return the generated text
 var responseData = JSON.parse(response.getContentText());
 return responseData.choices[0].text.trim();
}
