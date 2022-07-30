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