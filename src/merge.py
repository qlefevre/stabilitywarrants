import utils

def handle(event, context):
    """
    Fusionne les fichiers csv de SG et UC => ALL
    """
    stabilitywarrants_sg = utils.download_file('sw/sg/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')
    stabilitywarrants_uc = utils.download_file('sw/uc/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')
    stabilitywarrants_all = utils.createTempFile()

    with open(stabilitywarrants_all, 'w') as file_all:
        file_all.write('isin;sous-jacent;borne basse;borne haute;maturite;achat;vente;prix sous-jacent\n')
        with open(stabilitywarrants_sg, 'r') as file_sg:
            file_all.writelines(file_sg.readlines()[1:])
        with open(stabilitywarrants_uc, 'r') as file_uc:
            file_all.writelines(file_uc.readlines()[1:])

    utils.upload_file(stabilitywarrants_all, 'sw/all/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')

    return {
        "message": "merge ok"
    }


if __name__ == '__main__':
    handle(None, None)
