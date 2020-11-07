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

function myFunction(e) {
  var id = e.id;
  var nr = id.split("_")[1];
  var dots = document.getElementById("dots" + nr);
  var moreText = document.getElementById("more" + nr);
  var btnText = document.getElementById("myBtn_" + nr);
  console.log(nr);
  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "Read more";
    moreText.style.display = "none";
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "Read less";
    moreText.style.display = "inline";
  }
}
