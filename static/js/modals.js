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

  $("#modal_point_image_color").css("background-color", colorLight);
  $("#modal_point_description_color").css("background-color", colorDark);
  $("#modal_point_shedule_color").css("background-color", colorLight);
  $("#modal_point_price_color").css("background-color", colorDark);
  $("#modal_point_coord_color").css("background-color", colorLight);
  $("#modal_point_location_color").css("background-color", colorDark);

  $.ajax({
    url: url,
    type: "GET",
    success: function (data) {
      $("#modalContentLoading").attr("hidden", true);
      $("#modalContent").attr("hidden", false);

      $("#modal_point_name").text(data.name);

      if (data.presentation && data.presentation !== "") {
        $("#modal_point_presentation").attr("hidden", false);
        $("#modal_point_presentation").text(data.presentation);
      } else {
        $("#modal_point_presentation").attr("hidden", true);
      }

      if (data.icon && data.icon !== "" && data.type && data.type !== "") {
        $("#modal_point_icon_type_div").attr("hidden", false);
        $("#modal_point_icon").attr("class", data.icon);
        $("#modal_point_type").text(data.type);
      } else {
        $("#modal_point_icon_type_div").attr("hidden", true);
      }

      if (data.image && data.image !== "") {
        $("#modal_point_image_div").attr("hidden", false);
        $("#modal_point_image_color").attr("hidden", false);
        $("#modal_point_image").attr("src", data.image);
        $("#modal_point_image").attr("alt", data.name);
      } else {
        $("#modal_point_image_div").attr("hidden", true);
        $("#modal_point_image_color").attr("hidden", true);
      }

      if (point_type == "poi" && data.history && data.history !== "") {
        $("#modal_point_description_div").attr("hidden", false);
        $("#modal_point_description_color").attr("hidden", false);
        $("#modal_point_description").text(data.history);
      } else if (data.description && data.description !== "") {
        $("#modal_point_description_div").attr("hidden", false);
        $("#modal_point_description_color").attr("hidden", false);
        $("#modal_point_description").text(data.description);
      } else {
        $("#modal_point_description_div").attr("hidden", true);
        $("#modal_point_description_color").attr("hidden", true);
      }

      if (data.shedule_avg && data.shedule_avg !== "") {
        $("#modal_point_shedule_div").attr("hidden", false);
        $("#modal_point_shedule_color").attr("hidden", false);
        $("#modal_point_shedule_avg").text(data.shedule_avg);
      } else {
        $("#modal_point_shedule_div").attr("hidden", true);
        $("#modal_point_shedule_color").attr("hidden", true);
      }

      if (data.price_avg && data.price_avg !== "") {
        $("#modal_point_price_div").attr("hidden", false);
        $("#modal_point_price_color").attr("hidden", false);
        $("#modal_point_price_avg").text(data.price_avg);
      } else {
        $("#modal_point_price_div").attr("hidden", true);
        $("#modal_point_price_color").attr("hidden", true);
      }

      if (data.latitude && data.latitude !== "" && data.longitude && data.longitude !== "") {
        $("#modal_point_coord_div").attr("hidden", false);
        $("#modal_point_coord_color").attr("hidden", false);
        $("#modal_point_latitude").text(data.latitude);
        $("#modal_point_longitude").text(data.longitude);
      } else {
        $("#modal_point_coord_div").attr("hidden", true);
        $("#modal_point_coord_color").attr("hidden", true);
      }

      if (data.location && data.location !== "" && data.map && data.map !== "") {
        $("#modal_point_location_div").attr("hidden", false);
        $("#modal_point_location_color").attr("hidden", false);
        $("#modal_point_location").text(data.location);
        $("#modal_point_map").html(data.map);
      } else {
        $("#modal_point_location_div").attr("hidden", true);
        $("#modal_point_location_color").attr("hidden", true);
      }
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
    "<p class='me-2'>Cargando información...</p> <div class='spinner-border text-primary' role='status'></div>"
  );

  $("#modalContentLoading").attr("hidden", false);
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
