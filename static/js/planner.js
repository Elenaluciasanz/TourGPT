/* Título */
function validate_title(){
    var title = $('#route_title').val();
    var error = false;

    if (title != ""){
        $("#route_title").css('border-color', 'green');
    } else{
        $("#route_title").css('border-color', 'red');
        error = true;
    }
    return error;
};

$(document).on('input', '#route_title', function(){
    validate_title();
});

/* Descripción */
function validate_description(){
    var route_description = $('#route_description').val();
    var error = false;

    if (route_description !=""){
        $("#route_description").css('border-color', 'green');
    } else{
        $("#route_description").css('border-color', 'red');
        error = true;
    }
    return error;
};

$(document).on('input', '#route_description', function(){
    validate_description();
});

/* Fechas */
function validate_start_end_date(){
    var start_date = $('#start_date').val();
    var end_date = $('#end_date').val();
    var error = false;

    if (start_date != "" ){
        $("#start_date").css('border-color', 'green');
    } else{
        $("#start_date").css('border-color', 'red');
        error = true;
    }
    
    if (end_date != ""){
        $("#end_date").css('border-color', 'green');
    } else{
        $("#end_date").css('border-color', 'red');
        error = true;
    }

    const start = new Date(start_date);
    const end = new Date(end_date);
    if (start_date != ""  && end_date != ""){
        if(start > end){
            $("#start_date").css('border-color', 'red');
            $("#end_date").css('border-color', 'red');
            error = true;
        } else{
            $("#start_date").css('border-color', 'green');
            $("#end_date").css('border-color', 'green');
        }
    }
    return error;
}


$(document).on('input', '#start_date', function(){
    validate_start_end_date();
});

$(document).on('input', '#end_date', function(){
    validate_start_end_date();
});

/* Origen */
// Filtrar primeras 5 coincidencias
function origin_selector(){
    var filter, cities_base;
    var count = 0;
    document.getElementById('origin_list').style.display = '';
    filter = document.getElementById('origin_filter').value.toLowerCase();         
    cities_base = document.querySelectorAll(".origin_search").forEach(city_base =>{
        if (count < 5 && filter !== "" && city_base.innerHTML.toLowerCase().includes(filter)){
            city_base.style.display = '';
            count++;
        }
        else{
            city_base.style.display = 'none';
        }
    });
}

// Seleccionar un origen del listado de coincidencias
$(document).on('click', '.origin_search', function(e){
    e.preventDefault();

    const id = $(this).data('id');
    const name = $(this).data('name');

    $("#origin_filter").val(name);
    $("#origin_id").val(id);
    $("#origin_filter").css('border-color', 'green');
    $('#origin_list').css('display', 'none');
})

// Si se modifica listado de coincidencias, borrar el id del origen
$(document).on('keydown', '#origin_filter', function(){
    $("#origin_id").val("");
    $("#origin_filter").css('border-color', 'red');
 
});

// Validar que se haya seleccionado un origen
function validate_origin_id(){
    var origin = $('#origin_id').val();
    var error = false;

    if (origin == ""){
        $('#origin_filter').css('border-color', 'red');
        error = true;
    }
    else{
        $('#origin_filter').css('border-color', 'green');
    }
    return error;
}

/* Destino */
// Filtrar primeras 5 coincidencias
function destination_selector(){
    var filter, cities_base;
    var count = 0;
    document.getElementById('destination_list').style.display = '';
    filter = document.getElementById('destination_filter').value.toLowerCase();         
    cities_base = document.querySelectorAll(".destination_search").forEach(city_base =>{
        if (count < 5 && filter !== "" && city_base.innerHTML.toLowerCase().includes(filter)){
            city_base.style.display = '';
            count++;
        }
        else{
            city_base.style.display = 'none';
        }
    });
}

// Seleccionar un destino del listado de coincidencias
$(document).on('click', '.destination_search', function(e){
    e.preventDefault();

    const id = $(this).data('id');
    const name = $(this).data('name');

    $("#destination_filter").val(name);
    $("#destination_id").val(id);
    $("#destination_filter").css('border-color', 'green');
    $('#destination_list').css('display', 'none');
})
  
// Si se modifica listado de coincidencias, borrar el id del destino
$(document).on('keydown', '#destination_filter', function(){
    $("#destination_id").val("");
    $("#destination_filter").css('border-color', 'red');
});


/* Validación final */
// Validar que se haya seleccionado un destino
function validate_destination_id(){
    var origin = $('#destination_id').val();
    var error = false;

    if (origin == ""){
        $('#destination_filter').css('border-color', 'red');
        error = true;
    }
    else{
        $('#destination_filter').css('border-color', 'green');
    }
    return error;
}

$(document).on('click', '#submit_route', function(e){
    var error_start_end = validate_start_end_date();
    var error_origin = validate_origin_id();
    var error_destination = validate_destination_id();

    if (error_start_end || error_origin || error_destination){
        e.preventDefault();
    }
    else{
        $("#route_alert").css('display', 'block');
    }    
})
