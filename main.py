import json
import os

from requests import get
from typing import List
from dataclasses import dataclass
from pyDataverse.api import Api
from pyDataverse.exceptions import ApiAuthorizationError

import dvconfig

output_dir = dvconfig.output_folder
base_url = dvconfig.base_url
api_token = dvconfig.api_token
api_url = f'{base_url}/api' if not base_url.endswith('/') else f'{base_url}api'

api = Api(base_url, api_token)
print('API status: ' + api.status)


@dataclass
class ExportFormats:
    """Data class for all the supported export formats"""
    ddi: str = 'ddi'
    oai_ddi: str = 'oai_ddi'
    dcterms: str = 'dcterms'
    oai_dc: str = 'oai_dc'
    '''
    json_ld is schema.org in the dataverse document
    https://guides.dataverse.org/en/latest/api/native-api.html#export-metadata-of-a-dataset-in-various-formats
    '''
    json_ld: str = 'schema.org'
    OAI_ORE: str = 'OAI_ORE'
    Datacite: str = 'Datacite'
    oai_datacite: str = 'oai_datacite'
    dataverse_json: str = 'dataverse_json'


def get_request(query_str, auth=False, params=None):
    """Make a GET request upon API with query.

    Parameters
    ----------
    query_str : string
        Query string for the request. Will be concatenated to
        `native_api_base_url`.
    auth : bool
        Should an api token be sent in the request. Defaults to `False`.
    params : dict
        Dictionary of parameters to be passed with the request.
        Defaults to `None`.

    Returns
    -------
    requests.Response
        Response object of requests library.

    """

    if params is None:
        params = {}
    url: str = f'{api_url}/{query_str}'

    if auth:
        if api_token:
            if not params:
                params = {}
            params['key'] = api_token
        else:
            ApiAuthorizationError(
                'ERROR: PUT - Api token not passed to '
                '`put_request` {}.'.format(url)
            )

    try:
        resp = get(
            url,
            params=params
        )
        if resp.status_code < 200 or resp.status_code > 299:
            raise Exception('calling semantic API failed')
        return resp
    except ConnectionError:
        raise ConnectionError(f'ERROR: PUT - Could not establish connection to api {url}.')


def find_datasets_in_dv(dv_name: str) -> List[str]:
    """get all the datasets under the given dataverse name"""
    dataset_ids: List[str] = []
    query_str = '/dataverses/' + str(dv_name) + '/contents'
    params = {}
    resp = api.get_request(query_str, params=params, auth=True)
    for dvobject in resp.json()['data']:
        dvtype = dvobject['type']
        if 'dataverse' != dvtype:
            dv_protocol = dvobject['protocol']
            dv_authority = dvobject['authority']
            dv_identifier = dvobject['identifier']
            dataset_ids.append(f'{dv_protocol}:{dv_authority}/{dv_identifier}')
    return dataset_ids


def export_datasets(ds_ids: List[str], export_format=ExportFormats.json_ld) -> None:
    """
    export all the datasets given in the list
    :param ds_ids:
    :param export_format:
    :return:
    """
    for ds_id in ds_ids:
        export_dataset(ds_id, export_format)


def export_datasets_dataverse(dv_name: str, export_format=ExportFormats.json_ld) -> None:
    """
    export all the datasets under the given dataverse
    :param dv_name:
    :param export_format:
    :return:
    """
    ds_ids: List[str] = find_datasets_in_dv(dv_name)
    export_datasets(ds_ids, export_format)


def write_json_to_file(json_dict, filename: str, ) -> None:
    """
    write json to file
    :param json_dict:
    :param filename:
    :return:
    """
    with open(os.path.join(output_dir, filename), 'a+') as f:
        f.write(json.dumps(json_dict))


def get_filename(ds_id: str) -> str:
    ds_id = ds_id.replace('/', '-')
    return f'{ds_id}.json'


def export_dataset(ds_id: str, export_format=ExportFormats.json_ld) -> None:
    """
    export the specific dataset with the given dataset PID

    :param ds_id:
    :param export_format:
    :return:
    """
    query_string = get_query_string(ds_id, export_format)
    resp = get_request(query_string, auth=True)

    if resp.status_code < 200 or resp.status_code > 299:
        raise Exception(f'API call failed, cannot export dataset {ds_id}')
    else:
        write_json_to_file(resp.json(), get_filename(ds_id))


def get_query_string(ds_id: str, export_format=ExportFormats.json_ld) -> str:
    """
    get the query string for the specific http call,
    this method makes custom queries more flexible

    :param ds_id:
    :param export_format:
    :return:
    """
    return f'datasets/export?exporter={export_format}&persistentId={ds_id}'


if __name__ == '__main__':
    export_datasets_dataverse('liss_dc')

