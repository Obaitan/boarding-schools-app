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

//Email Validation Function
function isValidEmailAddress(emailAddress) {
  var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
  return pattern.test(emailAddress);
}

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
    $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
  });

  // Search function for schools display
  $("#search, #search2").keyup(function () {
    // Search text
    var text = $(this).val();

    // Hide all content class element
    $(".school").hide();

    // Search
    $('.school .title:contains("' + text + '")')
      .closest(".school")
      .show();
  });

  // Tooltips Initialization
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

  $("#contact-form").validate({
    rules: {
      fullname: {
        required: true,
      },
      email: {
        required: true,
        email: true,
      },
      phone: {
        required: true,
      },
      message: {
        required: true,
        maxlength: 8000,
      },
    },

    messages: {
      // custom messages
      fullname: {
        required: "*",
      },
      email: {
        required: "*",
      },
      phone: {
        required: "*",
      },
      message: {
        required: "*",
        maxlength: jQuery.format("The maxlength for message is {0} !"),
      },
    },

    submitHandler: function (form) {
      $form = $(form);
      $container = $form.parent();
      w = $form.outerWidth();
      h = $form.outerHeight();
      $form.hide();

      $("#msg_submitting", $container).width(w).height(h).fadeIn(1000);
      $.ajax({
        type: "POST",
        url: $form.attr("action"),
        data: $form.serialize(),
        success: function (data) {
          $("#msg_submitting", $container).hide();
          if (data == "success") {
            $("#msg_submitted", $container).width(w).height(h).fadeIn(1000);
          } else {
            $("#errors", $container).html(data).show();
            $form.show();
          }
        },
      });

      return false;
    },
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
var input4 = document.querySelector("#telephone");
window.intlTelInput(input, {
  initialCountry: "auto",
  geoIpLookup: function (callback) {
    $.get("https://ipinfo.io", function () {}, "jsonp").always(function (resp) {
      var countryCode = resp && resp.country ? resp.country : "us";
      callback(countryCode);
    });
  },
  utilsScript: "../libraries/intl-tel-input-master/build/js/utils.js", // just for formatting/placeholders etc
});

window.intlTelInput(input4, {
  initialCountry: "auto",
  geoIpLookup: function (callback) {
    $.get("https://ipinfo.io", function () {}, "jsonp").always(function (resp) {
      var countryCode = resp && resp.country ? resp.country : "us";
      callback(countryCode);
    });
  },
  utilsScript: "../libraries/intl-tel-input-master/build/js/utils.js", // just for formatting/placeholders etc
});

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
