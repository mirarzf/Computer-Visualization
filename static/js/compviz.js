// Changing tabs 
function changeOnglet(_this){
    var getOnglets    = document.getElementById('mes_onglets').getElementsByTagName('span');
    for(var i = 0; i < getOnglets.length; i++){
        if(getOnglets[i].id){
            if(getOnglets[i].id == _this.id){
                getOnglets[i].className = 'mon_onglet_selected';
                document.getElementById('c' + _this.id).style.display            = 'block';
            }
            else{
                getOnglets[i].className = 'mon_onglet';
                document.getElementById('c' + getOnglets[i].id).style.display    = 'none';
            }
        }
    }   
}

// Select list 
function showSelectedIndex(_this){ 
    var sb = document.getElementById('select_list'); 
    // show the selected index
    if (sb.selectedIndex != 0){
        alert(sb.selectedIndex-1);
    }
    document.getElementById('video_id_sel_iframe').contentWindow.location.reload();
}