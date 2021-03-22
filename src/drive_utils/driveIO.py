from os import listdir
from os.path import isfile, isdir, join
import hashlib
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = 'drive_utils/credentials/app_credentials.json'

drive = None
local_data_path = '../data/'

# client_secrets.json should be at project root
def authenticate():
	gauth = GoogleAuth()
	# Try to load saved client credentials
	gauth.LoadCredentialsFile("drive_utils/credentials/client_credentials.txt")
	if gauth.credentials is None:
		# Authenticate if they're not there
		gauth.LocalWebserverAuth()
	elif gauth.access_token_expired:
		# Refresh them if expired
		gauth.Refresh()
	else:
		# Initialize the saved creds
		gauth.Authorize()
	# Save the current credentials to a file
	gauth.SaveCredentialsFile("drive_utils/credentials/client_credentials.txt")
	drive = GoogleDrive(gauth)
	return drive

def list_local_data_sources():
	return [f for f in listdir(local_data_path) if isdir(join(local_data_path, f))]

#def list_remote_data_sources():

#'application/vnd.google-apps.folder'

def list_local_data(source=''):
	to_out = {}
	if(source is ''):
		local_data_sources = list_local_data_sources()
		for data_source in local_data_sources:
			to_out[data_source] = [[f, md5sum(local_data_path+data_source+'/'+f)] for f in listdir(local_data_path+data_source+'/') if isfile(join(local_data_path+data_source+'/', f))]
	elif(isdir(join(local_data_path, source))):
		to_out[source] = [[f, md5sum(local_data_path+source+'/'+f)] for f in listdir(local_data_path+source+'/') if isfile(join(local_data_path+source+'/', f))]
	else:
		raise Exception("Data source doesnt exist.")
	return to_out

def list_remote_data(source=''):
	global drive
	if(drive is None):
		drive = authenticate()
	files = drive.ListFile({'q':"'0AAKdKFNhfFfAUk9PVA' in parents and trashed=false", 'corpora': 'teamDrive', 'teamDriveId': '0AAKdKFNhfFfAUk9PVA', 'includeTeamDriveItems': True, 'supportsTeamDrives': True}).GetList()
	#to_out = []
	#for file in files:
	#	if(file['mimeType'] == 'text/') 
	return files

def list_data(source=''):
	remote_data = list_remote_data()
	local_data = list_local_data()
	#for data in local_data:
	#	if(data)
	return

def read(file_name, store_local=False):
	# check if file already exists in data/
	# if doesnt, download it from $DRIVE/AI Democracy/data/
	#if store_local, save file on data/
	return

def write(file_name, store_local=False):
	global drive
	if(drive is None):
		drive = authenticate()
	file1 = drive.CreateFile({'title': file_name})
	file1.SetContentString('Hello')
	file1.Upload() # Files.insert()

def file_as_bytes(file):
    with file:
        return file.read()

def md5sum(file_path):
	return hashlib.md5(file_as_bytes(open(file_path, 'rb'))).hexdigest()

if __name__ == '__main__':
	#drive = authenticate()
	write('nada', 'teste.txt')