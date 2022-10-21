$(document).ready(function () {
  $(".side-bar").css("min-height", $(document).height() + "px");
  let condition = true;
  $(".profile-circle").click(function () {
    if (condition) {
      $(".profile-menu").removeClass("d-none");
      $(this).css("background-color", "#EEE");
      condition = false;
    } else {
      $(".profile-menu").addClass("d-none");
      $(this).css("background-color", "transparent");
      condition = true;
    }
  });

  $("#filter").click(function () {
    $(".popup").removeClass("d-none");
  });

  $("#close").click(function () {
    $(".popup").addClass("d-none");
  });

  $(".results .popup").click(function () {
    if ($(this).is(event.target)) {
      $(".results .popup").addClass("d-none");
    }
  });

  $(function () {
    let dtToday = new Date();

    let month = dtToday.getMonth() + 1;
    let day = dtToday.getDate();
    let year = dtToday.getFullYear();

    if (month < 10) month = "0" + month.toString();
    if (day < 10) day = "0" + day.toString();

    let maxDate = year + "-" + month + "-" + day;
    $("#txtDate1").attr("max", maxDate);
    $("#txtDate2").attr("max", maxDate);
  });

  let swiper = new Swiper(".mySwiper", {
    slidesPerView: "auto",
    spaceBetween: 20,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });
});
