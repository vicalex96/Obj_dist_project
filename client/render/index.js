function getAllData(){
      fetch('http://distributed.ddns.net:8000/api/objects/consult/estructure', {
            method: 'GET',
            mode: 'cors',
            headers: {
                  'Content-Type': 'application/json'
            }
      })
      .then( Response => Response.json())
      .then( json => {
            $('.respuesta-allObjects').text(JSON.stringify(json));
            console.log(json)
      })
 };

function getData(name){
     fetch('http://distributed.ddns.net:8000/api/objects/consult/data/'+name, {
           method: 'GET',
           mode: 'cors',
           headers: {
                 'Content-Type': 'application/json'
           }
     })
     .then( Response => Response.json())
     .then( json => {
      $('.respuesta-consultObject').text(JSON.stringify(json));
      console.log(json)
      });
};

function sendData(name){
      let date = new Date()
      fetch('http://distributed.ddns.net:8000/api/objects/create', {
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
      .then( json => {
            $('.respuesta-createObject').text(JSON.stringify(json));
            console.log(json)
      });
}

function deleteData(name){
      fetch('http://distributed.ddns.net:8000/api/objects/delete/'+name, {
            method: 'DELETE',
            mode: 'cors',
            headers: {
                  'Content-Type': 'application/json'
            }
      })
      .then( Response => Response.json())
      .then( json => {
            $('.respuesta-deleteObject').text(JSON.stringify(json));
            console.log(json)
      });
 };

document.getElementById('sendInfo')
.addEventListener("click", (evt) => {
      evt.preventDefault();

      //let name = document.getElementById('namePost').value;
      let name = $('.namePost').val()
      console.log(name)
      sendData(name);

});

document.getElementById('getInfo')
.addEventListener("click", (evt) => {
      evt.preventDefault();

      let name = $('.nameConsult').val()
      getData(name);

});

document.getElementById('deleteInfo')
.addEventListener("click", (evt) => {
      evt.preventDefault();

      let name = $('.nameDelete').val()
      deleteData(name);

});


document.getElementById('getAllInfo')
.addEventListener("click", (evt) => {
      evt.preventDefault();
 
      getAllData();

});