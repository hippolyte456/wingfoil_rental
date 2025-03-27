document.addEventListener('DOMContentLoaded', function() {
    // Sélectionne tous les checkboxes de filtre
    const filterCheckboxes = document.querySelectorAll('.filter-type');
    
    // Fonction pour mettre à jour l'affichage des équipements
    function updateEquipmentDisplay() {
        // Récupère les types sélectionnés
        const selectedTypes = Array.from(filterCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);
        
        // Sélectionne tous les éléments d'équipement
        const equipmentItems = document.querySelectorAll('.equipment-item');
        
        // Pour chaque équipement
        equipmentItems.forEach(item => {
            const itemType = item.dataset.type;
            // Affiche l'élément si son type est sélectionné
            if (selectedTypes.includes(itemType)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    // Ajoute l'écouteur d'événements à chaque checkbox
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateEquipmentDisplay);
    });
}); 