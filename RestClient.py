import requests
import json
import os
import re
import typing

class RestClient:
    def __init__(self, base_url, username, password, verify_ssl_certificate=True, verbose=False):
        self.base_url = base_url+"/api/v1";
        self.auth = requests.auth.HTTPBasicAuth(username, password);
        self.verify_ssl_certificate = verify_ssl_certificate;
        self.verbose = verbose
        if not verify_ssl_certificate:
            requests.packages.urllib3.disable_warnings()

    def _url(self, path):
        return self.base_url+path;

    def _check_error(self, response):
        # Repackage the exception if an error occurs
        # It is ugly, but serves a purpose :)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try: 
                error_message = response.json()['error']
                raise RuntimeError(error_message) from e;
            except ValueError:
                raise RuntimeError(e) from e

    def _get(self, path, params=None):
        url = self._url(path)
        if self.verbose:
            print ("GET "+url)

        r = requests.get(url,params=params, verify=self.verify_ssl_certificate, auth=self.auth)
        self._check_error(r)

        return r

    def _post(self, path, data=""):
        url = self._url(path)
        if self.verbose:
            print("POST "+url)
            print("request payload: "+data)

        r = requests.post(url, data=data, verify=self.verify_ssl_certificate, auth=self.auth)
        self._check_error(r)
        return r

    # This method uses a workaround for a faulty implementation regarding non-ascii filenames
    # in urllib (used by the requests library). This approach seems to work well, but  there may 
    # be performance concerns (especially with large files). This has only been tested agains
    # the PHP backend (other backends may support the "real" method).
    # See http://linuxonly.nl/docs/68/167_Uploading_files_with_non_ASCII_filenames_using_Python_requests.html
    # and https://github.com/urllib3/urllib3/issues/303 for more information.
    def _post_file(self, path, file, mime_type):
        url = self._url(path)
        if self.verbose:
            print("POST "+url+" (file upload)")

        session = requests.Session()

        with open( file, 'rb') as f:
            fname = os.path.basename(f.name)

            request = requests.Request('POST', url, files=[('file', (fname, f, mime_type))], auth=self.auth)
            request = session.prepare_request(request)
            # this part is the workaround
            request.body = re.sub(b'filename\*=[^\r\n]*', b'filename="' + fname.encode('utf-8') + b'\"', request.body)
            request.headers['Content-Length'] = len(request.body)
            
            r = session.send( request, verify=self.verify_ssl_certificate )
            self._check_error(r)
            return r

    def _delete(self, path):
        url = self._url(path)
        if self.verbose: 
            print("DELETE "+url)

        r = requests.delete(url, verify=self.verify_ssl_certificate, auth=self.auth)
        self._check_error(r)
        return r

    ########
    # test

    # /test/hello
    def get_hello_for_authorized_user(self):
        return self._get("/test/hello").content

    # /test/hello/{name}
    def get_hello_with_name(self, name):
        return self._get("/test/hello/"+name).content

    ########
    # users

    # Optionally filters on username and email)
    #, username=None, email=None):
    def get_users(self, **query_params):
#        params={'username':username, 'email':email}
        return self._get("/users", query_params).json()

    def get_user(self, id:str ):
        return self._get("/users/"+str(id)).json()

    def get_myself(self):
        return self._get("/users/me").json()

    def get_my_systems(self, **query_params ):
        return self._get("/users/me/systems", query_params).json()

    ############
    # systems

    def create_system(self, name:str="", description:str="", is_public=False ):
        data = json.dumps( { "name":name, "description":description, "public":is_public })
        return self._post("/systems", data).json()

    def get_systems(self, **query_params ):
        return self._get("/systems", query_params).json()

    def get_system(self, id:str):
        return self._get("/systems/"+str(id)).json()

    def upload_system_file(self, id:str, file):
        return self._post_file("/systems/"+str(id)+"/file", file, "application/xml")

    def get_system_file(self, id:str):
        return self._get("/systems/"+str(id)+"/file").content

    def get_system_file_components(self, id:str):
        return self._get("/systems/"+str(id)+"/file/components").json()

    def delete_system(self, id:str ):
        return self._delete("/systems/"+str(id)).json()

    ## system resources

    def create_system_resource(self, system_id:str ):
        return self._post("/systems/"+str(system_id)+"/resources").json()

    def get_system_resources(self, system_id:str ):
        return self._get("/systems/"+str(system_id)+"/resources").json()

    def get_system_resource(self, system_id:str, resource_id:str):
        return self._get("/systems/"+str(system_id)+"/resources/"+str(resource_id)).json()

    def upload_system_resource_file(self, system_id:str, resource_id:str, file, mime_type='application/octet-stream'):
        return self._post_file("/systems/"+str(system_id)+"/resources/"+str(resource_id)+"/file", file, mime_type)

    def get_system_resource_file(self, system_id:str, resource_id:str):
        return self._get("/systems/"+str(system_id)+"/resources/"+str(resource_id)+"/file").content

    def delete_system_resource(self, system_id:str, resource_id:str):
        return self._delete("/systems/"+str(system_id)+"/resources/"+str(resource_id)).json()

    ############
    # components

    def create_component(self, name:str="", description:str="", is_public=False ):
        data = json.dumps( { "name":name, "description":description, "public":is_public })
        return self._post("/components", data).json()

    def get_components(self, **query_params):
        return self._get("/components", query_params).json()

    def get_component(self, id:str):
        return self._get("/components/"+str(id)).json()

    def upload_component_file(self, id:str, file):
        return self._post_file("/components/"+str(id)+"/file", file, "application/xml")

    def get_component_file(self, id:str):
        return self._get("/components/"+str(id)+"/file").content

    def delete_component(self, id:str ):
        return self._delete("/components/"+str(id)).json()

    ## component resources

    def create_component_resource(self, component_id:str ):
        return self._post("/components/"+str(component_id)+"/resources").json()

    def get_component_resources(self, component_id:str ):
        return self._get("/components/"+str(component_id)+"/resources").json()

    def get_component_resource(self, component_id:str, resource_id:str):
        return self._get("/components/"+str(component_id)+"/resources/"+str(resource_id)).json()

    def upload_component_resource_file(self, component_id:str, resource_id:str, file, mime_type='application/octet-stream'):
        return self._post_file("/components/"+str(component_id)+"/resources/"+str(resource_id)+"/file", file, mime_type)

    def get_component_resource_file(self, component_id:str, resource_id:str):
        return self._get("/components/"+str(component_id)+"/resources/"+str(resource_id)+"/file").content

    def delete_component_resource(self, component_id:str, resource_id:str):
        return self._delete("/components/"+str(component_id)+"/resources/"+str(resource_id)).json()
