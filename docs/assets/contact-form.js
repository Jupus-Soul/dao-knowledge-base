// Sends the "Contact the DAO Council" form without leaving the page.
document.addEventListener("submit", function (event) {
  var form = event.target;
  if (!form.matches || !form.matches("form.kb-contact")) return;
  event.preventDefault();
  var status = form.querySelector(".kb-contact__status");
  var button = form.querySelector("button[type=submit]");
  function say(text, kind) {
    status.textContent = text;
    status.className = "kb-contact__status kb-contact__status--" + kind;
  }
  if (!form.checkValidity()) { form.reportValidity(); return; }
  var data = {};
  new FormData(form).forEach(function (value, key) { data[key] = value; });
  if (!data.access_key) { say("The contact form is still being set up. Please check back soon.", "error"); return; }
  if (data.botcheck) return; // filled in only by spam bots
  button.disabled = true;
  say("Sending…", "info");
  fetch(form.action, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(data),
  })
    .then(function (response) { return response.json(); })
    .then(function (result) {
      if (!result.success) throw new Error(result.message || "failed");
      form.reset();
      say("Thank you. Your message has been sent to the DAO Council.", "ok");
    })
    .catch(function () {
      say("Sorry, your message could not be sent. Please try again in a moment.", "error");
    })
    .then(function () { button.disabled = false; });
});
