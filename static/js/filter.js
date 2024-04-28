function country_filter(){
    var filter, countries_base, countries, count = 0;
    filter = document.getElementById('country_filter').value.toLowerCase();        
    countries_base = document.querySelectorAll(".country_filter_search").forEach(country_base =>{
        if (count < 5 && filter !== "" && country_base.innerHTML.toLowerCase().includes(filter)){
            country_base.style.display = '';
            count++;
        }
        else{
            country_base.style.display = 'none';
        }
    });

    countries = document.querySelectorAll(".country_filter_card").forEach(country =>{
        if (country.id.toLowerCase().includes(filter)){
            country.style.display = '';
        }
        else{
            country.style.display = 'none';
        }
    });
}



function city_filter(){
    var filter, cities_base, cities;
    var count = 0;
    filter = document.getElementById('city_filter').value.toLowerCase();            
    cities_base = document.querySelectorAll(".city_filter_search").forEach(city_base =>{
        if (count < 5 && filter !== "" && city_base.innerHTML.toLowerCase().includes(filter)){
            city_base.style.display = '';
            count++;
        }
        else{
            city_base.style.display = 'none';
        }
    });

    cities = document.querySelectorAll(".city_filter_card").forEach(city =>{
        if (city.id.toLowerCase().includes(filter)){
            city.style.display = '';
        }
        else{
            city.style.display = 'none';
        }
    });
}


function poi_filter(){
    var filter, pois;
    var count = 0;
    filter = document.getElementById('poi_filter').value.toLowerCase();   
    pois = document.querySelectorAll(".poi_filter_card").forEach(poi =>{
        if (poi.id.toLowerCase().includes(filter)){
            poi.style.display = '';
        }
        else{
            poi.style.display = 'none';
        }
    });
}

function poe_filter(){
    var filter, poes;
    var count = 0;
    filter = document.getElementById('poe_filter').value.toLowerCase();   
    poes = document.querySelectorAll(".poe_filter_card").forEach(poe =>{
        if (poe.id.toLowerCase().includes(filter)){
            poe.style.display = '';
        }
        else{
            poe.style.display = 'none';
        }
    });
}

function poa_filter(){
    var filter, poas;
    var count = 0;
    filter = document.getElementById('poa_filter').value.toLowerCase();   
    poas = document.querySelectorAll(".poa_filter_card").forEach(poa =>{
        if (poa.id.toLowerCase().includes(filter)){
            poa.style.display = '';
        }
        else{
            poa.style.display = 'none';
        }
    });
}

function pog_filter(){
    var filter, poags;
    var count = 0;
    filter = document.getElementById('pog_filter').value.toLowerCase();   
    pogs = document.querySelectorAll(".pog_filter_card").forEach(pog =>{
        if (pog.id.toLowerCase().includes(filter)){
            pog.style.display = '';
        }
        else{
            pog.style.display = 'none';
        }
    });
}


$(document).on('click', '.country_search', function(e){
    e.preventDefault();

    const country_id = $(this).data('country');
    const url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        data:{
            country_id: country_id
        },
        success: function(response) {
            $('#countries').load(location.href + ' ' + '#countries');
        },
        error: function(xhr,errmsg,err){}
    });

    $(".country_filter_search").each(function (index, element){
        $(this).css("display", "none");
    });
})


$(document).on('click', '.city_search', function(e){
    e.preventDefault();

    const city_id = $(this).data('city');
    const url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        data:{
            city_id: city_id
        },
        success: function(response) {
            $('#cities').load(location.href + ' ' + '#cities')
            $('#countries').load(location.href + ' ' + '#countries')
        },
        error: function(xhr,errmsg,err){}
    });

    $(".city_filter_search").each(function (index, element){
        $(this).css("display", "none");
    });
})


$(document).on('click', '#show_canceled_routes', function(e){
    var routes = document.querySelectorAll(".canceled_route")
    if (this.checked == true){
        routes.forEach(route =>{
            route.style.display = 'block';
        });
    }
    else{
        routes.forEach(route =>{
            route.style.display = 'none';
        });
    }

});

$(document).ready(function(){
    routes = document.querySelectorAll(".canceled_route").forEach(route =>{
        route.style.display = 'none';
    });
});

$(document).on('click', '#new_poi', function(e){
    e.preventDefault();

    const url = $(this).data('url');
    console.log(url);

    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            $('#city_pois' ).load(location.href + ' ' + '#city_pois')
        },
        error: function(xhr,errmsg,err){}
    });
})

$(document).on('click', '#new_poe', function(e){
    e.preventDefault();

    const url = $(this).data('url');
    console.log(url);

    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            $('#city_poes' ).load(location.href + ' ' + '#city_poes')
        },
        error: function(xhr,errmsg,err){}
    });
})

$(document).on('click', '#new_pog', function(e){
    e.preventDefault();

    const url = $(this).data('url');
    console.log(url);

    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            $('#city_pogs' ).load(location.href + ' ' + '#city_pogs')
        },
        error: function(xhr,errmsg,err){}
    });
})

$(document).on('click', '#new_poa', function(e){
    e.preventDefault();

    const url = $(this).data('url');
    console.log(url);

    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            $('#city_poas' ).load(location.href + ' ' + '#city_poas')
        },
        error: function(xhr,errmsg,err){}
    });
})

