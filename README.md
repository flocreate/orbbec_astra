# Orbbec Astra sur PI3

## télécharger le driver pour le capteur

Les drivers sont disponnibles sur le site du constructeur: [ici](https://orbbec3d.com/develop/#linux)

Il faut choisir en fonction du type de processuer. pour savoir le processeur on peut utiliser la commande suivante: 

```
sudo cat /proc/cpuinfo
```

Pour le Pi3B+, il y a 4 coeurs de type ARMv7 qui est de type 32 bits, ce qui conduit donc à télécharger et décompresser l'archive suivante:

```
wget http://dl.orbbec3d.com/dist/astra/v2.0.19/AstraSDK-v2.0.19-1793e6b2ca-20191224T065800Z-Linux-arm.tar.gz
tar -xf AstraSDK-*.tar.gz
rm AstraSDK-*.tar.gz
```

## Activer le driver pour orbbec

```
cd AstraSDK-v2.0.19-1793e6b2ca-20191224T065800Z-Linux-arm
chmod +x install/install.sh
sudo ./install/install.sh
```

## Si on veut utiliser l'USB-2.0

creer un fichier de configuration: `nano AstraSDK-v2.0.19-1793e6b2ca-20191224T065800Z-Linux/lib/Plugins/openni2/orbbec.ini`

```
[Device]
UsbInterface=2 ; BULK endpoints

[Depth]
Resolution=17 ; 640x400
InputFormat=3 ; Packed 11-bit
```

## installer les dépendances python

la doccumentation pour l'installation est disponnible sur le site du constructeur: [ici](https://astra-wiki.readthedocs.io/en/latest/examples.html#depth-stream-using-python-and-opencv)

- numpy: `sudo pip3 install numpy`
- opencv: `sudo pip3 install opencv-python`
- openni: `sudo pip3 install openni`
