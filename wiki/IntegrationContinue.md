# Fonctionnement de l'intégration continue

L'intégration continue (CI) et la conteneurisation sont des éléments cruciaux dans le processus de développement logiciel moderne. L'intégration continue permet une détection précoce des erreurs et une livraison plus rapide des fonctionnalités, tandis que la conteneurisation assure une portabilité et une gestion plus efficace des applications.

Les étapes d'intégration continue dans le contexte de l'API sont les suivantes :

À chaque *push* sur la branche `develop` :

1. Le CI lance un build.
2. Le CI lance les tests unitaires.

Si le *push* se fait sur la branche `main` :

1. Le CI lance un build.
2. Le CI lance les tests unitaires.
3. Le CI lance la construction de l’image Docker.
4. Le CI lance le déploiement de l'image Docker du DockerHub.

En cas d'échec d'une des étapes, le pipeline arrête et ne procède pas aux étapes suivantes.

Dans le cas de OxygenCS, les mêmes étapes sont exécutées, mais avec une étape de vérification de la qualité du code (linting et formatting) :

1. Exécute un linter qui assure la qualité du code.
   - Pylint 3.0.2
2. Exécute formattage qui assure une uniformité du code.
   - Black 23.10.1

# Fonctionnement du déploiement continue sur Kubernetes

Le cluster Kubernetes est hébergé sur les serveurs de l'ETS et n'est accessible qu'à travers le VPN de l'ETS. Cet aspect de l'architecture ajoute une couche de complexité et de sécurité supplémentaire qui fait en sorte que le déploiement continu à travers les pipelines CI/CD de GitHub est plus complexe. Pour contourner le problème, un service supplémentaire a été implémenté sur le cluster Kubernetes (`cluster-service.yaml`), permettant de redémarrer les *pods* aux 8 heures.

Lorsque ce service s'exécute, le *pod* contenant l'API de OxygenCS est redémarré (`rollout restart deployment/oxygen`). Ce faisant, il télécharge la dernière version de l'image disponible sur DockerHub, ce qui permet de mettre à jour l'application sans avoir à redéployer le cluster Kubernetes. Cette façon de faire assure aussi qu'il n'y a pas de temps d'arrêt entre chaque déploiement, grâce aux *réplicas* de Kubernetes.