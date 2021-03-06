from utils import create_temp_file
from utils import upload_file
from utils import download_file


def handle(event, context):
    """
    Fusionne les fichiers csv de SG et UC => ALL
    """
    print('Fusionne les fichiers csv de SG et UC en fichier csv ALL')
    stabilitywarrants_all = create_temp_file()

    with open(stabilitywarrants_all, 'w') as file_all:
        file_all.write(
            'issuer;mnemo;isin;sous-jacent;borne basse;borne haute;maturite;achat;vente;prix sous-jacent\n')
        try:
            stabilitywarrants_sg = download_file(
                'sw/sg/%Y/%m/stabilitywarrants-sg-%Y-%m-%d.csv')
            with open(stabilitywarrants_sg, 'r') as file_sg:
                file_all.writelines(file_sg.readlines()[1:])
        except IOError:
            print('Erreur lors du traitement des stability warrants SG')
        try:
            stabilitywarrants_uc = download_file(
                'sw/uc/%Y/%m/stabilitywarrants-uc-%Y-%m-%d.csv')
            with open(stabilitywarrants_uc, 'r') as file_uc:
                file_all.writelines(file_uc.readlines()[1:])
        except IOError:
            print('Erreur lors du traitement des stability warrants UC')

    upload_file(stabilitywarrants_all,
                'sw/all/%Y/%m/stabilitywarrants-all-%Y-%m-%d.csv')
    return {
        "message": "merge ok"
    }


if __name__ == '__main__':
    handle(None, None)
