function getData(name){
     fetch('http://localhost:5000/api/objects/consult/data/'+name, {
           method: 'GET',
           mode: 'cors',
           headers: {
                 'Content-Type': 'application/json'
           }
     })
     .then( Response => Response.json())
     .then( json => console.log(json))
}

function sendData(name, date){
      fetch('http://localhost:5000/api/objects/consult/data/'+name, {
            method: 'GET',
            mode: 'cors',
            headers: {
                  'Content-Type': 'application/json'
            }, 
            body: JSON.stringify({
                  "fecha_creacion": date,
                  "nombre": name
                })
      })
      .then( Response => Response.json())
      .then( json => console.log(json))
 }