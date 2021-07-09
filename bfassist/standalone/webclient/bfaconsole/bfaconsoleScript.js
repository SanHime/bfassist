function addPlayerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/addPlayer'
	let parameters = {
		 'Keyhash' : document.getElementById('addPlayerKeyhash').value,
		 'Alias' : document.getElementById('addPlayerAlias').value
	}
	xmlhttp.responseType = "json"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function bfaUpdateRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/bfaUpdate'
	xmlhttp.responseType = "json"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function bfaUpgradeRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/bfaUpgrade'
	xmlhttp.responseType = "json"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function createBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/createBFAUser'
	let parameters = {
		 'Keyhash' : document.getElementById('createBFAUserKeyhash').value
	}
	xmlhttp.responseType = "json"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function createServerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/createServer'
	let parameters = {
		 'BFAName' : document.getElementById('createServerBFAName').value,
		 'BFPath' : document.getElementById('createServerBFPath').value
	}
	xmlhttp.responseType = "json"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function deleteBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/deleteBFAUser'
	let parameters = {
		 'Keyhash' : document.getElementById('deleteBFAUserKeyhash').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function deleteServerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/deleteServer'
	let parameters = {
		 'BFAName' : document.getElementById('deleteServerBFAName').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function executeConsoleCommandRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/executeConsoleCommand'
	let parameters = {
		 'BFAName' : document.getElementById('executeConsoleCommandBFAName').value,
		 'command' : document.getElementById('executeConsoleCommandcommand').value
	}
	xmlhttp.responseType = "json"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function writeToServerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/writeToServer'
	let parameters = {
		 'BFAName' : document.getElementById('writeToServerBFAName').value,
		 'inMessage' : document.getElementById('writeToServerinMessage').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function connectWithServerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/connectWithServer'
	let parameters = {
		 'BFAName' : document.getElementById('connectWithServerBFAName').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function disconnectFromServerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/disconnectFromServer'
	let parameters = {
		 'BFAName' : document.getElementById('disconnectFromServerBFAName').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function editBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/editBFAUser'
	let parameters = {
		 'newKeyhash' : document.getElementById('editBFAUsernewKeyhash').value,
		 'newMultiLogin' : document.getElementById('editBFAUsernewMultiLogin').value,
		 'Keyhash' : document.getElementById('editBFAUserKeyhash').value,
		 'newRights' : document.getElementById('editBFAUsernewRights').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function editServerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/editServer'
	let parameters = {
		 'BFAName' : document.getElementById('editServerBFAName').value,
		 'newBFPath' : document.getElementById('editServernewBFPath').value,
		 'newBFAName' : document.getElementById('editServernewBFAName').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function loginBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/loginBFAUser'
	let parameters = {
		 'User' : document.getElementById('loginBFAUserUser').value,
		 'Keyhash' : document.getElementById('loginBFAUserKeyhash').value,
		 'Pass' : document.getElementById('loginBFAUserPass').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function logoutBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = '/logout'
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function(){}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function registerBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/registerBFAUser'
	let parameters = {
		 'Pass' : document.getElementById('registerBFAUserPass').value,
		 'Keyhash' : document.getElementById('registerBFAUserKeyhash').value,
		 'User' : document.getElementById('registerBFAUserUser').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function startRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/start'
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function stopRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/stop'
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function toggleAutoUpdateSettingRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/toggleAutoUpdateSetting'
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function toggleAutoUpgradeSettingRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/toggleAutoUpgradeSetting'
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getAutoUpdateSettingRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getAutoUpdateSetting'
	xmlhttp.responseType = "text"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getAutoUpgradeSettingRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getAutoUpgradeSetting'
	xmlhttp.responseType = "text"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getBFARightSchemeRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getBFARightScheme'
	xmlhttp.responseType = "json"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getBFAUser'
	let parameters = {
		 'Keyhash' : document.getElementById('getBFAUserKeyhash').value
	}
	url += '/params?'
	for (const [key, value] of Object.entries(parameters)) {
		    url += key + '=' + value + '&'
	}
	url = url.slice(0, -1)
	xmlhttp.responseType = "json"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getBFAUsersRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getBFAUsers'
	xmlhttp.responseType = "json"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getGlobalMonitoringRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getGlobalMonitoring'
	xmlhttp.responseType = "text"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getInGameCommandsRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getInGameCommands'
	let parameters = {
		 'BFAName' : document.getElementById('getInGameCommandsBFAName').value
	}
	url += '/params?'
	for (const [key, value] of Object.entries(parameters)) {
		    url += key + '=' + value + '&'
	}
	url = url.slice(0, -1)
	xmlhttp.responseType = "json"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getLeagueExtensionAvailabilityRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getLeagueExtensionAvailability'
	xmlhttp.responseType = "text"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = xmlhttp.response
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getPlayerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getPlayer'
	let parameters = {
		 'Keyhash' : document.getElementById('getPlayerKeyhash').value
	}
	url += '/params?'
	for (const [key, value] of Object.entries(parameters)) {
		    url += key + '=' + value + '&'
	}
	url = url.slice(0, -1)
	xmlhttp.responseType = "json"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getServerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getServer'
	let parameters = {
		 'BFAName' : document.getElementById('getServerBFAName').value
	}
	url += '/params?'
	for (const [key, value] of Object.entries(parameters)) {
		    url += key + '=' + value + '&'
	}
	url = url.slice(0, -1)
	xmlhttp.responseType = "json"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getServersRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getServers'
	xmlhttp.responseType = "json"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function getUpdateRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getUpdate'
	xmlhttp.responseType = "json"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			document.getElementById('bfaConsoleOutput').innerHTML = JSON.stringify(xmlhttp.response)
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

