$(document).on('click', '.country_like', function(e){
    e.preventDefault();

    const slug = $(this).data('slug');
    const country = $(this).data('country');
    const url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        data:{
            country: country
        },
        success: function(response) {
            $('#' + slug).load(location.href + ' ' + '#' + slug)
        },
        error: function(xhr,errmsg,err){}
    });

})

$(document).on('click', '.city_like', function(e){
    e.preventDefault();

    const slug = $(this).data('slug');
    const city = $(this).data('city');
    const url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        data:{
            city: city
        },
        success: function(response) {
            $('#' + slug).load(location.href + ' ' + '#' + slug)
        },
        error: function(xhr,errmsg,err){}
    });

})

$(document).on('click', '.poi_like', function(e){
    e.preventDefault();

    const slug = $(this).data('slug');
    const poi = $(this).data('poi');
    const url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        data:{
            poi: poi
        },
        success: function(response) {
            $('#' + slug).load(location.href + ' ' + '#' + slug)
        },
        error: function(xhr,errmsg,err){}
    });

})

$(document).on('click', '.poe_like', function(e){
    e.preventDefault();

    const slug = $(this).data('slug');
    const poe = $(this).data('poe');
    const url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        data:{
            poe: poe
        },
        success: function(response) {
            $('#' + slug).load(location.href + ' ' + '#' + slug)
        },
        error: function(xhr,errmsg,err){}
    });

})

$(document).on('click', '.pog_like', function(e){
    e.preventDefault();

    const slug = $(this).data('slug');
    const pog = $(this).data('pog');
    const url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        data:{
            pog: pog
        },
        success: function(response) {
            $('#' + slug).load(location.href + ' ' + '#' + slug)
        },
        error: function(xhr,errmsg,err){}
    });

})

$(document).on('click', '.poa_like', function(e){
    e.preventDefault();

    const slug = $(this).data('slug');
    const poa = $(this).data('poa');
    const url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        data:{
            poa: poa
        },
        success: function(response) {
            $('#' + slug).load(location.href + ' ' + '#' + slug)
        },
        error: function(xhr,errmsg,err){}
    });

})
