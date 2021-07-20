// for smooth scrolling to page sections
$(function () {
  $('a[href*="#"]:not([href="#"])').click(function () {
    if (
      location.pathname.replace(/^\//, "") ==
        this.pathname.replace(/^\//, "") &&
      location.hostname == this.hostname
    ) {
      var target = $(this.hash);
      target = target.length ? target : $("[name=" + this.hash.slice(1) + "]");
      if (target.length) {
        $("html, body").animate(
          {
            scrollTop: target.offset().top,
          },
          1750
        );
        return false;
      }
    }
  });
});

// To open and close sidebar
var e = document.getElementById("sidenav");
function toggleNav() {
  if (e.style.left == "0px") {
    e.style.left = "-270px";
    document.getElementById("content-wrap").style.display = "none";
  } else {
    e.style.left = "0px";
    document.getElementById("content-wrap").style.display = "block";
  }
}


$(document).ready(function () {
  var showChar = 175;
  var ellipsestext = "...";
  var moretext = "More";
  var lesstext = " Less";
  $(".more").each(function () {
    var content = $(this).html();

    if (content.length > showChar) {
      var c = content.substr(0, showChar);
      var h = content.substr(showChar - 1, content.length - showChar);

      var html =
        c +
        '<span class="moreellipses">' +
        ellipsestext +
        '&nbsp;</span><span class="morecontent"><span>' +
        h +
        '</span>&nbsp;&nbsp;<a href="" class="morelink toggle">' +
        moretext +
        "</a></span>";

      $(this).html(html);
    }
  });

  $(".morelink").click(function () {
    if ($(this).hasClass("less")) {
      $(this).removeClass("less");
      $(this).html(moretext);
    } else {
      $(this).addClass("less");
      $(this).html(lesstext);
    }
    $(this).parent().prev().toggle();
    $(this).prev().toggle();
    return false;
  });
});
