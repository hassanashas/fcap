const addChallengeForm = document.querySelector("#add_challenge_forms");

const players = document.querySelector("#players");
const submitButton = document.querySelector("#submit_button");

var now = new Date();
now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
document.getElementById('date').value = now.toISOString().slice(0,16);
now.setMinutes(now.getMinutes() + 45);
document.getElementById('end_date').value = now.toISOString().slice(0,16);

var expiry_date = new Date();
expiry_date.setMinutes(expiry_date.getMinutes() - expiry_date.getTimezoneOffset() + 10080); 
document.getElementById('expiry_date').value = expiry_date.toISOString().slice(0, 16); 


document.getElementById('date').addEventListener('change', (e) => {
    const value = new Date(e.target.value); 
    value.setMinutes(value.getMinutes() + 45);
    value.setMinutes(value.getMinutes() - value.getTimezoneOffset());
    document.getElementById('end_date').value = value.toISOString().slice(0,16);
});


var accounts_endpoint = 'api/users/get_accounts';
var players_data = []
$.ajax({
    method:"GET", 
    url: accounts_endpoint, 
    success: function(response_data) {
        players_data = response_data.data; 
    }, 
    error: function(error_data) {
        console.log("Error");
        console.log(error_data);
    }
});

players.addEventListener("keyup", (e) => {
    const number = e.target.value; 
   
    addChallengeForm.innerHTML = "";
    var select_forms = []
    for (let i = 1; i <= number; i++)
    {
        var iDiv = document.createElement('div');
        iDiv.classList = 'form-group mt-2';
        addChallengeForm.appendChild(iDiv);
        var div2 = document.createElement('label');
        div2.innerHTML = "Player #" + i; 
        iDiv.appendChild(div2);
        var player_select = document.createElement('select');
        player_select.name = 'player_select' + i; 
        player_select.classList = "form-control mt-1 mb-2";

        var temp_disabled_option = document.createElement('option');
        temp_disabled_option.hidden = true;
        temp_disabled_option.value = "None"; 
        temp_disabled_option.selected = true; 
        temp_disabled_option.innerHTML = "Choose Player"; 
        player_select.append(temp_disabled_option);
        for (let k = 0; k < players_data.length; k++)
        {
            // For the Player Names
            var player_option = document.createElement('option');
            player_option.innerHTML = players_data[k][1] + " - " + players_data[k][0];
            player_option.value = players_data[k][1]; 
            player_select.append(player_option);
        }
        // For the Player Score 

        iDiv.append(player_select); 
    }
});