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

  // $(".data-table .cancel").click(function () {
  //   $("main .overlay").removeClass("d-none");
  //   $("main .overlay .delete_popup").removeClass("d-none");
  // });

  // $("#close").click(function () {
  //   $(this).parent().parent().parent().addClass("d-none");
  //   $(this).parent().parent().parent().parent().addClass("d-none");
  // });

  // $("main .overlay").click(function () {
  //   if ($(this).is(event.target)) {
  //     $("main .overlay").addClass("d-none");
  //   }
  // });

  // //datatable
  // $("#example").DataTable();
});
