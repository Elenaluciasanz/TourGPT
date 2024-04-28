
function validate_first_name(){
    var first_name = $('#id_first_name').val();
    var error = false;
    if (first_name == ""){
        $('#id_first_name').css('border-color', 'red');
        error = true;
    }
    else{
        $('#id_first_name').css('border-color', 'green');
    }
    return error;
}

function validate_last_name(){
    var last_name = $('#id_last_name').val();
    var error = false;
    if (last_name == ""){
        $('#id_last_name').css('border-color', 'red');
        error = true;
    }
    else{
        $('#id_last_name').css('border-color', 'green');
    }
    return error;
}

function validate_date(){
    var date = $('#id_date').val();
    var error = false;
    const today = Date.now();
    const start = new Date('Jan 1 1900');
    console.log(start);
    const nac = new Date(date);
    if (date == "" || nac > today || nac < start){
        $('#id_date').css('border-color', 'red');
        error = true;
    }
    else{
        $('#id_date').css('border-color', 'green');
    }
    return error;
}

function validate_number(){
    var id_number = $('#id_number').val();
    var error = false;
    if (id_number == "" || id_number.length < 9){
        $('#id_number').css('border-color', 'red');
        error = true;
    }
    else{
        $('#id_number').css('border-color', 'green');
    }
    return error;
}

function validate_username(){
    var username = $('#id_username').val();
    var error = false;
    if (username == ""){
        $('#id_username').css('border-color', 'red');
        error = true;
    } else{
        const url = $('#id_username').data('url');
        $.ajax({
            type: 'GET',
            url: url,
            data:{
                username: username
            },
            success: function(response) {
                if (response.is_taken){
                    $('#id_username').css('border-color', 'red');
                    $('#username_is_taken').css('display', 'block');
                    error = true;
                } else{
                    $('#id_username').css('border-color', 'green');
                    $('#username_is_taken').css('display', 'none');
                }
            },
            error: function(xhr,errmsg,err){
                $('#id_username').css('border-color', 'red');
            error = true;
            }
        });
    }

    return error;
}

function validate_email(){
    var email = $('#id_email').val();
    var error = false;
    if (email == "" || !email.includes('@') || !email.includes('.')){
        $('#id_email').css('border-color', 'red');
        error = true;
    } 
    else{
        const url = $('#id_email').data('url');
        $.ajax({
            type: 'GET',
            url: url,
            data:{
                email: email
            },
            success: function(response) {
                if (response.is_taken){
                    $('#id_email').css('border-color', 'red');
                    $('#email_is_taken').css('display', 'block');
                    error = true;
                } else{
                    $('#id_email').css('border-color', 'green');
                    $('#email_is_taken').css('display', 'none');
                }
            },
            error: function(xhr,errmsg,err){
                $('#id_email').css('border-color', 'red');
            error = true;
            }
        });
    }

    return error;
}


function validate_password(){
    var password = $('#id_password1').val();

    var first_name = $('#id_first_name').val().toLowerCase();
    var last_name = $('#id_last_name').val().toLowerCase();
    var username = $('#id_username').val().toLowerCase();

    var numbers = 0;
    var uppercase = 0;
    var lowercase = 0;
    var error = false;

    for (var i = 0; i < password.length; i++){
        if (password[i] >= 'A' && password[i] <= 'Z'){
            uppercase++;
        }
        else if (password[i] >= 'a' && password[i] <= 'z'){
            lowercase++;
        }
        else if ((password[i]) >= '0' && (password[i]) <= '9'){
            numbers++;
        }
    }

    if (password.length < 8){
        $('#minChar').css('color', 'red');
        error = true;
    }
    else{
        $('#minChar').css('color', 'green');
    }
    if (uppercase <= 0 || lowercase <= 0){
        $('#mayMin').css('color', 'red');
        error = true;
    }
    else{
        $('#mayMin').css('color', 'green');
    }
    if (numbers <= 0){
        $('#minNum').css('color', 'red');
        error = true;
    }
    else{
        $('#minNum').css('color', 'green');
    }

    if (numbers <= 0){
        $('#minNum').css('color', 'red');
        error = true;
    }
    else{
        $('#minNum').css('color', 'green');
    }

    password = password.toLowerCase();

    if (password != "" && first_name != "" && password.includes(first_name)){
        $('#perInfo').css('color', 'red');
        error = true;
    }
    else if (password != "" && last_name != "" && password.includes(last_name)){
        $('#perInfo').css('color', 'red');
        error = true;
    }
    else if (password != "" && username != "" && password.includes(username)){
        $('#perInfo').css('color', 'red');
        error = true;
    }
    else{
        $('#perInfo').css('color', 'green');
    }

    if (error){
        $('#id_password1').css('border-color', 'red');
    }
    else{
        $('#id_password1').css('border-color', 'green');
    }

    return error;
}


function validate_password_confirm(){
    var password = $('#id_password1').val();
    var password_confirm = $('#id_password2').val();

    if (password != password_confirm){
        $('#id_password2').css('border-color', 'red');
        $('#matchPass').css('display', 'block');
    }
    else{
        $('#id_password2').css('border-color', 'green');
        $('#matchPass').css('display', 'none');
    }
}



$(document).on('input', '#id_first_name', function(){
    validate_first_name();
});

$(document).on('input', '#id_last_name', function(){
    validate_last_name();
});

$(document).on('input', '#id_date', function(){
    validate_date();
});

$(document).on('input', '#id_number', function(){
    validate_number();
});

$(document).on('input', '#id_username', function(){
    validate_username();
});

$(document).on('input', '#id_email', function(){
    validate_email();
});

$(document).on('input', '#id_password1', function(){
    validate_password();
});

$(document).on('input', '#id_password2', function(){
    validate_password_confirm();
});


$(document).on('submit', '#id_signup', function(event){
    var error_fist_name = validate_first_name();
    var error_last_name = validate_last_name();
    var error_date = validate_date();
    var error_number = validate_number();
    var error_username = validate_username();
    var error_email = validate_email();
    var error_password = validate_password();
    var error_password_confirm = validate_password_confirm();
    
    if (error_fist_name || error_last_name || error_date || error_number || error_username || error_email || error_password || error_password_confirm){
        event.preventDefault();
    }
});
