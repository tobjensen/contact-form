# Contact Form for Static Websites

Static websites are pretty great.
* Static websites are quick to set up.
* Static websites are cheap to host.
* Static websites don't need you to deal with pesky servers.

Yet, setting up a contact form on a static website is not so great.
It can be a challenge to set up a contact form on a static website,
and most websites *do* need some type of contact form.

Contact form for static websites allows you set up a working contact form with AWS.
The contact form allows a user to input thier name, email and a message.
When the form is submitted, the data is captured and sent as an email to a specified email address.

Here is an overview of how Contact Form for Static Websites works:
* Contact form is built and styled with HTML and CSS
* On form submission, the form input is captured with jQuery and sent as JSON data to AWS API Gateway
* AWS API Gateway receives the data and passes it to an AWS Lambda function
* The AWS Lambda function composes an email by inserting the data into an email template
* The AWS Lambda function instructs AWS SES to send the email to a specified email address

## Let's get started

To get started with Contact form for static websites, you need an AWS account.
If you don't have an AWS account, you can get started with a [free tier account](https://aws.amazon.com/free/).

Below are detailed instructions for going through the steps to set up Contact form for static websites with AWS.
Here is an overview of the steps:
* Verify your sending and receiving email with SES
* Create an IAM role for the Lambda function, to allow it to send email and write logs
* Create a Lambda function with the IAM role, using Python 3.6 as runtime
* Attach the email templates (.txt & .html) to the Lambda function
* Set up an API endpoint with API Gateway to receive data
* Insert the form, the `contact.js` script, and jQuery on your site
* Insert your API endpoint in the `contact.js` script

### Verify your sending and receiving email with SES
Before you can send email with AWS SES, you need to verify your email.
You'll be looking to verify two email addresses:

* Your Sending Email Address (ex: hello@yourdomain.com)
* Your Receiving Email Address (ex: sales@yourdomain.com)

[Verifying an email address](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html) with SES is straight forward.
In the AWS Console, [navigate to SES](https://console.aws.amazon.com/ses/).
Under Identity Management, choose email addresses and then Verify a New Email Address.
You'll type in your email address and Amazon will send a verification email to that address.

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
* Insert the code from the `template.txt` file and `template.html` file, respectivly

### Test that the Lambda function is working as intended

You can now test that the Lambda function actually works.
Try configuring a new test event, passing test values for name, email and message:
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

Below are the steps to set up the API endpoint,
leaving all the defaults as they are.

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

### Insert the form, the `contact.js` script, and jQuery on your site

For this step, you can either choose to put the entire `form.html` file directly on your site.
Alternativly, you can simply open the `form.html` file with a browser.

* Insert the form (HTML and CSS) on your site
* Insert the `contact.js` script on your site
* Insert the jQuery library on your site

### Insert your API endpoint in the `contact.js` script

Finally, make sure that you replace the placeholder URL value with the API endpoint URL you created with API Gateway.
Take the URL endpoint and insert it in place of `INSERT_API_ENDPOINT_HERE` in the `submitForm` function in `contact.js`.

```
var URL = "https://xxxxxx.execute-api.us-east-1.amazonaws.com/1/contact"
```

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
