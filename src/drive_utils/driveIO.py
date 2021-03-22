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
	global drive
	#if(drive is None):
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

def list_remote_data_sources():
	drive = authenticate()
	files = drive.ListFile({'q':"'0AAKdKFNhfFfAUk9PVA' in parents and trashed=false", 'corpora': 'teamDrive', 'teamDriveId': '0AAKdKFNhfFfAUk9PVA', 'includeTeamDriveItems': True, 'supportsTeamDrives': True}).GetList()
	to_out = []
	for file in files:
		if (file['mimeType'] == 'application/vnd.google-apps.folder'):
			to_out.append([file['title'], file['id']])
	return to_out

def list_local_data(source=''):
	to_out = {}
	if(source is ''):
		local_data_sources = list_local_data_sources()
		for data_source in local_data_sources:
			to_out[data_source] = [[f, md5sum(local_data_path+data_source+'/'+f)] for f in listdir(local_data_path+data_source+'/') if isfile(join(local_data_path+data_source+'/', f))]
	elif(isdir(join(local_data_path, source))):
		to_out[source] = [[f, md5sum(local_data_path+source+'/'+f)] for f in listdir(local_data_path+source+'/') if isfile(join(local_data_path+source+'/', f))]
	else:
		print("Data source doesnt exist in local path.")
	return to_out

def list_remote_data(source=''):
	drive = authenticate()
	to_out = {}
	data_sources = list_remote_data_sources()
	if(source==''):
		for data_source in data_sources:
			to_out[data_source[0]] = {'title' : data_source[0], 'id' : data_source[1], 'files' : []}
			files = drive.ListFile({'q':"'" + data_source[1] + "' in parents and trashed=false", 'corpora': 'teamDrive', 'teamDriveId': '0AAKdKFNhfFfAUk9PVA', 'includeTeamDriveItems': True, 'supportsTeamDrives': True}).GetList()
			for file in files:
				#print(file)
				if(file['mimeType'] != 'application/vnd.google-apps.folder'):
					to_out[data_source[0]]['files'].append([file['title'], file['md5Checksum'], file['id']])
	else:
		src_id = None
		src_title = None
		for src in data_sources:
			if(src[0] == source):
				src_id = src[1]
				src_title = src[0]
		if (src_title != None):
			to_out[src_title] = {'title' : src_title, 'id' : src_id, 'files' : []}
			files = drive.ListFile({'q':"'" + src_id + "' in parents and trashed=false", 'corpora': 'teamDrive', 'teamDriveId': '0AAKdKFNhfFfAUk9PVA', 'includeTeamDriveItems': True, 'supportsTeamDrives': True}).GetList()
			for file in files:
				if(file['mimeType'] != 'application/vnd.google-apps.folder'):
					to_out[src_title]['files'].append([file['title'], file['md5Checksum'], file['id']])
		else:
			print("Data source doesnt exist in remote path.")
	return to_out

def list_data(source=''):
	to_out = {}
	remote_data = list_remote_data(source)
	local_data = list_local_data(source)
	for data_source in remote_data:
		to_out[data_source] = {'title': data_source}
		to_out[data_source]['id'] = remote_data[data_source]['id']
		to_out[data_source]['files'] = [file[0] for file in remote_data[data_source]['files']]
		to_out[data_source]['ids'] = [file[2] for file in remote_data[data_source]['files']]
		if(data_source in local_data):
			to_out[data_source]['where'] = 'local/remote'
			missed_checksum = False
			for file in remote_data[data_source]['files']:
				if(file not in local_data[data_source]):
					missed_checksum = True
			for file in local_data[data_source]:
				if(file not in remote_data[data_source]['files']):
					missed_checksum = True
			if(missed_checksum):
				to_out[data_source]['sync'] = False
			else:
				to_out[data_source]['sync'] = True
		else:
			to_out[data_source]['where'] = 'remote'
			to_out[data_source]['sync'] = False
	for data_source in local_data:
		if(data_source not in remote_data):
			to_out[data_source] = {'title': data_source}
			to_out[data_source]['sync'] = False
			to_out[data_source]['where'] = 'local'
			to_out[data_source]['files'] = [file[0] for file in local_data[data_source]]
	return to_out

def open_file(source, file_name, index=None):
	drive = authenticate()
	file = None
	src_dict = list_data(source)
	if(index is None):
		i = 0
		found = False
		for src_file_name in src_dict[source]['files']:
			if (file_name == src_file_name):
				found = True
				index = src_dict[source]['ids'][i]
				break
			i = i + 1
		if(found):
			file = drive.CreateFile({'id': index})
		else:
			file = drive.CreateFile({'title': file_name, "parents": [{"id": src_dict[source]['id']}]})
	else:
		file = drive.CreateFile({'id': index})
		print(file)
	return file

def download_source(source):
	sources = list_data(source)
	if(source in sources):
		source_data = sources[source]
		if(source_data['sync'] is False):
			i = 0
			for index in source_data['ids']:
				download_file(source, source_data['files'][i], index)
				i = i + 1
		else:
			print('Source up-to-date locally at data/')

def download_file(source, file_name, index=None):
	file = open_file(source, file_name, index)
	file.GetContentFile(local_data_path+source+'/'+file_name)

def upload_file(source, file_name):
	file = open(source, file_name)
	file.SetContentString(data)
	file.Upload() # Files.insert()


def write(data, source, file_name, write_type='w', store_local=False):
	drive = authenticate()
	file = open(source, file_name)
	if(write_type=='w'):
		file.SetContentString(data)
		file.Upload() # Files.insert()
	elif(write_type=='w+'):
		content = file.GetContentString()  # 'Hello'
		file1.SetContentString(content + data)  # 'Hello World!'
		file1.Upload() # Files.update()
	if(store_local):
		with open(local_data_path+source+'/'+file_name, write_type) as local_file:
			local_file.write(data)

def file_as_bytes(file):
    with file:
        return file.read()

def md5sum(file_path):
	return hashlib.md5(file_as_bytes(open(file_path, 'rb'))).hexdigest()

if __name__ == '__main__':
	#drive = authenticate()
	write('nada', 'teste.txt')