// Sticky Top Nav
document.addEventListener("DOMContentLoaded", function () {
  window.addEventListener("scroll", function () {
    if (window.scrollY > 100) {
      document.getElementById("header").classList.add("sticky-top");
    } else {
      document.getElementById("header").classList.remove("sticky-top");
    }
  });
});

// Animate menu icon
function myFunction(x) {
  x.classList.toggle("change");
}

// Scroll to top script
document.addEventListener("scroll", handleScroll);
// get a reference to our predefined button
var scrollToTopBtn = document.querySelector(".up");

function handleScroll() {
  var scrolled = window.pageYOffset;
  if (scrolled > 400) {
    //show button
    scrollToTopBtn.style.display = "block";
  } else {
    //hide button
    scrollToTopBtn.style.display = "none";
  }
}

scrollToTopBtn.addEventListener("click", scrollToTop);

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}
// End of script

$(document).ready(function () {
  // for smooth scrolling to page sections
  $(function () {
    $('a[href*="#"]:not([href="#"])').click(function () {
      if (
        location.pathname.replace(/^\//, "") ==
          this.pathname.replace(/^\//, "") &&
        location.hostname == this.hostname
      ) {
        var target = $(this.hash);
        target = target.length
          ? target
          : $("[name=" + this.hash.slice(1) + "]");
        if (target.length) {
          $("html, body").animate(
            {
              scrollTop: target.offset().top,
            },
            1450
          );
          return false;
        }
      }
    });
  });

  var url = window.location;
  // Will only work if string in href matches with location
  $('ul.navbar-nav a[href="' + url + '"]')
    .parent()
    .addClass("active");

  // Will also work for relative and absolute hrefs
  $(function () {
    $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass(
      "active"
    );
  });

  // Search function for schools display
  $("#search").keyup(function () {
    // Search text
    var text = $(this).val();

    // Hide all content class element
    $(".school").hide();

    // Search
    $('.school .title:contains("' + text + '")')
      .closest(".school")
      .show();
  });
});

$.expr[":"].contains = $.expr.createPseudo(function (arg) {
  return function (elem) {
    return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
  };
});

AOS.init({
  once: true,
  duration: 1200,
});

var input = document.querySelector("#phone");

window.intlTelInput(input, {
  initialCountry: "auto",
  geoIpLookup: function (callback) {
    $.get("https://ipinfo.io", function () {}, "jsonp").always(function (resp) {
      var countryCode = resp && resp.country ? resp.country : "ng";
      callback(countryCode);
    });
  },
  utilsScript:
    "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.13/js/utils.js", // just for formatting/placeholders etc
});

// Limit input to the + sign and numbers only
function isNumberKey(evt) {
  var charCode = evt.which ? evt.which : event.keyCode;
  if (charCode != 43 && charCode > 31 && (charCode < 48 || charCode > 57))
    return false;

  return true;
}

// Add new file input field
function addMoreAttachment() {
  $(".attachment-row:last").clone().insertAfter(".attachment-row:last");
  $(".attachment-row:last").find("input").val("");
}

