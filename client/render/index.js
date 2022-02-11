function getData(name){
     fetch('http://localhost:5000/api/objects/consult/data/'+name, {
           method: 'GET',
           mode: 'cors',
           headers: {
                 'Content-Type': 'application/json'
           }
     })
     .then( Response => Response.json())
     .then( json => console.log(json));
};

function sendData(name, date){
      fetch('http://localhost:5000/api/objects/create', {
            method: 'POST',
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
      .then( json => console.log(json));
}

function deleteData(name){
      fetch('http://localhost:5000/api/objects/delete/'+name, {
            method: 'DELETE',
            mode: 'cors',
            headers: {
                  'Content-Type': 'application/json'
            }
      })
      .then( Response => Response.json())
      .then( json => console.log(json));
 };

document.getElementById('sendInfo')
.addEventListener("click", (evt) => {
      evt.preventDefault();

      let name = document.getElementById('namePost').value;
      let date = document.getElementById('date').value ;

      sendData(name, date);

});

document.getElementById('getInfo')
.addEventListener("click", (evt) => {
      evt.preventDefault();

      let name = document.getElementById('nameDelete').value;

      deleteData(name);

});

document.getElementById('deleteInfo')
.addEventListener("click", (evt) => {
      evt.preventDefault();

      let name = document.getElementById('nameConsult').value;
      
      getData(name);

});