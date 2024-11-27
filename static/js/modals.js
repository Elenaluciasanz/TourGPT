function loadData(url, point_type) {
  resetModal();

  if (point_type == "poi") {
    colorLight = "#B2F591";
    colorDark = "#63954A";
  } else if (point_type == "poe") {
    colorLight = "#FFCCCC";
    colorDark = "#CB4335";
  } else if (point_type == "pog") {
    colorLight = "#B0E2FF";
    colorDark = "#2471A3";
  } else if (point_type == "poa") {
    colorLight = "#FFDAB9";
    colorDark = "#E67E22";
  } else {
    colorLight = "";
    colorDark = "";
  }

  console.log("modal_point_description_color", colorDark);
  $("modal_point_description_color").css("background-color", colorDark);
  $("modal_point_shedule_color").css("background-color", colorLight);
  $("modal_point_price_color").css("background-color", colorDark);
  $("modal_point_coord_color").css("background-color", colorLight);
  $("modal_point_location_color").css("background-color", colorDark);

  $.ajax({
    url: url,
    type: "GET",
    success: function (data) {
      $("#modalContentLoading").attr("hidden", true);
      $("#modalContent").attr("hidden", false);

      $("#modal_point_name").text(data.name);
      $("#modal_point_presentation").text(data.presentation);
      $("#modal_point_icon").attr("class", data.icon);
      $("#modal_point_type").text(data.type);
      if (point_type == "poi") {
        $("#modal_point_description").text(data.history);
      } else {
        $("#modal_point_description").text(data.description);
      }
      $("#modal_point_shedule_avg").text(data.shedule_avg);
      $("#modal_point_price_avg").text(data.price_avg);
      $("#modal_point_latitude").text(data.latitude);
      $("#modal_point_longitude").text(data.longitude);
      $("#modal_point_location").text(data.location);
      $("#modal_point_map").html(data.map);
    },

    error: function (error) {
      $("#modalContentLoading").html(
        '<p class="text-danger">Error al cargar la información.</p>'
      );
      $("#modalContent").attr("hidden", true);

      $("#modal_point_name").text("");
      $("#modal_point_presentation").text("");
      $("#modal_point_description").text("");
      $("#modal_point_shedule_avg").text("");
      $("#modal_point_price_avg").text("");
      $("#modal_point_latitude").text("");
      $("#modal_point_longitude").text("");
      $("#modal_point_location").text("");
      $("#modal_point_map").html();
    },
  });
}

function resetModal() {
  $("#modalContentLoading").html(
    "<p>Cargando información...</p> <div class='spinner-border text-primary mx-2' role='status'></div>"
  );

  $("#modalContent").attr("hidden", true);

  $("#modal_point_name").text("");
  $("#modal_point_presentation").text("");
  $("#modal_point_description").text("");
  $("#modal_point_shedule_avg").text("");
  $("#modal_point_price_avg").text("");
  $("#modal_point_latitude").text("");
  $("#modal_point_longitude").text("");
  $("#modal_point_location").text("");
  $("#modal_point_map").html();
}
