function validateForm() {
    var isAccountValid = true;
    var isTrailValid = true;

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var name = document.getElementById('name').value;

    document.getElementById('usernameError').innerHTML = '';
    document.getElementById('passwordError').innerHTML = '';
    document.getElementById('nameError').innerHTML = '';


    if (username.trim() === '') {
        document.getElementById('usernameError').innerHTML = 'Username is required.';
        isAccountValid = false;
    }

    if (password.trim() === '') {
        document.getElementById('passwordError').innerHTML = 'Password is required.';
        isAccountValid = false;
    }

    if (name.trim() === '') {
        document.getElementById('nameError').innerHTML = 'Name is required.';
        isAccountValid = false;
    }

    var trailName = document.getElementById('trail_name').value;
    var miles = document.getElementById('miles').value;
    
    document.getElementById('trailNameError').innerHTML = '';
    document.getElementById('milesError').innerHTML = '';
    
    
    if (trailName.trim() === '') {
        document.getElementById('trailNameError').innerHTML = 'Trail Name is required.';
        isTrailValid = false;
    }
    
    if (isNaN(miles) || miles <= 0) {
        document.getElementById('milesError').innerHTML = 'Enter a positive number for miles.';
        isTrailValid = false;
    }
    
    return isTrailValid && isAccountValid;
}
