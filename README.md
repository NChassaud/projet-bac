Voici comment marche mon programme : 

- J’ai associer à tout mes composants une patte de GPIO de ma Raspi
- J’ai s’étiole tout mes composants en sortie ou en entrée 
- Ensuite j’ai fait tout mes def, pour pouvoir faire appel à toute les fonctions dont j’ai besoin (ex : allumer ventilateur /activer mode chauffage / convertir la valeur que me donne mon capteur de température en valeur analogique (mV) / etc…) 
- J’ai ensuite défini mon mode auto et mon mode manuel 
- Et pour finir j’ai fait ma boucle « While true » pour permettre grâce à un commutateur de choisir entre ces 2 modes
