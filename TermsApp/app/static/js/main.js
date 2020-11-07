function validate() {
  console.log("hei");
  var xhttp = new XMLHttpRequest();
  var urlForm = document.getElementById("url").value;
  var textForm = document.getElementById("terms").value;
  var data = {};
  data["url"] = urlForm;
  data["text"] = textForm;
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("result").innerHTML = this.responseText;
    }
  };
  xhttp.open("POST", "/check/terms", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(JSON.stringify(data));
}
