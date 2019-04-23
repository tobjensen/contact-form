# Contact Form for Static Websites

Static websites are pretty great.
* Static websites are quick to set up.
* Static websites are cheap to host.
* Static websites don't need you to deal with pesky servers.

Yet, setting up a contact form on a static website is not so great.
It can be a challenge to set up a contact form on a static website,
and most websites do need some type of contact form.

Contact Form for Static Websites allows you set up a working contact form with AWS.
The contact form allows a user to input thier name, email and a message.
When the form is submitted, the data is captured and sent as an email to a specified email address.

Here is an overview of how Contact Form for Static Websites works:
* Contact form is built and styled with HTML and CSS
* On form submission, the form input is captured with jQuery and sent as JSON to AWS API Gateway
* AWS API Gateway receives the data and passes it to an AWS Lambda function
* The AWS Lambda function composes an email by inserting the data into an email template
* The AWS Lambda function instructs AWS SES to send the email to a specified email address

## Let's get started

To get started with Contact Form for Static Websites, you need an AWS account.
If you don't have an AWS account, you can get started with a [free tier account](https://aws.amazon.com/free/).

Below are detailed instructions for going through the steps to set up Contact Form for Static Websites with AWS.
Here is an overview of the steps:
* Verify your sending and receiving email with SES
* Create an IAM role for the Lambda function, to allow the Lambda function to send email and write logs
* Create a Lambda function with the IAM role, using Python 3.6 as runtime
* Attach the email templates (.txt & .html) to the Lambda function
* Set up an API endpoint with API Gateway to receive data
* Insert your API endpoint URL in the `form.js` script
* Insert the form, the customised `form.js` script, and jQuery on your site

### Verify your sending and receiving email with SES

Before you can send email with AWS SES, you need to verify your email.
You'll be looking to verify two email addresses:

* Your Sending Email Address (ex: hello@yourdomain.com)
* Your Receiving Email Address (ex: sales@yourdomain.com)

[Verifying an email address](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html) with SES is straight forward.

* Log into your AWS Console and [navigate to SES](https://console.aws.amazon.com/ses/)
* Under Identity Management, choose email addresses and then Verify a New Email Address
* Enter the email address that you're verifying and confirm
* Click the link in the verification email sent to that address

Do this for both your sending and receiving email address.

After you're done, you can test an email address by selecting it and pressing Send a Test Email.

### Create an IAM role for the Lambda function, to allow it to send email and write logs

Permission roles are great for managing permission access to different AWS services. 
You'll make a new role for our Lambda function with AWS IAM.
The role should allow the Lambda function to send email with SES and write logs to CloudWatch.

* [Navigate to AWS IAM](https://console.aws.amazon.com/iam/) and select Roles -> Create role
* Choose Lambda and go on to Permissions
* Select 'AmazonSESFullAccess' and 'AWSLambdaBasicExecutionRole'
* Go on to Review and give the role a descriptive name, like 'LambdaSES'

With the role set up, you're now ready to create the Lambda function. 

### Create a Lambda function with the IAM role, using Python 3.6 as runtime

* [Navigate to AWS Lambda](https://console.aws.amazon.com/lambda/) and select Create function
* Name the function (ex. 'emailer') and select Python 3.6 as the runtime
* Under Permissions, select Use existing role and then select the IAM role we created
* Press Create function
* Replace the default code with the code from the `lambda_function.py` file
* Replace the default values for `sender`, `reciever`, and `aws_region` with your own values 

### Attach the email templates (.txt & .html) to the Lambda function

You will have two email templates, one plain text template and one HTML template.
It is good practice to provide both a plain text and HTML version of email.

* Create two new files in the Function code section.
* Name them template.txt and template.html
* Insert the code from the [template.txt file](https://github.com/tobjensen/contact-form/blob/master/lambda/template.txt) and [template.html file](https://github.com/tobjensen/contact-form/blob/master/lambda/template.html), respectivly

### Test that the Lambda function is working as intended

You can now test that the Lambda function actually works.
Try configuring a new test event, passing values for name, email and message:
```
{
  "name": "Test Namington",
  "email": "test@testing.com",
  "message": "Hello, this is a test. I'm very interested in testing. Cheers"
}
```

### Setting up an API endpoint with AWS API Gateway to receive data

To recieve form data on send it to the Lambda function,
you need to set up an API endpoint with API Gateway.

Below are the steps to set up the API endpoint.
You can leave all the defaults as they are.

* Navigate to API Gateway and press 'Create API'
* Give your API a name (ex: contact)
* Press 'Actions' and then 'Create Ressource'
* Give the ressource a name (ex: contact) and press 'Create Ressource'
* Press 'Actions', then 'Create Method', choose 'POST' and press ✅
* Type in the name of the Lambda function (emailer) and press 'Save'
* Press 'Actions', then 'Enable CORS' and press 'Enable CORS and replace existing CORS headers'
* Press 'Actions' and then 'Deploy API'
* Choose `[New Stage]` as Deployment stage and give it a name (ex: `1`)
* Press the ▶ next to `1` to unfold the menu and press 'POST' to see Invoke URL
* Take note of the URL (ex: `https://xxxxxx.execute-api.us-east-1.amazonaws.com/1/contact`)

### Insert your API endpoint URL in the `form.js` script

Replace the placeholder URL value with the API endpoint URL you created with API Gateway.
Insert the URL endpoint in [form.js](https://github.com/tobjensen/contact-form/blob/master/form/form.js) in place of `INSERT_API_ENDPOINT_HERE`.

```
var URL = "https://xxxxxx.execute-api.us-east-1.amazonaws.com/1/contact"
```

### Insert the form, the customised `form.js` script, and jQuery on your site

You are now ready to deploy Contact Form for Static Websites to your site.

* Insert the [HTML form](https://github.com/tobjensen/contact-form/blob/master/form/form.html) on your site
* Insert the [CSS styling](https://github.com/tobjensen/contact-form/blob/master/form/form.css) on your site
* Insert the your customised form.js script on your site
* Insert the [jQuery library](https://developers.google.com/speed/libraries/#jquery) on your site

## Notes

### Customizing the email templates

There is potential to do more custom CSS styling to make the form blend with your site.
You can customise the templates from Contact Form for Static Websites,
but remember to give unique values to where you would like to insert form data for name, email and message.
Notice the use of the values `_name`, `_email` and `_message` in the template files.

### Inline CSS styling in email templates 

When customising the HTML template, notice that the CSS styling in the HTML template is inline.
While many email clients now allow for dedicated style elements,
some strip out these style elements when forwarding.
Inline your CSS to avoid email clients stripping it out.

There is potential to do more custom CSS styling to make the form blend with your site.
For now though, we'll move on to the next step: Capturing and sending off the form input with jQuery.

### Validating form input

We are validating the input to our form.
Notice that validation is split out to a seperate function for clarity.
Validation makes sure that the users has filled out all the fields.
Validation is also checking if the email is valid using a regular expression.

### Customising the Lambda function

You can customise the Lambda function to better suit your needs.
Here is a brief overview of how the function is structured.

We're importing the Boto 3 library, as well as `ClientError` from exceptions.
Boto 3 is the Python library for interacting with AWS services. 

The Python code consists of a single function: `lambda_handler`.
`lambda_handler`.
The function will execute every time the form is submitted.
Notice the `event` argument. This is the form data.
The form data is passed to the function as a dictionary called `event`.
This dictionary is used to replace the values for name, email and message in the templates.
The `lambda_handler` function is also passed a second argument `context` which we are not using.

The function starts by printing the contents of `event` to the log.
It then sets the values for `sender`, `recipient` and `subject`.
It opens the template files and replaces the placeholder values with the form data.

Next it instantiates an SES client to send the email, and passes instructions to it.
This is where it is actually sending the email.
Notice that this is a `try/except/else` statement, where it also logs the response.

You should customise the values for `sender`, `recipient` and `aws_region`.
Make sure to check that the names of your .txt and .html templates match with the values in the Python function.

## Final Words

If you like Contact Form for Static Websites, please feel free to say so! All the files are available in the Github repo:

[Contact Form for Static Websites](https://github.com/tobjensen/contact-form)

You can get in touch with me at tobias@hyperwonk.com
