// To open and close sidebar
var e = document.getElementById("sidenav");
function toggleNav() {
  if (e.style.left == "0px") {
    e.style.left = "-190px";
    document.getElementById("content-wrap").style.display = "none";
  } else {
    e.style.left = "0px";
    document.getElementById("content-wrap").style.display = "block";
  }
}

// Animate menu icon
function myFunction(x) {
  x.classList.toggle("change");

  if (e.style.left == "0px") {
    e.style.left = "-190px";
    document.getElementById("content-wrap").style.display = "none";
  } else {
    e.style.left = "0px";
    document.getElementById("content-wrap").style.display = "block";
  }
}

$(document).ready(function () {
  $("a.fix").click(function () {
    $("a.fix").removeClass("actively");
    $(this).addClass("actively");
  });
});

function previewImages() {
  var preview = document.querySelector("#preview");
  if (this.files) {
    [].forEach.call(this.files, readAndPreview);
  }

  function readAndPreview(file) {
    // Make sure `file.name` matches our extensions criteria
    if (!/\.(jpe?g|png)$/i.test(file.name)) {
      return alert(file.name + " is not an image (PNG | JPG | JPEG)");
    } // else...

    var reader = new FileReader();
    reader.addEventListener("load", function () {
      var image = new Image();
      image.height = 100;
      image.style.padding = "3px";
      image.title = file.name;
      image.src = this.result;
      preview.appendChild(image);
    });
    reader.readAsDataURL(file);
  }
}
document.querySelector("#file-input").addEventListener("change", previewImages);

function previewImages2() {
  var preview2 = document.querySelector("#preview2");
  if (this.files) {
    [].forEach.call(this.files, readAndPreview);
  }

  function readAndPreview(file) {
    // Make sure `file.name` matches our extensions criteria
    if (!/\.(jpe?g|png)$/i.test(file.name)) {
      return alert(file.name + " is not an image (PNG | JPG | JPEG)");
    } // else...

    var reader = new FileReader();
    reader.addEventListener("load", function () {
      var image = new Image();
      image.height = 100;
      image.style.padding = "3px";
      image.title = file.name;
      image.src = this.result;
      preview2.appendChild(image);
    });
    reader.readAsDataURL(file);
  }
}
document
  .querySelector("#file-input2")
  .addEventListener("change", previewImages2);

$(document).ready(function () {
  $("#countries").DataTable();
  $("#schools").DataTable();
});
