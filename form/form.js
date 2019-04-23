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