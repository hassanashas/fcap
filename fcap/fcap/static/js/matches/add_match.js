
const addMatchForm = document.querySelector("#add_match_forms");

const players = document.querySelector("#players");
const submitButton = document.querySelector("#submit_button");

var now = new Date();
now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
document.getElementById('date').value = now.toISOString().slice(0,16);

players.addEventListener("keyup", (e) => {
    const number = e.target.value; 
   
    add_match_forms.innerHTML = "";

    for (let i = 1; i <= number; i++)
    {
        var iDiv = document.createElement('div');
        iDiv.classList = 'form-group mt-2';
        addMatchForm.appendChild(iDiv);
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
            player_option.innerHTML = players_data[k][0] + " (" + players_data[k][1] + ")";
            player_option.value = players_data[k][1]; 
            player_select.append(player_option);

            
        }
        // For the Player Score 
        var player_score_label = document.createElement('label');
        player_score_label.innerHTML = "Player #" + i + " Points"; 

        var player_score_input = document.createElement('input');
        player_score_input.id = "player_score" + i; 
        player_score_input.type = "number";
        player_score_input.step = "0.01";
        player_score_input.classList = "form-control-sm form-control mb-3";
        player_score_input.name = "player_score" + i; 
        iDiv.append(player_select); 
        iDiv.append(player_score_label)
        iDiv.appendChild(player_score_input);


    }
});

// function addFormValidations(select_forms, points_forms)
// {
//     var select_form_duplicate = true;
//     var select_form_empty = true;  
//     for (const select_form in select_forms)
//     {
//         select_form.addEventListener("keyup", (e)=> {
//             console.log("heeeeeeeelll");
//             if (select_form.value == "None")
//             {
//                 select_form_empty = false; 
//             }
//             for (const temp in select_forms)
//             {
//                 if (temp != select_form)
//                 {
//                     if (temp.value == select_form.value)
//                     {
//                         select_form_duplicate = false;
//                     }
//                 }
//             }
//         });
//     }

//     if (select_form_empty == true)
//     {
//         document.getElementById('select_empty').hidden = true; 
//     }
//     else 
//         document.getElementById('select_empty').hidden = true; 
// }