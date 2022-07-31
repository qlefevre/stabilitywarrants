import extract_sg
import extract_uc
import merge
import transform
import csv_to_json
import extract_sg_cfw
import csv_to_json_cfw


def handle(event, context):
    extract_sg.handle(None, None)
    extract_uc.handle(None, None)
    merge.handle(None, None)
    transform.handle(None, None)
    csv_to_json.handle(None, None)
    extract_sg_cfw.handle(None, None)
    csv_to_json_cfw.handle(None, None)


if __name__ == '__main__':
    handle(None, None)
