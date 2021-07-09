function logoutBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = '/logout'
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function(){}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function clearScrollTable(scrollTable){
	var old_tbody = scrollTable.tBodies[0]
	var new_tbody = document.createElement('tbody')
	new_tbody.id = old_tbody.id
	new_tbody.className = old_tbody.className
	scrollTable.replaceChild(new_tbody, old_tbody)
	
}

function clearScrollTables(){
	var scrollTables = document.getElementsByClassName('scrollTable')
	for (const scrollTable of scrollTables) {
		clearScrollTable(scrollTable)
	
	}
	
}

function getBFAUsersRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/get/getBFAUsers'
	xmlhttp.responseType = "json"
	xmlhttp.open('GET', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			let results = []
			for (const result_data of xmlhttp.response){
				var result = []
				result.push(result_data['Keyhash'])
				result.push(result_data['Rights']['Name'])
				result.push(result_data['User'])
				result.push(result_data['Pass'])
				result.push(result_data['Online'])
				result.push(result_data['MultiLogin'])
				results.push(result)
			}
			bfaUsersFillScrollTable(results)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
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
			let results = []
			for (const result_data of xmlhttp.response){
				var result = []
				result.push(result_data['BFAName'])
				result.push(result_data['BFPath'])
				result.push(result_data['local_monitoring'])
				results.push(result)
			}
			bfaServersFillScrollTable(results)
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function setupOnLoad(){
	getBFAUsersRequest()
	getServersRequest()
	
}

function startRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/start'
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function(){}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function stopRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/stop'
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function(){}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function createServerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/post/createServer'
	let parameters = {
		 'BFPath' : document.getElementById('createServerBFPath').value,
		 'BFAName' : document.getElementById('createServerBFAName').value
	}
	xmlhttp.responseType = "json"
	xmlhttp.open('POST', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			clearScrollTables()
			setupOnLoad()
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
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
			clearScrollTables()
			setupOnLoad()
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function editServerRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/editServer'
	let parameters = {
		 'BFAName' : document.getElementById('editServerBFAName').value,
		 'newBFAName' : document.getElementById('editServernewBFAName').value,
		 'newBFPath' : document.getElementById('editServernewBFPath').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			clearScrollTables()
			setupOnLoad()
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function editBFAUserRequest(){
	let xmlhttp = new XMLHttpRequest()
	let url = 'bfassist/standalone/api/put/editBFAUser'
	let parameters = {
		 'Keyhash' : document.getElementById('editBFAUserKeyhash').value,
		 'newMultiLogin' : document.getElementById('editBFAUsernewMultiLogin').value,
		 'newKeyhash' : document.getElementById('editBFAUsernewKeyhash').value,
		 'newRights' : document.getElementById('editBFAUsernewRights').value
	}
	xmlhttp.responseType = "text"
	xmlhttp.open('PUT', url, true)
	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
			clearScrollTables()
			setupOnLoad()
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
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
			clearScrollTables()
			setupOnLoad()
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
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
			clearScrollTables()
			setupOnLoad()
			}
		if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
			}
		
	}
	if (typeof parameters !== 'undefined') {xmlhttp.send(JSON.stringify(parameters))} else {xmlhttp.send()}
}

function editServerFillFormWithData(data){
	let parameters = ['BFAName', 'newBFAName', 'newBFPath']
	for (const param of parameters) {
		if (param in data){
			document.getElementById('editServer' + param).value = data[param]
		}
	}
	
}

function editBFAUserFillFormWithData(data){
	let parameters = ['Keyhash', 'newKeyhash', 'newRights', 'newMultiLogin']
	for (const param of parameters) {
		if (param in data){
			document.getElementById('editBFAUser' + param).value = data[param]
		}
	}
	
}

function deleteServerFillFormWithData(data){
	let parameters = ['BFAName']
	for (const param of parameters) {
		if (param in data){
			document.getElementById('deleteServer' + param).value = data[param]
		}
	}
	
}

function deleteBFAUserFillFormWithData(data){
	let parameters = ['Keyhash']
	for (const param of parameters) {
		if (param in data){
			document.getElementById('deleteBFAUser' + param).value = data[param]
		}
	}
	
}

function bfaUsersgetDataFromRow(dataRow){
	let data = []
	for (const dat of dataRow.cells){
		data.push(dat.children[0].innerHTML)
	}
	let annotated_data = {}
	annotated_data['Keyhash'] = data[0]
	annotated_data['Rights'] = data[1]
	annotated_data['User'] = data[2]
	annotated_data['Pass'] = data[3]
	annotated_data['Online'] = data[4]
	annotated_data['MultiLogin'] = data[5]
	return annotated_data
}

function bfaUsersRowClick(){
	if ('clickedScrollTableRow' === this.className) {
		this.classList.remove('clickedScrollTableRow')
	}
	else {
		let clicked = this.parentElement.getElementsByClassName('clickedScrollTableRow')
		for (const row of clicked) {
			row.classList.remove('clickedScrollTableRow')
		}
		this.classList.add('clickedScrollTableRow')
		data = bfaUsersgetDataFromRow(this)
	}
	editBFAUserFillFormWithData(data)
	deleteBFAUserFillFormWithData(data)
	
}

function bfaUsersFillScrollTable(input){
	for (const row_data of input) {
		row = document.getElementById('bfaUsersScrollTable').tBodies[0].insertRow(-1)
		row.onclick = bfaUsersRowClick
		for (const cell_data of row_data) {
			let cell = row.insertCell(-1)
			cell.innerHTML = '<div class=\'scrollTableCellContentWrapper\'>' + cell_data + '</div>'
			cell.classList.add('scrollTableCell')
		}
	}
	
}

function bfaServersgetDataFromRow(dataRow){
	let data = []
	for (const dat of dataRow.cells){
		data.push(dat.children[0].innerHTML)
	}
	let annotated_data = {}
	annotated_data['BFAName'] = data[0]
	annotated_data['BFPath'] = data[1]
	annotated_data['local_monitoring'] = data[2]
	return annotated_data
}

function bfaServersRowClick(){
	if ('clickedScrollTableRow' === this.className) {
		this.classList.remove('clickedScrollTableRow')
	}
	else {
		let clicked = this.parentElement.getElementsByClassName('clickedScrollTableRow')
		for (const row of clicked) {
			row.classList.remove('clickedScrollTableRow')
		}
		this.classList.add('clickedScrollTableRow')
		data = bfaServersgetDataFromRow(this)
	}
	editServerFillFormWithData(data)
	deleteServerFillFormWithData(data)
	
}

function bfaServersFillScrollTable(input){
	for (const row_data of input) {
		row = document.getElementById('bfaServersScrollTable').tBodies[0].insertRow(-1)
		row.onclick = bfaServersRowClick
		for (const cell_data of row_data) {
			let cell = row.insertCell(-1)
			cell.innerHTML = '<div class=\'scrollTableCellContentWrapper\'>' + cell_data + '</div>'
			cell.classList.add('scrollTableCell')
		}
	}
	
}

