#!/bin/bash

# Vérifier si la clé USB est branchée
if [ -b $USB ]; then
    PARTITION_NAME=$(lsblk -o LABEL $USB | tail -n 1)  # Récupérer le nom de la partition
    MOUNT_POINT="/mnt/data/share/usb/$PARTITION_NAME"  # Chemin où la partition sera montée

    # Vérifier si le point de montage existe, sinon le créer
    if [ ! -d "$MOUNT_POINT" ]; then
        mkdir -p "$MOUNT_POINT"
    fi

    mount $USB "$MOUNT_POINT"  # Monter la clé USB dans le dossier spécifique

    rsync -avu "/mnt/data/share/usb/$PARTITION_NAME/" "$MOUNT_POINT/"  # Synchroniser les données non synchronisées

    umount "$MOUNT_POINT"  # Démonter la clé USB
else
    echo "Aucune clé USB trouvée."
fi
