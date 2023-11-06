//Replace with your API key
var API_key = ""

function GPT(prompt) {
  var Model_ID = "gpt-4";
  var temperature = 0;
  // Build the API payload
  var payload = {
    'model': Model_ID, // Use "gpt-3.5-turbo" for chat model
    'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                 {'role': 'user', 'content': prompt}], // Use messages for chat model
    'temperature': temperature,
  };
  var options = {
    "method": "post",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + API_key
    },
    "payload": JSON.stringify(payload)
  };
  // Make the API request to the correct endpoint for chat model
  var response = UrlFetchApp.fetch("https://api.openai.com/v1/chat/completions", options);
  // Parse the response and return the generated text
  var responseData = JSON.parse(response.getContentText());
  return responseData.choices[0].message['content'].trim(); // Access the 'content' field of the 'message' object
}