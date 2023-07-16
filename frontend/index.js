async function signupFormSubmit() {
    let username = document.querySelector('input[name="username"]').value;
    let password = document.querySelector('input[name="password"]').value;

    // Form validation
    if (username == '' || password == '') {
        alert("Check your username or password");
        return
    }

    // Create form data
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    response = await fetch('http://127.0.0.1:8000/signup', { method: 'POST', body: formData })
    if (response.status == 200) {
        alert(" Signup Success");
    } else {
        data = await response.json();
        alert(await data.detail);
    }
}



async function loginFormSubmit() {
    let username = document.querySelector('input[name="username"]').value;
    let password = document.querySelector('input[name="password"]').value;

    // Form validation
    if (username == '' || password == '') {
        alert("Check your username or password");
        return
    }

    // Create form data
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    response = await fetch('http://127.0.0.1:8000/login', { method: 'POST', body: formData })
    if (response.status == 200) {
        alert(" Login Success, click ok to redirect to home page");
        data = await response.json();
        localStorage.setItem('access_token', data["access_token"]);
        localStorage.setItem('token_type', data["token_type"]);
        window.location.href = '/index.html';
    } else {
        data = await response.json();
        alert(await data.detail);
    }
}

function logout(){
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    window.location.href = '/login.html';
}


function parseJwt(token) {
    if (token == null) {
        return { expired: null, username: null };
    }
    // Parse JWT token using browser's atob function
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    const { exp, sub: username } = JSON.parse(jsonPayload);

    // Check if token is expired
    const expired = Date.now() >= exp * 1000

    // Return username and expired status
    return { expired, username };
}

function useAuth() {
    // If existing user, check token validity
    const { expired, username } = parseJwt(localStorage.getItem('access_token'));

    //Cater for login and signup page
    if (window.location.pathname == '/login.html' || window.location.pathname == '/signup.html') {
        if (expired == null | username == null) {
            return
        }
        else if (expired) {
            return
        }
        else if (!expired) {
            alert("Already logged in as " + username + ", click ok to redirect to home page");
            window.location.href = '/index.html';
            return { expired, username }
        }
    }
    //Cater for other pages
    else {
        if (expired == null | username == null) {
            alert("Not logged in, click ok to redirect to login page");
            window.location.href = '/login.html';
            return
        }
        else if (expired) {
            alert("Token expired, click ok to redirect to login page");
            window.location.href = '/login.html';
            return
        }
        else {
            return { expired, username };
        }

    }

}

function homePage() {
    const { expired, username } = useAuth(localStorage.getItem('access_token'));
    const mainElement = document.querySelector('main');
    const welcome = document.createElement('p');
    welcome.innerHTML = `Welcome ${username}!`;
    const sessions = document.createElement('p');
    sessions.innerHTML = `View your <a href='/me.html'>login session</a>`;
    mainElement.appendChild(welcome);
    mainElement.appendChild(sessions);
}

async function mePage() {
    const { expired, username } = useAuth(localStorage.getItem('access_token'));
    //hit 8000/me endpoint which gets a list of logins, render them
    response = await fetch('http://127.0.0.1:8000/me', {
        method: 'GET',
        headers: {
            'Authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token')

        }
    })
    if (response.status == 200) {
        data = await response.json();
        const mainElement = document.querySelector('main');
        //create a list from data["sessions"], which is a list of objects, with the field created_at
        const list = document.createElement('ul');
        for (let i = 0; i < data["sessions"].length; i++) {
            const item = document.createElement('li');
            let datetime = new Date(data["sessions"][i]["created_at"]);
            console.log(datetime)
            item.innerHTML = datetime;
            list.appendChild(item);
        }
        mainElement.appendChild(list);
    } else {
        data = await response.json();
        alert(await data.detail);
    }

}
