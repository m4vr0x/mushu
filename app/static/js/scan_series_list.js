// The name of the Python script that returns the scraped data is scrapeJSON.py
let scrapeJSON = 'http://bluegalaxy.info/cgi/scrapeJSON.py'
$.get(scrapeJSON, function(data) {
   // Get JSON data from Python script
   if (data){
      console.log("Data returned:", data)
   }
   jobDataJSON = JSON.parse(data)
})
