# Contact form for static websites

Hosting static websites on S3 is pretty great.
* Static websites are quick to set up.
* Static websites are *really* cheap to host.
* Static websites don't require you to deal with pesky servers.

However, setting up a contact form on a static website is not so great.
It can be a real challenge setting up a contact form on a static website,
and most websites *do* need some type of contact form.

Together we'll go through the steps to set up a working contact form on a static website using AWS.
At the end, we'll have a contact form that collects a user's name, email and a message.
That information is then captured and sent to our specified email address.

Here are the steps we'll go through to make it work:
* Building a contact form with HTML and CSS
* Using jQuery to capture and send the form input as JSON data
* Setting up an API endpoint with AWS API Gateway to receive the data
* Composing an email with the data using AWS Lambda and Python
* Sending the composed email with AWS SES to our email address

## Let's get started

Making a contact form work for a static website seems like a straight forward task.
Our contact form should be able to collect a user's info (name, email, message, etc.),
and send that info as an email to our email address.

With a static website, a few things complicates our life a bit.
While we can collect and send user info from a static website using jQuery,
we don't have a web server to receive and process this data.
Sending information makes little difference if there is nothing to recieve it!

We need to enlist outside help to receive and process the data from our contact form.
We can collect and send data from our static website, but we need help with the following:
* Reciving the data from our contact form (AWS API Gateway)
* Composing an email with the data (AWS Lambda, Python)
* Sending the email to our email address (AWS SES)

Later, we'll use AWS services to help us collect and send the data.
First though, we'll create our contact form with HTML and CSS.

## Building a contact form with HTML and CSS

For our contact form, we'll be collecting a user's name, email address and a message.
Our basic form is quite simple.
Notice that both the form and each input element has a unique id.
We'll use these ids later in our submit function to capture the data in the form.

```
<form id="contact" method="post">
  <input id="name" type="text" placeholder="Name">
  <input id="email" type="email" placeholder="Email address">
  <textarea id="message" placeholder="Your message here..."></textarea>
  <button onClick="submitForm(event)">Submit</button>
</form>
```
Optionally, we can style the form by adding some custom CSS.
```
input, textarea, button {
  margin: 10px 0;
  border: 1px solid #CCC;
}
input, textarea {
  width: 100%;
  padding: 10px;
}
textarea {
  resize: vertical;
}
button {
  border-radius: 4px;
  padding: 10px 30px;
  color: #555;
  cursor: pointer;
}
button:hover {
  color: #333;
  border-color: #888;
}
```
We've got a decent looking form now! 
There is potential to do more custom CSS styling to make the form blend with your site.
For now though, we'll move on to the next step: Capturing and sending off the form input with jQuery.

## Using jQuery to capture and send the form input as JSON
Now that we have a good looking form, 
we'll want to capture and send the form input when our users click on the submit button.
To do that, we're going to use jQuery – so make sure to include it on your page.
```
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
```

Our code is composed of four parts.

First, we're specifing the URL that we will be posting the data to.
We don't have the URL yet, we'll be getting that later as we set up AWS API Gateway.
For now, we simply have a placeholder there.

Second, we are validating the input to our form.
As you're going through the code,
notice that I've split out the validation into a seperate function for clarity.
Here, we want to make sure that the users has filled out all the fields.
We're also checking if the email is valid using a regular expression.

Third, we're bundeling the name, email and message up as a JavaScript object.

Finally, we're sending the object as JSON in a POST request to our URL.
If we get a succesful response back, we're making an alert with "Success!".
If we get an error back, we're making an alert with "Error - something went wrong".

```
function submitForm(e) {
  e.preventDefault()
  var URL = "INSERT_API_ENDPOINT_HERE"

  if(!formIsValid()) {
    return
  }

  var data = {
  name : $("#name").val(),
  email : $("#email").val(),
  message : $("#message").val(),
  }

  $.ajax({
    type: "POST",
    url : URL,
    data: JSON.stringify(data),

    success: function () {
      alert("Success!")
      document.getElementById("contact").reset()
    },
    error: function () {
      alert("Error - something went wrong")
    }
  })
}

function formIsValid() {
  if ($("#name").val()=="") {
    alert ("Please enter your name")
    return false
  }
  if ($("#email").val()=="") {
    alert ("Please enter your email")
    return false
  }
  var email_regex = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,6})?$/
  if (!email_regex.test($("#email").val())) {
    alert ("Please enter a valid email address")
    return false
  }
  if ($("#message").val()=="") {
    alert ("Please enter your message")
    return false
  }
  return true
}
```
Alright, we're ready to move to the AWS Console to set up the backend of our form.
From AWS we need to set up (1) API Gateway to receive our data,
(2) a Lambda function to insert the data into an email template,
and (3) SES to send the email to our email address.
However, to make our lives easier, we'll go through these steps in *reverse* order.

## Setting up AWS SES to send email
Before we can send email with AWS SES, we need to verify our email.
We're looking to verify two email addresses:

* The Sending Email Address (ex: hello@yourdomain.com)
* The Receiving Email Address (ex: sales@yourdomain.com)

[Verifying an email address](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html) with SES is fairly straight forward.
In the AWS Console, [navigate to SES](https://console.aws.amazon.com/ses/).
Under Identity Management, choose email addresses and then Verify a New Email Address.
You'll type in your email address and Amazon will send a verification email to that address.

Do this for both your sending and receiving email address.
After you're done, you can test an email address by selecting it and pressing Send a Test Email.

Next, we'll be creating the Lambda function inserts the form input in an email template,
and instructs SES to send the email.

## Composing an email using AWS Lambda and Python
Our Lambda function will compose an email by inserting the data from the form into an email template,
and then instruct AWS SES to send the email.
However, before we actually create our Lambda function and email template,
we'll first create a permissions role for the Lambda function.

### Creating an IAM role for our Lambda function
Permission roles are great for managing permission access to different AWS services. 
We'll make a new role for our Lambda function with AWS IAM.
The role should allow the Lambda function to send email with SES and write logs to CloudWatch.

* [Navigate to AWS IAM](https://console.aws.amazon.com/iam/) and select Roles -> Create role
* Choose Lambda and go on to Permissions
* Select 'AmazonSESFullAccess' and 'AWSLambdaBasicExecutionRole'
* Go on to Review and give the role a descriptive name, like 'LambdaSES'

With the role set up, we're now ready to create our Lambda function. 

### Setting up the Lambda function

* [Navigate to AWS Lambda](https://console.aws.amazon.com/lambda/) and select Create function
* Name the function (ex. 'emailer') and select Python 3.6 as the runtime
* Under Permissions, select Use existing role and then select the IAM role we just created
* Finish by pressing Create function

### Creating an Email Template

Before we start writing Python in our Lambda function,
let's start by preparing our email template.
We're actually going to have two templates, one plain text template and one HTML template.
It is good practice to provide both a plain text and HTML version of email,
so that is what we'll do.

* Create two new files in the Function code section.
* Name them template.txt and template.html

You can use the templates below to fill in the files or you can create your own.
Remember to give unique values to where you would like to insert form data for name, email and message.
We'll be using replace in Python to replace these values with our data.
I've used the values `_name`, `_email` and `_message` respectively.

Plain text (.txt) template:
```
A New Customer Submitted the Contact Form
_name
_email
_message

This is great news! We should get back to them as soon as possible to help them get started. This could be the beginning of something great.

Write Email
_email

Hyperwonk
Sydney, Australia
```

The HTML template can be really simple, but I have spiced mine up with a bit of styling.
Notice that the CSS styling in my HTML template is mostly inline.
While many email clients now allow for dedicated style elements,
some strip out these style elements when forwarding.
Often the safest bet is to inline any CSS – although it compromises legibility and maintenance.

HTML (.html) template:
```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>New Customer Submitted Contact Form</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <div style="padding: 1.5rem 0 1rem; background-color: #FFF; text-align: left;">
    <div style="position: relative; width: 100%; max-width: 600px; margin: 0 auto; padding: 0 20px; box-sizing: border-box;">
      <img style="max-width: 50%; max-height: 50px;" src="https://s3-ap-southeast-2.amazonaws.com/www.hyperwonk.com/images/logo-color.png" alt="Hyperwonk">
    </div>
  </div>
  <div style="padding: 4rem 0 3rem; background-color: #f7f7f7; text-align: center;">
    <div style="position: relative; width: 100%; max-width: 600px; margin: 0 auto; padding: 0 20px; box-sizing: border-box;">
      <h1 style="font-family: sans-serif; color: #444; margin-top: 0; font-weight: 600; line-height: 1.2; margin-bottom: 1rem; font-size: 1.4rem;">
      	A New Customer Submitted the Contact Form
      </h1>
      <div style="width: 5.3rem; height: 0.25rem; background-color: #FF9C5B; border-radius: 10px; margin-bottom: 2rem; margin-left: auto; margin-right: auto;"></div>
      <h2 style="font-family: sans-serif; color: #444; margin-top: 0; font-weight: 600; line-height: 1.2; margin-bottom: 1rem; font-size: 1.2rem;">
      	_name
      </h2>
      <h2 style="font-family: sans-serif; color: #444; margin-top: 0; font-weight: 600; line-height: 1.2; margin-bottom: 1rem; font-size: 1.2rem;">
        <a href="mailto:_email" target="_top" style="color: #444; text-decoration: none;">_email</a>
      </h2>
      <p style="font-family: sans-serif; color: #444; font-size: 0.9rem; line-height: 1.6; font-weight: 400; margin-bottom: 2rem; padding: 30px; background-color: #FFF; border: 1px solid #ccc;">
        _message
      </p>
      <p style="font-family: sans-serif; color: #444; font-size: 0.9rem; line-height: 1.6; font-weight: 400; margin-bottom: 2rem;">
      	This is great news! We should get back to them as soon as we can to help them get started. This could be the beginning of something great.
      </p>
      <a style="font-family: sans-serif; text-decoration: none; display: inline-block; height: 38px; padding: 0 30px; text-align: center; font-size: 11px; font-weight: 600; line-height: 38px; letter-spacing: .1rem; text-transform: uppercase; white-space: nowrap; background-color: #ED303C; border-radius: 4px; cursor: pointer;" href="mailto:_email?Subject=Welcome%20to%20Great%20Things">
      	<span style="color: #FFF;">Write Email</span>
      </a>
    </div>
  </div>
  <div style="padding: 2rem 0 1rem; background-color: #FFF; text-align: center; ">
    <div style="position: relative; width: 100%; max-width: 600px; margin: 0 auto; padding: 0 20px; box-sizing: border-box;">
      <p style="font-family: sans-serif; color: #444; font-size: 0.9rem; line-height: 1.6; font-weight: 400; margin-bottom: 2rem;">
      	<span style="font-weight: 600;">Hyperwonk</span><br>Sydney, Australia
      </p>
    </div>
  </div>
</body>
</html>
```

### Writing the Lambda function in Python

Alright – we're now ready to write our Lambda function with Python.
I'll be going through the code below step-by-step:

First we import the Boto 3 library, as well as `ClientError` from exceptions.
Boto 3 is the Python library for interacting with AWS services. 

Our Python code consists of a single function: `lambda_handler`.
`lambda_handler` will execute every time our form is submitted.
Notice the `event` argument. This is our form data.
The form data is passed to our function as a dictionary called `event`.
We'll use this dictionary to replace the values for name, email and message in our templates.
The function also is passed a second argument `context` which we wont use.

The function starts by printing the contents of `event` to the log.
It then sets the values for `sender`, `recipient` and `subject`.
We're then opening the template files, and replacing the placeholder values with the form data.

Now, we're instantiating an SES client to send our email, and pass instructions to it.
This is where we're actually sending the email.
Notice that this is a `try/except/else` statement, where we also make sure to log the response.

In using the below code, you should customize the values for `sender`, `recipient` and `aws_region`.
Make sure to also check that the names of your .txt and .html templates match with values in Python.

```
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
  print(f"Received data from form: {event}")
  
  sender = "Hello <hello@yourdomain.com>"
  recipient = "sales@yourdomain.com"
  subject = f"New Customer: {event['name']}"

  with open('template.txt') as file:
    text = file.read()
  text = text.replace('_name', event['name'])
  text = text.replace('_email', event['email'])
  text = text.replace('_message', event['message'])
  
  with open('template.html') as file:
    html = file.read()
  html = html.replace('_name', event['name'])
  html = html.replace('_email', event['email'])
  html = html.replace('_message', event['message'])

  charset = "UTF-8"
  
  aws_region = "us-east-1"
  client = boto3.client('ses',region_name=aws_region)
  
  try:
    response = client.send_email(
      Destination={
        'ToAddresses': [
          recipient,
        ],
      },
      Message={
        'Body': {
          'Html': {
            'Charset': charset,
            'Data': html,
          },
          'Text': {
            'Charset': charset,
            'Data': text,
          },
        },
        'Subject': {
          'Charset': charset,
          'Data': subject,
        },
      },
      Source=sender,
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print(f"Email sent, Message ID: {response['MessageId']}")
```

We can now test that our Lambda function actually works.
Try configuring a new test event, passing test values for name, email and message:
```
{
  "name": "Test Namington",
  "email": "test@testing.com",
  "message": "Hello, this is simply a test. I'm very interested in testing. Cheers"
}
```
Running this test, you should be able to recieve an email with our test values. 
Try testing different values for name, email and message to see how it effects the email.

Next, we'll be setting up the API Gateway, so we can recieve real data from our form.

## Setting up an API endpoint with AWS API Gateway to receive data

To connect our form data with our Lambda function,
we need to set up an API endpoint with API Gateway.

Below are the steps to set up the API.
You'll be well off simply leaving all the defaults as they are.

* Navigate to API Gateway and press 'Create API'
* Give your API a name (ex: contact)
* Press 'Actions' and then 'Create Ressource'
* Give the ressource a name (ex: contact) and press 'Create Ressource'
* Press 'Actions', then 'Create Method', choose 'POST' and press ✅
* Type in the name of the lambda function (emailer) and press 'Save'
* Press 'Actions', then 'Enable CORS' and press 'Enable CORS ...' and confirm
* Press 'Actions' and then 'Deploy API'
* Choose `[New Stage]` as Deployment stage and give it a name (ex: `1`)
* Press the ▶ next to `1` to unfold the menu and press 'POST' to see Invoke URL
* Take note of the URL (ex: `https://xxxxxx.execute-api.us-east-1.amazonaws.com/1/contact`)

Whew! What a ride. But it will all be worth it soon as we're now ready to make our form fully functional.

## Enable the Contact Form

For this last step, take the URL endpoint we just created and insert it in place of `INSERT_API_ENDPOINT_HERE` in our `submitForm` function.

```
var URL = "https://xxxxxx.execute-api.us-east-1.amazonaws.com/1/contact"
```
## Final Words

*Congratulations!*
You now have a fully functioning form - perfect for a static website.

If you like this post, please feel free to say so! All the files are available in the Github repo:

[Contact Form for Static Websites](https://github.com/tobjensen/contact-form)

You can get in touch with at tobias@hyperwonk.com
