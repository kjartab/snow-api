import flask





# GET-handler (/utno/turer/{id})
	job = tasks.add.delay(1,id)
	return jsonify({"jobid" : job.id }) 
	