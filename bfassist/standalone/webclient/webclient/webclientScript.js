function logoutBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = '/logout'
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function(){}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

