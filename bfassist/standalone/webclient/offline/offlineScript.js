function registerBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = '/register'
	let parameters = {
		 'Keyhash' : document.getElementById('registerBFAUserKeyhash').value,
		 'User' : document.getElementById('registerBFAUserUser').value,
		 'Pass' : document.getElementById('registerBFAUserPass').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('registerBFAUserOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('registerBFAUserOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function loginBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = '/login'
	let parameters = {
		 'Keyhash' : document.getElementById('registerBFAUserKeyhash').value,
		 'User' : document.getElementById('registerBFAUserUser').value,
		 'Pass' : document.getElementById('registerBFAUserPass').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('registerBFAUserOutput').innerHTML = xmlhttp.response
			window.location.href = "webclient"
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('registerBFAUserOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

