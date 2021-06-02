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
    $("a.fix.active").removeClass("active");
    $(this).addClass("active");
  });

  // Activate DataTable
  $("#device-table").DataTable();
  $("#client-table").DataTable();
  $("#quote-table").DataTable();
  $("#policy-table").DataTable();
});
